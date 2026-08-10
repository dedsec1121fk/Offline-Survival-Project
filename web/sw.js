/* MAINTENANCE: Cache only the local app shell. API and Library content must stay outside runtime cache writes. */
const CACHE='offline-survival-shell';
const SHELL=['/','/styles.css','/app.js','/field-operations.js','/continuity-operations.js','/knowledge-atlas.js','/phone-test.html','/phone-test.js','/reader.html','/manifest.webmanifest'];
const SHELL_PATHS=new Set(SHELL);
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting())));
self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',event=>{
  if(event.request.method!=='GET')return;
  const url=new URL(event.request.url);
  if(url.origin!==self.location.origin)return;
  if(url.pathname.startsWith('/api/')||url.pathname.startsWith('/library/'))return;
  if(SHELL_PATHS.has(url.pathname)){
    event.respondWith(caches.match(event.request).then(hit=>hit||fetch(event.request).then(resp=>{if(resp.ok){const clone=resp.clone();caches.open(CACHE).then(c=>c.put(event.request,clone));}return resp;})));
    return;
  }
  if(event.request.mode==='navigate'){
    event.respondWith(fetch(event.request).catch(()=>caches.match('/')));
  }
});
