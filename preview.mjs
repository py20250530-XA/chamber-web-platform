import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
const root = dirname(fileURLToPath(import.meta.url));
const pages = new Set(['index.html','company-application.html','service-application.html','cooperation-application.html','activity-application.html','research-application.html','consultation-application.html','applications.html','ru.html','uz.html','styles.css','tailwind.css','app.js']);
const types = { html: 'text/html; charset=utf-8', css: 'text/css; charset=utf-8', js: 'text/javascript; charset=utf-8' };
const port = Number(process.env.PORT || 8000);
createServer(async (req, res) => {
  res.setHeader('X-Content-Type-Options','nosniff');
  res.setHeader('Referrer-Policy','same-origin');
  res.setHeader('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'");
  if (!['GET','HEAD'].includes(req.method)) { res.writeHead(405); res.end(); return; }
  let path;
  try { path = decodeURIComponent(new URL(req.url, 'http://localhost').pathname); } catch { res.writeHead(400); res.end(); return; }
  const file = path === '/' ? 'index.html' : path.slice(1);
  if (!pages.has(file)) { res.writeHead(404); res.end('Not found'); return; }
  try {
    const body = await readFile(join(root,file));
    res.setHeader('Content-Type', types[file.split('.').pop()]);
    res.setHeader('Content-Length',body.length);
    res.setHeader('Cache-Control','no-cache');
    res.writeHead(200); res.end(req.method === 'HEAD' ? undefined : body);
  } catch { res.writeHead(404); res.end('Not found'); }
}).listen(port,'0.0.0.0',()=>console.log(`Static preview started on port ${port}`));
