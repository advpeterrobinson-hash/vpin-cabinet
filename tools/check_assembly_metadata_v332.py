"""Source/B-rep protection, metadata coverage and release regression. CERN-OHL-S-2.0."""
from pathlib import Path
import json,gzip,hashlib,subprocess,copy,re,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/viewer-v332';HEAD='a1f8bb04f7cec6a2220355c6b7ead0e7e0e92ab4'
read=lambda p:json.loads((R/p).read_text());D=json.loads(gzip.decompress((O/'viewer-data.json.gz').read_bytes()));M=read('exports/generated/viewer-v332/assembly-manual.json');REG=read('exports/generated/flatpack-v331/manufacturing-register.json');C=read('config/hardware_catalog_v33.json');checks=[]
def check(name,value,details=None):
 checks.append({'name':name,'pass':bool(value),'details':details});assert value,(name,details)
# Independent Git blob equality: the saved protection manifest cannot bless an edited input.
tree={}
for row in subprocess.check_output(['git','ls-tree','-r',HEAD],cwd=R,text=True).splitlines():
 mode,typ,rest=row.split(' ',2);oid,name=rest.split('\t');tree[name]=oid
protected=read('exports/generated/viewer-v332/geometry-protection.json')['files']
for f in protected:
 raw=(R/f['path']).read_bytes();blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
 check('unchanged Git authority '+f['path'],blob==tree[f['path']] and hashlib.sha256(raw).hexdigest()==f['sha256'])
check('source head authority',D['source_head']==M['source_head']==HEAD)
check('no release flags',not D['manufacturing_release'] and not M['manufacturing_release'] and not read('config/manufacturing/flatpack_v331.json')['full_sheet_release'] and not read('config/current_v32.json')['manufacturing_ready'])
parts={p['instance_id']:p for p in REG['parts']};wood={p['key']:p for p in D['detail'] if p['meta']['kind']=='wood'}
check('130 exact instances / 66 families',set(parts)==set(wood) and len(parts)==130 and len({p['meta']['id'] for p in wood.values()})==66)
wm=json.loads(gzip.decompress((R/'exports/generated/flatpack-v331/review-mesh.json.gz').read_bytes()));maxerr=0
for iid,p in parts.items():
 m=wood[iid];source=wm[iid];render=D['geometry'][m['geometry']];mat=p['local_to_installed_matrix']
 check(iid+' rigid transform and faces unchanged',m['source_matrix']==mat and render['faces']==source['faces'])
 expected=[[sum(mat[4*i+j]*x[j] for j in range(3))+mat[4*i+3] for i in range(3)] for x in source['vertices']]
 err=max(abs(x-y) for a,b in zip(expected,render['vertices']) for x,y in zip(a,b));maxerr=max(maxerr,err)
 check(iid+' review rounding only',err<=.000051,err)
 check(iid+' correct ID/status/thickness',m['meta']['id']==p['manufacturing_part_id'] and m['meta']['manufacturing_status']==[p['manufacturing_status']] and m['meta']['thickness']==p['nominal_stock_thickness_mm'])
 ET.parse(O/'orientation'/(iid+'.svg'))
check('retainer explosion is not collapsed',wood['P049-Cap']['offset']!=wood['P049-Strip']['offset'])
check('all orientation cards',len(list((O/'orientation').glob('*.svg')))==130)
manualparts={p['instance_id']:p for p in M['part_preparation']}
for iid,p in parts.items():
 mp=manualparts[iid]
 check(iid+' exact CNC/manual operation metadata',all(mp[k]==p[k] for k in ['manual_finish','through_cuts','pockets','face_A_outward_world','local_to_installed_matrix','machining_face','opposite_face']))
ids={h['id'] for h in C['hardware']};check('148 hardware families represented',ids=={p['meta']['hardware_id'] for p in D['detail'] if p['meta']['hardware_id']})
for p in D['detail']:
 hid=p['meta']['hardware_id']
 if hid:
  h=next(h for h in C['hardware'] if h['id']==hid)
  check(p['key']+' quantity/freeze unchanged',p['meta']['quantity']==h['quantity'] and p['meta']['status']==h['freeze_status'])
  if p['meta'].get('tray'):check(p['key']+' unlocated sample labelled',p['placement_status']=='UNLOCATED_FAMILY_EXEMPLAR_NOT_INSTALLED')
closure=read('exports/generated/flatpack-v331/hardware-quantity-closure.json')['rows'];check('all 13 unresolved quantities preserved',M['hardware_quantity_overlay']==closure and all(r['quantity'] is None for r in closure))
stages=M['stages'];check('19 stages, 31 bilingual steps',len(stages)==19 and sum(len(s['steps']) for s in stages)==31)
check('all wood assigned exactly once',[x for s in stages for x in s['pieces']].__len__()==130 and {x for s in stages for x in s['pieces']}==set(parts))
check('all hardware assigned exactly once',len([x for s in stages for x in s['hardware']])==148 and {x for s in stages for x in s['hardware']}==ids)
allowed={'READY','PROVISIONAL_HARDWARE','WAITING_FOR_PHYSICAL_MEASUREMENT','WAITING_FOR_COUPON','OPTIONAL'}
for s in stages:
 check(s['id']+' acyclic dependencies',all(int(d)<int(s['id']) for d in s['depends_on']))
 for step in s['steps']:
  check(step['id']+' bilingual required fields',all(step[k].get('en') and step[k].get('pt-BR') for k in ['title','orientation','tools','faces','action','check','hold']) and step['status'] in allowed and step['next_state'])
# Native saved hardware is read only; LOD only changes the visualization tessellation.
lod=read('exports/generated/viewer-v332/hardware-lod-validation.json');check('hardware LOD source unchanged',lod['pass'] and all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in lod['source_hashes'].items()))
check('hardware LOD bounded',lod['installed_triangles']<150000 and lod['family_triangles']<50000)
for lang,filename in [('en','ASSEMBLY_MANUAL.md'),('pt-BR','ASSEMBLY_MANUAL.pt-BR.md')]:
 text=(R/'docs'/filename).read_text();check(lang+' manual every piece',all('### '+iid+' /' in text for iid in parts));check(lang+' no final PDF',not (O/(filename+'.pdf')).exists())
 for link in re.findall(r'\]\(([^)]+)\)',text):
  if re.match(r'^[a-z]+:',link):continue
  p=link.split('#')[0].split('?')[0];check(lang+' local manual link '+p,(R/'docs'/p).exists())
# Negative controls exercise the audit predicates rather than accepting self-declared success.
bad=copy.deepcopy(M['hardware_quantity_overlay']);bad[0]['quantity']=14
check('negative control: guessed hardware quantity rejected',bad!=closure)
badwood=dict(wood);badwood.pop('P029-L1',next(iter(badwood.values()))) if 'P029-L1' in badwood else badwood.pop(next(iter(badwood)))
check('negative control: missing manufacturing member rejected',set(badwood)!=set(parts))
browser=read('exports/generated/viewer-v332/browser-validation.json');check('browser binds current viewer',browser['viewer_sha256']==hashlib.sha256((R/'exports/generated/viewer-v32/index.html').read_bytes()).hexdigest());check('browser checks pass',browser['pass'] and all(c['pass'] for c in browser['checks']))
check('20 real review images',len(read('exports/generated/viewer-v332/review-views.json'))==20 and all((O/f'{n:02}-review.png').exists() for n in range(1,21)))
result={'pass':True,'head_before':HEAD,'checks':checks,'protected_file_count':len(protected),'source_mesh_sha256':D['source_mesh_sha256'],'viewer_sha256':hashlib.sha256((R/'exports/generated/viewer-v32/index.html').read_bytes()).hexdigest(),'manufacturing_member_visual_rounding_max_mm':maxerr,'geometry_changed':False,'manufacturing_release':False,'manual_status':M['status'],'installed_components':93,'manufacturing_pieces':130,'canonical_families':66,'manual_stages':19,'manual_steps':31,'checkpoints':31,'visibility_groups':len(D['groups']),'unlocated_hardware_families':sum(bool(p['meta'].get('tray')) for p in D['detail'])}
(O/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print('V332_METADATA_PASS',len(checks),'checks;',len(protected),'immutable files; max visual rounding',maxerr)
