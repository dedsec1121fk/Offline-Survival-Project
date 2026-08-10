/* MAINTENANCE: Runs only inside the installed/default browser. Never add telemetry or remote diagnostic uploads. */
'use strict';
(() => {
  const $ = id => document.getElementById(id);
  let lang = (navigator.language || '').toLowerCase().startsWith('el') ? 'el' : 'en';
  let latest = {generated_at:null,language:lang,checks:[]};
  const T = {
    en:{
      eyebrow:'OFFLINE SURVIVAL PROJECT', title:'Phone Browser Diagnostics', intro:'Run this page inside the browser actually installed on your phone. Results stay on this device and are not uploaded.',
      langBtn:'Ελληνικά', openApp:'Open Command Center', deviceHeading:'This browser', uaLabel:'User agent', viewportLabel:'Viewport', touchLabel:'Touch points', onlineLabel:'Browser network flag',
      checksHeading:'Local capability checks', checksHelp:'A failure here does not contact the internet; it identifies a browser/device feature that may limit a local function.', runBtn:'Run diagnostics', exportBtn:'Export report',
      offlineHeading:'Offline-use interpretation', offlineText:'The core project is served only from this phone/computer. A green result means the installed browser can use that local feature. Service-worker support improves shell caching, but the local Python server remains the source of database, state and Library content.',
      privacyText:'Privacy: the diagnostic report contains browser/device capability information. It is generated locally and is downloaded only if you choose Export.', rawHeading:'Raw local report',
      pass:'PASS', fail:'FAIL', warn:'LIMITED', ready:'Ready', notAvailable:'Not available', yes:'yes', no:'no',
      tests:{meta:'Command Center API',diagnostics:'Server diagnostics',fetch:'Local fetch',storage:'Local storage',blob:'Local file/export APIs',crypto:'Web Crypto',serviceWorker:'Service worker',manifest:'App manifest',shell:'Offline shell assets',touch:'Touch input',viewport:'Phone viewport/overflow',geolocation:'Geolocation capability',orientation:'Device orientation capability'}
    },
    el:{
      eyebrow:'OFFLINE SURVIVAL PROJECT', title:'Διαγνωστικός έλεγχος browser τηλεφώνου', intro:'Τρέξε αυτή τη σελίδα μέσα στον browser που είναι πραγματικά εγκατεστημένος στο τηλέφωνό σου. Τα αποτελέσματα μένουν στη συσκευή και δεν ανεβαίνουν πουθενά.',
      langBtn:'English', openApp:'Άνοιγμα Κέντρου Ελέγχου', deviceHeading:'Αυτός ο browser', uaLabel:'Αναγνωριστικό browser', viewportLabel:'Περιοχή προβολής', touchLabel:'Σημεία αφής', onlineLabel:'Ένδειξη δικτύου browser',
      checksHeading:'Έλεγχοι τοπικών δυνατοτήτων', checksHelp:'Μια αποτυχία εδώ δεν συνδέεται στο διαδίκτυο· δείχνει ποια δυνατότητα του browser/τηλεφώνου μπορεί να περιορίζει μια τοπική λειτουργία.', runBtn:'Εκτέλεση ελέγχων', exportBtn:'Εξαγωγή αναφοράς',
      offlineHeading:'Ερμηνεία χρήσης χωρίς σύνδεση', offlineText:'Ο πυρήνας του έργου σερβίρεται μόνο από αυτό το τηλέφωνο/υπολογιστή. Πράσινο αποτέλεσμα σημαίνει ότι ο εγκατεστημένος browser μπορεί να χρησιμοποιήσει τη συγκεκριμένη τοπική δυνατότητα. Η υποστήριξη service worker βελτιώνει την προσωρινή αποθήκευση του κελύφους, όμως ο τοπικός Python server παραμένει η πηγή της βάσης, της κατάστασης και της Βιβλιοθήκης.',
      privacyText:'Απόρρητο: η διαγνωστική αναφορά περιέχει πληροφορίες δυνατοτήτων browser/συσκευής. Δημιουργείται τοπικά και κατεβαίνει μόνο αν επιλέξεις Εξαγωγή.', rawHeading:'Ακατέργαστη τοπική αναφορά',
      pass:'ΕΠΙΤΥΧΙΑ', fail:'ΑΠΟΤΥΧΙΑ', warn:'ΠΕΡΙΟΡΙΣΜΟΣ', ready:'Έτοιμο', notAvailable:'Μη διαθέσιμο', yes:'ναι', no:'όχι',
      tests:{meta:'API Κέντρου Ελέγχου',diagnostics:'Διαγνωστικά server',fetch:'Τοπικό fetch',storage:'Τοπική αποθήκευση',blob:'Τοπικά αρχεία/εξαγωγές',crypto:'Web Crypto',serviceWorker:'Service worker',manifest:'Manifest εφαρμογής',shell:'Αρχεία offline κελύφους',touch:'Είσοδος αφής',viewport:'Προβολή τηλεφώνου/υπερχείλιση',geolocation:'Δυνατότητα γεωεντοπισμού',orientation:'Δυνατότητα προσανατολισμού συσκευής'}
    }
  };

  function text(id,key){ const el=$(id); if(el) el.textContent=T[lang][key]; }
  function applyLanguage(){
    document.documentElement.lang=lang==='el'?'el':'en';
    ['eyebrow','title','intro','langBtn','openApp','deviceHeading','uaLabel','viewportLabel','touchLabel','onlineLabel','checksHeading','checksHelp','runBtn','exportBtn','offlineHeading','offlineText','privacyText','rawHeading'].forEach(k=>text(k,k));
    render();
  }
  function setDeviceInfo(){
    $('ua').textContent=navigator.userAgent || '—';
    $('viewport').textContent=`${window.innerWidth}×${window.innerHeight} CSS px · DPR ${window.devicePixelRatio || 1}`;
    $('touch').textContent=String(navigator.maxTouchPoints || 0);
    $('online').textContent=navigator.onLine ? T[lang].yes : T[lang].no;
  }
  function row(name,status,detail){ return {name,status,detail:String(detail || '')}; }
  function status(ok,limited=false){ return ok?'pass':(limited?'warn':'fail'); }
  async function fetchJson(path){ const r=await fetch(path,{cache:'no-store',credentials:'same-origin'}); if(!r.ok) throw new Error(`${r.status} ${r.statusText}`); return r.json(); }
  async function fetchText(path){ const r=await fetch(path,{cache:'no-store',credentials:'same-origin'}); if(!r.ok) throw new Error(`${r.status} ${r.statusText}`); return r.text(); }

  async function run(){
    $('runBtn').disabled=true;
    const checks=[];
    try{ const meta=await fetchJson('/api/meta'); checks.push(row('meta',status(!!meta),'Local API available')); }catch(e){ checks.push(row('meta','fail',e.message)); }
    try{ const d=await fetchJson('/api/diagnostics'); checks.push(row('diagnostics',status(Boolean(d.ok)),`${(d.checks||[]).filter(x=>x.ok).length}/${(d.checks||[]).length}`)); }catch(e){ checks.push(row('diagnostics','fail',e.message)); }
    try{ const txt=await fetchText('/manifest.webmanifest'); checks.push(row('fetch',status(txt.length>20),`${txt.length} bytes from localhost`)); }catch(e){ checks.push(row('fetch','fail',e.message)); }
    try{ const key='osp-phone-test'; localStorage.setItem(key,'ok'); const ok=localStorage.getItem(key)==='ok'; localStorage.removeItem(key); checks.push(row('storage',status(ok),ok?'read/write works':'read/write mismatch')); }catch(e){ checks.push(row('storage','fail',e.message)); }
    try{ const blob=new Blob(['offline-survival'],{type:'text/plain'}); const u=URL.createObjectURL(blob); URL.revokeObjectURL(u); checks.push(row('blob','pass',`${blob.size} bytes`)); }catch(e){ checks.push(row('blob','fail',e.message)); }
    checks.push(row('crypto',status(Boolean(globalThis.crypto && crypto.subtle),true),globalThis.crypto && crypto.subtle ? 'crypto.subtle available' : 'crypto.subtle unavailable'));
    if('serviceWorker' in navigator){
      try{ const reg=await navigator.serviceWorker.register('/sw.js'); checks.push(row('serviceWorker','pass',reg.scope)); }catch(e){ checks.push(row('serviceWorker','fail',e.message)); }
    }else checks.push(row('serviceWorker','warn',T[lang].notAvailable));
    try{ const m=JSON.parse(await fetchText('/manifest.webmanifest')); checks.push(row('manifest',status(Boolean(m.name && m.start_url)),m.name || 'manifest parsed')); }catch(e){ checks.push(row('manifest','fail',e.message)); }
    try{ const paths=['/styles.css','/app.js','/field-operations.js','/continuity-operations.js','/knowledge-atlas.js']; const sizes=[]; for(const p of paths){ const t=await fetchText(p); sizes.push(`${p}:${t.length}`); } checks.push(row('shell','pass',sizes.join(' · '))); }catch(e){ checks.push(row('shell','fail',e.message)); }
    const touch=(navigator.maxTouchPoints||0)>0 || 'ontouchstart' in window;
    checks.push(row('touch',status(touch,true),`${navigator.maxTouchPoints||0} touch points`));
    const overflow=Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)-window.innerWidth;
    checks.push(row('viewport',status(overflow<=2),`viewport ${window.innerWidth}px · horizontal overflow ${Math.max(0,overflow)}px`));
    checks.push(row('geolocation',status('geolocation' in navigator,true),'geolocation' in navigator?'API present; permission not requested':'API absent'));
    checks.push(row('orientation',status('DeviceOrientationEvent' in window,true),'DeviceOrientationEvent' in window?'API present; permission not requested':'API absent'));
    latest={
      generated_at:new Date().toISOString(), language:lang, project:'Offline Survival Project',
      location:{origin:location.origin,pathname:location.pathname},
      browser:{user_agent:navigator.userAgent,language:navigator.language,max_touch_points:navigator.maxTouchPoints||0,viewport:[window.innerWidth,window.innerHeight],device_pixel_ratio:window.devicePixelRatio||1,on_line_flag:navigator.onLine},
      checks
    };
    $('runBtn').disabled=false;
    render();
  }
  function render(){
    setDeviceInfo();
    const names=T[lang].tests;
    $('results').innerHTML=(latest.checks||[]).map(c=>{
      const label=c.status==='pass'?T[lang].pass:c.status==='warn'?T[lang].warn:T[lang].fail;
      return `<div class="diag-result"><strong>${escapeHtml(names[c.name]||c.name)}</strong><span class="${c.status}">${escapeHtml(label)}</span><code>${escapeHtml(c.detail)}</code></div>`;
    }).join('') || `<p>${escapeHtml(T[lang].ready)}</p>`;
    $('raw').textContent=JSON.stringify(latest,null,2);
  }
  function escapeHtml(v){ return String(v).replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c])); }
  function exportReport(){
    const payload=JSON.stringify(latest,null,2)+'\n';
    const blob=new Blob([payload],{type:'application/json'});
    const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=`offline-survival-phone-browser-${new Date().toISOString().replace(/[:.]/g,'-')}.json`; document.body.appendChild(a); a.click(); a.remove(); setTimeout(()=>URL.revokeObjectURL(a.href),1000);
  }
  $('langBtn').addEventListener('click',()=>{lang=lang==='en'?'el':'en';latest.language=lang;applyLanguage();});
  $('runBtn').addEventListener('click',run);
  $('exportBtn').addEventListener('click',exportReport);
  addEventListener('resize',()=>{setDeviceInfo();});
  applyLanguage(); run();
})();
