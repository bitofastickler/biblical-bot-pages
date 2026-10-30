import {lookup,search,newStudy,parseStudy,serializeStudy,MAX_BYTES} from './core.js';
const $ = id=>document.getElementById(id), key='biblical-bot-recovery-v1';
let bible, study, passage, dirty=false, recoveryEnabled=true, pending=null, results=[], resultLimit=30;
const status=(message,error=false)=>{$('status').textContent=message;$('status').classList.toggle('error',error);};
const node=(tag,text,className)=>{const e=document.createElement(tag);e.textContent=text;if(className)e.className=className;return e;};
function recovery() {
  if(!recoveryEnabled) return;
  try {localStorage.setItem(key,serializeStudy(study,bible));$('recovery-status').textContent='Recovery copy updated in this browser.';}
  catch {$('recovery-status').textContent='Browser recovery unavailable. Download a snapshot to protect your work.';}
}
function changed() {study.updatedAt=new Date().toISOString();dirty=true;recovery();}
function renderReader(reference, focus=false, updateHistory=true) {
  const next=lookup(bible,reference);passage=next;
  const book=bible.books.find(b=>b.id===next.book);
  const graphUrl=new URL('./graph/',location.href);
  graphUrl.searchParams.set('book',next.book==='genesis'?'GEN':next.book);
  if(next.book==='genesis')graphUrl.searchParams.set('verse',`GEN.${next.chapter}.${next.start||1}`);
  $('passage-graph').href=graphUrl.href;
  $('passage-graph').textContent=next.book==='genesis'?'Explore this passage in the graph':'Explore Bible graph';
  $('graph-coverage').textContent=next.book==='genesis'?' — Selected Genesis annotations.':' — Graph coverage is currently Genesis only.';
  const hash='#'+encodeURIComponent(next.reference);
  if(updateHistory && location.hash!==hash)history.pushState({readerReference:next.reference},'',hash);
  $('passage-title').textContent=next.reference;$('book').value=book.id;
  $('chapter').replaceChildren(...Object.keys(book.chapters).map(c=>new Option(c,c)));$('chapter').value=next.chapter;
  $('verses').replaceChildren(...Object.entries(book.chapters[next.chapter]).filter(([v])=>next.start===null||(Number(v)>=next.start&&Number(v)<=next.end)).map(([v,text])=>{
    const p=node('p','',`verse${next.start!==null?' focused':''}`);p.append(node('span',v,'verse-num'),document.createTextNode(text));return p;
  }));
  $('full-chapter').hidden=next.start===null;
  $('previous').disabled=book===bible.books[0]&&next.chapter===1;
  $('next').disabled=book===bible.books.at(-1)&&next.chapter===Object.keys(book.chapters).length;
  if(study) {study.reader=next.reference;recovery();}
  if(focus)$('reader').focus();
}
function renderStudy() {
  $('study-title').value=study.title;
  for(const field of ['observation','interpretation','application','notes'])$(field).value=study.content[field];
  $('references').replaceChildren(...study.references.map(ref=>{const b=node('button',ref,'ref-chip');b.onclick=()=>renderReader(ref,true);return b;}));
  $('entries').replaceChildren(...study.entries.map(entry=>{const e=node('section','','entry');const b=node('button',entry.reference,'ref-chip');b.onclick=()=>renderReader(entry.reference,true);e.append(b,node('p',entry.body));return e;}));
}
function save() {
  try {
    const data=serializeStudy(study,bible), blob=new Blob([data],{type:'application/json'}), url=URL.createObjectURL(blob);
    const a=document.createElement('a');a.href=url;a.download=`${study.title.replace(/[^a-z0-9]+/gi,'-').slice(0,65)||'study'}-${new Date().toISOString().replace(/[:.]/g,'-')}.json`;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),10000);dirty=false;
    status('Snapshot download requested. Keep the JSON file; future saves create new snapshots.');return true;
  } catch(e){status(e.message,true);return false;}
}
function replace(next) {
  pending=()=>{study=next;dirty=false;renderStudy();renderReader(study.reader);recovery();status('Study ready. Your notes stay on this device until you download or share a file.');};
  if(dirty || study.content.observation || study.content.interpretation || study.content.application || study.content.notes || study.entries.length) $('replace-dialog').showModal();
  else {pending();pending=null;}
}
function renderResults() {
  $('result-count').textContent=`${results.length} matching verses · showing ${Math.min(resultLimit,results.length)}`;
  $('results').replaceChildren(...results.slice(0,resultLimit).map(result=>{const b=node('button','','result');b.append(node('strong',result.reference),node('span',result.text));b.onclick=()=>{renderReader(result.reference,true);status(`Reading ${result.reference}. Add this passage to your study to keep its reference.`);};return b;}));
  $('more-results').hidden=resultLimit>=results.length;
}
async function start() {
  try {
    const response=await fetch(new URL('../data/web.json',import.meta.url));if(!response.ok)throw Error('Bible download failed');bible=await response.json();
    $('book').replaceChildren(...bible.books.map(b=>new Option(b.name,b.id)));
    $('search-scope').append(...bible.books.map(b=>new Option(b.name,b.id)));
    study=newStudy('John 1');let recovered=false, invalidRecovery=false;
    try {const stored=localStorage.getItem(key);if(stored){study=parseStudy(stored,bible);recovered=true;}} catch {invalidRecovery=true;}
    renderStudy();renderReader(study.reader,false,false);$('workspace').hidden=false;$('save').disabled=false;$('open').disabled=false;
    status(invalidRecovery?'Browser recovery could not be read. Open a downloaded snapshot to restore your study.':recovered?'Restored your browser recovery copy. Download a snapshot for a durable backup.':'A quiet place to read, reflect, and keep what you discover. No account needed.',invalidRecovery);
    if(!location.hash)history.replaceState(null,'','#'+encodeURIComponent(study.reader));
    if(location.hash && !['#reader','#study-notebook','#bible-navigation'].includes(location.hash)){try{renderReader(decodeURIComponent(location.hash.slice(1)),false,false);}catch(e){status(e.message,true);}}
    history.replaceState({readerReference:passage.reference},'',location.href);
  }catch{status('The Bible could not load. Check your connection and reload this page. Your downloaded study files are safe.',true);}
}
$('lookup-form').onsubmit=e=>{e.preventDefault();try{renderReader($('lookup').value,true);status(`Reading ${passage.reference}.`);}catch(err){status(err.message,true);}};
$('book').onchange=()=>renderReader(bible.books.find(b=>b.id===$('book').value).name+' 1');
$('chapter').onchange=()=>renderReader(bible.books.find(b=>b.id===passage.book).name+' '+$('chapter').value);
function moveChapter(direction) {const index=bible.books.findIndex(b=>b.id===passage.book),book=bible.books[index];let c=passage.chapter+direction,b=book;if(c<1){b=bible.books[index-1];c=Object.keys(b.chapters).length;}else if(c>Object.keys(book.chapters).length){b=bible.books[index+1];c=1;}renderReader(`${b.name} ${c}`,true);}
$('previous').onclick=()=>moveChapter(-1);$('next').onclick=()=>moveChapter(1);
$('full-chapter').onclick=()=>renderReader(`${bible.books.find(b=>b.id===passage.book).name} ${passage.chapter}`,true);
$('text-size').onclick=()=>{$('reader').classList.toggle('large');$('text-size').setAttribute('aria-pressed',$('reader').classList.contains('large'));};
document.querySelectorAll('[data-ref]').forEach(b=>b.onclick=()=>renderReader(b.dataset.ref,true));
$('search-form').onsubmit=e=>{e.preventDefault();if(!$('search').value.trim()){status('Enter a word or phrase to search.',true);return;}results=search(bible,$('search').value,$('search-scope').value);resultLimit=30;renderResults();$('results-panel').hidden=false;status(`${results.length} verses found. Search matches words in the Bible text, not themes or synonyms.`);$('results-panel').scrollIntoView({block:'start'});};
$('close-results').onclick=()=>{$('results-panel').hidden=true;};$('more-results').onclick=()=>{resultLimit+=30;renderResults();};
$('study-passage').onclick=()=>{if(!study.references.includes(passage.reference)){if(study.references.length>=500){status('A study can contain up to 500 references.',true);return;}study.references.push(passage.reference);changed();renderStudy();}status(`${passage.reference} is in your study. Add your observations in the notebook.`);};
$('study-title').oninput=()=>{study.title=$('study-title').value;changed();};
for(const field of ['observation','interpretation','application','notes'])$(field).oninput=()=>{study.content[field]=$(field).value;changed();};
$('save').onclick=save;$('open').onclick=()=>$('file').click();
$('file').onchange=async()=>{const file=$('file').files[0];$('file').value='';if(!file)return;try{if(file.size>MAX_BYTES)throw Error('Study file is too large. Maximum size is 2 MB.');const next=parseStudy(await file.text(),bible);replace(next);}catch(e){status(e.message+' Your current notebook has not been replaced.',true);}};
$('new-study').onclick=()=>replace(newStudy(passage.reference));
$('replace-cancel').onclick=()=>{pending=null;$('replace-dialog').close();};
$('replace-confirm').onclick=()=>{pending?.();pending=null;$('replace-dialog').close();};
$('replace-save').onclick=()=>{if(save()){pending?.();pending=null;$('replace-dialog').close();status('Previous study download requested. The new notebook is ready.');}};
$('replace-dialog').addEventListener('cancel',()=>{pending=null;});
$('clear-recovery').onclick=()=>{try{localStorage.removeItem(key);recoveryEnabled=false;$('recovery-status').textContent='Browser recovery cleared and paused until reload. Your current notebook remains open.';}catch{status('This browser did not allow recovery storage to be cleared.',true);}};
window.addEventListener('beforeunload',e=>{if(dirty){e.preventDefault();e.returnValue='';}});
const sectionHashes=['#reader','#study-notebook','#bible-navigation'];
document.querySelectorAll('a[href^="#"]').forEach(link=>link.addEventListener('click',e=>{
  const hash=link.getAttribute('href');
  if(!passage || !sectionHashes.includes(hash))return;
  e.preventDefault();
  if(location.hash!==hash)history.pushState({readerReference:passage.reference},'',hash);
  const target=document.getElementById(hash.slice(1));target.scrollIntoView();target.focus({preventScroll:true});
}));
window.addEventListener('popstate',e=>{
  if(!bible || !sectionHashes.includes(location.hash) || !e.state?.readerReference)return;
  try{renderReader(e.state.readerReference,false,false);}catch(err){status(err.message,true);}
});
window.addEventListener('hashchange',()=>{
  if(!bible || !location.hash || ['#reader','#study-notebook','#bible-navigation'].includes(location.hash))return;
  try{renderReader(decodeURIComponent(location.hash.slice(1)),false,false);}catch(e){status(e.message,true);}
});
start();
