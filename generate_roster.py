"""Generates roster.html - a self-contained Duty Roster app (HTML + CSS + JS).
Edit DEFAULTS below, run:  python generate_roster.py  then open roster.html"""
import json

DEFAULTS = {
    "designations": ["Consultant", "Senior Registrar", "Registrar", "Medical Officer", "House Officer", "Nurse"],
    "shifts": [
        {"code": "M", "name": "Morning", "time": "08:00-14:00", "color": "#fde68a"},
        {"code": "E", "name": "Evening", "time": "14:00-20:00", "color": "#a7d3ff"},
        {"code": "N", "name": "Night", "time": "20:00-08:00", "color": "#c9b8ff"},
        {"code": "OFF", "name": "Off", "time": "", "color": "#e3e8ee"},
    ],
}

CSS = """
:root{--bg:#eef2f6;--surface:#fff;--ink:#0e2236;--muted:#62758a;--line:#dde4ec;--accent:#2f6bff;--accent-ink:#fff;--today:#eaf1ff;--danger:#d93a3a;--r:14px}
@media(prefers-color-scheme:dark){:root{--bg:#0b1522;--surface:#122033;--ink:#e8eef6;--muted:#8da1b8;--line:#223650;--today:#16294a}}
*{box-sizing:border-box}
body{margin:0;font-family:'Plus Jakarta Sans',system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;background:var(--bg);color:var(--ink);font-size:14px;line-height:1.45}
.top{display:flex;align-items:center;gap:12px;padding:18px 28px}
.logo{width:38px;height:38px;border-radius:11px;background:var(--accent);display:grid;place-items:center;color:#fff;font-size:20px;font-weight:700}
.top h1{margin:0;font-size:1.25rem;letter-spacing:-.01em}.top p{margin:0;color:var(--muted);font-size:.85rem}
.app{display:grid;grid-template-columns:330px minmax(0,1fr);gap:20px;padding:0 28px 28px;align-items:start}
@media(max-width:960px){.app{grid-template-columns:1fr;padding:0 14px 20px}.top{padding:14px}}
.side{display:grid;gap:20px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:18px;box-shadow:0 1px 2px rgba(14,34,54,.04)}
.card h2{margin:0 0 12px;font-size:.98rem;letter-spacing:-.005em}
.field{display:grid;gap:10px}
label.l{font-size:.78rem;color:var(--muted);font-weight:600;margin-bottom:-6px}
input,select{font:inherit;color:var(--ink);background:var(--bg);border:1px solid transparent;border-radius:10px;padding:10px 12px;width:100%;outline:none;transition:border-color .15s,box-shadow .15s}
input:focus,select:focus-visible{border-color:var(--accent);box-shadow:0 0 0 3px rgba(47,107,255,.18)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:10px}
input[type=color]{padding:3px;height:40px;cursor:pointer}
button{font:inherit;font-weight:600;border:none;border-radius:10px;padding:10px 14px;cursor:pointer;background:var(--accent);color:var(--accent-ink);transition:filter .15s,transform .05s}
button:hover{filter:brightness(1.08)}button:active{transform:scale(.98)}button:focus-visible{outline:3px solid rgba(47,107,255,.35);outline-offset:2px}
button.ghost{background:transparent;color:var(--ink);border:1px solid var(--line)}button.ghost:hover{background:var(--bg);filter:none}
button.danger{background:transparent;color:var(--danger);border:1px solid var(--line)}
.shifts{display:grid;gap:8px;margin-bottom:14px}
.shift{display:flex;align-items:center;gap:10px;padding:8px 10px;border:1px solid var(--line);border-radius:10px}
.badge{min-width:34px;text-align:center;padding:4px 8px;border-radius:8px;font-weight:700;font-size:.8rem;color:#0e2236}
.shift b{font-weight:600}.shift small{color:var(--muted);display:block;line-height:1.2}.shift .x{margin-left:auto}
.x{background:none;color:var(--muted);padding:2px 8px;font-size:1.1rem;border-radius:8px}.x:hover{color:var(--danger);background:var(--bg);filter:none}
.bar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:14px}
.bar .week{font-weight:700;font-size:1.05rem;letter-spacing:-.01em}.bar .sp{flex:1}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:10px;overflow:hidden}
.seg button{background:transparent;color:var(--ink);border-radius:0;padding:8px 12px}.seg button:hover{background:var(--bg);filter:none}
.bar input[type=date]{width:auto;padding:8px 10px}
.wrap{overflow-x:auto;border:1px solid var(--line);border-radius:12px}
table{border-collapse:separate;border-spacing:0;width:100%;min-width:820px;background:var(--surface)}
th,td{padding:10px 8px;text-align:center;border-bottom:1px solid var(--line)}
th{font-weight:600;color:var(--muted);font-size:.8rem;background:var(--surface)}
th .d{display:block;color:var(--ink);font-size:1.1rem;font-weight:700}
th.today,td.today{background:var(--today)}th.today .d{color:var(--accent)}
tr:last-child td{border-bottom:none}
.who{display:flex;align-items:center;gap:10px;text-align:left;min-width:190px;position:sticky;left:0;background:var(--surface);z-index:1}
th.who{z-index:2}
.av{width:36px;height:36px;border-radius:50%;display:grid;place-items:center;font-weight:700;font-size:.8rem;color:#0e2236;flex:none}
.who b{display:block;font-weight:600}.who small{color:var(--muted)}
.who .x{margin-left:auto;opacity:0}tr:hover .x,.x:focus-visible{opacity:1}
td select{appearance:none;-webkit-appearance:none;text-align:center;text-align-last:center;font-weight:700;border-radius:999px;padding:7px 4px;min-width:62px;cursor:pointer;border:1px dashed var(--line);background:transparent;color:var(--muted)}
td select.set{border:1px solid transparent;color:#0e2236}
.n{font-weight:700;font-variant-numeric:tabular-nums}
tfoot td{font-size:.82rem;color:var(--muted);background:var(--bg);border-bottom:none}tfoot td.who{background:var(--bg)}
.empty{padding:40px 10px;color:var(--muted);text-align:center;white-space:normal}
details.card>summary{font-weight:700;font-size:.98rem;cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;min-height:28px}
details.card>summary::-webkit-details-marker{display:none}
details.card>summary::after{content:'\\25BE';color:var(--muted);transition:transform .15s}
details.card[open]>summary{margin-bottom:12px}details.card[open]>summary::after{transform:rotate(180deg)}
@media(hover:none){.who .x{opacity:1}}
@media(max-width:700px){
.top h1{font-size:1.1rem}.top p{font-size:.78rem}
input,select{font-size:16px;min-height:44px}button{min-height:44px}
.bar{gap:8px}.bar .sp{display:none}.bar .week{flex:1 1 100%;order:-1}.bar>button,.bar input[type=date]{flex:1 1 auto}
.seg{flex:1 1 100%}.seg button{flex:1}
.card{padding:14px}main.card{padding:12px}
.wrap{border:none;overflow:visible;border-radius:0}
table,thead,tbody,tfoot,tr{display:block;min-width:0;width:100%}
table{background:transparent}thead{display:none}
tbody tr,tfoot tr{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:4px;border:1px solid var(--line);border-radius:12px;padding:12px;margin-bottom:12px;background:var(--surface)}
tfoot tr{background:var(--bg)}
td{display:block;border:none;padding:0;background:transparent!important}
td.who,tfoot td.who{grid-column:1/-1;position:static;min-width:0;margin-bottom:8px;background:transparent}
td[data-label]::before{content:attr(data-label);display:block;font-size:.7rem;font-weight:600;color:var(--muted);margin-bottom:4px}
td.today::before{color:var(--accent)}
td select{min-width:0;width:100%;padding:12px 0;font-size:.8rem;min-height:44px}
td.total{grid-column:1/-1;text-align:left;margin-top:8px;color:var(--muted);font-weight:500}
td.total::before{content:'Shifts this week: ';color:var(--muted)}
td:empty{display:none}
.empty{grid-column:1/-1;padding:24px 8px}
}
.tabs{margin-bottom:14px;width:100%}.tabs button{flex:1}.seg button.on{background:var(--accent);color:#fff}
.rv{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:10px}
@media(max-width:1100px){.rv{grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}}
@media(max-width:700px){.rv{grid-template-columns:1fr}}
.dc{border:1px solid var(--line);border-radius:12px;padding:12px;background:var(--surface)}
.dc.today{border-color:var(--accent);background:var(--today)}
.dh{font-weight:700;margin-bottom:4px;display:flex;justify-content:space-between;align-items:baseline}.dh span{color:var(--muted);font-weight:500;font-size:.8rem}
.rs{margin-top:12px}.rsh{display:flex;align-items:center;gap:6px;font-size:.8rem;font-weight:600}.rsh small{color:var(--muted);font-weight:400}
.rn{padding:6px 0 0 2px}.rn b{font-weight:600;display:block}.rn small{color:var(--muted)}.rn.none{color:var(--muted);font-size:.85rem}
@media print{.tabs{display:none!important}.rv{grid-template-columns:repeat(4,1fr)}}
@media print{.side,.bar button,.bar .seg,.bar input,.x,.top p{display:none!important}.app{display:block;padding:0}body{background:#fff}.who{position:static}}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
"""

JS = """
const DEF = __DEFAULTS__;
const KEY = 'dutyRosterV1';
let S = JSON.parse(localStorage.getItem(KEY) || 'null') || {staff:[],designations:DEF.designations,shifts:DEF.shifts,roster:{},weekStart:null};
const $ = id => document.getElementById(id);
const esc = t => String(t).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const iso = d => d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
function sunday(d){d=new Date(d);d.setDate(d.getDate()-d.getDay());d.setHours(0,0,0,0);return d}
if(!S.view) S.view='roster';
S.weekStart = iso(sunday(S.weekStart?new Date(S.weekStart+'T00:00'):new Date()));
const save = () => localStorage.setItem(KEY, JSON.stringify(S));
const days = () => [...Array(7)].map((_,i)=>{const d=new Date(S.weekStart+'T00:00');d.setDate(d.getDate()+i);return d});
const shiftOf = c => S.shifts.find(s=>s.code===c);
const initials = n => n.split(/\\s+/).filter(Boolean).slice(0,2).map(w=>w[0].toUpperCase()).join('');
const hue = n => {let h=0;for(const c of n)h=(h*31+c.charCodeAt(0))%360;return h};

function addStaff(){
  const n=$('sName').value.trim(); let d=$('sDesig').value;
  if(d==='__new'){d=$('sDesigNew').value.trim(); if(d&&!S.designations.includes(d))S.designations.push(d);}
  if(!n||!d){alert('Enter a name and a designation.');return}
  S.staff.push({id:Date.now()+''+Math.floor(Math.random()*999),name:n,desig:d});
  $('sName').value='';$('sDesigNew').value='';save();render();$('sName').focus();
}
function delStaff(id){if(confirm('Remove this staff member from the roster?')){S.staff=S.staff.filter(s=>s.id!==id);
  Object.values(S.roster).forEach(r=>delete r[id]);save();render()}}
function addShift(){
  const code=$('shCode').value.trim().toUpperCase(),name=$('shName').value.trim();
  if(!code||!name){alert('Enter a shift code and name.');return}
  if(shiftOf(code)){alert('That code is already used.');return}
  S.shifts.push({code,name,time:$('shTime').value.trim(),color:$('shColor').value});
  ['shCode','shName','shTime'].forEach(i=>$(i).value='');save();render();
}
function delShift(code){if(confirm('Delete shift '+code+'? Cells using it will be cleared.')){
  S.shifts=S.shifts.filter(s=>s.code!==code);
  Object.values(S.roster).forEach(r=>Object.keys(r).forEach(k=>{if(r[k]===code)delete r[k]}));save();render()}}
function setCell(date,id,code){(S.roster[date]=S.roster[date]||{});
  if(code)S.roster[date][id]=code;else delete S.roster[date][id];save();render()}
function setView(v){S.view=v;save();render()}
function moveWeek(n){const d=new Date(S.weekStart+'T00:00');d.setDate(d.getDate()+7*n);S.weekStart=iso(d);save();render()}
function thisWeek(){S.weekStart=iso(sunday(new Date()));save();render()}
function pickWeek(v){if(v){S.weekStart=iso(sunday(new Date(v+'T00:00')));save();render()}}
function exportCSV(){
  const D=days();const rows=[['Name','Designation',...D.map(d=>d.toDateString())]];
  S.staff.forEach(s=>rows.push([s.name,s.desig,...D.map(d=>(S.roster[iso(d)]||{})[s.id]||'')]));
  const csv=rows.map(r=>r.map(c=>'"'+String(c).replace(/"/g,'""')+'"').join(',')).join('\\n');
  const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv'}));
  a.download='roster_'+S.weekStart+'.csv';a.click();
}
function clearWeek(){if(confirm('Clear every shift in this week?')){days().forEach(d=>delete S.roster[iso(d)]);save();render()}}
function resetAll(){if(confirm('Delete all staff, shifts and rosters? This cannot be undone.')){localStorage.removeItem(KEY);location.reload()}}

function render(){
  const sel=$('sDesig').value;
  $('sDesig').innerHTML=S.designations.map(d=>`<option>${esc(d)}</option>`).join('')+'<option value="__new">Add new designation</option>';
  if(sel&&[...$('sDesig').options].some(o=>o.value===sel))$('sDesig').value=sel;
  $('sDesigNew').style.display=$('sDesig').value==='__new'?'':'none';
  $('shiftList').innerHTML=S.shifts.map(s=>`<div class="shift"><span class="badge" style="background:${s.color}">${esc(s.code)}</span><div><b>${esc(s.name)}</b>${s.time?`<small>${esc(s.time)}</small>`:''}</div><button class="x" aria-label="Delete shift ${esc(s.code)}" onclick="delShift('${esc(s.code)}')">&times;</button></div>`).join('');
  const D=days(),today=iso(new Date()),fmt=o=>D[o].toLocaleDateString(undefined,{day:'numeric',month:'short'});
  $('weekLabel').textContent=fmt(0)+' to '+fmt(6)+' '+D[6].getFullYear();$('weekPick').value=S.weekStart;
  let h='<thead><tr><th class="who">Staff</th>'+D.map(d=>`<th class="${iso(d)===today?'today':''}">${d.toLocaleDateString(undefined,{weekday:'short'})}<span class="d">${d.getDate()}</span></th>`).join('')+'<th>On duty</th></tr></thead><tbody>';
  if(!S.staff.length)h+='<tr><td colspan="9" class="empty">No staff yet. Open Add staff to add your first team member.</td></tr>';
  S.staff.forEach(s=>{
    const hh=hue(s.name);let cnt=0;
    h+=`<tr><td class="who"><span class="av" style="background:hsl(${hh} 70% 82%)">${esc(initials(s.name))}</span><div><b>${esc(s.name)}</b><small>${esc(s.desig)}</small></div><button class="x" aria-label="Remove ${esc(s.name)}" onclick="delStaff('${s.id}')">&times;</button></td>`;
    D.forEach(d=>{const lab=d.toLocaleDateString(undefined,{weekday:'short'}),k=iso(d),c=(S.roster[k]||{})[s.id]||'',sh=shiftOf(c);if(c&&c!=='OFF')cnt++;
      h+=`<td data-label="${lab}" class="${k===today?'today':''}"><select class="${sh?'set':''}" ${sh?`style="background:${sh.color}"`:''} aria-label="${esc(s.name)} ${k}" onchange="setCell('${k}','${s.id}',this.value)"><option value="">+</option>`+
        S.shifts.map(x=>`<option value="${esc(x.code)}" ${x.code===c?'selected':''}>${esc(x.code)}</option>`).join('')+'</select></td>'});
    h+=`<td class="n total">${cnt}</td></tr>`});
  h+='</tbody>';
  if(S.staff.length)h+='<tfoot><tr><td class="who">Staff on duty</td>'+D.map(d=>{const r=S.roster[iso(d)]||{};
    return '<td class="n" data-label="'+d.toLocaleDateString(undefined,{weekday:'short'})+'">'+Object.values(r).filter(c=>c!=='OFF').length+'</td>'}).join('')+'<td></td></tr></tfoot>';
  $('tbl').innerHTML=h;
  $('rosterView').innerHTML=!S.staff.length?'<div class="empty" style="grid-column:1/-1">No staff yet. Open Add staff to add your first team member.</div>':D.map(d=>{
    const k=iso(d),r=S.roster[k]||{};
    const body=S.shifts.map(sh=>{const names=S.staff.filter(s=>r[s.id]===sh.code);
      return `<div class="rs"><div class="rsh"><span class="badge" style="background:${sh.color}">${esc(sh.code)}</span><span>${esc(sh.name)}${sh.time?` <small>${esc(sh.time)}</small>`:''}</span></div>`+
        (names.length?names.map(s=>`<div class="rn"><b>${esc(s.name)}</b><small>${esc(s.desig)}</small></div>`).join(''):'<div class="rn none">No one</div>')+'</div>'}).join('');
    return `<div class="dc ${k===today?'today':''}"><div class="dh">${d.toLocaleDateString(undefined,{weekday:'long'})}<span>${d.toLocaleDateString(undefined,{day:'numeric',month:'short'})}</span></div>${body}</div>`}).join('');
  $('rosterView').style.display=S.view==='roster'?'':'none';
  $('editView').style.display=S.view==='edit'?'':'none';
  $('tabR').classList.toggle('on',S.view==='roster');$('tabE').classList.toggle('on',S.view==='edit');
}
document.addEventListener('DOMContentLoaded',()=>{
  $('sDesig').addEventListener('change',()=>{$('sDesigNew').style.display=$('sDesig').value==='__new'?'':'none'});
  $('sName').addEventListener('keydown',e=>{if(e.key==='Enter')addStaff()});
  if(innerWidth<960)document.querySelectorAll('.side details').forEach(d=>d.open=false);
  render();
});
"""

HTML = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Duty roster</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>__CSS__</style></head><body>
<header class="top"><div class="logo">+</div><div><h1>Duty roster</h1><p>Plan weekly shifts for your doctors and staff</p></div></header>
<div class="app">
<aside class="side">
<details class="card" open><summary>Add staff</summary><div class="field">
<label class="l" for="sName">Full name</label><input id="sName" placeholder="Dr. Ayesha Khan">
<label class="l" for="sDesig">Designation</label><select id="sDesig"></select>
<input id="sDesigNew" placeholder="Type the new designation" style="display:none">
<button onclick="addStaff()">Add staff</button></div></details>
<details class="card" open><summary>Shifts</summary><div id="shiftList" class="shifts"></div>
<div class="field"><div class="two"><input id="shCode" placeholder="Code" maxlength="5" aria-label="Shift code"><input id="shColor" type="color" value="#b7f0c8" aria-label="Shift colour"></div>
<input id="shName" placeholder="Shift name" aria-label="Shift name"><input id="shTime" placeholder="Hours, e.g. 08:00-14:00" aria-label="Shift hours">
<button class="ghost" onclick="addShift()">Add shift</button></div></details>
</aside>
<main class="card">
<div class="seg tabs"><button id="tabR" onclick="setView('roster')">Weekly roster</button><button id="tabE" onclick="setView('edit')">Assign shifts</button></div>
<div class="bar"><div class="seg"><button onclick="moveWeek(-1)" aria-label="Previous week">&lsaquo;</button><button onclick="thisWeek()">Today</button><button onclick="moveWeek(1)" aria-label="Next week">&rsaquo;</button></div>
<span class="week" id="weekLabel"></span><input type="date" id="weekPick" onchange="pickWeek(this.value)" aria-label="Jump to week"><span class="sp"></span>
<button class="ghost" onclick="window.print()">Print</button><button class="ghost" onclick="exportCSV()">Export CSV</button>
<button class="ghost" onclick="clearWeek()">Clear week</button><button class="danger" onclick="resetAll()">Reset all</button></div>
<div id="rosterView" class="rv"></div><div class="wrap" id="editView"><table id="tbl"></table></div></main>
</div><script>__JS__</script></body></html>"""

html = (HTML.replace("__CSS__", CSS).replace("__JS__", JS.replace("__DEFAULTS__", json.dumps(DEFAULTS))))
with open("roster.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Created roster.html")
