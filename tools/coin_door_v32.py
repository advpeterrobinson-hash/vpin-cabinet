"""Outward coin-door study. Candidate envelopes never certify unselected hardware.
Original work: CERN-OHL-S-2.0. Coordinates X width, Y rearward, Z up.
"""
import json
from pathlib import Path
import FreeCAD as A
import Part
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'exports/generated/front-panel-v32'

def box(v):return Part.makeBox(*v[3:],A.Vector(*v[:3]))
def turn(shape,c,angle):
 s=shape.copy();s.rotate(A.Vector(*c['hinge_axis_mm']),A.Vector(0,0,1),-angle);return s
def overlaps(a,b):
 if not a.BoundBox.intersect(b.BoundBox):return False
 return a.common(b).Volume>.01

def definitions(cfg,upgrade):
 c=cfg['coin_door'];x,z,w,h=cfg['coin_opening'];m=c['frame_margin_mm'];depth=c['frame_depth_mm']
 shapes={'CoinFrame':(box([x-m,-depth,z-m,w+2*m,depth,h+2*m]).cut(box([x,-depth-1,z,w,depth+2,h])),'frame',False)}
 for p in c['components']:
  if p['configuration']=='BOTH' or upgrade:shapes[p['name']]=(box(p['box']),p['kind'],p['moves_with_door'])
 if upgrade:
  t=c['tray'];v=t['outer_box'];wall=t['wall_mm'];inner=[v[0]+wall,v[1]+wall,v[2]+wall,v[3]-2*wall,v[4]-2*wall,v[5]]
  shapes['CoinTray']=(box(v).cut(box(inner)),'tray',False)
  b=c['tray_supports']
  for i,x in enumerate(b['x_positions'],1):
   s=box([x,b['front_y'],b['anchor_z'],b['width_mm'],b['thickness_mm'],b['seat_z']-b['anchor_z']])
   s=s.fuse(box([x,b['front_y'],b['seat_z']-b['thickness_mm'],b['width_mm'],b['rear_y']-b['front_y'],b['thickness_mm']])).removeSplitter()
   shapes['TraySupport'+str(i)]=(s,'support',False)
 return shapes

def fixed_obstacles(doc,cfg):
 obs={o.Name:o.Shape for o in doc.Objects if hasattr(o,'Shape') and not o.Name.startswith('CoinStudy_') and o.Name!='PLUNGER_RESERVED'}
 for i,b in enumerate(cfg['buttons']):
  obs['ButtonFace'+str(i)]=Part.makeCylinder(b['face_diameter']/2,14,A.Vector(b['x'],-14,b['z']),A.Vector(0,1,0))
 for i,b in enumerate(cfg['buttons']):
  obs['ButtonBody'+str(i)]=Part.makeCylinder(cfg['button_internal_radius'],cfg['button_internal_depth_with_cable'],A.Vector(b['x'],18,b['z']),A.Vector(0,1,0))
 obs['PlungerBody']=box(cfg['plunger_internal_box'])
 obs['PlungerFace']=box([490,-45,250,60,45,60])
 obs['LockdownReserve']=box([18,-35,380,564,60,20.05])
 return obs

def build_case(source,cfg,name,upgrade,angle):
 doc=A.newDocument(name)
 for old in source.Objects:
  if not hasattr(old,'Shape'):continue
  o=doc.addObject('PartDesign::Feature',old.Name);o.Shape=old.Shape.copy();o.Label=old.Label
  for prop in ['PartCode','LegacyId','PartStatus','NameEN','NamePTBR','Category']:
   o.addProperty('App::PropertyString',prop);setattr(o,prop,getattr(old,prop))
 for n,(s,kind,moving) in definitions(cfg,upgrade).items():
  o=doc.addObject('PartDesign::Feature','CoinStudy_'+n);o.Shape=turn(s,cfg['coin_door'],angle) if moving else s
  o.Label='PROPOSED ENVELOPE - '+n
  for prop,value in [('Evidence','UNVERIFIED_HARDWARE / EXPLICIT_SPACE_RESERVATION'),('Role',kind)]:o.addProperty('App::PropertyString',prop);setattr(o,prop,value)
 doc.recompute();path=OUT/(name+'.FCStd');doc.saveAs(str(path));A.closeDocument(doc.Name)
 return path

def inspect(doc,source,cfg,upgrade,angle):
 expected=definitions(cfg,upgrade);checks=[]
 def ck(n,v):checks.append({'check':n,'status':'PASS' if v else 'FAIL'})
 base={o.Name:o for o in doc.Objects if hasattr(o,'Shape') and not o.Name.startswith('CoinStudy_')}
 original={o.Name:o for o in source.Objects if hasattr(o,'Shape')}
 ck('45 source study objects preserved',set(base)==set(original) and len(base)==45 and all(base[n].Shape.cut(o.Shape).Volume+o.Shape.cut(base[n].Shape).Volume<1e-5 for n,o in original.items()))
 ck('exact component set', {o.Name for o in doc.Objects if o.Name.startswith('CoinStudy_')}=={'CoinStudy_'+n for n in expected})
 ck('all solids valid and recomputed',all(o.Shape.isValid() and len(o.Shape.Solids)==1 and not any('Invalid' in str(s) for s in o.State) for o in doc.Objects if hasattr(o,'Shape')))
 for n,(s,kind,moving) in expected.items():
  o=doc.getObject('CoinStudy_'+n);want=turn(s,cfg['coin_door'],angle) if moving else s
  ck(n+' serialized shape matches definition',o is not None and o.Shape.cut(want).Volume+want.cut(o.Shape).Volume<1e-5)
 obs=fixed_obstacles(doc,cfg);bad=[]
 for n in expected:
  shape=doc.getObject('CoinStudy_'+n).Shape
  bad.extend((n,k) for k,s in obs.items() if overlaps(shape,s))
 ck('saved components clear fixed model and exterior controls',not bad)
 names=list(expected)
 internal=[(n,m) for i,n in enumerate(names) for m in names[i+1:] if overlaps(doc.getObject('CoinStudy_'+n).Shape,doc.getObject('CoinStudy_'+m).Shape)]
 ck('component bodies do not overlap each other',not internal)
 return checks,bad

def sweep(doc,cfg,upgrade,sign=1,extra=None):
 defs=definitions(cfg,upgrade);obs=fixed_obstacles(doc,cfg);bad=[]
 for n,(s,kind,moving) in defs.items():
  if not moving:obs[n]=s
 if extra:obs.update(extra)
 moving={n:s for n,(s,k,m) in defs.items() if m}
 angles=range(0,cfg['coin_door']['target_open_angle_deg']+1,cfg['coin_door']['sweep_step_deg'])
 for a in angles:
  for n,s in moving.items():
   p=turn(s,cfg['coin_door'],sign*a)
   for key,o in obs.items():
    if overlaps(p,o):bad.append({'angle_deg':a,'moving':n,'obstacle':key})
 return bad

def tray_path(doc,cfg,extra=None):
 c=cfg['coin_door'];defs=definitions(cfg,True);obs=fixed_obstacles(doc,cfg)
 for n,(s,k,m) in defs.items():
  if n!='CoinTray':obs[n]=turn(s,c,c['target_open_angle_deg']) if m else s
 if extra:obs.update(extra)
 bad=[]
 for dy in range(0,c['tray']['withdrawal_y_mm']-1,-c['tray']['step_mm']):
  p=defs['CoinTray'][0].copy();p.translate(A.Vector(0,dy,0))
  for n,s in obs.items():
   if overlaps(p,s):bad.append({'translation_y_mm':dy,'obstacle':n})
 return bad

def run(source,cfg):
 c=cfg['coin_door'];records=[];meshes={};docs={}
 for name,upgrade,angle in [('coin-basic-closed',False,0),('coin-upgrade-closed',True,0),('coin-upgrade-open',True,c['target_open_angle_deg'])]:
  path=build_case(source,cfg,name,upgrade,angle);doc=A.openDocument(str(path));doc.recompute();docs[name]=doc
  checks,bad=inspect(doc,source,cfg,upgrade,angle)
  assert all(x['status']=='PASS' for x in checks),(name,checks,bad)
  records.append({'configuration':name,'checks':checks,'actual_hardware_fit':'UNVERIFIED'})
  meshes[name]=[]
  for o in doc.Objects:
   if not o.Name.startswith('CoinStudy_'):continue
   v,f=o.Shape.tessellate(1)
   meshes[name].append({'name':o.Name,'kind':o.Role,'vertices':[[p.x,p.y,p.z] for p in v],'faces':f})
 doc=docs['coin-upgrade-closed']
 motions={}
 for key,up in [('basic',False),('upgrade',True)]:motions[key]=sweep(doc,cfg,up)
 motions['tray_withdrawal']=tray_path(doc,cfg)
 probe=box(c['service_probe_box']);open_doc=docs['coin-upgrade-open'];obs=fixed_obstacles(open_doc,cfg)
 obs.update({o.Name:o.Shape for o in open_doc.Objects if o.Name.startswith('CoinStudy_')})
 access=[n for n,s in obs.items() if overlaps(probe,s)]
 # Verify straight drop corridors land within the tray's usable interior, with no intervening solids.
 drop=[];tray=c['tray']['outer_box'];wall=c['tray']['wall_mm']
 for b in c['coin_drop_reservations']:
  inside=(b[0]>=tray[0]+wall and b[0]+b[3]<=tray[0]+tray[3]-wall and b[1]>=tray[1]+wall and b[1]+b[4]<=tray[1]+tray[4]-wall)
  block=[n for n,s in fixed_obstacles(doc,cfg).items() if overlaps(box(b),s)]
  drop.append({'inside_tray':inside,'obstacles':block,'actual_coin_outlets':'UNVERIFIED'})
 leaf90=turn(definitions(cfg,False)['DoorLeaf'][0],c,90)
 assert leaf90.BoundBox.YMax <= c['hinge_axis_mm'][1]+.01, 'Door turns inward'
 assert c['verified_hardware_dimensions_mm'] is None and c['hardware_status']=='UNVERIFIED', 'Update evidence review before making verified-hardware claims'
 assert not any(motions.values()),motions
 assert not access,access
 assert all(q['inside_tray'] and not q['obstacles'] for q in drop),drop
 # Negative controls target the same evaluators used above, not separate imitation checks.
 inward=sweep(doc,cfg,True,sign=-1);assert inward
 mechanism=doc.getObject('CoinStudy_Mechanism1');original=mechanism.Shape.copy();shifted=original.copy();shifted.translate(A.Vector(0,30,0));mechanism.Shape=shifted;doc.recompute()
 bad_checks,hit=inspect(doc,source,cfg,True,0);assert any(n=='Mechanism1' and obstacle=='SHELF_1' for n,obstacle in hit) and any(q['status']=='FAIL' for q in bad_checks)
 mechanism.Shape=original;doc.recompute()
 blocked=tray_path(doc,cfg,extra={'InjectedTrayBlock':box([305,-40,115,115,10,25])});assert any(b['obstacle']=='InjectedTrayBlock' for b in blocked)
 bad_leaf=open_doc.getObject('CoinStudy_DoorLeaf');saved=bad_leaf.Shape.copy();bad_leaf.Shape=turn(definitions(cfg,True)['DoorLeaf'][0],c,-c['target_open_angle_deg']);open_doc.recompute()
 rejected,_=inspect(open_doc,source,cfg,True,c['target_open_angle_deg']);assert any(q['status']=='FAIL' for q in rejected);bad_leaf.Shape=saved
 report={'status':'PROPOSAL_TESTED_ON_ASSUMED_COMPONENT_ENVELOPES','manufacturing_ready':False,'hardware_fit':'UNVERIFIED','configurations':records,
 'opening':{'direction':'OUTWARD','angle_deg':c['target_open_angle_deg'],'sampling_deg':c['sweep_step_deg'],'findings':motions},
 'service_access':{'candidate_probe_box':c['service_probe_box'],'obstacles':access,'human_access':'UNVERIFIED'},'coin_drop':drop,
 'negative_controls':[{'case':n,'status':'PASS'} for n in ['inward swing rejected','interfering mechanism envelope rejected','blocked tray extraction rejected','saved inward leaf rejected']],
 'unverified_interfaces':c['unverified_interfaces'],'retired_findings':'Old full-depth prism overlaps are not actual-fit evidence; S1, display and StarTech unchanged'}
 (OUT/'coin-door-validation.json').write_text(json.dumps(report,indent=2)+'\n');(OUT/'coin-door-meshes.json').write_text(json.dumps(meshes)+'\n')
 for doc in docs.values():A.closeDocument(doc.Name)
 print('COIN_DOOR_STUDY_PASS 3 saved configurations; outward sweep; tray path; 4 negative controls; actual hardware UNVERIFIED')
 return report
