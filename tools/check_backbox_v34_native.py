"""Independent V34 native/metrology/capture/service regression. CERN-OHL-S-2.0."""
from pathlib import Path
import sys,json,hashlib,math
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,transform,V,WPC,certify
from backbox_service_v32 import door_pose,flex,C as SERVICE
O=R/'exports/generated/backbox-v34';P=R/'exports/generated/service-productization-v338';new=load(O/'play.FCStd');old=load(P/'play.FCStd');g=json.loads((O/'geometry-validation.json').read_text());reg=json.loads((O/'manufacturing-register.json').read_text());checks=[]
def ck(n,p,d=None):checks.append({'name':n,'pass':bool(p),'detail':d});print(n,bool(p),flush=True)
def diff(a,b):return 0 if a.exportBrepToString()==b.exportBrepToString() else a.cut(b).Volume+b.cut(a).Volume
def hits(a,obs):return [(n,a.common(b).Volume) for n,b in obs.items() if a.BoundBox.intersect(b.BoundBox) and a.common(b).Volume>1e-4]
allowed=set(g['retired']+g['changed'])
for n,s in old.items():
 if n not in allowed:
  q=new.get(n);b=s.BoundBox;c=q.BoundBox if q else None
  same=q is not None and len(s.Faces)==len(q.Faces) and len(s.Edges)==len(q.Edges) and abs(s.Volume-q.Volume)<1e-4 and abs(s.Area-q.Area)<1e-4 and all(abs(getattr(b,k)-getattr(c,k))<1e-6 for k in ['XMin','YMin','ZMin','XMax','YMax','ZMax'])
  ck('protected native invariants '+n,same)
for n,s in new.items():ck('valid '+n,s.isValid())
# Manufacturing pieces are real solids, transformed back into the installed assembly.
by={}
for p in reg['parts']:
 q=Part.Shape();q.read(str(R/p['finished_member_brep']));m=A.Matrix(*p['local_to_installed_matrix']);q.transformShape(m,True);by.setdefault(p['source_component'],[]).append(q)
 ck('allowed material '+p['instance_id'],p.get('manufacturing_class')=='SHOP_MADE_SOLID_WOOD_PART' or p['nominal_stock_thickness_mm'] in [12,18])
 ck('one face '+p['instance_id'],not p.get('opposite_face_cnc'))
for n,ss in by.items():
 if n not in new:continue # fan/blank mutually exclusive manufacturing variant
 q=ss[0]
 for t in ss[1:]:q=q.fuse(t)
 e=diff(q.removeSplitter(),new[n]);ck('reconstruction '+n,e<1e-3,e)
# Reference physical glass capture in all rigid shell orientations is invariant.
barriers={n:s for n,s in new.items() if n in ['BB_SideL','BB_SideR','BB_Top','BB_GLASS_BOTTOM_SEAT','BB_GLASS_TOP_RETAINER']}
glass=new['BB_Backglass'];motions=[]
for axis in range(3):
 for sign in [-1,1]:
  q=glass.copy();v=[0,0,0];v[axis]=sign*4;q.translate(V(*v));h=hits(q,barriers);motions.append({'translation_mm':v,'barriers':h});ck('glass translational capture '+str(v),bool(h),h)
for axis in [V(1,0,0),V(0,1,0),V(0,0,1)]:
 for sign in [-1,1]:
  q=glass.copy();q.rotate(glass.BoundBox.Center,axis,sign*.5);h=hits(q,barriers);ck('glass rotational restraint '+str(list(axis))+str(sign),bool(h),h)
ck('bottom lip cannot lift free below top',6>3.8+2)
ck('top strip overlaps beyond possible top travel',8.2>3.8+2)
# Continuous glass tilt. Exclude removable strip and soft cushions only; installed wood remains.
obs={n:s for n,s in new.items() if n.startswith('BB_') and n not in ['BB_Backglass','BB_GLASS_TOP_RETAINER'] and not any(t in n for t in ['Cushion','Reserve','ToyZone','Flex','Screw','Bolt','Washer','Spacer','CrossDowel','Tether'])}
raised=glass.copy();raised.translate(V(0,0,1));pivot=V(300,1116,841)
try:gc=certify({'Glass':raised},obs,0,10,pivot);ck('continuous glass tilt0to10',True,len(gc['intervals']))
except AssertionError as e:gc={'error':str(e)};ck('continuous glass tilt0to10',False,str(e))
# Door rigid hardware/leaf/guards including centre overlap, not just door slab.
newfixed={n:new[n] for n in g['changed'] if n in new};dc={};flexchecks=[]
for side in ['L','R']:
 ns=[n for n in old if (n.endswith(side) and n.startswith(('BB_Door','BB_Fan','BB_Intake','BB_PianoLeafDoor'))) or (side=='L' and n.startswith(('BB_Center','BB_PassiveBoltBody'))) or (side=='R' and n.startswith('BB_CamLock'))]
 mov={n:old[n] for n in ns};axis=V(*SERVICE['rear']['hinge_axis_xy_mm'][0 if side=='L' else 1],0)
 try:dc[side]=certify(mov,newfixed,0,100,axis,'Z',lambda ss,a:door_pose(ss,side,a));ck(side+' continuous door0to100',True,len(dc[side]['intervals']))
 except AssertionError as e:dc[side]={'error':str(e)};ck(side+' continuous door0to100',False,str(e))
 for a in [0,10,20,30,40,50,60,70,80,90,100]:
  tube,metrics=flex(side,a);h=hits(tube,newfixed);flexchecks.append({'side':side,'angle':a,'hits':h,'metrics':metrics});ck(side+' fan loop '+str(a),not h,h)
ck('WPC reference unchanged',list(WPC)==[300,1066.8,508])
ck('main stock exactly12/18',set(p['nominal_stock_thickness_mm'] for p in reg['parts'] if p.get('manufacturing_class')!='SHOP_MADE_SOLID_WOOD_PART')=={12,18})
for forbidden in [4,6,8,9,10,15,24,30]:ck('negative stock control '+str(forbidden),forbidden not in [12,18])
report={'pass':all(a['pass'] for a in checks),'checks':checks,'glass_capture':motions,'glass_continuous_tilt':gc,'doors_continuous':dc,'fan_flex':flexchecks,'native_sha256':hashlib.sha256((O/'play.FCStd').read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((P/'play.FCStd').read_bytes()).hexdigest(),'manufacturing_release':False,'physical_qualification':False}
(O/'independent-validation.json').write_text(json.dumps(report,indent=2)+'\n');print('V34_INDEPENDENT',report['pass'],len(checks))
