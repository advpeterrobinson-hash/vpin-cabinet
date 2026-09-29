"""Owner-directed simple top-release shelf study. CERN-OHL-S-2.0."""
import hashlib,json
from pathlib import Path
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/side-panel-v32';O.mkdir(parents=True,exist_ok=True)
cp=R/'config/simple_shelves_v32.json';fp=R/'config/front_panel_v32.json';c=json.loads(cp.read_text());f=json.loads(fp.read_text())
basepath=R/'exports/generated/cabinet-v32/vpin-central-v32.FCStd';frontpath=R/'exports/generated/front-panel-v32/coin-upgrade-closed.FCStd'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
inputs=[cp,fp,basepath,frontpath,Path(__file__).resolve()];hashes={str(p.relative_to(R)):sha(p) for p in inputs}
base=A.openDocument(str(basepath));front=A.openDocument(str(frontpath));base.recompute();front.recompute()
scene={o.Name:o.Shape.copy() for o in front.Objects if hasattr(o,'Shape')};checks=[];axes=[];hardware={}
def check(n,v):checks.append({'check':n,'pass':bool(v)})
def box(x,y,z,dx,dy,dz):return Part.makeBox(dx,dy,dz,A.Vector(x,y,z))
def cyl(x,y,z,r,h):return Part.makeCylinder(r,h,A.Vector(x,y,z))
def hits(moving,obstacles):
 out=[]
 for n,s in moving.items():
  for k,t in obstacles.items():
   if s.BoundBox.intersect(t.BoundBox):
    v=s.common(t).Volume
    if v>c['collision_threshold_mm3']:out.append({'moving':n,'obstacle':k,'mm3':v})
 return out
def sweep_box(s,v):
 b=s.BoundBox
 return box(b.XMin+min(0,v.x),b.YMin+min(0,v.y),b.ZMin+min(0,v.z),b.XLength+abs(v.x),b.YLength+abs(v.y),b.ZLength+abs(v.z))
for o in base.Objects:
 if hasattr(o,'Shape') and o.Name not in ('FRONT','PLUNGER_RESERVED'):
  check(o.Name+' front-study shape unchanged',scene[o.Name].cut(o.Shape).Volume+o.Shape.cut(scene[o.Name]).Volume<1e-4)
scene['PLUNGER_RESERVED']=box(*f['plunger_internal_box'])
for j,b in enumerate(f['buttons'],1):scene[f'CandidateFrontButton{j}']=Part.makeCylinder(f['button_internal_radius'],f['button_internal_depth_with_cable'],A.Vector(b['x'],18,b['z']),A.Vector(0,1,0))
sb=c['side_buttons']
for side,x,d in [('L',18,1),('R',582,-1)]:
 for y in sb['y_mm']:scene[f'CandidateSideButton{side}_{y}']=Part.makeCylinder(sb['radius_mm'],sb['depth_mm'],A.Vector(x,y,sb['z_mm']),A.Vector(d,0,0))
original={n:s.copy() for n,s in scene.items()}
for spec in c['shelves']:
 i=spec['number'];name=f'SHELF_{i}';b=scene[name].BoundBox;dy=spec['y_mm']-b.YMin
 scene[name].translate(A.Vector(0,dy,0));b=scene[name].BoundBox
 payload=name+'_CandidatePayload';scene[payload]=box(b.XMin,b.YMin,b.ZMax,b.XLength,b.YLength,c['equipment_height_mm'])
 for side,x in zip(('L','R'),c['bolt_x_mm']):
  sn=f'SHELF_SUPPORT_{i}{side}';old=original[sn].BoundBox;xmin=18 if side=='L' else 582-c['support_width_mm']
  support=box(xmin,spec['y_mm'],old.ZMin,c['support_width_mm'],old.YLength,old.ZLength)
  for j,offset in enumerate(spec['bolt_offsets_y_mm'],1):
   y=spec['y_mm']+offset;prefix=f'SimpleShelfBolt{i}{side}{j}';r=c['bore_diameter_mm']/2
   scene[name]=scene[name].cut(cyl(x,y,b.ZMin-1,r,b.ZLength+2))
   support=support.cut(cyl(x,y,old.ZMax-c['insert_pocket_depth_mm'],c['insert_bore_diameter_mm']/2,c['insert_pocket_depth_mm']+1))
   support=support.cut(cyl(x,y,old.ZMax-c['shaft_tip_pocket_depth_mm'],r,c['shaft_tip_pocket_depth_mm']+1))
   insert=cyl(x,y,old.ZMax-c['insert_length_mm'],c['insert_diameter_mm']/2,c['insert_length_mm']).cut(cyl(x,y,old.ZMax-c['insert_length_mm']-1,c['shaft_diameter_mm']/2,c['insert_length_mm']+2))
   hz=b.ZMax+c['washer_thickness_mm'];tip=hz-c['shaft_length_mm']
   bolt=cyl(x,y,tip,c['shaft_diameter_mm']/2,c['shaft_length_mm']).fuse(cyl(x,y,hz,c['head_diameter_mm']/2,c['head_height_mm'])).removeSplitter()
   washer=cyl(x,y,b.ZMax,c['washer_diameter_mm']/2,c['washer_thickness_mm']).cut(cyl(x,y,b.ZMax-1,r,c['washer_thickness_mm']+2))
   hardware[prefix]=bolt;hardware[prefix+'Washer']=washer;hardware[prefix+'Insert']=insert
   scene[payload]=scene[payload].cut(cyl(x,y,b.ZMax-1,c['access_well_radius_mm'],c['equipment_height_mm']+2))
   axes.append({'shelf':name,'support':sn,'bolt':prefix,'washer':prefix+'Washer','insert':prefix+'Insert','xyz_mm':[x,y,b.ZMax],'head_top_z_mm':hz+c['head_height_mm']})
  scene[sn]=support
scene.update(hardware)
shelf_gaps=[]
for i in (1,2):
 gap=scene[f'SHELF_{i+1}'].BoundBox.YMin-scene[f'SHELF_{i}'].BoundBox.YMax
 shelf_gaps.append(gap)
 check(f'S{i}-S{i+1} minimum longitudinal gap',gap>=c['minimum_shelf_gap_y_mm'])
check('reject previous 70 mm rear gap',70<c['minimum_shelf_gap_y_mm'])
check('exactly four top screws per shelf',all(sum(a['shelf']==f'SHELF_{i}' for a in axes)==4 for i in (1,2,3)))
check('no nut covers or side-anchor hardware',not any('NutCover' in n or 'SupportAnchor' in n for n in scene))
check('all candidate shapes valid',all(s.isValid() and len(s.Solids)==1 for s in scene.values()))
for n in ('SIDE_L','SIDE_R','FRONT','REAR','FLOOR','CROSS_1','CROSS_2','CROSS_3'):
 check(n+' unchanged from front study',scene[n].cut(original[n]).Volume+original[n].cut(scene[n]).Volume<1e-4)
# Test changed boards/supports and hardware against the entire installed scene;
# payload envelopes intentionally contain their mounted equipment.
changed=[f'SHELF_{i}' for i in (1,2,3)]+[f'SHELF_SUPPORT_{i}{s}' for i in (1,2,3) for s in ('L','R')]
installed=[]
for n in changed+list(hardware):
 installed+=hits({n:scene[n]},{k:s for k,s in scene.items() if k!=n and not k.endswith('_CandidatePayload')})
check('changed physical parts have no installed overlaps',not installed)
# The display parking position is not invented. Only its four moving shapes are
# excluded; crossmembers, guides, backbox base and modeled payloads stay present.
obs={n:s for n,s in scene.items() if n not in c['playfield_assembly']}
ceiling=max(s.BoundBox.ZMax for s in obs.values())+c['exit_margin_mm'];access=[]
for a in axes:
 x,y,z=a['xyz_mm'];excluding=(a['bolt'],a['washer']);neighbors={n:s for n,s in obs.items() if n not in excluding}
 tool=cyl(x,y,a['head_top_z_mm'],c['tool_radius_mm'],ceiling-a['head_top_z_mm'])
 th=hits({'full_top_tool_column':tool},neighbors)
 travel=c['withdrawal_mm'];hz=z+c['washer_thickness_mm']
 screw=cyl(x,y,hz-c['shaft_length_mm'],c['shaft_diameter_mm']/2,c['shaft_length_mm']+travel).fuse(cyl(x,y,hz,c['head_diameter_mm']/2,c['head_height_mm']+travel))
 washer=cyl(x,y,z,c['washer_diameter_mm']/2,c['washer_thickness_mm']+travel).cut(cyl(x,y,z-1,c['bore_diameter_mm']/2,c['washer_thickness_mm']+travel+2))
 wh=hits({'screw':screw,'washer':washer},neighbors)
 check(a['bolt']+' continuous top column clear',not th);check(a['bolt']+' upward withdrawal clear',not wh)
 access.append({'bolt':a['bolt'],'top_column_conflicts':th,'withdrawal_conflicts':wh})
routes=[]
for spec in c['shelves']:
 name=f'SHELF_{spec["number"]}';moving_names=[name,name+'_CandidatePayload']+(['AUDIO_STARTECH'] if spec['number']==1 else [])
 removed=[n for a in axes if a['shelf']==name for n in (a['bolt'],a['washer'])]
 neighbors={n:s for n,s in obs.items() if n not in moving_names+removed};moving={n:scene[n].copy() for n in moving_names}
 legs=[A.Vector(0,spec['stage_y_mm']-scene[name].BoundBox.YMin,0),A.Vector(0,0,ceiling-scene[name].BoundBox.ZMin)];conflicts=[]
 for v in legs:
  conflicts+=hits({n:sweep_box(s,v) for n,s in moving.items()},neighbors)
  for s in moving.values():s.translate(v)
 check(name+' loaded extraction with all crossmembers retained',not conflicts)
 routes.append({'shelf':name,'moving':moving_names,'removed_only':removed,'translations_mm':[[v.x,v.y,v.z] for v in legs],'conflicts':conflicts})
# Regression controls: old full-height access would hit T2 and BBBase.
controls=[]
for name,x,y,z,obstacle in [('old S2 rear screw',48,700,197,'CROSS_2'),('old S3 rear screw',48,1180,257,'BACKBOX_BASE'),('S2 rear at Y725',48,725,197,'CROSS_BRACKET_2L')]:
 h=hits({'tool':cyl(x,y,z,c['tool_radius_mm'],ceiling-z)},{obstacle:original[obstacle]})
 check('reject '+name,bool(h));controls.append({'case':name,'conflicts':h})
a=axes[0];x,y,z=a['xyz_mm'];b=scene[a['shelf']].BoundBox
check('reject equipment filling screw access',bool(hits({'tool':cyl(x,y,a['head_top_z_mm'],c['tool_radius_mm'],ceiling-a['head_top_z_mm'])},{'filled_payload':box(b.XMin,b.YMin,b.ZMax,b.XLength,b.YLength,c['equipment_height_mm'])})))
check('source and inputs unchanged',all(sha(R/n)==h for n,h in hashes.items()))
proposal=A.newDocument('SimpleShelfTopReleaseV32');proposal.Comment='CERN-OHL-S-2.0; Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet; candidate top-release study, not manufacturing'
for n,s in scene.items():
 o=proposal.addObject('PartDesign::Feature',n);o.Shape=s;o.addProperty('App::PropertyString','PartCode');o.PartCode=getattr(base.getObject(n),'PartCode','') if base.getObject(n) else '';o.Label=(o.PartCode or 'PROVISIONAL '+n)+' / simple top release'
proposal.recompute();path=O/'simple-shelves-proposal.FCStd';proposal.saveAs(str(path));A.closeDocument(proposal.Name)
proposal=A.openDocument(str(path));proposal.recompute();actual={o.Name:o.Shape for o in proposal.Objects if hasattr(o,'Shape')}
check('saved exact identity set',set(actual)==set(scene));check('saved valid solids',all(s.isValid() and len(s.Solids)==1 for s in actual.values()));check('saved exact shapes',all(actual[n].cut(s).Volume+s.cut(actual[n]).Volume<1e-4 for n,s in scene.items()))
# Render only one shelf assembly; explode for clarity in the renderer.
mesh=[]
for o in proposal.Objects:
 if o.Name in ('SHELF_1','SHELF_SUPPORT_1L','SHELF_SUPPORT_1R') or o.Name.startswith('SimpleShelfBolt1'):
  vertices,faces=o.Shape.tessellate(.5)
  mesh.append({'name':o.Name,'vertices':[[v.x,v.y,v.z] for v in vertices],'faces':faces})
(O/'simple-shelves-mesh.json').write_text(json.dumps(mesh)+'\n')
report={'status':c['status'],'manufacturing_ready':False,'source_hashes':hashes,'config':c,'checks':checks,'shelf_gaps_y_mm':shelf_gaps,'axes':axes,'access':access,'routes':routes,'negative_controls':controls,'installed_conflicts':installed,'saved_proposal':{'path':str(path.relative_to(R)),'sha256':sha(path),'solids':len(scene)},'unverified':['Actual raised playfield, hinge, captive props and harness occupancy','Fixed cleat attachment to side wall and load capacity','Selected screws and top inserts; stock/pilot/thread tolerances and physical proof','Whole hand/tool insertion and handling of populated shelves']}
(O/'simple-shelves-validation.json').write_text(json.dumps(report,indent=2)+'\n')
assert all(x['pass'] for x in checks),[x for x in checks if not x['pass']]
print('SIMPLE_SHELVES_PASS',len(checks),'checks; crossmembers retained; actual raised display unverified')
for d in (proposal,front,base):A.closeDocument(d.Name)
