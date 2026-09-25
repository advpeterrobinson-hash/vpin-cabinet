"""Isolated architecture proposal from current saved CAD. Never generates production holes."""
import hashlib,json,math
from pathlib import Path
import FreeCAD as A
import Part
from owner_review_scenes_v27 import scenes
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'exports/generated/simplification-v28'
SOURCE=ROOT/'cad/active/vpin-active.FCStd'

def bounds(s):
 b=s.BoundBox;return [b.XMin,b.XMax,b.YMin,b.YMax,b.ZMin,b.ZMax]
def box(b):return Part.makeBox(b[1]-b[0],b[3]-b[2],b[5]-b[4],A.Vector(b[0],b[2],b[4]))
def run():
 OUT.mkdir(parents=True,exist_ok=True);digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest();d=A.openDocument(str(SOURCE))
 original={o.Name:o.Shape.copy() for o in d.Objects if o.TypeId in ('Part::Feature','PartDesign::Feature') and not o.Shape.isNull()}
 bb=lambda n:bounds(original[n]);new={};meta={}
 group=d.addObject('App::Part','SimplificationV28');group.Label='DESIGN-PROVISIONAL / ARCHITECTURE NOT ACCEPTED'
 def add(n,s,kind,note):
  o=d.addObject('PartDesign::Feature',n);o.Shape=s;o.Label=n+' — '+note
  o.addProperty('App::PropertyString','EngineeringRole');o.EngineeringRole='DESIGN_PROVISIONAL'
  o.addProperty('App::PropertyBool','ManufacturingReady');o.ManufacturingReady=False
  group.addObject(o);new[n]=s;meta[n]=dict(kind=kind,note=note,bounds=bounds(s));return s
 def addbox(n,b,kind,note):return add(n,box(b),kind,note)
 removed_prefixes=('RearCPU','CPURail','Cradle','PivotPlate','PivotJournal','UCFL','BearingBacking','ClosedSupportSeat','SafetyStay','Prop','ClosedSupportDoubler','ElectronicsCarrier','ElectronicsLeftPayload','ElectronicsRightPayload','CarrierAngle','VesaAdapter','LowCrossmember3','DefinedCarrierMount')
 removed=[n for n in original if n.startswith(removed_prefixes)]
 removed+=['RearPanelWithCPUHatchV24','LowCrossmember1V20','LowCrossmember2V20']
 bottom=bb('CapturedBottomV20');t=bottom[5]-bottom[4];margin=20 # existing project review margin
 # CM1/2 retained, former carrier bores filled in the PROPOSAL ONLY.
 for i in (1,2):
  s=original[f'LowCrossmember{i}V20'].copy()
  for n,c in original.items():
   if n.startswith(f'DefinedCarrierMount{i}_'):s=s.fuse(c.common(box(bb(f'LowCrossmember{i}V20'))))
  add(f'STie{i}',s.removeSplitter(),'WOOD','existing structural tie; old carrier bores retired')
 hatch=bb('RearCPUHatchOpeningGhostV24');enclosure=bb('UtilityAMainsEnclosureV26')
 opening=[hatch[0],hatch[1],hatch[2],hatch[3],bottom[5]+2*t,enclosure[4]-margin]
 add('SRearPanel',original['RearPanelWithCPUHatchV24'].cut(box(opening)),'WOOD','existing jambs; lower opening extension; shear proof required')
 addbox('SRearOpening',opening,'ACCESS','340 x 293 investigation opening; no claim of structural maximum')
 door=bb('RearCPUServiceDoorClosedV24');overlap=hatch[0]-door[0]
 ds=addbox('SRearDoor',[opening[0]-overlap,opening[1]+overlap,door[2],door[3],opening[4]-overlap,opening[5]+overlap],'WOOD','ordinary hinge/latch interface unresolved')
 ds=ds.copy();ds.rotate(A.Vector(door[1],door[3],0),A.Vector(0,0,1),-105)
 add('SRearDoorOpen',ds,'STATE','outward ordinary door; hinge/latch holes not generated')
 base=bb('RearCPUShelfStowedV24');base[4]=bottom[5];base[5]=base[4]+t
 addbox('SPCBase',base,'WOOD','one detachable board directly on bottom; no rail or slide')
 case=original['RearCPUOpenCaseStowedV24'].copy();case.translate(A.Vector(0,0,base[5]-bb('RearCPUOpenCaseStowedV24')[4]));add('SPCCase',case,'PAYLOAD','existing open-frame case envelope; no new catalogue dimensions')
 lift_z=opening[4]+2 # existing installation clearance class; mock-up only
 top=bounds(case)[5];rise=lift_z-base[4]
 addbox('SPCLift',[base[0],base[1],base[2],base[3],base[4],top+rise],'ACCESS','lift clear of sill after unplugging/unbolting')
 addbox('SPCOut',[base[0],base[1],base[2],door[3]+base[3]-base[2]+margin,lift_z,top+rise],'ACCESS','hand-supported rear extraction; no rated drawer travel')
 # Three boards reuse the already checked project envelopes, not a competing carrier layer.
 review=json.loads((ROOT/'exports/generated/owner-change-v28/review-analysis.json').read_text())
 for key,old in [('A','F'),('B','G'),('C','P')]:
  b=review['boards'][old]['board_bounds'];addbox('SBoard'+key,b,'BOARD','sole removable electronics mounting board')
  addbox('SPayload'+key,review['boards'][old]['payload_bounds'],'PAYLOAD','provisional payload only, actual devices unassigned')
  for prefix in ('Cable','Lift','Extract'):
   addbox('S'+prefix+key,review['candidates']['Review'+prefix+old]['bounds'],'ACCESS','cable or removal reservation; physical access unproven')
 # Six identical commodity bracket capacity envelopes. No catalogue mounting pattern.
 reach=review['boards']['G']['board_bounds'][1]-18;h=99;th=3;z=174
 for k,y in [('B1',348),('B2',615),('C1',348),('C2',615)]:
  if k[0]=='B':a=[18,18+reach,y,y+25,z-th,z];v=[18,18+th,y,y+25,z-h,z]
  else:a=[582-reach,582,y,y+25,z-th,z];v=[582-th,582,y,y+25,z-h,z]
  add('SBracket'+k,box(a).fuse(box(v)),'COMMODITY','one common bracket family fit/rating unresolved; not fabricated drawing')
 for side,x in [('L',160),('R',440)]:
  add('SBracketA'+side,box([x-12.5,x+12.5,260-reach,260,z-th,z]).fuse(box([x-12.5,x+12.5,257,260,z-h,z])),'COMMODITY','same bracket reserve on CM1 front; pattern blocked')
 cfg=json.loads((ROOT/'config/playfield_mechanics_v18.json').read_text());c=cfg['cabinet'];disp=cfg['display_envelope']
 alpha=math.atan2(c['rear_height_mm']-c['front_height_mm'],c['side_length_mm']-c['rear_top_flat_mm'])
 slope=(c['rear_height_mm']-c['front_height_mm'])/(c['side_length_mm']-c['rear_top_flat_mm'])
 setback=disp['front_setback_mm'];bz=c['front_height_mm']+setback*slope-disp['glass_clearance_normal_mm']-disp['depth_mm']*math.cos(alpha)
 def tf(s):s=s.copy();s.rotate(A.Vector(),A.Vector(1,0,0),math.degrees(alpha));s.translate(A.Vector(0,setback,bz));return s
 def pt(x,y,z):return A.Vector(x,setback+y*math.cos(alpha)-z*math.sin(alpha),bz+y*math.sin(alpha)+z*math.cos(alpha))
 axis=pt(0,1005,-40);angle=cfg['hinge_axis']['relative_service_open_angle_deg']
 # Preserve beam depth, replace eight-part cradle + metal VESA carrier with three wood pieces.
 frame=[]
 for side,x in [('L',40),('R',542)]:
  yz=[(35,-75),(1045,-75),(1045,-5),(35,-5)]
  wire=Part.makePolygon([A.Vector(x,y,z) for y,z in yz]+[A.Vector(x,*yz[0])]);s=tf(Part.Face(wire).extrude(A.Vector(t,0,0)))
  frame.append(add('SBeam'+side,s,'WOOD','2D routed rear ear; pivot bore intentionally absent'))
 bridge=tf(box([40,560,355,615,-23,-5]));frame.append(add('SBridge',bridge,'WOOD','one wood VESA bridge; actual display pattern stays adapter-only'))
 # Two ordinary angles allow face drilling of both rail and bridge; no edge-drilling fixture.
 for side in 'LR':
  if side=='L':flange=[58,58+reach,480,505,-26,-23];web=[58,61,480,505,-122,-23]
  else:flange=[542-reach,542,480,505,-26,-23];web=[539,542,480,505,-122,-23]
  add('SBridgeAngle'+side,tf(box(flange).fuse(box(web))),'COMMODITY','same bracket family as boards; face-drilled rail/bridge attachment')
 add('SFrameOpen',Part.makeCompound(frame+[new['SBridgeAngleL'],new['SBridgeAngleR']]),'STATE','three-part holder raised; provisional')
 new['SFrameOpen'].rotate(axis,A.Vector(1,0,0),-angle);d.getObject('SFrameOpen').Shape=new['SFrameOpen'];meta['SFrameOpen']['bounds']=bounds(new['SFrameOpen'])
 for side,x in [('L',18),('R',564)]:
  addbox('SPivotCheek'+side,[x,x+t,axis.y-80,axis.y+80,axis.z-40,axis.z+40],'WOOD','plain CNC pivot support / stop interface requires proof')
  # Source journal diameter is a space probe only; tube section/capacity unselected.
  addbox('SShaftClamp'+side,[x,x+t,axis.y-15,axis.y+15,axis.z-15,axis.z+15],'COMMODITY','split shaft support reserve; physical pattern unselected')
 add('SCrossAxis',Part.makeCylinder(7.5,564,A.Vector(18,axis.y,axis.z),A.Vector(1,0,0)),'COMMODITY','stock tube/shaft space probe only; section and material NOT selected')
 for side,n in [('L','ClosedSupportDoublerLeftV19'),('R','ClosedSupportDoublerRightV19')]:
  b=bb(n);addbox('SLanding'+side,b,'WOOD','plain landing block replaces shaped prop anchor union; latch interface retained')
 # Straps resist closing torque at current service angle. A positive over-opening stop remains required.
 straps={}
 for side,x in [('L',28),('R',572)]:
  moving=pt(x,485,-65);rot=A.Rotation(A.Vector(1,0,0),-angle);moving=axis+rot.multVec(moving-axis)
  fixed=A.Vector(-72 if side=='L' else 672,bb('BackboxFloorV14')[2],1005);delta=fixed-moving
  add('SStrap'+side,Part.makeCylinder(4,delta.Length,moving,delta),'RESTRAINT','strap centerline space probe, NOT rope diameter/rated strap')
  straps[side]=dict(moving=list(moving),fixed=list(fixed),length=delta.Length,
   torque_per_unit_tension_about_x=((moving-axis).cross(delta/delta.Length)).x)
  # Explicit stop/anchor design volume, not a released contact profile.
  addbox('SStop'+side,[x-9,x+9,axis.y-30,axis.y+30,axis.z+25,axis.z+75],'UNRESOLVED','positive over-opening stop contact unresolved: no strap-only safety acceptance')
 # Vent comparison uses original project filter zone, no manufacturer's fan pattern.
 floor=original['CapturedBottomV20'].copy()
 for n,s in original.items():
  if n.startswith('DefinedIntake'):floor=floor.fuse(s.common(box(bottom)))
 for y in (380,520):floor=floor.cut(Part.makeCylinder(50,t,A.Vector(300,y,bottom[4])))
 add('SAlternativeVentFloor',floor.removeSplitter(),'ALTERNATIVE','two generic 100 mm apertures; rejected pending shear/filter/thermal review')
 # Compute exact CAD intersections; exclude deliberate attachment contacts and state duplicates.
 current=scenes(original)[0][2]+[n for n in original if n.startswith('SSF')]
 retained=[n for n in dict.fromkeys(current) if n not in removed and n not in ('GenericPlayfieldDisplayClosedV18','PlayfieldGlassTargetV20')]
 props=[n for n,v in meta.items() if v['kind'] not in ('STATE','ACCESS','ALTERNATIVE','UNRESOLVED','RESTRAINT')]
 def hits(shape,names):
  return [n for n in names if shape.BoundBox.intersect((new|original)[n].BoundBox) and shape.common((new|original)[n]).Volume>.01]
 obstacles=list(retained)
 pc_targets=[n for n in retained if n not in ('RearPanelWithCPUHatchV24',)]+['SRearPanel','STie1','STie2']+['SBoard'+k for k in 'ABC']
 checks=dict(pc_lift=hits(new['SPCLift'],pc_targets),pc_out=hits(new['SPCOut'],pc_targets),board_payload={},brackets={},straps={},holder_closed={},holder_open=[])
 for k in 'ABC':checks['board_payload'][k]=hits(new['SBoard'+k].fuse(new['SPayload'+k]),obstacles+['SPCCase','SBeamL','SBeamR','SBridge'])
 for n in new:
  if n.startswith('SBracket'):checks['brackets'][n]=hits(new[n],obstacles+['SPCCase'])
 for n in ['SBeamL','SBeamR','SBridge']:checks['holder_closed'][n]=hits(new[n],obstacles+['GenericPlayfieldDisplayClosedV18'])
 checks['bridge_brackets']={n:hits(new[n],obstacles+['SPayloadA','SPayloadB','SPayloadC']) for n in ['SBridgeAngleL','SBridgeAngleR']}
 checks['holder_open']=hits(new['SFrameOpen'],obstacles)
 for n in ['SStrapL','SStrapR']:checks['straps'][n]=hits(new[n],obstacles+['SFrameOpen','GenericPlayfieldDisplayOpenGhostV18'])
 checks['strap_free_paths']={}
 for side,data in straps.items():
  a=A.Vector(*data['moving']);b=A.Vector(*data['fixed']);delta=b-a
  probe=Part.makeCylinder(4,delta.Length-10,a,delta)
  checks['strap_free_paths'][side]=hits(probe,obstacles+['SFrameOpen','GenericPlayfieldDisplayOpenGhostV18'])
 checks['board_removal']={}
 for k in 'ABC':
  targets=obstacles+['SFrameOpen','SPCCase','SStrapL','SStrapR']+['SBoard'+o for o in 'ABC' if o!=k]+['SPayload'+o for o in 'ABC' if o!=k]
  checks['board_removal'][k]=hits(new['SLift'+k],targets)+hits(new['SExtract'+k],targets)
 checks['sampled_holder_motion']={}
 checks['inherited_display_motion']={}
 for deg in range(0,int(angle)+1,10):
  motion=Part.makeCompound(frame+[new['SBridgeAngleL'],new['SBridgeAngleR']]+[original['GenericPlayfieldDisplayClosedV18']]);motion.rotate(axis,A.Vector(1,0,0),-deg)
  targets=obstacles+['SPCCase','SBoardA','SBoardB','SBoardC','SPayloadA','SPayloadB','SPayloadC','SLandingL','SLandingR']
  checks['sampled_holder_motion'][str(deg)]=hits(motion,targets)
  baseline_display=original['GenericPlayfieldDisplayClosedV18'].copy();baseline_display.rotate(axis,A.Vector(1,0,0),-deg)
  checks['inherited_display_motion'][str(deg)]=hits(baseline_display,targets)
 # Deliberate negative controls: old CM3 prevents floor-base installation; old tray cannot disappear by assertion.
 checks['retained_CM3_conflict']=hits(new['SPCBase'],['LowCrossmember3V20'])
 d.recompute();path=OUT/'vpin-simplification-v28.FCStd';d.saveAs(str(path));A.closeDocument(d.Name)
 assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==digest
 d=A.openDocument(str(path));inventory=[]
 for o in d.Objects:
  if o.TypeId not in ('Part::Feature','PartDesign::Feature') or o.Shape.isNull():continue
  assert o.Shape.isValid(),o.Name
  v,tri=o.Shape.tessellate(1)
  inventory.append(dict(name=o.Name,role=getattr(o,'EngineeringRole',''),kind=meta.get(o.Name,{}).get('kind','CURRENT'),bounds=bounds(o.Shape),vertices=[list(x) for x in v],triangles=tri))
 report=dict(manufacturing_ready=False,status='DESIGN_PROVISIONAL',source_sha256=digest,removed_names=sorted(set(removed)),current_names=current,retained_names=retained,proposed_names=retained+props,candidates=meta,inventory=inventory,checks=checks,straps=straps,notes=['No stop contact profile or rated hardware selected. Holder NOT safe to execute from review.', 'No physical test claimed. Negative strap torque resists closure only; stop must limit opening.'])
 (OUT/'geometry.json').write_text(json.dumps(report,indent=2)+'\n');A.closeDocument(d.Name)
 print('SIMPLIFICATION_CAD_PASS');print(json.dumps(checks,indent=2));print('STRAPS',straps)
if __name__=='__main__':run()
