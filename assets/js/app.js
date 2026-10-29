(()=>{
const $=s=>document.querySelector(s),B=document.body;
const pre=$('#pre'),hide=()=>pre&&pre.classList.add('off');
addEventListener('load',hide);setTimeout(hide,2500);
const mb=$('#menu');if(mb)mb.onclick=()=>{const o=$('nav').classList.toggle('open');mb.setAttribute('aria-expanded',o)};
if(!$('#drop'))return;
const WARN=25*1048576,MAXPX=1.6e8;
const MIME={png:'image/png',jpg:'image/jpeg',webp:'image/webp'};
const ACC={any:'image/*,.jfif',jfif:'.jfif,.jpg,.jpeg,image/jpeg',jpg:'.jpg,.jpeg,.jfif,image/jpeg',png:'image/png',webp:'image/webp'};
const inS=$('#in'),outS=$('#out'),fi=$('#file'),list=$('#list'),prog=$('#prog'),st=$('#status');
let items=[],id=0,busy=false;
inS.value=B.dataset.in||'any';outS.value=B.dataset.out||'png';
const fmt=b=>b<1024?b+' B':b<1048576?(b/1024).toFixed(1)+' KB':(b/1048576).toFixed(2)+' MB';
const say=(m,e)=>{st.textContent=m;st.className=e?'er':''};
const setAcc=()=>{fi.accept=ACC[inS.value]};
const note=()=>{$('#jnote').hidden=outS.value!=='jpg'};
inS.onchange=setAcc;outS.onchange=()=>{note();items.forEach(i=>{if(i.state==='done'){URL.revokeObjectURL(i.out);i.state='ready';i.out=null}});render()};
setAcc();note();
function add(files){
 let big=0;
 for(const f of files){
  const it={id:++id,file:f,url:URL.createObjectURL(f),state:'ready'};
  if(!f.size){it.state='error';it.msg='File is empty (0 bytes).'}
  else if(f.size>WARN)big++;
  items.push(it)}
 if(big)say(big+' large file(s) over 25 MB. Very large images may fail on devices with limited memory.');
 render()}
async function decode(f){
 try{return await createImageBitmap(f)}catch(e){}
 return new Promise((ok,no)=>{const u=URL.createObjectURL(f),i=new Image();
  i.onload=()=>{URL.revokeObjectURL(u);ok(i)};i.onerror=()=>{URL.revokeObjectURL(u);no(new Error('Your browser could not decode this file. It may be corrupted or an unsupported format.'))};i.src=u})}
async function conv(f,fm){
 const img=await decode(f),w=img.width,h=img.height;
 if(!w||!h)throw new Error('Image has no readable dimensions.');
 if(w*h>MAXPX)throw new Error('Image dimensions are too large for this browser.');
 const c=document.createElement('canvas');c.width=w;c.height=h;
 const x=c.getContext('2d');if(!x)throw new Error('Canvas is not available (out of memory?).');
 if(fm!=='png'){x.fillStyle='#fff';x.fillRect(0,0,w,h)}
 x.drawImage(img,0,0);if(img.close)img.close();
 const b=await new Promise(r=>c.toBlob(r,MIME[fm],.92));c.width=c.height=0;
 if(!b||b.type!==MIME[fm])throw new Error('This browser cannot export '+fm.toUpperCase()+'. Try another output format.');
 return b}
function names(){const used=new Set();items.forEach(i=>{if(i.state!=='done')return;
 let b=i.file.name.replace(/\.[^.]+$/,'')||'image',n=b+'.'+i.ext,k=1;
 while(used.has(n.toLowerCase()))n=b+' ('+k++ +').'+i.ext;used.add(n.toLowerCase());i.outName=n})}
$('#go').onclick=async()=>{
 if(busy)return;const fm=outS.value,todo=items.filter(i=>i.state==='ready');
 if(!todo.length){say('Add at least one image first.',1);return}
 busy=true;$('#go').disabled=true;prog.hidden=false;prog.max=todo.length;prog.value=0;let ok=0,bad=0;
 for(const it of todo){
  if(!items.includes(it))continue;
  say('Converting '+it.file.name+' ('+(prog.value+1)+' of '+todo.length+')…');
  try{const b=await conv(it.file,fm);if(!items.includes(it))continue;it.out=URL.createObjectURL(b);it.size=b.size;it.ext=fm==='jpg'?'jpg':fm;it.state='done';ok++}
  catch(e){it.state='error';it.msg=e.message||'Conversion failed.';bad++}
  prog.value++;names();render();await new Promise(r=>setTimeout(r))}
 busy=false;$('#go').disabled=false;prog.hidden=true;
 say('Finished: '+ok+' converted, '+bad+' failed.',bad&&!ok)};
function rm(it){URL.revokeObjectURL(it.url);if(it.out)URL.revokeObjectURL(it.out);items=items.filter(x=>x!==it);names();render()}
function el(t,c,x){const e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function render(){
 list.replaceChildren();
 for(const it of items){
  const li=el('li'),im=el('img');im.src=it.url;im.alt='Preview of '+it.file.name;im.loading='lazy';
  const inf=el('div','inf');inf.append(el('strong',0,it.file.name),el('span',0,'Original: '+fmt(it.file.size)));
  const s=el('div');
  if(it.state==='done'){s.append(el('span','ok','✔ Converted'));inf.append(el('br'),el('span',0,'Output: '+it.outName+' · '+fmt(it.size)))}
  else if(it.state==='error')s.append(el('span','er','✖ Error: '+it.msg));
  else s.append(el('span',0,'Ready to convert'));
  inf.append(s);
  const a=el('div','acts');
  if(it.state==='done'){const d=el('a','btn','Download '+it.ext.toUpperCase());d.href=it.out;d.download=it.outName;a.append(d)}
  const r=el('button','btn s','Remove');r.type='button';r.setAttribute('aria-label','Remove '+it.file.name);r.onclick=()=>rm(it);a.append(r);
  li.append(im,inf,a);list.append(li)}
 const done=items.filter(i=>i.state==='done').length;
 $('#zip').hidden=done<2;$('#more').hidden=!items.length;$('#clr').hidden=!items.length}
$('#clr').onclick=()=>{[...items].forEach(i=>{URL.revokeObjectURL(i.url);if(i.out)URL.revokeObjectURL(i.out)});items=[];render();say('Cleared.')};
$('#more').onclick=()=>fi.click();$('#pick').onclick=()=>fi.click();
fi.onchange=()=>{add([...fi.files]);fi.value=''};
const dz=$('#drop');
['dragenter','dragover'].forEach(e=>dz.addEventListener(e,ev=>{ev.preventDefault();dz.classList.add('over')}));
['dragleave','drop'].forEach(e=>dz.addEventListener(e,ev=>{ev.preventDefault();dz.classList.remove('over')}));
dz.addEventListener('drop',ev=>add([...ev.dataTransfer.files]));
$('#zip').onclick=async()=>{
 if(typeof JSZip==='undefined'){say('ZIP library could not be loaded. Please use the individual download buttons.',1);return}
 const z=new JSZip();items.filter(i=>i.state==='done').forEach(i=>z.file(i.outName,i.out&&fetch(i.out).then(r=>r.blob())));
 say('Creating ZIP…');
 try{const b=await z.generateAsync({type:'blob'}),u=URL.createObjectURL(b),a=document.createElement('a');a.href=u;a.download='pixelconvert-images.zip';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),6e4);say('ZIP downloaded.')}
 catch(e){say('Could not create the ZIP file.',1)}};
})();
