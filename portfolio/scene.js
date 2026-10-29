// A zero-dependency 3D renderer: perspective projection, orbiting satellites,
// rotating polyhedral mesh, camera controls, depth sorting, and layered emissive lines.
// All geometry is original and synthesized at runtime; there are no fetched assets.
export function createOrbit(canvas,onSelect,projects){
 const ctx=canvas.getContext('2d',{alpha:true});
 if(!ctx)throw new Error('Canvas 2D is unavailable');
 let width=0,height=0,dpr=1, yaw=-0.3,pitch=.17,autoTime=0,last=performance.now(),paused=false, pointerDown=null, dragging=false, active=0, visible=true;
 let hitTargets=[];let disposed=false;
 const random=(seed)=>{const n=Math.sin(seed*127.1+78.23)*43758.5453;return n-Math.floor(n)};
 const particles=Array.from({length:115},(_,i)=>({x:(random(i*4+1)-.5)*15,y:(random(i*4+2)-.5)*9,z:(random(i*4+3)-.5)*12,size:random(i+4)*1.4+.35,alpha:random(i+6)*.30+.10}));
 const icoV=[[0,1,1.618],[0,-1,1.618],[0,1,-1.618],[0,-1,-1.618],[1,1.618,0],[-1,1.618,0],[1,-1.618,0],[-1,-1.618,0],[1.618,0,1],[-1.618,0,1],[1.618,0,-1],[-1.618,0,-1]].map(v=>v.map(x=>x*.83));
 const icoFaces=[[0,1,8],[0,8,4],[0,4,5],[0,5,9],[0,9,1],[1,9,7],[1,7,6],[1,6,8],[8,6,10],[8,10,4],[4,10,2],[4,2,5],[5,2,11],[5,11,9],[9,11,7],[7,11,3],[7,3,6],[6,3,10],[10,3,2],[2,3,11]];
 function resize(){const r=canvas.getBoundingClientRect();width=r.width;height=r.height;dpr=Math.min(window.devicePixelRatio||1,1.7);canvas.width=Math.max(1,Math.round(width*dpr));canvas.height=Math.max(1,Math.round(height*dpr));ctx.setTransform(dpr,0,0,dpr,0,0);}
 const turn=(p,angle)=>{const c=Math.cos(angle),s=Math.sin(angle);return {x:p.x*c+p.z*s,y:p.y,z:-p.x*s+p.z*c}};
 function transform(point){const a=turn(point,yaw);const c=Math.cos(pitch),s=Math.sin(pitch);return {x:a.x,y:a.y*c-a.z*s,z:a.y*s+a.z*c};}
 function project(point){const v=transform(point);const z=11.8-v.z;const f=Math.min(width*.78,height*.94)*1.35;const k=f/z;return{x:width*.51+v.x*k,y:height*.452-v.y*k,z:v.z,k};}
 function stroke(points,color='rgba(173,244,199,.15)',lineWidth=1){if(points.length<2)return;ctx.beginPath();ctx.moveTo(points[0].x,points[0].y);for(let i=1;i<points.length;i++)ctx.lineTo(points[i].x,points[i].y);ctx.strokeStyle=color;ctx.lineWidth=lineWidth;ctx.stroke();}
 function line3(a,b,color='rgba(173,244,199,.15)',lineWidth=1){stroke([project(a),project(b)],color,lineWidth);}
 function ring(radius,phase,tilt,color,segments=110,thick=1){const points=[];for(let i=0;i<=segments;i++){const a=i/segments*Math.PI*2+phase;points.push(project({x:Math.cos(a)*radius,y:Math.sin(a)*radius*Math.sin(tilt),z:Math.sin(a)*radius*Math.cos(tilt)}));}stroke(points,color,thick);}
 function drawGrid(){for(let i=-8;i<=8;i++){const opacity=(i%2===0)?.09:.047;line3({x:i,y:-2.95,z:-11},{x:i,y:-2.95,z:11},`rgba(151,224,169,${opacity})`);line3({x:-10,y:-2.95,z:i},{x:10,y:-2.95,z:i},`rgba(151,224,169,${opacity})`);}const origin=project({x:0,y:-2.95,z:0});const g=ctx.createRadialGradient(origin.x,origin.y,0,origin.x,origin.y,220);g.addColorStop(0,'rgba(130,239,164,.06)');g.addColorStop(1,'rgba(130,239,164,0)');ctx.fillStyle=g;ctx.fillRect(0,0,width,height);}
 function drawParticles(){for(const p of particles){const point=project(p);if(point.x<0||point.y<0||point.x>width||point.y>height)continue;ctx.beginPath();ctx.arc(point.x,point.y,Math.max(.35,Math.min(2.2,p.size*point.k*.025)),0,Math.PI*2);ctx.fillStyle=`rgba(178,226,209,${p.alpha})`;ctx.fill();}}
 function drawIco(time){const spin=paused?.27:time*.20+.27;const verts=icoV.map(v=>{const p=turn({x:v[0],y:v[1],z:v[2]},spin);const ax=Math.cos(.31),bx=Math.sin(.31);return{x:p.x,y:p.y*ax-p.z*bx,z:p.y*bx+p.z*ax}});const sorted=icoFaces.map(face=>({face,z:face.reduce((a,i)=>a+transform(verts[i]).z,0)/3})).sort((a,b)=>a.z-b.z);
  for(const {face,z} of sorted){const coords=face.map(i=>project(verts[i]));ctx.beginPath();ctx.moveTo(coords[0].x,coords[0].y);ctx.lineTo(coords[1].x,coords[1].y);ctx.lineTo(coords[2].x,coords[2].y);ctx.closePath();ctx.fillStyle=`rgba(31,${Math.round(66+z*8)},${Math.round(56+z*6)},${Math.max(.22,Math.min(.73,.38+z*.07))})`;ctx.fill();ctx.strokeStyle=z>0?'rgba(210,255,183,.43)':'rgba(109,166,137,.2)';ctx.lineWidth=.8;ctx.stroke();}
  const c=project({x:0,y:0,z:0});const halo=ctx.createRadialGradient(c.x,c.y,4,c.x,c.y,Math.max(50,c.k*1.8));halo.addColorStop(0,'rgba(204,255,165,.26)');halo.addColorStop(.3,'rgba(112,254,150,.07)');halo.addColorStop(1,'rgba(100,200,150,0)');ctx.fillStyle=halo;ctx.beginPath();ctx.arc(c.x,c.y,Math.max(50,c.k*1.8),0,Math.PI*2);ctx.fill();
 }
 function position(i,t){const a=i/projects.length*Math.PI*2-.48;return {x:Math.cos(a)*3.42,y:Math.sin(a*1.8)*.68+.08+Math.sin(t*.6+i*.7)*.09,z:Math.sin(a)*2.4};}
 function drawSatellite(node,i){const p=project(node),sel=i===active,radius=Math.max(9,Math.min(23,(sel?20:14)*p.k/52));const col=projects[i].tone; const g=ctx.createRadialGradient(p.x-radius*.25,p.y-radius*.36,1,p.x,p.y,radius*1.3);g.addColorStop(0,'#f3fff2');g.addColorStop(.20,col);g.addColorStop(.58,'#274b48');g.addColorStop(1,'rgba(10,29,26,.08)');ctx.fillStyle=g;ctx.beginPath();ctx.arc(p.x,p.y,radius,0,Math.PI*2);ctx.fill();ctx.lineWidth=sel?2.2:1;ctx.strokeStyle=sel?'rgba(223,255,188,1)':'rgba(178,228,218,.55)';ctx.stroke();
  if(sel){ctx.beginPath();ctx.arc(p.x,p.y,radius+9,0,Math.PI*2);ctx.strokeStyle='rgba(209,249,157,.63)';ctx.lineWidth=1;ctx.setLineDash([4,5]);ctx.stroke();ctx.setLineDash([]);ctx.beginPath();ctx.arc(p.x,p.y,radius+17,0,Math.PI*2);ctx.strokeStyle='rgba(175,235,175,.21)';ctx.stroke();}
  ctx.fillStyle=sel?'#101910':'#d3e6da';ctx.textAlign='center';ctx.textBaseline='middle';ctx.font=`${sel?'bold ':''}10px monospace`;ctx.fillText(String(i+1).padStart(2,'0'),p.x,p.y+1);
  if(sel){const label=(projects[i].name||'').toUpperCase();ctx.font='10px monospace';ctx.fillStyle='#d6f7be';ctx.textAlign='left';ctx.fillText(label,p.x+radius+13,p.y-9);ctx.beginPath();ctx.moveTo(p.x+radius+2,p.y);ctx.lineTo(p.x+radius+9,p.y-6);ctx.strokeStyle='rgba(206,249,159,.6)';ctx.stroke();}
  return {x:p.x,y:p.y,r:Math.max(19,radius+7),i};
 }
 function drawFrame(now){if(disposed)return;requestAnimationFrame(drawFrame);if(!visible||document.hidden)return;const delta=Math.min(.04,Math.max(0,(now-last)/1000));last=now;if(!paused)autoTime+=delta;ctx.clearRect(0,0,width,height);if(width<1||height<1)return;
  if(!dragging&&!paused)yaw+=delta*.025;
  drawParticles();drawGrid();
  ring(3.67,0,.35,'rgba(159,235,202,.21)',140,1.3);ring(2.43,0,1.25,'rgba(160,242,184,.18)',140,1);ring(2.72,.8,.9,'rgba(135,200,220,.11)',140,.9);
  const nodes=projects.map((p,i)=>({node:position(i,autoTime),i}));const behind=nodes.filter(n=>transform(n.node).z<.2).sort((a,b)=>transform(a.node).z-transform(b.node).z);const front=nodes.filter(n=>transform(n.node).z>=.2).sort((a,b)=>transform(a.node).z-transform(b.node).z);
  hitTargets=[];for(const n of behind)hitTargets.push(drawSatellite(n.node,n.i));
  const s=project({x:0,y:0,z:0});for(const n of nodes){if(n.i===active){const p=project(n.node);ctx.strokeStyle='rgba(205,248,168,.25)';ctx.beginPath();ctx.setLineDash([4,6]);ctx.moveTo(s.x,s.y);ctx.lineTo(p.x,p.y);ctx.stroke();ctx.setLineDash([]);}}
  drawIco(autoTime);
  for(const n of front)hitTargets.push(drawSatellite(n.node,n.i));
  ring(1.93,autoTime*.15,.32,'rgba(211,255,171,.56)',100,1.5);ring(1.93,autoTime*.15,.32,'rgba(211,255,171,.09)',100,5);
  const axis=project({x:0,y:-2.85,z:0});ctx.font='9px monospace';ctx.fillStyle='rgba(186,220,190,.5)';ctx.textAlign='center';ctx.fillText('ORIGIN / H.L.',axis.x,axis.y+11);
 }
 function pick(x,y){let best=null,dist=Infinity;for(const n of hitTargets){const d=Math.hypot(x-n.x,y-n.y);if(d<n.r&&d<dist){best=n.i;dist=d;}}return best;}
 canvas.addEventListener('pointerdown',e=>{pointerDown={x:e.clientX,y:e.clientY,yaw,pitch};dragging=false;canvas.setPointerCapture?.(e.pointerId);});
 canvas.addEventListener('pointermove',e=>{const b=canvas.getBoundingClientRect();if(pointerDown){const dx=e.clientX-pointerDown.x,dy=e.clientY-pointerDown.y;if(Math.hypot(dx,dy)>6)dragging=true;if(dragging){yaw=pointerDown.yaw+dx*.007;pitch=Math.max(-.85,Math.min(.85,pointerDown.pitch+dy*.005));}}else canvas.style.cursor=pick(e.clientX-b.left,e.clientY-b.top)!==null?'pointer':'grab';});
 canvas.addEventListener('pointerup',e=>{if(pointerDown&&!dragging){const r=canvas.getBoundingClientRect();const item=pick(e.clientX-r.left,e.clientY-r.top);if(item!==null)onSelect(item);}pointerDown=null;dragging=false;});
 canvas.addEventListener('pointercancel',()=>{pointerDown=null;dragging=false;});
 canvas.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();onSelect((active+(e.key==='ArrowRight'?1:-1)+projects.length)%projects.length);}});
 if('ResizeObserver' in window){new ResizeObserver(resize).observe(canvas);}else{window.addEventListener('resize',resize);}resize();
 if('IntersectionObserver' in window){new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;},{threshold:0}).observe(canvas);}
 requestAnimationFrame(drawFrame);
 return {select(i){active=i;},pause(flag){paused=flag;}};
}
