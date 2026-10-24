import http from 'node:http';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
const root = path.resolve('dist');
http.createServer(async (req,res)=>{
  try {
    let url = decodeURIComponent(new URL(req.url,'http://localhost').pathname);
    // Serve under a project subpath too, to exercise GitHub Pages paths.
    url = url.replace(/^\/biblical-bot-pages(?=\/)/,'');
    const file = path.resolve(root, `.${url.endsWith('/') ? url+'index.html' : url}`);
    if (!file.startsWith(root+path.sep)) throw Error();
    const content = await readFile(file);
    res.setHeader('Content-Type', ({'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json'})[path.extname(file)] || 'application/octet-stream');
    res.end(content);
  } catch {res.writeHead(404);res.end('Not found');}
}).listen(4173,'127.0.0.1',()=>console.log('http://127.0.0.1:4173/biblical-bot-pages/'));
