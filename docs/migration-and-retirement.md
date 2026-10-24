# Preserve the original; retire infrastructure only in a separate operation

This replacement does **not** export real user data, alter the original repository, or stop any service. The original checkout contains pre-existing uncommitted documentation changes; preserve those along with its Git history. The observations below come from its source and product/deployment documentation, not a fresh production database audit.

## Export cloud studies before retirement

The original app persists `studies` and `study_notes` in Supabase Postgres through the Render backend. Supabase authentication identifies the owner. Its Save Study is a cloud write, not a portable download.

For a signed-in individual, the existing read-only API provides:

1. `GET https://biblical-bot-app-1.onrender.com/api/studies` with their existing bearer access token (and `x-app-token` only if the original deployment requires it).
2. `GET /api/studies/{id}` for each owned study to retrieve the complete record **including notes**. The list omits notes and is capped at 100; a 100-row result must be treated as potentially incomplete. The API has no pagination in the inspected source.
3. Save detail responses as private JSON files outside any repository. Never save request headers, tokens, account exports, or credentials alongside those files. Do not use a public converter service.

For a complete owner-operated export, use a **read-only transaction** against the existing database or an authorized database backup, enumerating all studies and notes rather than the 100-row API. Group by owner, and deliver only each person's own studies. An example logical export query (to run only when separately authorized and with output directed to protected storage) is:

```sql
BEGIN TRANSACTION READ ONLY;
SELECT s.id, s.user_id, s.title, s.primary_reference, s.translation,
       s.passage_json, s.study_json, s.created_at, s.updated_at,
       COALESCE((
         SELECT jsonb_agg(jsonb_build_object(
           'reference', n.reference, 'body', n.body,
           'created_at', n.created_at, 'updated_at', n.updated_at
         ) ORDER BY n.created_at, n.id)
         FROM study_notes n WHERE n.study_id = s.id
       ), '[]'::jsonb) AS notes
FROM studies s
ORDER BY s.user_id, s.created_at, s.id;
ROLLBACK;
```

`user_id` is solely for private ownership reconciliation; omit it from user-facing portable files. Do not publish the query result. Maintain an encrypted full database backup separately for relaunch, including any necessary authentication/account state. Verify counts per owner, note counts, timestamps, and sample contents against the source, and test restoration into an isolated environment before shutdown. A database backup and user-readable study files serve different purposes.

## Mapping to the new study format

Legacy JSON is **not directly accepted** by Open study. Before retirement, build/test a local conversion tool against private copies or hand-convert small studies using `docs/study-format.md`:

| Legacy content | New version 1 field |
| --- | --- |
| `title` | `title` |
| `created_at`, `updated_at` | ISO `createdAt`, `updatedAt` |
| `translation` | `WEB` only when the source is actually WEB; never silently relabel another translation |
| `primary_reference`, passage reference, source references | validated `references`; choose one for `reader` |
| structured `study` / `study_json`, generated summary and conversation | plain text in `content.notes` or referenced `entries[].body`; preserve source references and distinguish generated commentary |
| each note's `reference`, `body`, `created_at` | an `entries` object with `reference`, `body`, `createdAt` |

For broad thematic studies whose primary reference is a label rather than scripture, choose a real cited WEB passage explicitly; preserve the original label and full study content as text. Missing references need user review, not fabricated mappings. Oversized or non-WEB studies require a future migration extension; preserve raw exports without truncation. Keep original IDs/session metadata only in the private archival export. New portable files deliberately omit owner IDs, emails, tokens, and database internals. Round-trip converted files through a fresh browser and compare all content before considering migration complete.

## Original application relaunch dependencies

- Repository: `bitofastickler/biblical-bot-app`; preserve the local checkout and existing uncommitted work, plus a private recovery archive. New repository: `bitofastickler/biblical-bot-pages`.
- Frontend: Render static site `biblical-bot`, root `frontend`, build `npm ci && npm run build`, output `dist`, original URL `https://biblical-bot.onrender.com`.
- Backend: Render Python service `biblical-bot-app-1`, original URL `https://biblical-bot-app-1.onrender.com`, install `pip install -r requirements.txt`, start `uvicorn backend.bible_bot.main:app --host 0.0.0.0 --port $PORT --workers 1`.
- Both observed services require manual deployments; verify current settings at relaunch. Preserve Python version, dependency locks, service region and configuration securely.
- Durable database: Supabase Postgres (`users`, `studies`, `study_notes`) plus Supabase Auth and its identity-to-user relationship. A restored database without corresponding auth identities may not restore access.
- Configuration names, **never values**: `DATABASE_URL` or complete `PGHOST`/`PGPORT`/`PGDATABASE`/`PGUSER`/`PGPASSWORD`; `SUPABASE_JWT_SECRET` and issuer settings as applicable; frontend `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`, `VITE_API_URL`; `FRONTEND_ORIGIN`; `OPENAI_API_KEY`, `OPENAI_MODEL`, `OPENAI_EMBED_MODEL`; `VECTOR_BACKEND`, `CHROMA_PERSIST_DIR` if used; rate limits and any app-token settings. Confirm the original code's actual environment names at relaunch.
- Rebuild or restore the original retrieval/vector index from Bible text. Original notes reported no persistent Render disk; do not assume a transient index survives shutdown.
- Recheck CORS, auth redirects, JWT issuer/audience, database TLS/credentials, and the backend's **current** outbound network allowlist. Recorded Oregon CIDRs may change; do not blindly reuse them.
- The inspected code returns a retired-billing response from checkout/portal routes. Preserve any historical Stripe configuration securely and audit actual active subscriptions/webhooks separately; do not assume stopping Render cancels subscriptions.
- Verify health, authenticated saved-study access, backend unit tests, frontend lint/build, and `scripts/chat_eval.py` before relaunch. A health endpoint alone does not establish database recovery.

## Future retirement checklist — not performed by this release

1. Confirm the Pages release and real-user file workflow are accepted, with an accessible link for existing users.
2. Inventory all cloud studies and notes; export complete per-user content, resolve migration gaps, and give users time to download and verify their files.
3. Securely archive original source (including uncommitted files), deployment settings, secret material in a password manager, database/auth backups, and retrieval dependencies. Prove a restore works.
4. Audit subscriptions, pending payments, webhooks, email/auth providers, and API usage. Decide billing and user-notification actions explicitly.
5. Obtain separate authorization for the actual retirement actions. Prefer reversible service suspension where possible; understand provider retention/deletion policies before deleting anything.
6. Stop the intended Render services and Supabase resources only after export/restore acceptance. Separately handle unused keys and billing obligations; confirm costs stop.
7. Retain the static repository, backups, and relaunch runbook. Never put private exports or secrets in either public repository.
