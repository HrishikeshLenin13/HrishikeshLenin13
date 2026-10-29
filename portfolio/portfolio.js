import { createOrbit } from './scene.js';

export const projects = [
  {id:'helix',name:'Helix',category:'systems',kind:'COMPILER / SYSTEMS',description:'An optimizing compiler with SSA, cache-aware loop transforms, SIMD, and native/Wasm output paths.',short:'An optimizing compiler you can inspect, from syntax to native code.',tags:['COMPILERS','SSA','LLVM'],shape:'cube',tone:'#d4f99d',private:true},
  {id:'atlas',name:'Atlas',category:'systems',kind:'DISTRIBUTED SYSTEMS',description:'A Rust distributed runtime exploring Raft consensus, work stealing, fault simulation, and linearizability checking.',short:'A fault-tested distributed runtime built around Raft consensus.',tags:['RUST','RAFT','DISTRIBUTED'],shape:'sphere',tone:'#95d9e8',private:true},
  {id:'aegisdb',name:'AegisDB',category:'systems',kind:'DATABASE ENGINE',description:'A C++ relational engine with SQL parsing, cost-based planning, indexing, MVCC, and ARIES-style crash recovery.',short:'A from-scratch relational engine benchmarked against SQLite.',tags:['C++20','SQL','STORAGE'],shape:'db',tone:'#bfa6ff',repo:'https://github.com/HrishikeshLenin13/AegisDB'},
  {id:'branchcade',name:'Branchcade',category:'impact',kind:'ROBOTICS / EDUCATION',description:'An interactive robotics programming and debugging environment for learning from predictions, sensor readings, and experiments.',short:'Explore robotics logic through real simulation and debugging.',tags:['ROBOTICS','SIMULATION','TYPESCRIPT'],shape:'cube',tone:'#f4b891',repo:'https://github.com/HrishikeshLenin13/Branchcade'},
  {id:'slice',name:'Slice',category:'systems',kind:'DEVELOPER TOOLING',description:'A dependency-aware Python code context slicer that traces symbols and reports where static analysis cannot be complete.',short:'Structure-aware code context for AI development workflows.',tags:['PYTHON','AST','STATIC ANALYSIS'],shape:'sphere',tone:'#d4f99d',repo:'https://github.com/HrishikeshLenin13/slice'},
  {id:'lumen',name:'Lumen',category:'product',kind:'INTERACTIVE SOFTWARE',description:'A Windows XP-inspired browser desktop with local apps, persistent files, and its own programmable scripting language.',short:'A full browser desktop with apps and its own scripting language.',tags:['JAVASCRIPT','UI ENGINE','SCRIPTING'],shape:'cube',tone:'#94bfff',repo:'https://github.com/HrishikeshLenin13/Lumen'},
  {id:'aptmark',name:'Aptmark',category:'impact',kind:'SAT STUDY PLATFORM',description:'A SAT practice workspace with generated question candidates, explanations, timed practice, and transparent progress tools.',short:'Thoughtful SAT practice with explanations and study tools.',tags:['NEXT.JS','EDTECH','SAT'],shape:'sphere',tone:'#e2db95',repo:'https://github.com/HrishikeshLenin13/aptmark',live:'https://aptmark.vercel.app'},
  {id:'gradelarp',name:'Gradelarp',category:'product',kind:'ACADEMIC WORKSPACE',description:'An academic dashboard with HAC connection support, grade history, what-if calculators, GPA planning, and a cinematic 3D landing.',short:'A grade and GPA planning workspace grounded in school records.',tags:['NEXT.JS','3D','EDTECH'],shape:'db',tone:'#ffb6ac',repo:'https://github.com/HrishikeshLenin13/gradelarp'},
  {id:'axiom',name:'Axiom Research',category:'impact',kind:'RESEARCH ACCESS',description:'A research education platform supporting foundations lessons, program pathways, sign-ups, and volunteer opportunities.',short:'Helping make research education and opportunities more accessible.',tags:['REACT','RESEARCH','COMMUNITY'],shape:'sphere',tone:'#d5efc6',repo:'https://github.com/HrishikeshLenin13/AxiomResearch',live:'https://axiommain.vercel.app'}
];
const projectGrid=document.querySelector('#project-grid');
let active=0;
let orbit=null;

function escapeHtml(str){return String(str).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function drawCards(){
 projectGrid.innerHTML=projects.map((p,i)=>`
 <article class="project-card" id="project-${escapeHtml(p.id)}" data-category="${p.category}">
   <div class="project-visual" aria-hidden="true"><span class="visual-corner">SYS.${String(i+1).padStart(2,'0')}</span><div class="glyph" data-shape="${p.shape}" style="--tone:${p.tone}"><div class="glyph-inner"></div></div><span class="visual-code">${p.private?'PRIVATE SOURCE':'OPEN REPOSITORY'}</span></div>
   <div class="project-content"><div class="project-eyebrow"><span class="project-index">${String(i+1).padStart(2,'0')} / 09</span><span class="project-type">${escapeHtml(p.kind)}</span></div>
   <h3 class="project-title">${escapeHtml(p.name)}</h3><p class="project-desc">${escapeHtml(p.description)}</p>
   <div class="project-tags">${p.tags.map(x=>`<span>${escapeHtml(x)}</span>`).join('')}</div>
   <div class="project-links">${p.repo?`<a href="${p.repo}" target="_blank" rel="noopener noreferrer" aria-label="View ${escapeHtml(p.name)} on GitHub">GITHUB ↗</a>`:'<span class="private-note">SOURCE: PRIVATE</span>'}${p.live?`<a href="${p.live}" target="_blank" rel="noopener noreferrer" aria-label="Open ${escapeHtml(p.name)} live site">LIVE SITE ↗</a>`:''}<button class="focus-project" data-focus="${i}" type="button" aria-label="Focus ${escapeHtml(p.name)} in the 3D visualization">FOCUS ◉</button></div>
   </div></article>`).join('');
 projectGrid.querySelectorAll('[data-focus]').forEach(button=>button.addEventListener('click',()=>{setActive(Number(button.dataset.focus));document.querySelector('#home').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});}));
}
function setActive(index){
 active=(index+projects.length)%projects.length;
 const p=projects[active];
 document.querySelector('#focus-number').textContent=String(active+1).padStart(2,'0');
 document.querySelector('#focus-title').textContent=p.name;
 document.querySelector('#focus-description').textContent=p.short;
 const link=document.querySelector('#focus-link');
 link.textContent=p.private?'SEE DETAILS ↓':'VIEW SOURCE ↗';
 link.href=p.private?`#project-${p.id}`:p.repo;
 if(p.private){link.removeAttribute('target');link.removeAttribute('rel');} else {link.target='_blank';link.rel='noopener noreferrer';}
 if(orbit)orbit.select(active);
}

function bindFilters(){
 document.querySelectorAll('.filter').forEach(button=>button.addEventListener('click',()=>{
  const type=button.dataset.filter;
  document.querySelectorAll('.filter').forEach(b=>{const yes=b===button;b.classList.toggle('active',yes);b.setAttribute('aria-pressed',String(yes));});
  document.querySelectorAll('.project-card').forEach(card=>card.hidden=type!=='all'&&card.dataset.category!==type);
 }));
}

drawCards();bindFilters();
document.querySelector('#focus-prev').addEventListener('click',()=>setActive(active-1));
document.querySelector('#focus-next').addEventListener('click',()=>setActive(active+1));
document.querySelector('#year').textContent=String(new Date().getFullYear());
const toggle=document.querySelector('#motion-toggle');
let paused=matchMedia('(prefers-reduced-motion: reduce)').matches;
function syncPause(){toggle.textContent=paused?'▶ RESUME MOTION':'◉ PAUSE MOTION';toggle.setAttribute('aria-pressed',String(paused));if(orbit)orbit.pause(paused);}
toggle.addEventListener('click',()=>{paused=!paused;syncPause();});
try {orbit=createOrbit(document.querySelector('#orbit'),setActive,projects);syncPause();setActive(0);}catch(e){console.error('3D visualization could not start',e);document.querySelector('.coordinate-right').textContent='3D VIEW UNAVAILABLE / USE PROJECT CARDS';}
