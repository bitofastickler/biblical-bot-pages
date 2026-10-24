# Translation and asset notices

## World English Bible (WEB)

Verified 2026-10-24 against the publisher:

- https://worldenglish.bible/
- https://ebible.org/eng-web/copyright.htm

The publisher declares the World English Bible public domain and explicitly permits redistribution, including Internet publication. No royalty or mandatory copyright attribution is imposed. We nevertheless identify the translation in the reader, saved files, and About page. “World English Bible” is a trademark: use the name for faithful copies, not altered scripture wording. No publisher endorsement is claimed.

This release imports the 66-book WEB dataset already bundled in `bitofastickler/biblical-bot-app`, preserving words from its paragraph/line segments and joining them by verse. Surrounding whitespace and empty layout segments are omitted. Footnotes, paragraph breaks, poetic layout, and other layout markers are not bundled. `data/provenance.json` records every source file SHA-256; `scripts/import-bible.mjs` makes the transformation reproducible. The legacy dataset is not claimed to be the latest publisher revision. It contains 1,189 chapters and 31,098 nonempty verse entries. Luke 17:36, Acts 8:37, Acts 15:34, and Acts 24:7 are absent in this dataset.

Reimport only from the named public Bible-data directory:

```sh
node scripts/import-bible.mjs ../biblical-bot-app/backend/bible_bot/data/bible_books
```

Do not import entire legacy directories or any configuration, studies, user tables, secrets, or database dumps.

## Other assets

The design uses original CSS and a text-based brand mark. Fonts are operating-system fonts; no font files, stock images, icon libraries, or original app assets were copied. There are no third-party JavaScript runtime packages. Playwright is a development-only Apache-2.0 dependency; its package includes its license. Browser binaries are test tooling and are not distributed in the website.
