export const MAX_BYTES = 2_000_000;
const normalize = s => s.toLowerCase().replace(/[^a-z0-9]/g,'');
export function lookup(bible, input) {
  const match = input.trim().match(/^(.+?)(?:\s+(\d+)(?::(\d+)(?:\s*[-–]\s*(\d+))?)?)?$/);
  if (!match) throw Error('Use a reference such as John 3:16–18 or Psalm 23.');
  const key = normalize(match[1]);
  const aliases = {ps:'psalms',psalm:'psalms',psa:'psalms',jn:'john',jhn:'john',songofsongs:'songofsolomon',canticles:'songofsolomon',jas:'james',phlm:'philemon'};
  const wanted = aliases[key] || key;
  let book = bible.books.find(b=>b.id===wanted);
  if (!book) {const candidates=bible.books.filter(b=>b.id.startsWith(wanted)); if(wanted.length>=2 && candidates.length===1) book=candidates[0];}
  if (!book) throw Error('Book not recognized. Try a full name, such as 1 Corinthians 13.');
  const chapter = Number(match[2] || 1), verses = book.chapters[chapter];
  if (!verses) throw Error(`${book.name} has ${Object.keys(book.chapters).length} chapters.`);
  const start = match[3] ? Number(match[3]) : null, end = match[4] ? Number(match[4]) : start;
  if (start!==null && (!verses[start] || !verses[end] || end<start)) throw Error(`That verse range is not available in ${book.name} ${chapter}.`);
  return {book:book.id,chapter,start,end,reference:`${book.name} ${chapter}${start!==null?`:${start}${end!==start?`–${end}`:''}`:''}`};
}
export function search(bible, query, bookId='') {
  const tokens = query.toLowerCase().trim().split(/\s+/).filter(Boolean);
  if (!tokens.length) return [];
  const found=[];
  for(const book of bible.books) {
    if(bookId && book.id!==bookId) continue;
    for(const [chapter,verses] of Object.entries(book.chapters)) for(const [verse,text] of Object.entries(verses)) {
      if(tokens.every(t=>text.toLowerCase().includes(t))) found.push({reference:`${book.name} ${chapter}:${verse}`,text});
    }
  }
  return found;
}
export function newStudy(reference='John 1') {
  const now = new Date().toISOString();
  return {format:'biblical-bot-study',version:1,title:`Study of ${reference}`,createdAt:now,updatedAt:now,translation:'WEB',references:[reference],reader:reference,content:{observation:'',interpretation:'',application:'',notes:''},entries:[]};
}
function text(value,max,label,empty=true) {
  if(typeof value!=='string' || value.length>max || (!empty&&!value.trim())) throw Error(`Invalid ${label}. Expected ${empty?'':'nonempty '}text up to ${max} characters.`);
  return value;
}
function date(value,label) {
  if(typeof value!=='string'||!/^\d{4}-\d{2}-\d{2}T/.test(value)||!Number.isFinite(Date.parse(value))) throw Error(`Invalid ${label}.`);
  return new Date(value).toISOString();
}
function keys(object, allowed,label) {
  if(!object || typeof object!=='object'||Array.isArray(object)||Object.keys(object).some(k=>!allowed.includes(k))) throw Error(`Invalid or unexpected fields in ${label}. Credentials and extra fields are not supported.`);
}
export function validateStudy(raw,bible) {
  keys(raw,['format','version','title','createdAt','updatedAt','translation','references','reader','content','entries'],'study');
  if(raw.format!=='biblical-bot-study') throw Error('This is not an Open Study file. Use a downloaded study JSON snapshot.');
  if(raw.version!==1) throw Error('Unsupported study version. This app supports version 1; keep your original file.');
  if(raw.translation!=='WEB') throw Error('Unsupported translation. This release supports WEB.');
  const ref = v=>lookup(bible,text(v,100,'scripture reference',false)).reference;
  if(!Array.isArray(raw.references)||raw.references.length<1||raw.references.length>500) throw Error('A study needs 1–500 scripture references.');
  keys(raw.content,['observation','interpretation','application','notes'],'study content');
  if(!Array.isArray(raw.entries)||raw.entries.length>500) throw Error('Invalid study entries (maximum 500).');
  const result={format:raw.format,version:1,title:text(raw.title,200,'title',false),createdAt:date(raw.createdAt,'creation timestamp'),updatedAt:date(raw.updatedAt,'update timestamp'),translation:'WEB',references:raw.references.map(ref),reader:ref(raw.reader),content:Object.fromEntries(['observation','interpretation','application','notes'].map(k=>[k,text(raw.content[k],100000,k)])),entries:raw.entries.map(e=>{
    keys(e,['reference','body','createdAt'],'entry');
    return {reference:ref(e.reference),body:text(e.body,100000,'entry',false),createdAt:date(e.createdAt,'entry timestamp')};
  })};
  if(Date.parse(result.updatedAt)<Date.parse(result.createdAt)) throw Error('Update timestamp cannot precede creation.');
  return result;
}
export function parseStudy(json,bible) {
  if(new TextEncoder().encode(json).length>MAX_BYTES) throw Error('Study file is too large. Maximum size is 2 MB.');
  let raw; try {raw=JSON.parse(json);} catch {throw Error('Invalid JSON. Choose an intact .json file downloaded with Save study.');}
  return validateStudy(raw,bible);
}
export function serializeStudy(study,bible) {
  const json=JSON.stringify(validateStudy(study,bible),null,2);
  if(new TextEncoder().encode(json).length>MAX_BYTES) throw Error('This study exceeds 2 MB. Shorten it before saving.');
  return json;
}
