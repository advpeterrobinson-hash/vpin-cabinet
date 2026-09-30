"""Read-only lockdown axis audit. CERN-OHL-S-2.0. No adopted receiver shape or holes."""
import json,hashlib
from pathlib import Path
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/lockdown-interface-v32';O.mkdir(parents=True,exist_ok=True);cp=R/'config/lockdown_interface_v32.json';c=json.loads(cp.read_text());rp=R/c['source_report'];r=json.loads(rp.read_text());sp=R/r['saved_proposals']['closed']['path'];posep=R/'exports/generated/side-panel-v32/shelf-service-pose-screen.json';pose=json.loads(posep.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(sp)==r['saved_proposals']['closed']['sha256'] and all(x['pass'] for x in r['checks']);inputs={str(p.relative_to(R)):sha(p) for p in [cp,rp,sp,posep,Path(__file__).resolve()]};d=A.openDocument(str(sp));d.recompute();scene={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')};checks=[]
def check(n,v):checks.append({'check':n,'pass':bool(v)})
z=c['adopted_candidate_row_z_mm'];axes=[];closed=[];opened=[];raised={n:s.copy() for n,s in scene.items() if n not in ['CandidateGlass']}
for n in ['PLAYFIELD_ENVELOPE','MONITOR_RAIL_L','MONITOR_RAIL_R','MONITOR_BRIDGE']:raised[n].rotate(A.Vector(*pose['pivot_xyz_mm']),A.Vector(1,0,0),-100)
for x in c['front_view_axes_x_mm']:
 tool=Part.makeCylinder(c['tool_radius_mm_candidate'],c['tool_length_mm_candidate'],A.Vector(x,c['tool_start_y_mm_candidate'],z),A.Vector(0,1,0));axes.append({'x_mm':x,'z_mm':z,'new_hole':x!=300})
 for label,obs,out in [('closed',scene,closed),('raised',raised,opened)]:
  for n,s in obs.items():
   if s.BoundBox.intersect(tool.BoundBox):
    v=s.common(tool).Volume
    if v>.01:out.append({'axis_x_mm':x,'obstacle':n,'mm3':v})
check('preserve upper shared coin door bore',not scene['FRONT'].isInside(A.Vector(300,9,z),1e-6,True))
check('outer reference axes lie in existing front material',all(scene['FRONT'].isInside(A.Vector(x,9,z),1e-6,True) for x in [68.225,477.8]))
check('converted reference agrees within0.03mm with existing center datum',abs(z-c['source_row_z_mm'])<.03)
check('source bore discrepancy recorded not silently selected',c['hole_diameter_adopted'] is None and c['source_image_diameter_mm']!=c['source_prose_diameter_mm'])
check('candidate tool corridors clear with display raised100deg',not opened)
check('negative closed display obstructs candidate tool corridors',any(x['obstacle']=='PLAYFIELD_ENVELOPE' for x in closed))
check('source geometry and input bytes unchanged',all(sha(R/p)==h for p,h in inputs.items()))
report={'manufacturing_ready':False,'source_hashes':inputs,'config':c,'checks':checks,'axes':axes,'closed_tool_conflicts':closed,'raised_tool_conflicts':opened,'unverified':['Actual receiver envelope, lever/tongues and nut/fastener stack','Complete hand/tool approach from coin door and real raised-playfield support','Selected mounting diameter and height against completed glass/siderails/bar','No receiver solid added and no permanent wood cut']};(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');assert all(x['pass'] for x in checks),[x for x in checks if not x['pass']];print('LOCKDOWN_INTERFACE_PASS',len(checks),'checks; reference axes only, no cuts');A.closeDocument(d.Name)
