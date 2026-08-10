#!/usr/bin/env node
// MAINTENANCE: Exercise UI/state/export logic deterministically without binding the project to a desktop browser engine.
'use strict';
const fs=require('fs'),vm=require('vm'),path=require('path');
const ROOT=path.resolve(__dirname,'..');
const elements=new Map();
function element(id=''){
  if(elements.has(id))return elements.get(id);
  const e={id,value:'',innerHTML:'',textContent:'',dataset:{},style:{},checked:false,files:[],
    classList:{add(){},remove(){},toggle(){},contains(){return false}},
    addEventListener(){},setAttribute(){},removeAttribute(){},focus(){},click(){},
    appendChild(){},querySelector(){return null},querySelectorAll(){return []}};
  elements.set(id,e);return e;
}
const document={
  documentElement:{lang:'en',classList:{toggle(){}}},activeElement:null,title:'',
  querySelector(sel){if(sel.startsWith('#'))return element(sel.slice(1));return element(sel)},
  querySelectorAll(){return []},createElement(){return element('created-'+Math.random())},body:element('body')
};
const localStore=new Map();
const box={console,document,window:{scrollTo(){},print(){},location:{origin:'http://127.0.0.1'}},navigator:{},
  localStorage:{getItem:k=>localStore.get(k)||null,setItem:(k,v)=>localStore.set(k,String(v))},
  structuredClone:global.structuredClone,URL,Blob,Date,Math,JSON,Number,String,Array,Object,Set,Map,Intl,
  decodeURIComponent,encodeURIComponent,setTimeout:()=>0,clearTimeout(){},fetch:async()=>{throw new Error('network disabled in UI logic test')}};
vm.createContext(box);
let app=fs.readFileSync(path.join(ROOT,'web','app.js'),'utf8').replace(/\ninit\(\);\s*$/,'');
let fieldOps=fs.readFileSync(path.join(ROOT,'web','field-operations.js'),'utf8').replace(/\napplyLang\(\);\s*$/,'');
let continuityOps=fs.readFileSync(path.join(ROOT,'web','continuity-operations.js'),'utf8').replace(/\napplyLang\(\);\s*$/,'');
let knowledgeAtlas=fs.readFileSync(path.join(ROOT,'web','knowledge-atlas.js'),'utf8').replace(/\napplyLang\(\);\s*$/,'');
vm.runInContext(app,box,{filename:'app.js'});
vm.runInContext(fieldOps,box,{filename:'field-operations.js'});
vm.runInContext(continuityOps,box,{filename:'continuity-operations.js'});
vm.runInContext(knowledgeAtlas,box,{filename:'knowledge-atlas.js'});
vm.runInContext('saveState=async()=>state; state=mergeState({}); lang="en";',box);
const checks=[];
function check(name,condition,detail=''){checks.push([name,!!condition,detail]);console.log(`[${condition?'PASS':'FAIL'}] ${name}${detail?' — '+detail:''}`)}
function set(id,value){element(id).value=String(value)}
function run(code){return vm.runInContext(code,box)}

try{
  set('zoneName','Main room');set('zoneStatus','safe');set('zoneOccupants',3);set('zoneUtilities','battery light');set('zoneNotes','dry access');run('addShelterZone()');
  check('shelter-add',run('state.shelter_zones.length===1 && state.shelter_zones[0].occupants===3'));
  check('shelter-render',element('shelterTable').innerHTML.includes('Main room'));

  set('waterSource','sealed storage');set('waterVolume',18);set('waterMethod','logged handling');set('waterStatus','ready');set('waterContainer','blue can');run('addWaterBatch()');
  check('water-add',run('state.water_batches.length===1 && state.water_batches[0].volume_l===18'));
  check('water-summary',element('waterBatchSummary').innerHTML.includes('18'));

  set('recoveryArea','South door');set('recoverySeverity','major');set('recoveryStatus','isolated');set('recoveryOwner','Alex');set('recoveryAction','keep closed');set('recoveryNotes','frame moved');run('addRecoveryItem()');
  check('recovery-add',run('state.recovery_items.length===1 && state.recovery_items[0].severity==="major"'));
  check('recovery-render',element('recoveryTable').innerHTML.includes('South door'));

  set('skillPerson','Alex');set('skillName','Radio check');set('skillLevel','practiced');set('skillLast','2026-08-01');set('skillNext','2026-09-01');run('addSkill()');
  set('skillPerson','Maria');set('skillName','Radio check');set('skillLevel','confident');set('skillLast','2026-08-02');set('skillNext','2026-09-02');run('addSkill()');
  check('skills-add',run('state.skill_matrix.length===2'));
  check('skills-backup-detected',element('skillsSummary').innerHTML.includes('1'));

  set('decisionIssue','Primary route blocked');set('decisionValue','Use north route');set('decisionReason','bridge closed');set('decisionOwner','Alex');set('decisionStatus','active');set('decisionNext','2026-08-09T01:00');run('addDecision()');
  check('decision-add',run('state.decision_board.length===1'));
  check('decision-render',element('decisionTable').innerHTML.includes('Primary route blocked'));

  run('lang="el"; renderFieldOperations();');
  check('greek-shelter-status',element('shelterTable').innerHTML.includes('Χρήσιμη'));
  check('greek-water-status',element('waterBatchTable').innerHTML.includes('Αποδεκτό'));
  check('greek-decision-status',element('decisionTable').innerHTML.includes('Ενεργή'));
  check('nav-field-sections',run('["shelter","waterops","recovery","skills","decisions"].every(id=>NAV.some(x=>x[0]===id))'));
  check('state-schema',run('DEFAULT_STATE.schema_version===7'));
  check('nav-knowledge-section',run('NAV.some(x=>x[0]==="knowledge") && MOBILE_NAV.includes("knowledge")'));
  run(`libraryCache=[{path:'Knowledge Compendium/EN/00-compendium-index-and-use.md',name:'00-compendium-index-and-use.md',size_human:'3 KB',readable:true},{path:'Knowledge Compendium/EN/01-emergency-water-reserve.md',name:'01-emergency-water-reserve.md',size_human:'4 KB',readable:true},{path:'Knowledge Compendium/EN/112-blackout-movement-emergency-lighting.md',name:'112-blackout-movement-emergency-lighting.md',size_human:'4 KB',readable:true},{path:'Knowledge Compendium/GR/00-compendium-index-and-use.md',name:'00-compendium-index-and-use.md',size_human:'3 KB',readable:true}]; lang='en'; state.risk_flags=['outage']; renderKnowledgeDomains(); renderKnowledgeStats(); renderKnowledgeRecommended(); renderKnowledgeProgress();`);
  check('knowledge-stats',element('knowledgeStats').innerHTML.includes('3'));
  check('knowledge-domains',element('knowledgeDomains').innerHTML.includes('Water'));
  check('knowledge-risk-reading-queue',element('knowledgeRecommended').innerHTML.includes('112-blackout-movement-emergency-lighting'));
  run(`setKnowledgeStatus('Knowledge Compendium/EN/01-emergency-water-reserve.md','reviewed'); renderKnowledgeStats(); renderKnowledgeProgress();`);
  check('knowledge-progress',run('state.knowledge_progress.length===1 && state.knowledge_progress[0].status==="reviewed"') && element('knowledgeProgress').innerHTML.includes('01-emergency-water-reserve'));
  run(`downloadBlob=(text,name,type)=>{globalThis.__knowledgeDownload={text,name,type}};exportKnowledgeQueue();`);
  check('knowledge-risk-queue-export',run('__knowledgeDownload.name.startsWith("offline-survival-knowledge-queue-") && __knowledgeDownload.text.includes("112-blackout-movement-emergency-lighting")'));
  run(`lang='el'; renderKnowledgeDomains(); renderKnowledgeStats();`);
  check('knowledge-greek',element('knowledgeDomains').innerHTML.includes('Νερό'));
  run(`lang='en';`);
  check('nav-continuity-sections',run('["briefing","foodops","sanitationops","powerops","commsops","dependents","financeops"].every(id=>NAV.some(x=>x[0]===id))'));

  run(`lang='en';state=mergeState({profile:{adults:2,children:1,battery_wh:1200},water_batches:[{id:'w',source:'Tank',volume_l:20,status:'ready'},{id:'u',source:'Rain',volume_l:5,status:'untreated'}]});`);
  set('foodLotName','Rice reserve');set('foodLotCategory','staple');set('foodLotQty',5);set('foodLotUnit','kg');set('foodLotKcal',18000);set('foodLotLocation','Pantry');element('foodLotStatus').value='use-first';run('addFoodLot()');
  check('food-add',run('state.food_lots.length===1 && state.food_lots[0].kcal_total===18000'));
  set('foodOpsKcalDay',2000);run('calculateFoodOpsCoverage()');check('food-coverage',element('foodCoverageOutput').innerHTML.includes('3'));

  set('sanName','Handwash A');element('sanKind').value='handwash';element('sanStatus').value='service';set('sanCapacity',12);set('sanUnit','L');set('sanOwner','Alex');run('addSanitationPoint()');
  check('sanitation-add',run('state.sanitation_points.length===1 && state.sanitation_points[0].status==="service"'));

  set('powerName','Radio');set('powerLoadWatts',10);set('powerLoadHours',4);element('powerPriority').value='critical';set('powerSource','battery');run('addPowerLoad()');
  set('powerName','Lamp');set('powerLoadWatts',5);set('powerLoadHours',2);element('powerPriority').value='optional';run('addPowerLoad()');
  check('power-add',run('state.power_loads.length===2 && loadWh(state.power_loads[0])===40'));
  set('powerRecharge',0);run('calculatePowerEndurance()');check('power-endurance',element('powerEnduranceOutput').innerHTML.includes('24'));

  set('commsWindowName','Evening');set('commsWindowMethod','radio');set('commsWindowChannel','CH3');set('commsWindowParticipants','Team');element('commsWindowStatus').value='missed';run('addCommsWindow()');
  check('comms-add',run('state.comms_windows.length===1 && state.comms_windows[0].status==="missed"'));

  set('depName','Service dog');element('depKind').value='service-animal';set('depNeeds','food and water');set('depCaregiver','Alex');set('depSupplies','3 day kit');run('addDependent()');
  check('dependent-add',run('state.dependents.length===1 && state.dependents[0].kind==="service-animal"'));

  set('expenseCategory','transport');set('expenseDescription','Emergency fuel');set('expenseAmount',30);set('expenseCurrency','EUR');element('expenseStatus').value='claim-ready';run('addExpense()');
  check('expense-add',run('state.expense_log.length===1 && state.expense_log[0].amount===30'));

  run(`state.checkins=[{name:'Nina',status:'needs-help'}];renderSituationBrief();`);
  check('situation-brief',element('briefingTextOutput').textContent.includes('18,000') && element('briefingActions').innerHTML.includes('communication'));
  run(`lang='el';renderContinuityOperations();renderSituationBrief();`);
  check('continuity-greek-render',element('foodOpsSummary').innerHTML.includes('Χρήσιμη') && element('briefingTextOutput').textContent.includes('Σύνοψη κατάστασης'));

  run(`downloadBlob=(text,name,type)=>{globalThis.__lastDownload={text,name,type}};
       state.routes=[{name:'North',source:'test',notes:'',points:[[40,22],[40.1,22.1]]}];
       exportRoutesGeoJSON();`);
  check('route-export-argument-order',run('__lastDownload.name==="offline-survival-routes.geojson" && __lastDownload.text.includes("FeatureCollection")'));
  run(`lang='en';exportFoodLotsCSV();`);check('food-export',run('__lastDownload.name==="offline-survival-food-lots.csv" && __lastDownload.text.includes("Rice reserve")'));
  run(`exportSanitationCSV();`);check('sanitation-export',run('__lastDownload.name==="offline-survival-sanitation.csv" && __lastDownload.text.includes("Handwash A")'));
  run(`exportPowerLoadsCSV();`);check('power-export',run('__lastDownload.name==="offline-survival-power-loads.csv" && __lastDownload.text.includes("Radio")'));
  run(`downloadCommsSchedule();`);check('comms-export',run('__lastDownload.name.startsWith("offline-survival-comms-") && __lastDownload.text.includes("Evening")'));
  run(`exportDependentsCSV();`);check('dependents-export',run('__lastDownload.name==="offline-survival-dependents.csv" && __lastDownload.text.includes("Service dog")'));
  run(`exportExpensesCSV();`);check('expenses-export',run('__lastDownload.name==="offline-survival-recovery-costs.csv" && __lastDownload.text.includes("Emergency fuel")'));
  run(`downloadSituationBrief();`);check('brief-export',run('__lastDownload.name.startsWith("offline-survival-situation-brief-") && __lastDownload.text.includes("Situation brief")'));
  run(`state.field_logs=[{time:'2026-08-09T00:00:00Z',label:'Battery voltage',value:'12.4',unit:'V',notes:'stable'}];
       exportFieldLogCSV();`);
  check('field-log-export-argument-order',run('__lastDownload.name==="offline-survival-field-log.csv" && __lastDownload.text.includes("Battery voltage")'));
  run(`state.inventory=[{name:'=1+1',category:'test',qty:1,unit:'pc',expiry:'',notes:''}];exportInventoryCSV();`);
  check('csv-formula-hardening',run("csvCell('=1+1').charCodeAt(1)===39"));
  run(`state.contacts=[{name:'Private'}];state.routes=[{name:'Private route',points:[[1,2],[3,4]]}];state.medical_card={person:'Private'};state.decision_board=[{issue:'Private',decision:'Private'}];exportRedactedState();`);
  check('redacted-template-empty',run(`(()=>{const x=JSON.parse(__lastDownload.text).state;return x.contacts.length===0&&x.routes.length===0&&Object.keys(x.medical_card).length===0&&x.decision_board.length===0&&x.inventory.length===0})()`));
  run(`lang='en';state.checkins=[{name:'Nina',status:'needs-help',location:'North room',next:'2026-08-09T01:30'}];
       state.shelter_zones.push({id:'z2',name:'Garage',status:'avoid',occupants:0,utilities:'',notes:'smoke'});
       state.water_batches.push({id:'w2',source:'roof barrel',volume_l:7,status:'untreated',container:'can',notes:''});
       generateHandoverBrief();`);
  check('handover-derived-state',element('handoverOutput').textContent.includes('Nina') && element('handoverOutput').textContent.includes('Garage') && element('handoverOutput').textContent.includes('roof barrel'));
  run(`lang='el';generateHandoverBrief();`);
  check('handover-greek',element('handoverOutput').textContent.includes('Σύνοψη παράδοσης βάρδιας'));
}catch(error){
  check('runtime-exception',false,error&&error.stack?error.stack:String(error));
}
const passed=checks.filter(x=>x[1]).length;
console.log('='.repeat(64));
console.log(`${passed}/${checks.length} UI logic checks passed`);
process.exit(passed===checks.length?0:2);
