"""V33.6 button datum and monitor-service B-rep study. CERN-OHL-S-2.0.
Positions are design decisions; provisional hardware bores are NOT machining authority.
"""
from pathlib import Path
import json,sys,math,gzip,hashlib
import FreeCAD as A, Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,pf_names,transform,PF,V
C=json.loads((R/'config/monitor_support_v336.json').read_text());O=R/C['output'];O.mkdir(parents=True,exist_ok=True);(O/'brep').mkdir(exist_ok=True)
old=load(R/C['source']);new=dict(old);study={};checks=[];data={}
review=json.loads((R/'exports/generated/notch-floor-fans-v32/validation.json').read_text())['review'];alpha=review['closed_slope_deg'];bz=400.05+45*math.tan(math.radians(alpha))-12-55*math.cos(math.radians(alpha))
def box(x,y,z,w,d,h):return Part.makeBox(w,d,h,V(x,y,z))
def tf(s):s=s.copy();s.rotate(V(),V(1,0,0),alpha);s.translate(V(0,45,bz));return s
def inv(s):s=s.copy();s.translate(V(0,-45,-bz));s.rotate(V(),V(1,0,0),-alpha);return s
def mirror(s):
 m=A.Matrix();m.A11=-1;m.A14=600;s=s.copy();s.transformShape(m,True);return s
def diff(a,b):
 if a.isSame(b):return 0.0
 if a.exportBrepToString()==b.exportBrepToString():return 0.0
 return a.cut(b).Volume+b.cut(a).Volume
def rounded(x,y,z,w,d,h,r):
 ss=[]
 if w>2*r:ss.append(box(x+r,y,z,w-2*r,d,h))
 if d>2*r:ss.append(box(x,y+r,z,w,d-2*r,h))
 ss += [Part.makeCylinder(r,h,V(xx,yy,z)) for xx in [x+r,x+w-r] for yy in [y+r,y+d-r]]
 s=ss[0]
 for q in ss[1:]:s=s.fuse(q)
 return s.removeSplitter()
def ck(n,v,detail=None):checks.append({'name':n,'pass':bool(v),'detail':detail});print(n,bool(v),flush=True)
def hits(s,obs):
 out=[]
 for n,b in obs.items():
  if s.BoundBox.intersect(b.BoundBox):
   vol=s.common(b).Volume
   if vol>1e-4:out.append({'part':n,'volume_mm3':vol})
 return out
def mesh(s):
 vv,ff=s.tessellate(.3);return {'vertices':[list(p) for p in vv],'faces':ff}
clean=load(R/C['playfield']['clean_source'])['PF_BasePlywood'];bl=inv(clean);bb=bl.BoundBox
ck('historical clean base is exact rectangular 500 x 1020 x 18',diff(bl,box(50,20,-14,500,1020,18))<1e-5)
study['PreviousCleanBase']=clean;study['CurrentHornedBase']=old['PF_BasePlywood']
new['PF_BasePlywood']=clean.copy()
# Restore only the old reference bores/pockets, then put reference placeholders at
# the owner-selected centers. These dimensions remain visualization-only HOLD.
left=old['SIDE_L'].copy();bore=C['side_buttons']['reference_bore_for_visualization_mm'];pdiam,pdepth=C['side_buttons']['reference_nut_pocket_for_visualization_mm']
for kind,y in zip(['primary','secondary'],C['side_buttons']['candidate_y_mm']):
 prev=review['buttons'][kind];dy=y-prev['y_mm'];dz=270-prev['z_mm']
 left=left.fuse(Part.makeCylinder(bore/2,18,V(0,prev['y_mm'],prev['z_mm']),V(1,0,0))).fuse(Part.makeCylinder(pdiam/2,pdepth,V(18-pdepth,prev['y_mm'],prev['z_mm']),V(1,0,0))).removeSplitter()
 left=left.cut(Part.makeCylinder(bore/2,20,V(-1,y,270),V(1,0,0))).cut(Part.makeCylinder(pdiam/2,pdepth+1,V(18-pdepth,y,270),V(1,0,0))).removeSplitter()
 for n,s in old.items():
  if kind in n and n.startswith(('Leaf','Button')):
   q=s.copy();q.translate(V(0,dy,dz));new[n]=q;study['Old_'+n]=s.copy()
new['SIDE_L']=left;new['SIDE_R']=mirror(left)
ck('button center symmetry',diff(new['SIDE_R'],mirror(new['SIDE_L']))<1e-5)
for kind,y in zip(['primary','secondary'],C['side_buttons']['candidate_y_mm']):
 ck(kind+' axis Y/Z',abs(new['LeafButton_'+kind+'_L'].BoundBox.Center.y-y)<1e-6 and abs(new['LeafButton_'+kind+'_L'].BoundBox.Center.z-270)<1e-6)
# Test the low-button arrangement before opening any support wood.
phys=actual(new);obs={n:s for n,s in phys.items() if not n.startswith(('Leaf','Button')) and n not in ['SIDE_L','SIDE_R','CandidateGlass']}
rows=[]
for n,s in new.items():
 if n.startswith(('Leaf','Button')):
  hh=hits(s,obs);rows.append({'name':n,'hits':hh,'base_separation_mm':s.distToShape(clean)[0]})
ck('restored button occupied and existing wire/tool reserves clear installed structures',not any(r['hits'] for r in rows),[r for r in rows if r['hits']])
data['buttons']=rows
# Explicit palm/finger approach from open cabinet with playfield at 50 degrees.
service=dict(obs);service.update(transform({n:s for n,s in phys.items() if n in pf_names(phys)},angle=-50,axis=PF))
access=[]
for kind,y in zip(['primary','secondary'],C['side_buttons']['candidate_y_mm']):
 for side in ['L','R']:
  palm=box(65,y-30,250,70,60,50);entry=box(65,y-30,275,70,60,325);finger=box(38,y-12,248,27,24,35)
  driver=Part.makeCylinder(10,100,V(43,y,270),V(1,0,0))
  for label,s in [('palm',palm),('top_entry',entry),('finger',finger),('driver',driver)]:
   if side=='R':s=mirror(s)
   n=f'ButtonAccess_{kind}_{side}_{label}';study[n]=s;hh=hits(s,service);access.append({'name':n,'hits':hh})
ck('button hand/tool approach with playfield service and glass/matrix removed',not any(r['hits'] for r in access),[r for r in access if r['hits']]);data['button_access']=access
# One rear service window; preserve the complete modeled central VESA load zone.
op=C['playfield'];x,y,w,h=op['service_window_xywh_mm'];cut=rounded(x,y,-15,w,h,20,op['service_window_radius_mm']);cuts={'PF_MainServiceWindow':cut}
for i,(x,y,w,h) in enumerate(op['strain_slots_xywh_mm']):cuts[f'PF_StrainSlot{i+1}']=rounded(x,y,-15,w,h,20,op['strain_slot_radius_mm'])
base=clean.copy();openrows=[];features={n:s for n,s in new.items() if n.startswith(('PF_StrapScrew','PF_CommercialStrap')) or n in ['PF_WoodDowel','PF_VESAEnvelope']}
for n,local in cuts.items():
 world=tf(local);removed=base.common(world);base=base.cut(world).removeSplitter();study[n]=world
 nearest={k:world.distToShape(s)[0] for k,s in features.items()};b=local.BoundBox
 openrows.append({'name':n,'classification':'SERVICE_WINDOW' if 'Main' in n else 'STRAIN_RELIEF_SLOT','local_xy_bounds_mm':[b.XMin,b.YMin,b.XMax,b.YMax],'radius_mm':8 if 'Main' in n else 3,'nearest_outer_edge_mm':min(b.XMin-50,550-b.XMax,b.YMin-20,1040-b.YMax),'nearest_VESA_mm':nearest['PF_VESAEnvelope'],'nearest_strap_mm':min(v for k,v in nearest.items() if k.startswith('PF_CommercialStrap')),'nearest_fastener_mm':min(v for k,v in nearest.items() if k.startswith('PF_StrapScrew')),'nearest_insert':'No selected playfield insert positions; outside entire modeled VESA load reserve','removed_volume_mm3':removed.Volume,'mass_removed_kg_at650':removed.Volume*650/1e9,'nearest_other_opening_mm':min((local.distToShape(q)[0] for k,q in cuts.items() if k!=n),default=None)})
new['PF_BasePlywood']=base;data['openings']=openrows
ck('PLAYFIELD_BASE_HORN_ABSENT rectangular outside contour',diff(inv(base).common(box(50,20,-14,500,650,18)),box(50,20,-14,500,650,18))<1e-5)
ck('M025 one valid 18mm stock solid',base.isValid() and len(base.Solids)==1 and abs(inv(base).BoundBox.ZLength-18)<1e-5)
ck('VESA and all strap/dowel load material preserved',all(world.distToShape(s)[0]>15 for world in [tf(q) for q in cuts.values()] for s in features.values()))
# Generic connector insertion through new rear opening, below unselected TV back.
plug=box(277.5,770,-75,45,30,80);study['PF_GenericConnectorSweep']=tf(plug)
ck('generic connector withdrawal corridor through window',new['PF_BasePlywood'].common(tf(plug)).Volume<1e-5)
data['playfield_structural_screen']={'minimum_transverse_remaining_width_mm':320,'window_width_fraction_removed':.36,'continuous_side_band_mm':160,'main_window_to_VESA_local_mm':120,'main_window_to_rear_dowel_local_mm':144,'strain_slot_pair_between_slot_web_mm':28,'added_adjustment_mm':0,'VESA_load_zone_unchanged':True,'certification':False,'remaining_hold':'Chosen display port location, VESA adapter/fastener pattern and full-load stiffness/strap qualification. Window is not universal port access.'}
# Agent-authored backbox proposal is integrated only after its explicit gate.
bbp=O/'backbox-study/result.json'
if bbp.exists():
 br=json.loads(bbp.read_text());data['backbox_study']=br
 for n,path in br.get('promoted_breps',{}).items():
  s=Part.Shape();s.read(str(R/path));new[n]=s
wood={p['source_component'] for p in json.loads((R/'exports/generated/structural-v335/manufacturing-register.json').read_text())['parts']}
changed=[n for n in old if n in new and diff(old[n],new[n])>1e-4];added=[n for n in new if n not in old];removed=[n for n in old if n not in new]
# Reference button bodies intentionally enter their matching reference side bores.
coll=[]
for n in changed:
 if n not in wood:continue
 for k,s in phys.items():
  if k==n or k.startswith(('Leaf','Button')):continue
  if n in ['SIDE_L','SIDE_R'] and k in ['SIDE_L','SIDE_R']:continue
  if not new[n].BoundBox.intersect(new[k].BoundBox):continue
  before=old[n].common(old[k]).Volume;after=new[n].common(new[k]).Volume
  if after>before+1e-4:coll.append([n,k,before,after])
ck('no new positive-volume changed-wood interference',not coll,coll)
ck('all protected unrelated shapes exact',all(diff(s,new[n])<1e-5 for n,s in old.items() if n not in changed))
for label,ss in [('play',new),('study',study)]:
 d=A.newDocument('V336'+label)
 for n,s in ss.items():
  o=d.addObject('PartDesign::Feature',n);o.Shape=s;o.addProperty('App::PropertyString','GeometryAuthority');o.GeometryAuthority='config/monitor_support_v336.json' if n in changed or label=='study' else 'V33.5 unchanged: config/structural_simplification_v335.json'
 d.recompute();d.saveAs(str(O/(label+'.FCStd')));A.closeDocument(d.Name)
for n in changed+added:new[n].exportBrep(str(O/'brep'/(n+'.brep')))
for file,ss in [('changes-mesh', {n:new[n] for n in changed+added}),('study-mesh',study)]:
 (O/(file+'.json.gz')).write_bytes(gzip.compress(json.dumps({n:mesh(s) for n,s in ss.items()}).encode(),mtime=0))
data.update(changed=[{'name':n,'before_mm3':old[n].Volume,'after_mm3':new[n].Volume,'symmetric_difference_mm3':diff(old[n],new[n])} for n in changed],added=added,removed=removed,checks=checks,pass_=all(c['pass'] for c in checks),release=False,source_sha256=hashlib.sha256((R/C['source']).read_bytes()).hexdigest(),clean_source_sha256=hashlib.sha256((R/op['clean_source']).read_bytes()).hexdigest());data['pass']=data.pop('pass_');(O/'geometry-validation.json').write_text(json.dumps(data,indent=2)+'\n');print('V336_GEOMETRY_DONE',data['pass'],len(checks),flush=True)
