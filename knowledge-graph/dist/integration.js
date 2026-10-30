export function getBook(catalog,id='GEN') { return catalog.books.find(book=>book.id===id); }
export function readerReference(book,verse) {
  const parts=String(verse).split('.');
  if(parts.length!==3 || parts[0]!==book.id || !/^[1-9]\d*$/.test(parts[1]) || !/^[1-9]\d*$/.test(parts[2]) || Number(parts[1])>book.chapters)throw Error('Invalid source reference');
  return `${book.name} ${parts[1]}:${parts[2]}`;
}
export function readerLink(book,verse) { return '../#'+encodeURIComponent(readerReference(book,verse)); }
export function selectionUrl(href,book,entity,verse) {
  const url=new URL(href);url.searchParams.set('book',book);url.searchParams.set('entity',entity);
  if(verse)url.searchParams.set('verse',verse);else url.searchParams.delete('verse');
  return url;
}
