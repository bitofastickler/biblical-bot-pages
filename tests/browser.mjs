import {chromium,firefox} from '@playwright/test';
import assert from 'node:assert/strict';
import {mkdir,readFile,writeFile} from 'node:fs/promises';
const url=process.env.TEST_URL||'http://127.0.0.1:4173/biblical-bot-pages/';
await mkdir('.local',{recursive:true});
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1000}});
const errors=[];page.on('pageerror',e=>errors.push(e.message));
const responses=[];page.on('response',r=>{if(r.status()>=400)responses.push(`${r.status()} ${r.url()}`);});
await page.goto(url);await page.locator('#workspace').waitFor({state:'visible'});
await page.locator('#lookup').fill('John 3:16-18');await page.locator('#lookup-form button').click();
assert.equal(await page.locator('#passage-title').textContent(),'John 3:16–18');assert.equal(await page.locator('.verse').count(),3);
await page.locator('#new-study').click();await page.locator('#study-title').fill('A study of love');
await page.locator('#observation').fill('God so loved the world.');await page.locator('#interpretation').fill('Read this with John 3:1–21.');await page.locator('#application').fill('Show patient love today.');
await page.locator('#notes').fill('<img src=x onerror="alert(1)"> stays plain text.');
const downloadPromise=page.waitForEvent('download');await page.locator('#save').click();const download=await downloadPromise;await download.saveAs('.local/roundtrip.json');
const saved=JSON.parse(await readFile('.local/roundtrip.json','utf8'));assert.equal(saved.translation,'WEB');assert.equal(saved.references[0],'John 3:16–18');
await page.locator('#search').fill('peace');await page.locator('#search-form button').click();assert.ok(await page.locator('.result').count()>0);await page.locator('.result').first().click();await page.locator('#study-passage').click();assert.equal(await page.locator('.ref-chip').count(),2);await page.locator('#close-results').click();
await page.screenshot({path:'.local/desktop.png',fullPage:true});
for(const [name,content,expected] of [['malformed','{','Invalid JSON'],['version',JSON.stringify({...saved,version:7}),'Unsupported study version'],['key',JSON.stringify({...saved,apiKey:'test'}),'unexpected fields'],['large',' '.repeat(2_000_001),'too large']]){
  await page.locator('#file').setInputFiles({name:`${name}.json`,mimeType:'application/json',buffer:Buffer.from(content)});
  await page.getByRole('status').filter({hasText:expected}).waitFor();assert.equal(await page.locator('#study-title').inputValue(),'A study of love');
}
// An independent browser engine with a fresh profile receives only the downloaded file.
const second=await firefox.launch({headless:true});const fresh=await second.newPage();await fresh.goto(url);await fresh.locator('#workspace').waitFor({state:'visible'});await fresh.locator('#file').setInputFiles('.local/roundtrip.json');await fresh.getByRole('status').filter({hasText:'Study ready'}).waitFor();
assert.equal(await fresh.locator('#observation').inputValue(),'God so loved the world.');assert.equal(await fresh.locator('#passage-title').textContent(),'John 3:16–18');assert.equal(await fresh.locator('#notes').inputValue(),saved.content.notes);assert.equal(await fresh.locator('.notebook img').count(),0);
await fresh.locator('#notes').fill('Continued in Firefox.');const d2=fresh.waitForEvent('download');await fresh.locator('#save').click();await(await d2).saveAs('.local/continued.json');assert.equal(JSON.parse(await readFile('.local/continued.json','utf8')).content.notes,'Continued in Firefox.');
await fresh.reload();await fresh.getByRole('status').filter({hasText:'Restored'}).waitFor();assert.equal(await fresh.locator('#notes').inputValue(),'Continued in Firefox.');
// Replacement can be cancelled without losing edits.
await fresh.locator('#new-study').click();await fresh.locator('#replace-cancel').click();assert.equal(await fresh.locator('#notes').inputValue(),'Continued in Firefox.');await second.close();
for(const width of [390,320]){
  const mobile=await browser.newPage({viewport:{width,height:844},isMobile:true,hasTouch:true});await mobile.goto(url);await mobile.locator('#workspace').waitFor({state:'visible'});
  assert.ok(await mobile.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),`horizontal overflow at ${width}`);
  await mobile.locator('#lookup').fill('Psalm 23');await mobile.locator('#lookup-form button').click();assert.equal(await mobile.locator('#passage-title').textContent(),'Psalms 23');
  await mobile.locator('#study-passage').click();await mobile.locator('#observation').fill('A mobile reflection');
  const d=mobile.waitForEvent('download');await mobile.locator('#save').click();await(await d).saveAs(`.local/mobile-${width}.json`);
  await mobile.screenshot({path:`.local/mobile-${width}.png`,fullPage:true});await mobile.close();
}
// Denied storage must not prevent reading or saving.
const blocked=await browser.newPage();await blocked.addInitScript(()=>{Storage.prototype.setItem=()=>{throw Error('denied');};Storage.prototype.getItem=()=>{throw Error('denied');};});await blocked.goto(url);await blocked.locator('#workspace').waitFor({state:'visible'});await blocked.locator('#notes').fill('Still usable');assert.match(await blocked.locator('#recovery-status').textContent(),/unavailable/);await blocked.close();
assert.deepEqual(errors,[]);assert.deepEqual(responses,[]);await browser.close();
await writeFile('.local/browser-result.json',JSON.stringify({url,passed:true,checks:['Chromium save → Firefox open → continue → save','safe text rendering','malformed/version/extra-field/oversize rejection','cancel replacement','browser recovery','storage denial','390px and 320px mobile reading/edit/download','project subpath assets'],errors,responses},null,2));console.log('Browser checks passed:',url);
