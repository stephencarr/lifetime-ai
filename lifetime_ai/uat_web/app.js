const $ = selector => document.querySelector(selector);
const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const labels = {false_positive:'False positive',wrong_type:'Wrong type',bad_extraction:'Poor extraction',duplicate:'Duplicate',missing_context:'Missing context',retrieval_issue:'Retrieval issue',other:'Other'};
const titles = {overview:['Overview','Test whether useful context persists across sessions.'],review:['Capture inspector','Inspect captured candidates and source evidence.'],memory:['Stored memory','Inspect the local state used for retrieval.'],sources:['Sources','Trace each claim to its imported evidence.'],retrieval:['Retrieval lab','Ask questions and inspect cited matches.'],findings:['UAT findings','Track patterns in the examples you inspect.'],import:['Import & setup','Manage the disposable local workspace.']};
const PAGE_SIZE = 25;
let data = {sources:[],suggestions:[],reviews:[],state:[],findings:[],mode:''};
let activeView = 'overview';
let openRecord = null;
let editRecord = null;
let selected = new Set();
const pages = {review:0,memory:0,sources:0};

async function api(path, options = {}) {
  const response = await fetch(path, {headers:{'Content-Type':'application/json'}, ...options});
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || 'Request failed');
  return payload;
}
function toast(message) { const element=$('#toast'); element.textContent=message; element.classList.add('show'); clearTimeout(toast.timer); toast.timer=setTimeout(()=>element.classList.remove('show'),3500); }
function errorToast(error) { toast(error.message || 'Something went wrong'); }
function clean(value) { return String(value ?? '').replace(/[\u200B-\u200F\uFEFF\u034F]/g,'').replace(/https?:\/\/\S+/g,'[link]').replace(/\s+/g,' ').trim(); }
function short(value, limit=95) { const text=clean(value); return text.length>limit ? text.slice(0,limit-1)+'…' : text; }
function typeTag(value) { return `<span class="tag ${esc(value)}">${esc(value)}</span>`; }
function flagged(type,id) { return data.findings.some(f=>f.target_type===type && f.target_id===id); }
function flags(type,id) { return data.findings.filter(f=>f.target_type===type && f.target_id===id); }
function lookup(type,id) { return ({source:data.sources,suggestion:data.reviews,state:data.state}[type]||[]).find(x=>x[({source:'source_id',suggestion:'suggestion_id',state:'item_id'}[type])]===id); }
function sourceFor(type,item) { return type==='source' ? item : item.source; }
function related(sourceId) { return {review:data.reviews.find(r=>r.source_id===sourceId), state:data.state.find(s=>s.source_id===sourceId)}; }
function count(values,key) { return values.reduce((map,item)=>{const value=item[key] || 'unknown';map[value]=(map[value]||0)+1;return map},{}); }
function chart(target,values,empty='No observations yet') { const rows=Object.entries(values).sort((a,b)=>b[1]-a[1]); const max=Math.max(...rows.map(row=>row[1]),1); $(target).innerHTML=rows.length?rows.map(([label,n])=>`<div class="bar-row"><span>${esc(labels[label]||label)}</span><div class="bar-track"><div class="bar-fill" style="width:${n/max*100}%"></div></div><span class="bar-count">${n}</span></div>`).join(''):`<p class="muted">${empty}</p>`; }

function setView(name) {
  if (!titles[name]) return;
  if (openRecord) closeDrawer();
  activeView=name;
  document.querySelectorAll('.view').forEach(el=>el.classList.toggle('active',el.id===`view-${name}`));
  document.querySelectorAll('.nav-item').forEach(el=>el.classList.toggle('active',el.dataset.view===name));
  $('#view-title').textContent=titles[name][0]; $('#view-subtitle').textContent=titles[name][1];
  window.scrollTo(0,0);
}
async function refresh() {
  data=await api('/api/dashboard');
  $('#adapter-name').textContent=data.mode;
  $('#nav-pending').textContent=data.reviews.length;
  $('#nav-findings').textContent=data.findings.length;
  selected=new Set([...selected].filter(id=>data.suggestions.some(s=>s.suggestion_id===id)));
  renderAll();
}
function renderAll() { renderOverview();renderReview();renderMemory();renderSources();renderFindings(); if(openRecord) showRecord(openRecord.type,openRecord.id,false); }
function renderOverview() {
  const counts=[['Sources',data.sources.length,'Imported evidence'],['Suggestions',data.reviews.length,'Proposed by adapter'],['Stored items',data.state.length,'Active local memory'],['UAT findings',data.findings.length,'Human observations']];
  $('#metrics').innerHTML=counts.map(([label,value,foot])=>`<div class="metric"><div class="metric-value">${value}</div><div class="metric-label">${label}</div><div class="metric-foot">${foot}</div></div>`).join('');
  chart('#outcome-chart',count(data.reviews,'status'),'No suggestions yet. Import a source to begin.');
  chart('#type-chart',count(data.reviews,'kind'),'No suggested types yet.');
  chart('#finding-chart',count(data.findings,'category'),'No feedback tagged yet. Open a record to tag a pattern.');
}
function matches(item,terms) { const text=[item.title,item.context,item.excerpt,item.proposition,item.source?.title,item.source?.context,item.source?.excerpt].join(' ').toLowerCase(); return terms.every(term=>text.includes(term)); }
function filteredRows(view) {
  const query=$(`#${view==='sources'?'source':view}-search`).value.toLowerCase().trim().split(/\s+/).filter(Boolean);
  if(view==='review') return data.reviews.filter(item=>($('#review-status').value==='all'||item.status===$('#review-status').value)&&($('#review-type').value==='all'||item.kind===$('#review-type').value)&&matches(item,query));
  if(view==='memory') return data.state.filter(item=>($('#memory-type').value==='all'||item.kind===$('#memory-type').value)&&($('#memory-feedback').value==='all'||flagged('state',item.item_id)||flagged('suggestion',`suggestion:${item.source_id}`))&&matches(item,query)).slice().reverse();
  const sources=data.sources.filter(item=>($('#source-feedback').value==='all'||flagged('source',item.source_id))&&matches(item,query));
  return $('#source-sort').value==='newest'?sources.reverse():sources;
}
function paginate(view,items) {
  const pageCount=Math.max(1,Math.ceil(items.length/PAGE_SIZE));
  pages[view]=Math.min(pages[view],pageCount-1);
  const page=pages[view];
  const start=page*PAGE_SIZE;
  const visible=items.slice(start,start+PAGE_SIZE);
  $(`#${view==='sources'?'source':view}-pager`).innerHTML=`<span>${items.length?`${start+1}–${Math.min(start+PAGE_SIZE,items.length)} of ${items.length}`:'0 records'}</span><div class="pager-controls"><button class="button quiet small" data-page="${view}:prev" ${page===0?'disabled':''}>Previous</button><span>Page ${page+1} / ${pageCount}</span><button class="button quiet small" data-page="${view}:next" ${page+1>=pageCount?'disabled':''}>Next</button></div>`;
  return visible;
}
function table(headers,rows,widths='') { return rows.length?`<div class="table-wrap"><table class="data-table">${widths}<thead><tr>${headers.map(h=>`<th>${h}</th>`).join('')}</tr></thead><tbody>${rows.join('')}</tbody></table></div>`:'<div class="empty"><h3>No matching records</h3><p>Try a broader search or another filter.</p></div>'; }
function renderReview() {
  const items=filteredRows('review'); const visible=paginate('review',items);
  const hasPending=visible.some(item=>item.status==='pending');
  const rows=visible.map(item=>`<tr>${hasPending?`<td>${item.status==='pending'?`<input aria-label="Select suggestion" type="checkbox" data-select="${esc(item.suggestion_id)}" ${selected.has(item.suggestion_id)?'checked':''}>`:''}</td>`:''}<td class="cell-date">${esc(item.source.occurred_at)}</td><td>${typeTag(item.kind)}</td><td><button class="row-button" data-open="suggestion" data-id="${esc(item.suggestion_id)}" title="Open details">${esc(short(item.proposition))}</button></td><td class="cell-clip cell-muted" title="${esc(item.source.title)}">${esc(short(item.source.title,56))}${flagged('suggestion',item.suggestion_id)?'<span class="flag">● Flagged</span>':''}</td><td>${typeTag(item.status)}</td></tr>`);
  const pendingVisible=visible.filter(item=>item.status==='pending');
  const pendingToolbar=pendingVisible.length?`<div class="toolbar"><button class="button quiet small" data-select-page="true">Select page (${pendingVisible.length})</button><button class="button quiet small" data-clear-selection="true">Clear</button><span class="muted">${selected.size} selected</span><button class="button primary small" data-bulk="accepted" ${!selected.size?'disabled':''}>Accept</button><button class="button quiet small" data-bulk="deferred" ${!selected.size?'disabled':''}>Defer</button><button class="button quiet small" data-bulk="rejected" ${!selected.size?'disabled':''}>Reject</button></div>`:'<p class="muted">Captured automatically after confirmed import. Open any row to inspect the source or record an observation.</p>';
  $('#review-list').innerHTML=pendingToolbar+table([...(hasPending?['']:[]),'Date','Type','Captured claim','Source','Outcome'],rows,`<colgroup>${hasPending?'<col style="width:36px">':''}<col style="width:100px"><col style="width:110px"><col><col style="width:22%"><col style="width:100px"></colgroup>`);
}
function renderMemory() {
  const visible=paginate('memory',filteredRows('memory'));
  $('#memory-list').innerHTML=table(['Date','Type','Stored claim','Source'],visible.map(item=>`<tr><td class="cell-date">${esc(item.source.occurred_at)}</td><td>${typeTag(item.kind)}</td><td><button class="row-button" data-open="state" data-id="${esc(item.item_id)}">${esc(short(item.proposition))}</button></td><td class="cell-clip cell-muted" title="${esc(item.source.title)}">${esc(short(item.source.title,55))}${flagged('state',item.item_id)?'<span class="flag">● Flagged</span>':''}</td></tr>`),'<colgroup><col style="width:105px"><col style="width:115px"><col><col style="width:26%"></colgroup>');
}
function renderSources() {
  const visible=paginate('sources',filteredRows('sources'));
  $('#source-list').innerHTML=table(['Date','Source','Context','Path'],visible.map(item=>{const links=related(item.source_id);return `<tr><td class="cell-date">${esc(item.occurred_at)}</td><td><button class="row-button" data-open="source" data-id="${esc(item.source_id)}">${esc(short(item.title))}</button>${flagged('source',item.source_id)?'<span class="flag">● Flagged</span>':''}</td><td class="cell-clip cell-muted" title="${esc(item.context)}">${esc(short(item.context,72))}</td><td class="cell-muted">${links.state?'Stored':links.review?links.review.status:'No suggestion'}</td></tr>`}),'<colgroup><col style="width:105px"><col style="width:32%"><col><col style="width:115px"></colgroup>');
}
function findingTarget(f) {const item=lookup(f.target_type,f.target_id);if(item) return f.target_type==='source'?item.title:item.proposition;return 'Record no longer active';}
function renderFindings() {
  const counts=count(data.findings,'category');
  $('#finding-summary').innerHTML=Object.entries(counts).sort((a,b)=>b[1]-a[1]).map(([name,n])=>`<span class="finding-chip">${esc(labels[name]||name)} · ${n}</span>`).join('')||'<p class="muted">No findings yet. Open a source, suggestion, or stored item to record one.</p>';
  $('#finding-list').innerHTML=data.findings.length?data.findings.map(f=>`<div class="finding-row"><div><span class="finding-chip">${esc(labels[f.category]||f.category)}</span><div class="meta">${esc(f.target_type)} · ${esc(f.created_at.slice(0,10))}</div></div><div><button class="row-button" data-open="${esc(f.target_type)}" data-id="${esc(f.target_id)}">${esc(short(findingTarget(f),120))}</button>${f.note?`<p>${esc(f.note)}</p>`:''}</div><button class="button quiet small" data-remove-finding="${esc(f.finding_id)}">Remove finding</button></div>`).join(''):'<div class="empty"><h3>No findings recorded</h3><p>Use the record inspector to tag examples while you test.</p></div>';
}
function detailSection(label,value) {return `<div class="detail-label">${label}</div><div class="detail-value">${esc(value)}</div>`;}
function sourceDetail(source) {return `${detailSection('Source',source.title)}<p class="muted">${esc(source.occurred_at)} · ${esc(source.context)}</p><div class="detail-label">Excerpt</div><div class="source-preview">${esc(short(source.excerpt,360))}</div><details><summary>Read full stored excerpt</summary><div class="source-full">${esc(source.excerpt)}</div></details>`;}
function feedbackForm(type,id) {return `<form class="feedback-form" id="feedback-form"><h3>Record a UAT finding</h3><p>Choose the pattern you observed. These are human notes, not classifier labels or accuracy metrics.</p><input type="hidden" name="target_type" value="${esc(type)}"><input type="hidden" name="target_id" value="${esc(id)}"><label>Issue category<select name="category">${Object.entries(labels).map(([value,label])=>`<option value="${value}">${label}</option>`).join('')}</select></label><label>Short note (optional, 240 characters)<textarea name="note" maxlength="240" placeholder="Describe the failure without copying source text"></textarea></label><button class="button secondary small">Review finding</button></form>`;}
function showRecord(type,id,focus=true) {
  const item=lookup(type,id);if(!item){closeDrawer();return;}
  openRecord={type,id};const source=sourceFor(type,item);const ownFlags=flags(type,id);
  $('#drawer-title').textContent=type==='source'?short(item.title,90):type==='state'?'Stored memory':'Suggestion';
  let body='';
  if(type==='suggestion') body=`${detailSection('Proposed claim',item.proposition)}<p>${typeTag(item.kind)} ${typeTag(item.status)}</p>${detailSection('Why it appeared',item.rationale)}<div class="detail-label">Uncertainty</div><div class="detail-box">${esc(item.uncertainty)}</div>${sourceDetail(source)}${item.status==='pending'?`<div class="drawer-actions"><button class="button primary" data-action="accepted" data-id="${esc(id)}">Accept</button><button class="button secondary" data-edit="suggestion" data-id="${esc(id)}">Edit</button><button class="button quiet" data-action="deferred" data-id="${esc(id)}">Defer</button><button class="button quiet" data-action="rejected" data-id="${esc(id)}">Reject</button></div>`:''}`;
  if(type==='state') body=`${detailSection('Stored claim',item.proposition)}<p>${typeTag(item.kind)} <span class="tag accepted">Active</span></p>${sourceDetail(source)}<div class="drawer-actions"><button class="button secondary" data-edit="state" data-id="${esc(id)}">Correct claim</button><button class="button danger" data-delete-state="${esc(id)}">Delete test item</button></div>`;
  if(type==='source'){const links=related(item.source_id);body=`${sourceDetail(item)}<div class="detail-label">Source → suggestion → memory</div><div class="detail-box">${links.review?`Suggestion: ${esc(links.review.kind)} · ${esc(links.review.status)}`:'No suggestion'}<br>${links.state?'Active stored item':'No active stored item'}</div><div class="drawer-actions">${links.review?`<button class="button secondary small" data-open="suggestion" data-id="${esc(links.review.suggestion_id)}">Open suggestion</button>`:''}${links.state?`<button class="button quiet small" data-open="state" data-id="${esc(links.state.item_id)}">Open stored item</button>`:''}</div>`;}
  body+=`<div class="detail-label">Recorded findings</div>${ownFlags.length?ownFlags.map(f=>`<span class="finding-chip">${esc(labels[f.category])}</span>`).join(''):'<p class="muted">No findings on this record.</p>'}${feedbackForm(type,id)}`;
  $('#drawer-body').innerHTML=body;
  $('#drawer').classList.add('open');$('#drawer').setAttribute('aria-hidden','false');$('#drawer-scrim').hidden=false;
  if(focus) $('#drawer-close').focus();
}
function closeDrawer(){openRecord=null;$('#drawer').classList.remove('open');$('#drawer').setAttribute('aria-hidden','true');$('#drawer-scrim').hidden=true;}
function confirmLocal(title,body,label='Confirm') {return new Promise(resolve=>{const dialog=$('#confirm-dialog');$('#confirm-title').textContent=title;$('#confirm-body').innerHTML=body;$('#confirm-yes').textContent=label;dialog.onclose=()=>resolve(dialog.returnValue==='confirm');dialog.showModal();});}
async function change(path,method,payload,success){try{await api(path,{method,body:JSON.stringify({...payload,confirmed:true})});await refresh();toast(success);}catch(error){errorToast(error)}}

document.addEventListener('click',async event=>{
  const nav=event.target.closest('[data-view],[data-go]');if(nav){setView(nav.dataset.view||nav.dataset.go);return;}
  const pager=event.target.closest('[data-page]');if(pager){const [view,direction]=pager.dataset.page.split(':');pages[view]+=direction==='next'?1:-1;({review:renderReview,memory:renderMemory,sources:renderSources})[view]();return;}
  const opener=event.target.closest('[data-open]');if(opener){showRecord(opener.dataset.open,opener.dataset.id);return;}
  const selectPage=event.target.closest('[data-select-page]');if(selectPage){paginate('review',filteredRows('review')).filter(x=>x.status==='pending').forEach(x=>selected.add(x.suggestion_id));renderReview();return;}
  if(event.target.closest('[data-clear-selection]')){selected.clear();renderReview();return;}
  const bulk=event.target.closest('[data-bulk]');if(bulk){const ids=[...selected];if(!ids.length)return;const names=ids.slice(0,5).map(id=>data.reviews.find(x=>x.suggestion_id===id)?.source.title||id);const verb={accepted:'Accept',deferred:'Defer',rejected:'Reject'}[bulk.dataset.bulk];const approved=await confirmLocal(`${verb} ${ids.length} suggestions?`,`<p>This will change the outcome of exactly ${ids.length} selected suggestions${bulk.dataset.bulk==='accepted'?' and add their claims to local memory':''}.</p><p>${names.map(name=>esc(name)).join('<br>')}${ids.length>5?'<br>…':''}</p>`,`${verb} selected`);if(approved)await change('/api/suggestions/bulk-action','POST',{suggestion_ids:ids,action:bulk.dataset.bulk},`${ids.length} suggestions updated`);return;}
  const action=event.target.closest('[data-action]');if(action){const item=lookup('suggestion',action.dataset.id);if(!item)return;const verb={accepted:'Accept',deferred:'Defer',rejected:'Reject'}[action.dataset.action];const approved=await confirmLocal(`${verb} suggestion?`,`<p>${esc(item.kind)}: ${esc(short(item.proposition,250))}</p><p>Source: ${esc(item.source.title)}</p><p>${action.dataset.action==='accepted'?'This will add the claim to local memory.':'This changes the review outcome.'}</p>`,verb);if(approved)await change(`/api/suggestions/${encodeURIComponent(action.dataset.id)}/action`,'POST',{action:action.dataset.action},'Suggestion updated');return;}
  const editor=event.target.closest('[data-edit]');if(editor){const item=lookup(editor.dataset.edit,editor.dataset.id);if(!item)return;editRecord={type:editor.dataset.edit,id:editor.dataset.id};$('#edit-title').textContent=editRecord.type==='state'?'Correct stored claim':'Edit suggestion';$('#edit-current').textContent=`Current: ${short(item.proposition,180)}`;$('#edit-value').value=item.proposition;$('#edit-dialog').showModal();return;}
  const deletion=event.target.closest('[data-delete-state]');if(deletion){const item=lookup('state',deletion.dataset.deleteState);if(!item)return;const approved=await confirmLocal('Delete this test item?',`<p>${esc(short(item.proposition,260))}</p><p>This removes it from active memory and retrieval. There is no undo in this prototype.</p>`,'Delete test item');if(approved)await change(`/api/state/${encodeURIComponent(item.item_id)}`,'DELETE',{},'Test item deleted');return;}
  const remove=event.target.closest('[data-remove-finding]');if(remove){const approved=await confirmLocal('Remove this finding?','<p>This removes the structured UAT observation from the local workspace.</p>','Remove finding');if(approved)await change(`/api/findings/${encodeURIComponent(remove.dataset.removeFinding)}`,'DELETE',{},'Finding removed');return;}
});
document.addEventListener('change',event=>{if(event.target.matches('[data-select]')){event.target.checked?selected.add(event.target.dataset.select):selected.delete(event.target.dataset.select);renderReview();return;}if(event.target.matches('#review-status,#review-type,#memory-type,#memory-feedback,#source-sort,#source-feedback')){const view=event.target.id.startsWith('review')?'review':event.target.id.startsWith('memory')?'memory':'sources';pages[view]=0;({review:renderReview,memory:renderMemory,sources:renderSources})[view]();}});
document.addEventListener('input',event=>{if(event.target.matches('#review-search,#memory-search,#source-search')){const view=event.target.id.startsWith('review')?'review':event.target.id.startsWith('memory')?'memory':'sources';pages[view]=0;({review:renderReview,memory:renderMemory,sources:renderSources})[view]();}});
$('#drawer-close').onclick=closeDrawer;$('#drawer-scrim').onclick=closeDrawer;document.addEventListener('keydown',event=>{if(event.key==='Escape'&&$('#drawer').classList.contains('open')&&!document.querySelector('dialog[open]'))closeDrawer();});
$('#drawer-body').addEventListener('submit',async event=>{if(event.target.id!=='feedback-form')return;event.preventDefault();const form=new FormData(event.target);const type=form.get('target_type'),id=form.get('target_id'),category=form.get('category'),note=String(form.get('note')||'').trim();const approved=await confirmLocal('Record this UAT finding?',`<p>${esc(labels[category])} on ${esc(type)}.</p>${note?`<p>Note: ${esc(note)}</p>`:''}<p>Stored locally for pattern analysis.</p>`,'Record finding');if(approved)await change('/api/findings','POST',{target_type:type,target_id:id,category,note},'Finding recorded');});
$('#edit-cancel').onclick=()=>$('#edit-dialog').close();
$('#edit-form').onsubmit=async event=>{event.preventDefault();const item=lookup(editRecord.type,editRecord.id),value=$('#edit-value').value.trim();if(!value)return;$('#edit-dialog').close();const approved=await confirmLocal(editRecord.type==='state'?'Confirm correction?':'Confirm edited suggestion?',`<p><strong>Current:</strong> ${esc(short(item.proposition,230))}</p><p><strong>New:</strong> ${esc(short(value,230))}</p>`,editRecord.type==='state'?'Correct item':'Confirm edit');if(!approved)return;if(editRecord.type==='state')await change(`/api/state/${encodeURIComponent(editRecord.id)}`,'PATCH',{proposition:value},'Stored item corrected');else await change(`/api/suggestions/${encodeURIComponent(editRecord.id)}/action`,'POST',{action:'edited',proposition:value},'Edited suggestion stored');};
$('#question-form').onsubmit=async event=>{event.preventDefault();const question=$('#question').value.trim();if(!question)return;try{const result=await api('/api/retrieve',{method:'POST',body:JSON.stringify({question})});$('#results').innerHTML=`<div class="detail-label">${result.matches.length} CITED MATCH${result.matches.length===1?'':'ES'}</div>${result.matches.length?result.matches.map(match=>`<div class="result-card"><h3>${esc(short(match.item.proposition,220))}</h3><p>${esc(match.source.title)} · ${esc(match.source.occurred_at)}</p><button class="text-button" data-open="state" data-id="${esc(match.item.item_id)}">Inspect claim and source →</button></div>`).join(''):'<div class="empty"><h3>No matching stored items</h3><p>Try different terms or inspect the sources directly.</p></div>'}<p class="muted">${esc(result.uncertainty)}</p>`;}catch(error){errorToast(error)}};
$('#refresh').onclick=()=>refresh().then(()=>toast('Workspace refreshed')).catch(errorToast);
function candidateSummary(candidates,sources=[]) {return candidates.length?`<p><strong>${candidates.length} candidate memories</strong> will be captured to local memory as part of this confirmed import. Nothing is added for messages with no strong local cue.</p><ul class="capture-preview">${candidates.map(c=>{const source=sources.find(s=>s.source_id===c.source_id);return `<li><strong>${esc(c.kind)}:</strong> ${esc(c.proposition)}${source?`<small>${esc(source.occurred_at)} · ${esc(source.title)} · ${esc(source.context)}</small>`:''}<small>${esc(c.rationale)} ${esc(c.uncertainty)}</small></li>`}).join('')}</ul>`:'<p>No candidate memories matched the local rules. Sources can still be imported for later inspection.</p>'}
$('#load-fixtures').onclick=async()=>{const preview=await api('/api/preview-fixtures');const approved=await confirmLocal('Load synthetic fixtures?',`<p>Three synthetic sources will be saved locally.</p>${candidateSummary(preview.candidates,preview.sources)}<p>Captured items can be corrected or deleted later.</p>`,'Load fixtures');if(approved)await change('/api/load-fixtures','POST',{},'Fixtures loaded');};
$('#import-json').onclick=async()=>{const file=$('#json-file').files[0];if(!file){toast('Choose a JSON file first');return;}try{const payload=JSON.parse(await file.text());if(payload.format!=='lifetime-ai-uat-sources/v1'||!Array.isArray(payload.sources)||!payload.sources.length)throw Error('Expected a source-only UAT JSON file');const candidates=await api('/api/preview-sources',{method:'POST',body:JSON.stringify({sources:payload.sources})});$('#json-preview').innerHTML=`${payload.sources.length} sources · ${candidates.candidate_count} candidate memories${candidateSummary(candidates.candidates,payload.sources)}`;const approved=await confirmLocal(`Import ${payload.sources.length} JSON sources?`,`${candidateSummary(candidates.candidates,payload.sources)}<p>Source excerpts and candidates stay in this local workspace. Correct or delete stored items after import.</p>`,'Import and capture');if(approved)await change('/api/import-json','POST',{payload},'JSON sources imported');}catch(error){errorToast(error)}};
$('#import-mbox').onclick=async()=>{const file=$('#mbox-file').files[0];if(!file){toast('Choose an MBOX file first');return;}try{const result=await api('/api/preview-mbox',{method:'POST',body:JSON.stringify({mbox_text:await file.text()})});$('#mbox-preview').innerHTML=`${result.sources.length} readable messages · ${result.candidate_count} candidate memories. Attachments excluded.${result.sources.slice(0,8).map(s=>`<div class="preview-item">${esc(s.occurred_at)} · ${esc(s.title)}</div>`).join('')}${candidateSummary(result.candidates,result.sources)}`;const approved=await confirmLocal(`Import ${result.sources.length} MBOX sources?`,'<p>Attachments are excluded and the raw MBOX file is not retained.</p>'+candidateSummary(result.candidates,result.sources)+'<p>Import confirmation captures these candidates to active local memory in one step. Review, correct, or delete them afterward.</p>','Import and capture');if(approved)await change('/api/import-mbox','POST',{sources:result.sources},'MBOX sources imported');}catch(error){errorToast(error)}};
$('#source-form').onsubmit=async event=>{event.preventDefault();const form=new FormData(event.target);const payload={title:form.get('title'),occurred_at:form.get('date'),context:form.get('context'),excerpt:form.get('excerpt')};const source={source_id:'local:preview',...payload};const candidates=await api('/api/preview-sources',{method:'POST',body:JSON.stringify({sources:[source]})});const approved=await confirmLocal('Add this local source?',candidateSummary(candidates.candidates,[source])+'<p>This confirmed action stores the source and any candidate in the local workspace.</p>','Add source');if(approved){await change('/api/sources','POST',payload,'Source added');event.target.reset();}};
$('#reset').onclick=async()=>{const approved=await confirmLocal('Reset the entire workspace?','<p>All local sources, suggestions, stored items, findings, and interaction history will be removed. This cannot be undone.</p>','Reset workspace');if(approved){await change('/api/reset','POST',{},'Workspace reset');closeDrawer();$('#results').innerHTML='';}};
refresh().catch(errorToast);
