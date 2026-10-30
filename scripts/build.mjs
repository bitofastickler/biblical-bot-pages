import { mkdir, cp } from 'node:fs/promises';
await mkdir('dist', {recursive:true});
for (const p of ['index.html','styles.css','src','data','about.html']) await cp(p, `dist/${p}`, {recursive:true});
await cp('knowledge-graph/dist', 'dist/graph', {recursive:true});
await cp('knowledge-graph/LICENSING.md', 'dist/graph/licensing.md');
await cp('LICENSE', 'dist/graph/code-license.txt');
console.log('Static app built in dist/; all asset URLs are relative.');
