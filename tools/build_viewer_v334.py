"""V33.4 documentation overlay, installed meshes retained exactly. CERN-OHL-S-2.0."""
from pathlib import Path
import re,json,gzip,base64,subprocess,copy,hashlib
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/solid-leg-v334'
read=lambda p:json.loads((R/p).read_text())
HEAD=read('config/solid_leg_blocks_v334.json')['head_before']
base=subprocess.check_output(['git','show',HEAD+':exports/generated/viewer-v32/index.html'],cwd=R,text=True)
b64=re.search(r'<script id="viewer-data"[^>]*>(.*?)</script>',base,re.S).group(1)
D=json.loads(gzip.decompress(base64.b64decode(b64)));oldD=copy.deepcopy(D)
Q=json.loads(re.search(r'<script id="v333-data"[^>]*>(.*?)</script>',base,re.S).group(1))
jig=json.loads(gzip.decompress((O/'review-mesh.json.gz').read_bytes()))
reg=read('exports/generated/solid-leg-v334/manufacturing-register.json');manual=read('exports/generated/solid-leg-v334/assembly-manual.json')
solid=[p for p in reg['parts'] if p.get('manufacturing_class')=='SHOP_MADE_SOLID_WOOD_PART'];sources={p['source_component'] for p in solid}
D['detail']=[d for d in D['detail'] if d['meta']['source'] not in sources]
for p in solid:
 a=next(i for i in D['installed'] if i['key']==p['source_component']);a['meta'].update(names={'en':p['description_en'],'pt-BR':p['description_pt_BR']},stage='02',material='STRUCTURAL_SOLID_WOOD',thickness=None,quantity=4,families=['SW01'],instances=[p['instance_id']],manufacturing_status=['SHOP_MADE_SOLID_WOOD_PART'],status='WAITING_FOR_PHYSICAL_MEASUREMENT',tooling_url='../solid-leg-v334/README.md',face_A=p['face_A_outward_world'])
 b=copy.deepcopy(a);b.update(key=p['instance_id'],offset=[-90 if p['assembly_id'] in ('P029','P031') else 90,0,-50],source_mesh='V33.4 solid wood; unchanged CURRENT reference B-rep',source_matrix=p['local_to_installed_matrix'])
 b.pop('overview',None);b['meta'].update(id='SW01',instance=p['instance_id']);D['detail'].append(b)
D['manual']=manual;D['source_head']=HEAD
assert sum(d['meta']['kind']=='wood' for d in D['detail'])==106
for a,b in zip(D['installed'],oldD['installed']):assert a['key']==b['key'] and a['geometry']==b['geometry']
assert D['states']==oldD['states'] and D['geometry']==oldD['geometry']
for k,file in [('metrics','project-metrics'),('mass','mass-budget'),('hardware','hardware-dashboard'),('packaging','packaging')]:Q[k]=read('exports/generated/solid-leg-v334/'+file+'.json')
Q['material']=read('exports/generated/solid-leg-v334/material-utilization.json')['stocks']
Q['pieces']={p['instance_id']:{k:p[k] for k in ['local_to_installed_matrix','finished_xy_size_mm','finished_xy_bounds_mm','manufacturing_part_id']} for p in reg['parts']}
for p in solid:Q['pieces'][p['instance_id']]['packing_mesh']=jig['packing_blocks'][p['instance_id']]
clips=[]
for stage in manual['stages']:
 for step in stage['steps']:
  old=next(c for c in Q['clips'] if c['id']=='assembly-'+('16.1' if step['id']=='02.0' else step['id']))
  c=copy.deepcopy(old);c.update(id='assembly-'+step['id'],title={k:step['id']+' · '+v for k,v in step['title'].items()},stage=stage['id'],step=step['id'],first_stage_step=step==stage['steps'][0],piece_ids=step['component_ids'],hardware_ids=step['hardware_ids'],action=step['action'],check=step['check']);clips.append(c)
clips += [c for c in Q['clips'] if c['type']!='assembly']
for mode,en,pt in [('place','Solid block placement','Posicionamento do bloco maciço'),('fit','Fit universal jig / F-R stop','Encaixe do gabarito / batente F-R'),('clamp','Clamp jaw locations','Posições das sapatas dos grampos'),('drill','Drill reference axes','Furação nos eixos de referência'),('test','Test real backing plate / leg bolts','Teste da chapa e parafusos reais')]:
 clips.append({'id':'jig-'+mode,'type':'jig','mode':mode,'title':{'en':en,'pt-BR':pt},'duration_s':8,'status':'SCHEMATIC_ASSEMBLY_ANIMATION','note':{'en':'SCHEMATIC — tooling only.58mm reference versus57.15mm remains HOLD. Register before FLOOR / PC_BASE / SHELF_1 installation. Clamp jaws show reserved lands, not a qualified complete clamp. Test purchased hardware before accepting bores; no drilling release.','pt-BR':'ESQUEMÁTICO — somente ferramental.58mm versus57,15mm permanece PENDENTE. Posicione antes de FLOOR / PC_BASE / SHELF_1. Sapatas indicam áreas reservadas, não grampo completo qualificado. Teste ferragens reais antes de aceitar; furação não liberada.'}})
for c in clips:
 if c['id']=='jig-test':
  c['note']['en']+=' B13 is the existing plate envelope; translucent probes mark axes, not selected bolts.'
  c['note']['pt-BR']+=' B13 é o envelope existente da chapa; cilindros translúcidos indicam eixos, não parafusos selecionados.'
Q['clips']=clips
Q['validation']['order_changes']=manual['order_changes']
Q['validation']['order_decision']='Solid blocks register/drill at02.0 before FLOOR, PC_BASE and SHELF_1. Selected hardware/tool/clamp and physical fixture qualification remain HOLD.'
Q['validation']['steps']=[step['validation'] for s in manual['stages'] for step in s['steps']]
(O/'animations.json').write_text(json.dumps(clips,indent=2,ensure_ascii=False)+'\n')
(O/'viewer-data.json.gz').write_bytes(gzip.compress(json.dumps(D,separators=(',',':')).encode(),mtime=0))
base=base[:base.index('<script id="v333-data"')]+ '</body></html>'
base=re.sub(r'(<script id="viewer-data"[^>]*>).*?(</script>)',lambda m:m[1]+base64.b64encode(gzip.compress(json.dumps(D,separators=(',',':')).encode(),mtime=0)).decode()+m[2],base,flags=re.S)
base=base.replace('Leg-block layers','Solid leg blocks').replace('Camadas dos blocos dos pés','Blocos maciços dos pés').replace('V33.3','V33.4').replace('V33.2','V33.4')
base=base.replace("'../flatpack-v331/manufacturing-wood-bom-'+(language==='en'?'en':'pt-BR')+'.md'","'../solid-leg-v334/manufacturing-bom'+(language==='en'?'':'.pt-BR')+'.md'")
base=base.replace("</p><button id=\"part-manual\"", "${m.tooling_url?' · <a href=\"'+m.tooling_url+'\" target=\"_blank\">LEG DRILL JIG / GABARITO DOS PÉS</a>':''}</p><button id=\"part-manual\"")
ext=(R/'tools/viewer-v333/extension.js').read_text().replace('../assembly-v333/README.md','../solid-leg-v334/README.md').replace('wood at650kg/m³','wood · planning density').replace('madeira a650kg/m³','madeira · densidade estimada')
ext=ext.replace('function exit(){playing=false;','function exit(){window.legJig?.hide();playing=false;')
ext=ext.replace("if(clip.type==='assembly'){", "if(clip.type==='jig'){window.legJig.show(clip.mode);}else if(clip.type==='assembly'){",1)
ext=ext.replace("const g=src.geometry.clone().applyMatrix4(dest),m=","const original=info.packing_mesh?new T.BufferGeometry():src.geometry;if(info.packing_mesh){original.setAttribute('position',new T.Float32BufferAttribute(info.packing_mesh.vertices.flat(),3));original.setIndex(info.packing_mesh.faces.flat());original.computeVertexNormals();}const g=original.clone().applyMatrix4(dest),m=")
ext=ext.replace("clip.type==='assembly'?tr('SCHEMATIC","['assembly','jig'].includes(clip.type)?tr('SCHEMATIC")
needle="if(clip.type==='assembly'){\n  for(const m of V.detail)"
ext=ext.replace(needle,"if(clip.type==='jig'){window.legJig.seek(p);caption=L(clip.title)+' · SCHEMATIC / ESQUEMÁTICO';}else "+needle)
jig=json.loads(gzip.decompress((O/'review-mesh.json.gz').read_bytes()))
scripts='<script id="v333-data" type="application/json">'+json.dumps(Q,separators=(',',':'),ensure_ascii=False).replace('</','<\\/')+'</script><script id="v334-jig" type="application/json">'+json.dumps(jig,separators=(',',':'))+'</script><script>'+(R/'tools/viewer-v334/jig.js').read_text()+'</script><script>'+ext+'</script>'
base=base.replace('</body>',scripts+'</body>');(R/'exports/generated/viewer-v32/index.html').write_text(base)
(O/'viewer-regression.json').write_text(json.dumps({'all_installed_geometry_and_state_ids_unchanged':True,'geometry_dictionary_unchanged':True,'CNC_manufacturing_meshes_unchanged':all(d in D['detail'] for d in oldD['detail'] if d['meta']['source'] not in sources),'wood_pieces':106,'solid_blocks':4,'jig_is_tooling_only':True,'source_mesh_sha256':D['source_mesh_sha256'],'head_before':HEAD,'viewer_html_sha256':hashlib.sha256(base.encode()).hexdigest(),'release':False},indent=2)+'\n')
print('V334_VIEWER_PASS',len(clips),'clips',len(base),'bytes')
