# Portable study format, version 1

UTF-8 JSON, maximum 2,000,000 bytes. Example:

```json
{
  "format": "biblical-bot-study",
  "version": 1,
  "title": "Love and hope",
  "createdAt": "2026-10-24T12:00:00.000Z",
  "updatedAt": "2026-10-24T12:00:00.000Z",
  "translation": "WEB",
  "references": ["John 3:16–18"],
  "reader": "John 3:16–18",
  "content": {
    "observation": "What does the passage say?",
    "interpretation": "What does it mean in context?",
    "application": "How might I respond?",
    "notes": "Questions, reflections, or conversation text."
  },
  "entries": []
}
```

All shown fields are required. No extra fields are accepted. `entries` may contain objects with exactly `reference`, `body`, and `createdAt`, preserving earlier referenced study content. They are displayed read-only; use the notebook to continue. Dates must be parseable ISO-shaped timestamps; updates cannot precede creation. References must resolve in the bundled WEB data. Ranges use a hyphen or en dash and stay within one chapter. The parser canonicalizes references and timestamps.

Titles are nonempty and at most 200 characters. References: 1–500, at most 100 characters each. Each content field and entry body: at most 100,000 characters. Entries: at most 500. Strict field validation rejects API-key/configuration fields; export never serializes unrelated browser data. Arbitrary text remains inert text, including tags and Markdown. Do not type secrets into study content itself.

Each Save study requests a new download with a timestamped filename. Browser cancellation cannot be detected reliably, so check that the file exists. Reopening restores a snapshot, not a live connection to the original file. Changes made afterward require a new download. File imports do not upload anything and do not modify the source file. The replacement dialog lets the user cancel or request a backup before replacing an existing notebook.

Future formats must increment the version and ship explicit migrations. Never silently interpret a newer version as version 1. Retain unsupported original files unchanged.
