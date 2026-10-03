"""Read-only CURRENT closed support audit. No rest geometry or load certification.
CERN-OHL-S-2.0. A collision-free PLAY pose does not establish static support.
"""
import FreeCAD as A,Part,sys,json,math,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,pf_names,actual,PF,V
C=json.loads((R/'config/playfield_rest_v3362.json').read_text());O=R/C['output'];p=O/'play.FCStd';h=hashlib.sha256(p.read_bytes()).hexdigest();ss=load(p);base=ss['PF_BasePlywood'];moving=pf_names(ss)
alpha=math.radians(json.loads((R/'exports/generated/notch-floor-fans-v32/validation.json').read_text())['review']['closed_slope_deg'])
report={'status':'CLOSED_POSITION_SUPPORT_BLOCKED','audit_completed':False,'closed_position_support_valid':False,'manufacturing_release':False,'source':str(p.relative_to(R)),'sha256':h,'pivot_xyz_mm':list(PF),'moving':moving,'parts':{},'contacts':[],'small_downward_rotation':[],'checks':[],
 'scope':'Exact B-rep contacts and small downward rotation. Geometry audit only; no stiffness/friction/load proof. No front rest or retention hardware has been invented.'}
def bb(s):b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def com(s):return sum((q.CenterOfMass*q.Volume for q in s.Solids),V())/sum(q.Volume for q in s.Solids)
for n in ['PF_BasePlywood','PF_WoodDowel','PF_OpenCradleL','PF_OpenCradleR','CROSS_1','CROSS_2','CROSS_3','FRONT','SIDE_L','SIDE_R']:
 s=ss[n];d,pts,info=base.distToShape(s);r={'bbox_mm':bb(s),'center_of_volume_mm':list(com(s)),'volume_mm3':s.Volume,'base_distance_mm':d,'witness_xyz_mm':[[list(a),list(b)] for a,b in pts[:2]],'penetration_mm3':0 if n=='PF_BasePlywood' else base.common(s).Volume}
 if n.startswith('CROSS_'):
  y=(s.BoundBox.YMin+s.BoundBox.YMax)/2
  base_section=base.common(Part.makeLine(V(300,y,0),V(300,y,1000)));cross_section=s.common(Part.makeLine(V(300,y,0),V(300,y,1000)))
  r.update(section_y_mm=y,base_underside_z_mm=base_section.BoundBox.ZMin,crossmember_top_z_mm=cross_section.BoundBox.ZMax,same_Y_vertical_gap_mm=base_section.BoundBox.ZMin-cross_section.BoundBox.ZMax,normal_gap_mm=d)
 report['parts'][n]=r
actuals=actual(ss);fixed={n:s for n,s in actuals.items() if n not in moving}
for n in moving:
 if n not in actuals:continue
 s=actuals[n]
 for k,t in fixed.items():
  b=s.BoundBox;c=t.BoundBox;lb=math.sqrt(sum(max(0,getattr(b,a+'Min')-getattr(c,a+'Max'),getattr(c,a+'Min')-getattr(b,a+'Max'))**2 for a in 'XYZ'))
  if lb>.05:continue
  d,pts,info=s.distToShape(t)
  if d<.05:report['contacts'].append({'moving':n,'fixed':k,'distance_mm':d,'penetration_mm3':s.common(t).Volume,'witness_xyz_mm':[[list(a),list(b)] for a,b in pts[:1]]})
for angle in [.1,.5,1]:
 hits=[]
 for n in moving:
  if n not in actuals:continue
  s=actuals[n].copy();s.rotate(V(*PF),V(1,0,0),angle)
  for k,t in fixed.items():
   if s.BoundBox.intersect(t.BoundBox):
    v=s.common(t).Volume
    if v>1e-4:hits.append({'moving':n,'fixed':k,'penetration_mm3':v})
 report['small_downward_rotation'].append({'angle_deg':angle,'hits':hits,'meaning':'Diagnostic downward motion; incidental contact is NOT a designed support.'})
base_mass=base.Volume*650/1e9
report['wood_base_alone']={'density_kg_m3':650,'estimated_mass_kg':base_mass,'horizontal_COM_distance_forward_of_axis_mm':PF[1]-com(base).y,'gravity_moment_about_rear_axis_Nm':base_mass*9.80665*(PF[1]-com(base).y)/1000,'note':'Illustrates nonzero forward gravity moment even before display/payload. No allowable load or friction capacity claimed.'}
report['history']=[{'source':'exports/generated/cabinet-v32/build_v32.py:109','finding':'T1–T3 tops matched the old monitor-rail underside at localZ−36.'},{'source':'tools/wood_dowel_pivot_v32_entry.py:32','finding':'Replacement plywood underside is localZ−14;22mm normal gap remains.'},{'source':'config/playfield_mechanics_v18.json:125','finding':'Historical two front pads/two latches are not present in CURRENT; no historical dimensions promoted.'}]
expected={('PF_WoodDowel','PF_OpenCradleL'),('PF_WoodDowel','PF_OpenCradleR')}
report['checks']=[{'name':'only rear dowel seats contact fixed assembly','pass':{(r['moving'],r['fixed']) for r in report['contacts']}==expected}, {'name':'all three crossmember normal gaps22mm','pass':all(abs(report['parts'][n]['normal_gap_mm']-22)<1e-6 for n in ['CROSS_1','CROSS_2','CROSS_3'])}, {'name':'sameYverticalgaps equal22/cos(slope)','pass':all(abs(report['parts'][n]['same_Y_vertical_gap_mm']-22/math.cos(alpha))<1e-6 for n in ['CROSS_1','CROSS_2','CROSS_3'])}, {'name':'free0.1degree downward rotation is not stopped','pass':not report['small_downward_rotation'][0]['hits']}, {'name':'basealone forward gravity moment positive','pass':report['wood_base_alone']['gravity_moment_about_rear_axis_Nm']>0}, {'name':'native input unchanged','pass':hashlib.sha256(p.read_bytes()).hexdigest()==h}]
report['audit_completed']=all(r['pass'] for r in report['checks']);(O/'closed-support-audit.json').write_text(json.dumps(report,indent=2)+'\n');print('V3362_CLOSED_SUPPORT_AUDIT',report['audit_completed'],report['status']);assert report['audit_completed']
