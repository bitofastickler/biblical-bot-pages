# Open Study — static study workspace

A free, passage-centered Bible reader and notebook. No account, subscription, backend, AI key, database, analytics, or third-party runtime dependencies.

- Live: https://bitofastickler.github.io/biblical-bot-pages/
- This repository is independent of `bitofastickler/biblical-bot-app`. Building and deploying it does not alter the original checkout, Render services, Supabase, or billing.

## First release

Read the 66-book World English Bible; navigate chapters; look up books, chapters, verses, and same-chapter ranges; search for all query words across the Bible or one book. Add passages to a notebook, reflect with Observe / Understand / Respond, and keep freeform notes.

**Save study** downloads a new versioned JSON snapshot. **Open study** imports it in another browser and restores the notebook and reader position. Save again after continuing. It does not overwrite a previous file. A single automatic localStorage recovery copy is only a convenience; downloaded files are durable backups. Files are unencrypted personal documents, and users should never put credentials in notes.

## Run and verify

Use Node 24 or newer:

```sh
npm ci
npm test
npm run build
npm run dev
```

Open http://127.0.0.1:4173/biblical-bot-pages/. `dist/` contains only static files. For browser integration tests, while that server is running:

```sh
npx playwright install chromium firefox
npm run test:browser
```

The browser test saves in Chromium, opens the downloaded file in a fresh Firefox profile, edits and downloads again, checks recovery, invalid imports, replacement cancellation, denied storage, and 320/390px layouts. It also verifies all loaded project-subpath resources return successfully. Screenshots and synthetic test files stay in ignored `.local/`. Set `TEST_URL` to run the same checks against the live deployment. Mobile checks are browser viewport emulation, not physical device testing.

## Architecture and deployment

Buildless native ES modules (`src/core.js` for pure data functions; `src/app.js` for UI), semantic HTML, CSS, system fonts, and a bundled ~5 MB JSON Bible. The build copies public files into `dist/`; npm dependencies are only for development tests. Every asset URL is relative. There are no SPA routes requiring rewrites. Reference links may use a hash such as `#John%203%3A16`.

`.github/workflows/pages.yml` runs unit tests, builds, uploads a Pages artifact, and deploys on pushes to `main`. In GitHub Settings → Pages, choose **GitHub Actions**. The workflow requires `contents: read`, `pages: write`, and `id-token: write`; no repository secret is needed. Use Actions → Deploy GitHub Pages → Run workflow for a manual deployment. Revert a commit and push to roll back. Never point this workflow at the legacy Render services.

The full Bible is downloaded on first load and searched in memory. There is no guaranteed offline restart: the browser cache may help, but this release has no service worker. Save files contain references and study content, not the full Bible. Reading saved files requires this app and its Bible assets to load.

## Files, privacy, and licensing

See [study file format](docs/study-format.md), [translation and asset notices](THIRD_PARTY_NOTICES.md), [migration and legacy relaunch](docs/migration-and-retirement.md), and [optional AI assessment](docs/ai-options.md).

Imports are limited to 2 MB and validated against an explicit allowlist before replacement. Unsupported versions/translations and unexpected fields are rejected. All imported content uses text nodes or textarea values; there is no HTML or Markdown execution. The app exports only defined study fields, never browser/session storage, authentication material, or configuration. CSP blocks external scripts and network connections. Notes never leave the browser through the app; GitHub still receives ordinary static hosting requests.

## Known limits

- WEB only; 66 books; original footnotes and typography omitted. The source dataset omits Luke 17:36, Acts 8:37, Acts 15:34, and Acts 24:7. These references are unavailable, not invented or renumbered.
- Search is case-insensitive substring matching for every entered word, not semantic search, stemming, or AI. Ranges cannot cross chapter boundaries.
- One active notebook/recovery copy; use JSON files to manage multiple studies. Up to 500 references and 500 imported entries; title 200 characters; each content field/entry 100,000 characters; whole file 2 MB.
- No AI, cloud sync, generated commentary, Markdown export, automatic legacy import, or encrypted backups in this release.
- Browser file-download behavior and recovery storage availability vary. Check that a download completed before discarding valuable work.

App source is MIT licensed; Bible text is public domain under its separate notice.

## Bible graph integration

The Graph entry opens selected Genesis 1–50 annotations with source evidence, the existing 3D/list explorer, and the quality report. Reader passages link to the graph; graph source passages link back to the reader. Other Bible books remain readable but are explicitly not yet annotated. See [integration guide](docs/knowledge-graph.md). Run `npm test`, `npm run build` (Python 3 required), then `npm run test:browser` with the local server running. Graph code and documentation are MIT; curated annotations are CC BY 4.0, credited to bitofastickler; WEB scripture remains public domain. See [license scope and attribution](knowledge-graph/LICENSING.md).
