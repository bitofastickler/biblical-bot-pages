import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {getBook,readerReference,readerLink,selectionUrl} from '../knowledge-graph/dist/integration.js';
const read=p=>JSON.parse(readFileSync(new URL(p,import.meta.url),'utf8'));
const catalog=read('../knowledge-graph/dist/catalog.json');
test('book registry is explicit and unsupported books do not fall back to Genesis',()=>{
  assert.equal(getBook(catalog,'EXO'),undefined);
  assert.equal(getBook(catalog,'GEN').readerBook,'genesis');
  const exodus={id:'EXO',name:'Exodus',chapters:40};
  assert.equal(readerReference(exodus,'EXO.2.3'),'Exodus 2:3');
  assert.throws(()=>readerReference(exodus,'GEN.2.3'));
  assert.throws(()=>readerReference(exodus,'EXO.41.1'));
});
test('every source verse links to matching reader text without altering offsets or evidence',()=>{
  const bible=read('../data/web.json'), book=getBook(catalog,'GEN');
  const genesis=bible.books.find(b=>b.id===book.readerBook);
  for(const verse of read('../knowledge-graph/dist/verses.json')){
    const [,chapter,number]=verse.id.split('.');
    assert.equal(verse.text,genesis.chapters[chapter][number]);
    assert.equal(decodeURIComponent(readerLink(book,verse.id).split('#')[1]),`Genesis ${chapter}:${number}`);
  }
});
test('shareable selections preserve stable entity and verse identifiers',()=>{
  const url=selectionUrl('https://example.test/biblical-bot-pages/graph/','GEN','bg:abram','GEN.14.17');
  assert.equal(url.searchParams.get('entity'),'bg:abram');
  assert.equal(url.searchParams.get('verse'),'GEN.14.17');
  assert.equal(selectionUrl(url.href,'GEN','bg:noah',null).searchParams.has('verse'),false);
});
test('annotation licensing remains undecided',()=>{
  assert.equal(read('../knowledge-graph/dist/provenance.json').annotation_license,'Not selected; user decision required. No new license is imposed.');
});
