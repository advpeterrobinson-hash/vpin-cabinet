"""Reopen cassette CAD and enforce the accepted V32 boundary. CERN-OHL-S-2.0."""
from pathlib import Path
import FreeCAD as A,Part,json,hashlib,subprocess,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from validate_wood_dowel_pivot_v32 import validate_visible_mechanism
O=R/'exports/generated/matrix-cassette-v32';r=json.loads((O/'validation.json').read_text());b=json.loads((O/'mesh.json').read_text());src=R/'exports/generated/notch-floor-fans-v32';checks=[]
def check(name,ok):
 assert ok,name
 checks.append({'check':name,'pass':True});print('REGRESSION',name,flush=True)
def same(a,b):return a.cut(b).Volume+b.cut(a).Volume<1e-5
base=A.openDocument(str(src/'play.FCStd'));old={o.Name:o.Shape.copy() for o in base.Objects if hasattr(o,'Shape')}
for state,path in r['saved_poses'].items():
 d=A.openDocument(str(O/path));d.recompute();objs={o.Name:o for o in d.Objects if hasattr(o,'Shape')}
 check(state+' valid saved/recomputed solids',all(o.Shape.isValid() and len(o.Shape.Solids)==1 and 'Invalid' not in o.State for o in objs.values()))
 if state not in ('EXPLODED','MATRIX EXPLODED'):
  check(state+' explicit saved prerequisites',d.MatrixPrerequisites==', '.join(r['review']['matrix_cassette']['prerequisites'][state]))
 if state in ('SERVICE','PLAYFIELD SERVICE','LIFT-OUT','BACKBOX FOLD','MATRIX REMOVED'):
  check(state+' cassette and glass absent only with declared removal',d.getObject('MatrixCarrier') is None and d.getObject('CandidateGlass') is None and 'MATRIX_REMOVED' in d.MatrixPrerequisites)
 if state=='PLAY':
  for n,s in old.items():
   if n!='BACKBOX_BASE':check(n+' accepted geometry unchanged',same(s,objs[n].Shape))
  after=objs['BACKBOX_BASE'].Shape;expected=old['BACKBOX_BASE'].copy()
  for x in (45,555):
   for y in (1140,1180):expected=expected.cut(Part.makeCylinder(1.5,12,A.Vector(x,y,578.9)))
  check('rear shelf only four scoped blind matrix mounting pilots',same(expected,after))
  check('accepted live pivot expression retained',bool(objs['PF_WoodDowel'].ExpressionEngine))
 A.closeDocument(d.Name)
for n in ('PF_BasePlywood','LeafButton_primary_L','FloorIntakeFanL','RemovableIntakeFilterL','FAN_230','PF_WoodDowel','PF_OpenCradleL','SHELF_2','PC_BASE'):
 altered=old[n].copy();altered.translate(A.Vector(.1,0,0));check('negative geometry mutation rejected: '+n,not same(old[n],altered))
validate_visible_mechanism(b)
for state in ('SERVICE','PLAYFIELD SERVICE','LIFT-OUT','BACKBOX FOLD'):
 saved=b['review']['matrix_cassette']['prerequisites'][state];b['review']['matrix_cassette']['prerequisites'][state]=['GLASS_REMOVED']
 try:validate_visible_mechanism(b);raise RuntimeError('Silent removal accepted')
 except AssertionError:pass
 b['review']['matrix_cassette']['prerequisites'][state]=saved
check('negative state metadata controls reject undeclared matrix removal',True)
for p,h in r['source_hashes'].items():
 check('source bytes preserved: '+p,hashlib.sha256((R/p).read_bytes()).hexdigest()==h)
 committed=subprocess.check_output(['git','show',r['source_head']+':'+p],cwd=R)
 check('source matches accepted HEAD: '+p,hashlib.sha256(committed).hexdigest()==h)
m=r['review']['matrix_cassette']
check('route sampled at <= 0.25 degree and 1 mm',len(m['route']['samples'])==275 and not any(s['hits'] for s in m['route']['samples']))
check('all five initial lift controls fail',len(m['priority_a'])==5 and all(not t['clear'] for t in m['priority_a']))
check('fold blocker retained honestly',m['backbox_fold_clear'] is False and bool(m['baseline_fold_conflicts']))
check('viewer metadata/mesh provenance matches',hashlib.sha256((O/'mesh.json').read_bytes()).hexdigest()==r['mesh_sha256'])
# Minimum forward translation is derived from the rotated carrier's actual rear bound.
forward_doc=A.openDocument(str(O/'matrix-forward.FCStd'))
ps={o.Name:o.Shape.copy() for o in forward_doc.Objects if hasattr(o,'Shape') and (o.Name.startswith('Matrix') or o.Name in ('MX_MovingConnectorReserve','MX_CableLoopReserve'))}
obstacles={o.Name:o.Shape.copy() for o in forward_doc.Objects if hasattr(o,'Shape') and o.Name not in ps and o.Name!='CandidateGlass' and (o.Name.startswith('MX_') or not any(t in o.Name for t in ('Reserve','RESERVED','CandidatePayload','ServiceEnvelope')))}
# Recheck the complete playfield sweep against all physical/current modeled obstacles,
# including the reserved backbox volume and stationary connector, after explicit removal.
pf_names=[n for n in old if n.startswith('PF_') and n not in ('PF_OpenCradleL','PF_OpenCradleR','PF_BackboxCheckEnvelope') and not n.startswith('PF_SupportMountScrew')]+['PLAYFIELD_ENVELOPE']
fixed={n:t for n,t in obstacles.items() if n not in pf_names}
full_motion=[]
for state,values in [('SERVICE',range(51)),('LIFT-OUT',range(49))]:
 hits=[]
 for value in values:
  moving={n:old[n].copy() for n in pf_names}
  for q in moving.values():
   if state=='SERVICE':q.rotate(A.Vector(*r['review']['pivot_xyz_mm']),A.Vector(1,0,0),-value)
   else:q.translate(A.Vector(0,0,value))
  hh=sorted({n for q in moving.values() for n,t in fixed.items() if q.BoundBox.intersect(t.BoundBox) and q.common(t).Volume>.001})
  if hh:hits.append({'step':value,'hits':hh})
 full_motion.append({'state':state,'hits':hits,'clear':not hits})
check('full current modeled SERVICE and LIFT-OUT clear with matrix and glass removed',all(t['clear'] for t in full_motion))
(O/'after-removal-motion.json').write_text(json.dumps({'prerequisites':['GLASS_REMOVED','MATRIX_REMOVED'],'checks':full_motion,'service_increment_deg':1,'lift_increment_mm':1,'backbox_fold_clear':False},indent=2)+'\n')
rear=max(s.BoundBox.YMax for s in ps.values())+68;limit=old['PF_BackboxCheckEnvelope'].BoundBox.YMin;threshold=rear-limit
limits=[]
for travel in (65,66,67,68):
 hits=[]
 for lift in range(101):
  moved={n:s.copy() for n,s in ps.items()}
  for s in moved.values():s.translate(A.Vector(0,68-travel,lift))
  hits.extend(n for s in moved.values() for n,t in obstacles.items() if s.BoundBox.intersect(t.BoundBox) and s.common(t).Volume>.001)
 limits.append({'forward_mm':travel,'hits':sorted(set(hits)),'rear_plane_clearance_mm':travel-threshold})
check('negative insufficient forward travel fails',bool(limits[0]['hits']))
check('67 mm first integer travel with 1 mm rear-plane margin clears final lift',not limits[2]['hits'] and limits[2]['rear_plane_clearance_mm']>=1 and limits[1]['rear_plane_clearance_mm']<1)
check('selected 68 mm gives 2 mm rear-plane allowance',not limits[3]['hits'] and limits[3]['rear_plane_clearance_mm']>=2)
(O/'removal-route-limits.json').write_text(json.dumps({'geometric_forward_threshold_mm':threshold,'minimum_integer_travel_for_1mm_rear_plane_margin':67,'selected_forward_mm':68,'selected_reason':'2 mm allowance ahead of the backbox rearward obstruction; 1 mm route review target','vertical_extraction_tests':limits,'manufacturing_ready':False},indent=2)+'\n')
A.closeDocument(forward_doc.Name)

(O/'regression-validation.json').write_text(json.dumps({'checks':checks,'all_pass':True,'fold_clear':False,'manufacturing_ready':False},indent=2)+'\n');print('MATRIX_CASSETTE_REGRESSION_PASS',len(checks),flush=True)
