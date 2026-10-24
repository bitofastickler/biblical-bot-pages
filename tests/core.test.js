import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {lookup,search,newStudy,parseStudy,serializeStudy,MAX_BYTES} from '../src/core.js';
const bible=JSON.parse(readFileSync(new URL('../data/web.json',import.meta.url)));
test('all 66 books and expected chapter boundaries are available',()=>{
  assert.equal(bible.books.length,66);assert.equal(bible.books.reduce((n,b)=>n+Object.keys(b.chapters).length,0),1189);
  for(const book of bible.books)for(const [c,verses]of Object.entries(book.chapters)){assert.ok(verses[1],`${book.name} ${c}`);for(const text of Object.values(verses))assert.ok(text.trim());}
  assert.match(bible.books.find(b=>b.id==='john').chapters[3][16],/God so loved the world/);
});
test('passage lookup supports numbered books, abbreviations, chapters and ranges',()=>{
  for(const [input,reference]of [['John 3:16-18','John 3:16–18'],['1 Cor 13','1 Corinthians 13'],['Psalm 23','Psalms 23'],['Jn 1:1','John 1:1'],['Genesis','Genesis 1'],['Song of Songs 2','Song of Solomon 2']])assert.equal(lookup(bible,input).reference,reference);
  for(const invalid of ['John 999','John 3:99','John 3:18-16','Unknown 1','John 0','John 3:0','John 3:16-4:2'])assert.throws(()=>lookup(bible,invalid));
});
test('search supports all words, case insensitivity, scope and no matches',()=>{
  assert.ok(search(bible,'GOD loved world','john').some(r=>r.reference==='John 3:16'));
  assert.equal(search(bible,'zzzzxyyy').length,0);assert.equal(search(bible,'').length,0);
  assert.ok(search(bible,'love','romans').every(r=>r.reference.startsWith('Romans ')));
});
test('JSON round trip preserves complete study and can continue',()=>{
  const s=newStudy('John 3:16');s.title='Love & hope';s.references.push('Romans 8');s.content.observation='Unicode: χάρις ❤️';s.content.notes='<script>alert(1)</script>';s.entries.push({reference:'Romans 8:1',body:'A prior note',createdAt:s.createdAt});
  const restored=parseStudy(serializeStudy(s,bible),bible);assert.deepEqual(restored,s);
  restored.content.application='Continue in another browser';assert.equal(parseStudy(serializeStudy(restored,bible),bible).content.application,restored.content.application);
});
test('malformed, unsupported, oversized, credential and unsafe structural inputs rejected',()=>{
  assert.throws(()=>parseStudy('{',bible),/Invalid JSON/);assert.throws(()=>parseStudy(' '.repeat(MAX_BYTES+1),bible),/too large/);
  for(const update of [{version:99},{format:'other'},{translation:'NIV'},{title:''},{createdAt:'yesterday'},{updatedAt:'2000-01-01T00:00:00Z'},{references:['John 999']},{reader:'bad'},{content:null},{entries:{}},{apiKey:'never-export'},{references:[]},{title:'x'.repeat(201)}])assert.throws(()=>parseStudy(JSON.stringify({...newStudy(),...update}),bible));
  assert.throws(()=>parseStudy('{"__proto__":{}}',bible));
});
