// Only public Bible text is read from the reference checkout. No configuration is copied.
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import path from 'node:path';
const source = process.argv[2];
if (!source) throw new Error('Usage: node scripts/import-bible.mjs <bible_books directory>');
const names = 'Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|1 Samuel|2 Samuel|1 Kings|2 Kings|1 Chronicles|2 Chronicles|Ezra|Nehemiah|Esther|Job|Psalms|Proverbs|Ecclesiastes|Song of Solomon|Isaiah|Jeremiah|Lamentations|Ezekiel|Daniel|Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|Zephaniah|Haggai|Zechariah|Malachi|Matthew|Mark|Luke|John|Acts|Romans|1 Corinthians|2 Corinthians|Galatians|Ephesians|Philippians|Colossians|1 Thessalonians|2 Thessalonians|1 Timothy|2 Timothy|Titus|Philemon|Hebrews|James|1 Peter|2 Peter|1 John|2 John|3 John|Jude|Revelation'.split('|');
const books = [], provenance = [];
for (const name of names) {
  const id = name.toLowerCase().replaceAll(' ', '');
  const raw = await readFile(path.join(source, `${id}.json`));
  const chapters = {};
  for (const row of JSON.parse(raw)) {
    if (!['paragraph text', 'line text'].includes(row.type)) continue;
    // The legacy dataset includes empty layout segments with stale verse numbers.
    // They are not verses (e.g. an empty Psalm 23:31 after Psalm 23:6).
    if (!row.value.trim()) continue;
    const c = row.chapterNumber, v = row.verseNumber;
    if (!Number.isInteger(c) || c < 1 || !Number.isInteger(v) || v < 1 || typeof row.value !== 'string') throw new Error(`Invalid verse in ${id}`);
    chapters[c] ??= {};
    chapters[c][v] = [chapters[c][v], row.value.trim()].filter(Boolean).join(' ');
  }
  books.push({ id, name, chapters });
  provenance.push({ file: `${id}.json`, sha256: createHash('sha256').update(raw).digest('hex') });
}
await mkdir('data', { recursive: true });
await writeFile('data/web.json', JSON.stringify({ translation: 'WEB', books }));
await writeFile('data/provenance.json', JSON.stringify({ source: 'bitofastickler/biblical-bot-app:backend/bible_bot/data/bible_books', imported: '2026-10-24', transformation: 'Join paragraph text and line text segments by chapter and verse, trimming surrounding whitespace. Footnotes and layout markers are omitted; verse wording is unchanged.', files: provenance }, null, 2));
console.log(`${books.length} books, ${books.reduce((n,b)=>n+Object.values(b.chapters).reduce((s,c)=>s+Object.keys(c).length,0),0)} verses`);
