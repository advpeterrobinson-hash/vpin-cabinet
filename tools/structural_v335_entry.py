"""V33.5 B-rep candidates, differential geometry and access screen. CERN-OHL-S-2.0.
Nominal design study only. No hardware drilling or production CNC release.
"""
from pathlib import Path
import json,math,sys,gzip,hashlib
import FreeCAD as A, Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
C=json.loads((R/'config/structural_simplification_v335.json').read_text());O=R/C['output'];O.mkdir(parents=True,exist_ok=True);(O/'brep').mkdir(exist_ok=True)
V=A.Vector
d=A.openDocument(str(R/C['source']));old={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape') and not o.Shape.isNull()};A.closeDocument(d.Name)
new={n:s.copy() for n,s in old.items()};checks=[];data={};studies={}
def box(x,y,z,dx,dy,dz):return Part.makeBox(dx,dy,dz,V(x,y,z))
def union(ss):
 s=ss[0].copy()
 for b in ss[1:]:s=s.fuse(b)
 return s.removeSplitter()
def diff(a,b):
 if a.exportBrepToString()==b.exportBrepToString():return 0.0
 return a.cut(b).Volume+b.cut(a).Volume
def ck(n,v,detail=None):
 checks.append({'name':n,'pass':bool(v),'detail':detail});print('CHECK',n,bool(v),flush=True)
def mesh(s):
 v,f=s.tessellate(.3);return {'vertices':[list(p) for p in v],'faces':f}
def hits(s,obs):
 out=[]
 for n,b in obs.items():
  if s.BoundBox.intersect(b.BoundBox):
   v=s.common(b).Volume
   if v>1e-4:out.append({'part':n,'volume_mm3':v})
 return out
# Transfer existing wood at the interfaces from sides to captured panels.
# Intersect with actual side material to retain ALL historical leg/pilot voids.
transfers=[];depth=C['selected_capture_depth_mm']
for name,y,z,dy,dz in [('FLOOR',18,18,1272.1,18),('FRONT',0,0,18,400.05),('REAR',1290.1,0,18,596.9),('BACKBOX_BASE',1127.125,578.9,162.975,18)]:
 dd=depth if name in ('FLOOR','BACKBOX_BASE') else C['front_rear_capture_depth_mm']
 for side,x in [('SIDE_L',18-dd),('SIDE_R',582)]:
  strip=box(x,y,z,dd,dy,dz);tab=old[side].common(strip).removeSplitter()
  new[name]=new[name].fuse(tab).removeSplitter();new[side]=new[side].cut(tab).removeSplitter()
  transfers.append({'part':name,'side':side,'depth_mm':dd,'volume_mm3':tab.Volume,'shoulder_area_mm2':dd*dy if name in ('FLOOR','BACKBOX_BASE') else dd*dz})
woodnames={p['object'] for p in json.loads((R/'config/wood_materials_v334.json').read_text())['parts']}
joined=['SIDE_L','SIDE_R','FLOOR','FRONT','REAR','BACKBOX_BASE']
ck('captured lower-shell and shelf union equals original exact wood union',diff(union([new[n] for n in joined]),union([old[n] for n in joined]))<1e-3)
ck('joinery transfers have no wood overlap',not any(new[a].common(new[b]).Volume>1e-4 for i,a in enumerate(joined) for b in joined[i+1:]))
data['captures']=transfers
data['rear_fan_bore_revision']={'retired_through_bores':8,'old_diameter_mm':4.5,'new_pilot_mm':None,'status':'PURCHASE_BEFORE_CNC','reason':'Clearance holes are not wood-screw anchors; restore nominal wood pending selected pilot.'}
# Remove only the nonfunctional upper front cantilever; preserve all functional roots.
for n in ['PF_OpenCradleL','PF_OpenCradleR']:
 new[n]=old[n].cut(box(-100,900,489.4801077622672,800,110.5,100)).removeSplitter()
 ck(n+' valid single solid',new[n].isValid() and len(new[n].Solids)==1)
 seat_region=box(0,1018.75061984718,460,600,33,60)
 ck(n+' exact seat region unchanged',diff(new[n].common(seat_region),old[n].common(seat_region))<1e-5)
 ck(n+' all retained wood is subset of original',new[n].cut(old[n]).Volume<1e-5)
 data[n]={'removed_mm3':old[n].Volume-new[n].Volume,'seat_wrap_before_after_deg':[180,180],'minimum_rear_ligament_before_after_mm':[6.279669885093483]*2,'front_seat_root_before_after_mm':[8.25061984718]*2,'exterior_edges_before_after':[13,11]}
# Minimum root thickness alone does not prove equal guide-ear stiffness.
# Preserve CURRENT cradle; keep the trim as a rejected diagnostic only.
for n in ['PF_OpenCradleL','PF_OpenCradleR']:
 studies['RejectedSimplification_'+n]=new[n].copy()
 data[n]['decision']='KEEP_ORIGINAL'
 data[n]['reason']='Upper front wall narrowed from23.5 to8.251mm over the guide height. Same minimum root does not prove same local stiffness; no structural qualification supports removal.'
 data[n]['promoted']=False
 new[n]=old[n].copy()
# Monitor-stop rail, simple one-piece 18 x 18 transverse member. Front-face
# end captures transfer vertical load into the two carriers; rear screws retain.
r=C['monitor_rail']['candidate_bounds_mm'];rail=box(*r[:3],*[r[i+3]-r[i] for i in range(3)])
railremoved=[n for n in old if n.startswith(('BB_MonitorStopBlock','BB_MonitorStopContact','BB_MonitorStopScrewReserve'))]
for n in railremoved:new.pop(n)
for n in ['BB_MonitorCarrier0','BB_MonitorCarrier1']:new[n]=new[n].cut(rail).removeSplitter()
new['BB_MonitorStopRail']=rail
for i,(x,y) in enumerate(C['monitor_rail']['adjuster_xy_mm']):
 # References only: 18 mm metal thread engagement, 14 mm nominal protrusion,
 # 10 mm contact disk whose upper face meets the existing adapter underside.
 new[f'BB_StopAdjuster{i}']=Part.makeCylinder(3,28,V(x,y,919))
 new[f'BB_StopTip{i}']=Part.makeCylinder(5,2,V(x,y,947))
 new[f'BB_StopInsert{i}']=Part.makeCylinder(4.5,14,V(x,y,921)).cut(Part.makeCylinder(3,14,V(x,y,921)))
 pts=[V(x+5*math.cos(j*math.pi/3),y+5*math.sin(j*math.pi/3),935) for j in range(7)]
 new[f'BB_StopLocknut{i}']=Part.Face(Part.makePolygon(pts)).extrude(V(0,0,5)).cut(Part.makeCylinder(3,5,V(x,y,935)))
for i,(x,z) in enumerate(C['monitor_rail']['attachment_reference_xz_mm']):
 new[f'BB_StopRailRetention{i}']=Part.makeCylinder(2.25,24,V(x,1258,z),V(0,-1,0)).fuse(Part.makeCylinder(4.5,3,V(x,1258,z),V(0,1,0)))
railobs={n:s for n,s in new.items() if n in woodnames or n.startswith(('BB_Display','BB_Backglass','BB_Speaker','BB_DMD','BB_MonitorDepth','BB_MonitorClamp'))}
railobs.pop('BB_MonitorStopRail',None)
ck('stop rail clear of occupied wood/display envelopes',not hits(rail,railobs),hits(rail,railobs))
for n in ['BB_MonitorCarrier0','BB_MonitorCarrier1']:ck(n+' remains single valid solid',new[n].isValid() and len(new[n].Solids)==1)
for i in range(2):
 ck('stop tip '+str(i)+' clear display',new[f'BB_StopTip{i}'].common(old['BB_Display32']).Volume<1e-5)
 ck('stop tip '+str(i)+' bears on unchanged VESA underside',new[f'BB_StopTip{i}'].distToShape(old['BB_ReplaceableVESAPlate'])[0]<1e-6)
# Provisional plunger illustration, authoritative X/Z only; NO FRONT machining.
f=json.loads((R/'config/front_panel_v32.json').read_text())
new['PlungerFrontInterfaceProvisional']=box(490,-3,250,60,3,60)
new['PlungerShaftProvisional']=Part.makeCylinder(4,55,V(520,-3,280),V(0,-1,0))
new['PlungerHandleProvisional']=Part.makeCylinder(12,12,V(520,-58,280),V(0,-1,0))
# Physical occupied internal authority remains PLUNGER_RESERVED; front extraction
# corridor is schematic because the exact purchased plunger is unknown.
studies['PlungerRemovalReference']=box(490,-260,250,60,257,60)
# Replace main rear through-bolts, outside nuts/washers. Keep fan body + inner grill.
fanremoved=[n for n in new if n.startswith('CandidateFanBolt') or n.startswith('CandidateFanGuard') and n.endswith('Outer')]
for n in fanremoved:new.pop(n)
for x in (230,370):
 for i,(dx,dz) in enumerate([(-52.5,-52.5),(-52.5,52.5),(52.5,-52.5),(52.5,52.5)]):
  # 1.5 guard +25 fan +12 reference wood engagement; length not a BOM selection.
  a=V(x+dx,1263.6,500+dz)
  # Withdraw obsolete Ø4.5 through clearance from current machining.
  new['REAR']=new['REAR'].fuse(Part.makeCylinder(2.25,18,V(x+dx,1290.1,500+dz),V(0,1,0))).removeSplitter()
  new[f'RearFanWoodScrew{x}_{i+1}']=Part.makeCylinder(2,38.5,a,V(0,1,0)).fuse(Part.makeCylinder(4,3,a,V(0,-1,0)))
# Actual pocket-axis packaging at each candidate depth. These solids are
# separate review geometry; physical jig qualification is not represented as PASS.
rows=[];a=math.radians(C['pockets']['reference_angle_deg']);radius=C['pockets']['reference_counterbore_radius_mm']
for part,base,ys in [('FLOOR',18,C['pockets']['floor_y_mm']),('BACKBOX_BASE',578.9,C['pockets']['shelf_y_mm'])]:
 for side,sgn,hx in [('L',-1,32),('R',1,568)]:
  for j,y in enumerate(ys):
   head=V(hx,y,base+6);axis=V(sgn*math.cos(a),0,math.sin(a));tip=head+axis*28;entry=head-axis*(6/math.sin(a))
   screw=Part.makeCylinder(2,28,head,axis);pocket=Part.makeCylinder(radius,34,head,-axis);driver=Part.makeCylinder(9,160,head-axis*28,-axis)
   studies[f'{part}_Pocket{side}{j+1}']=pocket;studies[f'{part}_Screw{side}{j+1}']=screw;studies[f'{part}_Driver{side}{j+1}']=driver
   obs={n:s for n,s in new.items() if n in woodnames and n not in [part,'SIDE_L','SIDE_R','FLOOR_CLEAT_18','FLOOR_CLEAT_552']}
   # Material above/below intersection is inspected analytically; host parts are
   # excluded only as intended screw engagement, never other hardware reserves.
   obs.update({n:s for n,s in new.items() if ('Reserve' in n or 'Lock' in n or 'Fan' in n) })
   collisions=hits(screw,obs);driverhits=hits(driver,obs)
   for dep in C['capture_depth_candidates_mm']:
    wallx=18-dep if side=='L' else 582+dep
    distance=(wallx-hx)/axis.x;entrywall=head+axis*distance
    outside=tip.x-2*math.sin(a) if side=='L' else 600-tip.x-2*math.sin(a)
    rows.append({'part':part,'pocket':f'{side}{j+1}','depth_mm':dep,'head_mm':list(head),'underside_entry_mm':list(entry),'axis':list(axis),'tip_mm':list(tip),'side_entry_mm':list(entrywall),'side_engagement_mm':28-distance,'outside_skin_mm':outside,'floor_top_to_counterbore_mm':18-6-radius*math.cos(a),'screw_to_panel_top_mm':base+18-tip.z-2*math.cos(a),'dado_edge_margin_mm':min(entrywall.z-base,base+18-entrywall.z)-2*math.cos(a),'screw_hits':collisions,'driver_hits':driverhits,'status':'HARDWARE_DEPENDENT','geometry_pass':not collisions and not driverhits and outside>2 and 28-distance>7})
ck('pocket packaging cases clear after deferred cleat installation',all(r['geometry_pass'] for r in rows),[r for r in rows if not r['geometry_pass']])
data['pockets']=rows
# Current M006 would obstruct drill/driver approach. Sequence is explicit:
# construct captured shell and install pockets first, then add retained ledges.
data['M006']={'decision':'KEEP','unsupported_span_before_mm':504,'unsupported_span_without_mm':564,'stress_ratio':(564/504)**2,'deflection_ratio':(564/504)**4,'mass_kg':sum(old[n].Volume for n in ['FLOOR_CLEAT_18','FLOOR_CLEAT_552'])*650/1e9,'pocket_access_prerequisite':'M006 installed after pocket drilling/retention; shelf pockets before backbox assembly'}
for i,y in enumerate([390,780]):studies[f'OptionalTemporarySupport{i+1}']=box(18,y,0,564,50,18)
# T3 forward diagnostic changes no seat/reserve constraints and is not promoted.
data['T3']={'translation_y_mm':-20,'meaningful_simplification':False,'decision':'KEEP','reason':'The seat root, WPC relief and S3-controlled floor foot remain. Exterior cantilever can be removed without moving any accepted support.'}
for n in ['CROSS_3','CROSS_GUIDE_3L','CROSS_GUIDE_3R']:
 s=old[n].copy();s.translate(V(0,-20,0));studies['Diagnostic_'+n]=s
 data['T3'][n+'_cradle_clearance_mm']=min(s.distToShape(new[q])[0] for q in ['PF_OpenCradleL','PF_OpenCradleR'])
# Exact changed-part collision differential against current occupied wood.
changes=[n for n in old if n in new and diff(old[n],new[n])>1e-4];added=[n for n in new if n not in old];removed=[n for n in old if n not in new]
woodnew={n:s for n,s in new.items() if n in woodnames or n=='BB_MonitorStopRail'};unexpected=[]
for i,n in enumerate(woodnew):
 for m in list(woodnew)[i+1:]:
  if n not in changes+added and m not in changes+added:continue
  s,t=woodnew[n],woodnew[m]
  if not s.BoundBox.intersect(t.BoundBox):continue
  vol=s.common(t).Volume;prev=old[n].common(old[m]).Volume if n in old and m in old else 0
  if vol>prev+1e-4:unexpected.append([n,m,vol,prev])
ck('no new positive-volume wood collisions',not unexpected,unexpected)
ck('all changed or added wood valid single solids',all(new[n].isValid() and len(new[n].Solids)==1 for n in changes+added if n in woodnew))
protected=[n for n in old if n not in changes+removed]
ck('all unrelated installed shapes exact',all(diff(old[n],new[n])<1e-5 for n in protected))
data['changed']=[{'name':n,'before_mm3':old[n].Volume,'after_mm3':new[n].Volume,'symmetric_difference_mm3':diff(old[n],new[n])} for n in changes];data['added']=added;data['removed']=removed;data['protected_count']=len(protected)
# Axis and nominal exterior maintained by exact union, protected hinges/playfield.
ck('SW01 installed blocks unchanged',all(diff(s,new[n])<1e-5 for n,s in old.items() if n.startswith('CandidateLegBlock')))
ck('WPC and playfield functional objects unchanged',all(diff(s,new[n])<1e-5 for n,s in old.items() if any(k in n for k in ['Dowel','WPC','HingeArm']) and n in new))
for label,scene in [('play',new),('study',studies)]:
 doc=A.newDocument('V335'+label)
 for n,s in scene.items():
  ob=doc.addObject('PartDesign::Feature',n);ob.Shape=s
 doc.recompute();doc.saveAs(str(O/(label+'.FCStd')));A.closeDocument(doc.Name)
for n in changes+added:
 new[n].exportBrep(str(O/'brep'/(n+'.brep')))
(O/'changes-mesh.json.gz').write_bytes(gzip.compress(json.dumps({n:mesh(new[n]) for n in changes+added}).encode(),mtime=0))
(O/'study-mesh.json.gz').write_bytes(gzip.compress(json.dumps({n:mesh(s) for n,s in studies.items()}).encode(),mtime=0))
data['checks']=checks;data['pass']=all(c['pass'] for c in checks);data['release']=False;data['source_sha256']=hashlib.sha256((R/C['source']).read_bytes()).hexdigest()
(O/'geometry-validation.json').write_text(json.dumps(data,indent=2)+'\n')
print('V335_GEOMETRY_DONE',data['pass'],len(checks),flush=True)
