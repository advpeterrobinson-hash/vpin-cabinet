"""V33.7 isolated 12 mm stock conversions; original CERN-OHL-S-2.0.
Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet
No production release, no inherited component is moved.
"""
from pathlib import Path
import sys,json,math,hashlib,traceback
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,V,box,coarse_mesh
C=json.loads((R/'config/plywood_conversion_v337.json').read_text());O=R/C['output'];B=O/'conversion-brep';B.mkdir(parents=True,exist_ok=True)
report={'checks':[],'parts':[],'manufacturing_release':False,'pass':False}
def dump(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def ck(n,v,detail=None):
 report['checks'].append({'name':n,'pass':bool(v),'detail':detail});dump(O/'conversion-validation.json',report);print(n,bool(v),flush=True)
 if not v:raise AssertionError((n,detail))
def bounds(s):b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def difference(a,b):return a.cut(b).Volume+b.cut(a).Volume
def planar(s,axis,val):
 i='XYZ'.index(axis);return max([f for f in s.Faces if type(f.Surface).__name__=='Plane' and abs(f.CenterOfMass[i]-val)<1e-5 and abs(f.normalAt(0,0)[i])>.999],key=lambda f:f.Area)
def localize(s,normal):
 normal=V(*normal);normal.normalize();rot=A.Rotation(-normal,V(0,0,1));q=s.copy();q.rotate(V(),rot.Axis,math.degrees(rot.Angle));b=q.BoundBox;off=V(b.XMin,b.YMin,b.ZMin);q.translate(-off);p=A.Placement(-off,rot).inverse();return q,p

def main():
 src=R/C['source'];old=load(src);optional=load(R/'exports/generated/backbox-lock-integration-v32/blank-fans.FCStd');new={n:s.copy() for n,s in old.items()};original={};members=[];changes={}
 report['source_sha256']=hashlib.sha256(src.read_bytes()).hexdigest();report['source']=C['source']
 def add(i,n,s,normal,note,finished=12,facing=0,pockets=None):
  members.append({'instance_id':i,'source_component':n,'shape':s,'face_A_outward_world':normal,'note':note,'finished_thickness_mm':finished,'facing_reduction_mm':facing,'pockets':pockets or []})
 for side,inst,x in [('L','P037-Main',150),('R','P038-Main',450)]:
  n='RemovableIntakeFilter'+side;s=old[n];top=planar(s,'Z',18);q=top.extrude(V(0,0,-12));q=q.cut(Part.makeCylinder(86,4,V(x,710,6)))
  for xx in [x-70,x+70]:
   for yy in [640,780]:q=q.cut(Part.makeCylinder(7,4,V(xx,yy,6)))
  q=q.removeSplitter();new[n]=q;original[n]=s
  note='12 mm stock with 4 mm underside service pocket; original 8 mm media/guard/head stack retained. Broad 12 mm corner lands remain. All original cuts are through cuts, now entered from underside.'
  add(inst,n,q,[0,0,-1],note,pockets=[{'shape':'circle','center_world_mm':[x,710,6],'radius_mm':86,'depth_mm':4,'purpose':'media/guard service plane'},{'shape':'four circles','centers_world_mm':[[xx,yy,6] for xx in [x-70,x+70] for yy in [640,780]],'radius_mm':7,'depth_mm':4,'purpose':'existing filter screw heads'}])
  changes[n]={'old_volume_mm3':s.Volume,'new_volume_mm3':q.Volume,'retained_12mm_land_area_mm2':q.common(box(x-100,600,6,200,220,4)).Volume/4,'old_wood_removed_mm3':s.cut(q).Volume,'old_mating_face_difference_mm2':top.cut(planar(q,'Z',18)).Area,'media_guard_minimum_gap_mm':min(q.distToShape(old[k])[0] for k in ['FloorFilterMediaReserve'+side,'FloorCommercialGuardReserve'+side]),'installed_lowest_z_mm':6,'floor_reference_z_mm':0,'service': 'Remove four holder screws; filter/media/guard travel down80 mm. Fan mounting nuts remain in pass-through holes.'}
 n='BB_DisplayReplaceableBezel';original[n]=old[n];add('P063-Main',n,new[n],[0,1,0],'EXPLICIT full-face rear reduction: 12 mm nominal stock -> 6 mm finished bezel. Protected glass/display planes leave only6 mm finished wood. Facing precedes all through cutting.',finished=6,facing=6)
 changes[n]={'old_volume_mm3':old[n].Volume,'new_volume_mm3':new[n].Volume,'finished_shape_difference_mm3':0,'protected_glass_gap_mm':new[n].distToShape(old['BB_Backglass'])[0],'protected_display_gap_mm':new[n].distToShape(old['BB_Display32'])[0],'finished_web_mm':6,'nominal_stock_mm':12,'full_blank_facing_removal_mm3':740*457*6,'net_outline_facing_removal_mm3':old[n].Volume}
 for side,inst in [('L','P081-Main'),('R','P082-Main')]:
  n='BB_IntakeFilterFrame'+side;s=old[n];q=planar(s,'Y',s.BoundBox.YMax).extrude(V(0,-12,0));q.translate(V(0,6,0));q=q.removeSplitter();new[n]=q;original[n]=s
  add(inst,n,q,[0,1,0],'12 mm exterior frame; door mating plane and 220 x80 clear aperture unchanged. Selected mounting fastener stack requires6 mm more length.')
  changes[n]={'old_volume_mm3':s.Volume,'new_volume_mm3':q.Volume,'old_wood_removed_mm3':s.cut(q).Volume,'aperture_mm':[220,80],'mating_y_mm':1322.1,'rearward_growth_mm':6}
 for side,assembly,dx in [('L','P083',0),('R','P084',350)]:
  n='BB_IntakeDownBaffle'+side;s=old[n];original[n]=s
  parts=[('Face',box(3+dx,1262.1,686,244,12,110),[0,-1,0]),('Top',box(3+dx,1274.1,784,244,36,12),[0,0,1]),('Side1',box(3+dx,1274.1,686,12,36,98).cut(box(3+dx,1274.1,686,3,36,32)),[-1,0,0]),('Side2',box(235+dx,1274.1,686,12,36,98).cut(box(244+dx,1274.1,686,3,36,32)),[1,0,0])]
  q=parts[0][1]
  for tag,t,normal in parts[1:]:q=q.fuse(t)
  q=q.removeSplitter();new[n]=q
  for tag,t,normal in parts:add(assembly+'-'+tag,n,t,normal,'Outside-only growth. Preserve inner chamber and downward mouth exactly; nonoverlapping butt-seam planar members. Assembly order Face, Top, Side1/Side2.'+(' Side members share an exterior lower-edge rebate3 mm deep x32 mm high across36 mm, leaving9 mm wall; clears passive bolt body without moving hardware.' if tag.startswith('Side') else ''),pockets=[{'shape':'open lower-edge strip','depth_mm':3,'height_mm':32,'width_mm':36,'purpose':'preserve passive-door bolt body; common identical side-member profile'}] if tag.startswith('Side') else [])
  chamber=box(15+dx,1274.1,686,220,36,98);mouth=box(15+dx,1274.1,685,220,36,1);inlet=box(15+dx,1310.1,698,220,1,80)
  changes[n]={'old_volume_mm3':s.Volume,'new_volume_mm3':q.Volume,'old_wood_removed_mm3':s.cut(q).Volume,'inner_chamber_mm':[220,36,98],'inner_chamber_volume_mm3':chamber.Volume,'old_chamber_penetration_mm3':chamber.common(s).Volume,'new_chamber_penetration_mm3':chamber.common(q).Volume,'downward_mouth_before_mm2':mouth.Volume-mouth.common(s).Volume,'downward_mouth_after_mm2':mouth.Volume-mouth.common(q).Volume,'inlet_before_mm2':inlet.Volume-inlet.common(s).Volume,'inlet_after_mm2':inlet.Volume-inlet.common(q).Volume,'speaker_gap_mm':q.distToShape(old['BB_SpeakerEnvelope'+side])[0],'passive_bolt_body_gap_mm':q.distToShape(old['BB_PassiveBoltBodyReserve0'])[0],'side_member_rebate_mm':{'depth':3,'height':32,'width':36,'remaining_wall':9}}
 for side,inst in [('L','P092-Main'),('R','P093-Main')]:
  n='BB_FanBlank'+side;s=optional[n];q=planar(s,'Y',s.BoundBox.YMax).extrude(V(0,-12,0));q.translate(V(0,6,0));q=q.removeSplitter();original[n]=s;changes[n]={'old_volume_mm3':s.Volume,'new_volume_mm3':q.Volume,'old_wood_removed_mm3':s.cut(q).Volume,'mating_y_mm':1322.1,'hole_pitch_mm':105,'outline_mm':[128,128],'rearward_growth_mm':6,'selected_fastener_extra_stack_mm':6}
  add(inst,n,q,[0,1,0],'Optional blank variant, mutually exclusive with fan/guard/mesh. Same128x128 outline and105 mm station; fastener stack increases6 mm and remains purchased-hardware HOLD.')
  # Blanks are exported separately, never added over populated fan assemblies.
  changes[n]['optional']=True
 optional_new={m['source_component']:m['shape'] for m in members if m['source_component'].startswith('BB_FanBlank')}
 ck('15 manufacturing members audited',len(members)==15)
 ck('all finished members are valid single solids',all(m['shape'].isValid() and len(m['shape'].Solids)==1 for m in members))
 unchanged_bad=[n for n,s in old.items() if n not in original and s.exportBrepToString()!=new[n].exportBrepToString()]
 ck('all unchanged CURRENT objects preserved',not unchanged_bad,{'method':'exact serialized B-rep equality; avoids invalid self-overlap Booleans on intentional compound reference envelopes','differences':unchanged_bad})
 ck('conversions preserve all original wood or exact bezel',all(v.get('old_wood_removed_mm3',0)<1e-5 for v in changes.values()),{k:v.get('old_wood_removed_mm3') for k,v in changes.items()})
 maps=[];meshes=[]
 for m in members:
  s=m.pop('shape');q,p=localize(s,m['face_A_outward_world']);ii=m['instance_id'];ip=B/(ii+'-installed.brep');lp=B/(ii+'-local.brep');s.exportBrep(str(ip));q.exportBrep(str(lp));roundtrip=q.copy();roundtrip.Placement=p.multiply(roundtrip.Placement);error=difference(s,roundtrip)
  row={**m,'installed_brep':str(ip.relative_to(R)),'local_brep':str(lp.relative_to(R)),'local_to_installed_matrix':list(p.toMatrix().A),'nominal_stock_thickness_mm':12,'machining_face':'FACE_A','opposite_face':'FACE_B / NO CNC','roundtrip_difference_mm3':error,'volume_mm3':s.Volume,'bounds_world_mm':bounds(s),'finished_xy_mm':[q.BoundBox.XLength,q.BoundBox.YLength]};maps.append(row);meshes.append(coarse_mesh(ii,s))
 ck('all exact local-installed manufacturing roundtrips',all(m['roundtrip_difference_mm3']<1e-5 for m in maps),max(m['roundtrip_difference_mm3'] for m in maps))
 reconstruction={}
 for n in ['BB_IntakeDownBaffleL','BB_IntakeDownBaffleR']:
  ss=[]
  for m in maps:
   if m['source_component']==n:t=Part.Shape();t.read(str(R/m['installed_brep']));ss.append(t)
  u=ss[0]
  for t in ss[1:]:u=u.fuse(t)
  reconstruction[n]=difference(u,new[n])
 ck('baffles reconstruct exactly from four real12mm members',all(v<1e-5 for v in reconstruction.values()),reconstruction)
 ck('baffle chamber and airflow unchanged',all(v['new_chamber_penetration_mm3']<1e-6 and abs(v['downward_mouth_before_mm2']-v['downward_mouth_after_mm2'])<1e-6 and abs(v['inlet_before_mm2']-v['inlet_after_mm2'])<1e-6 for n,v in changes.items() if 'inner_chamber_mm' in v))
 # Static differential check includes electronics/reference occupied shapes that
 # actual() deliberately excludes. Service-only tool/hand reserves are omitted.
 occupied=old # Conservative: include every source reference/reserve, not merely actual().
 hh=[]
 for n in original:
  if n not in new:continue
  delta=new[n].cut(original[n]);
  if delta.Volume<1e-6:continue
  for k,t in occupied.items():
   if k==n or not delta.BoundBox.intersect(t.BoundBox):continue
   vol=delta.common(t).Volume
   if vol>1e-5:hh.append({'changed':n,'obstacle':k,'added_wood_collision_mm3':vol})
 ck('all added installed wood clears every preserved shape including hardware reserves',not hh,hh)
 for n,s in {**{n:new[n] for n in original if n in new},**optional_new}.items():
  p=B/(n+'.brep');s.exportBrep(str(p));changes[n]['installed_brep']=str(p.relative_to(R));oldp=B/(n+'-before.brep');original[n].exportBrep(str(oldp));changes[n]['before_brep']=str(oldp.relative_to(R));changes[n]['volume_delta_mm3']=s.Volume-original[n].Volume;changes[n]['mass_delta_kg']=changes[n]['volume_delta_mm3']*650e-9
 d=A.newDocument('V337Conversion');d.addProperty('App::PropertyString','Authority');d.Authority='Isolated V33.7 thin-stock conversion;12/18 nominal only; manufacturing BLOCKED'
 for n,s in new.items():d.addObject('PartDesign::Feature',n).Shape=s
 d.recompute();d.saveAs(str(O/'conversion.FCStd'));A.closeDocument(d.Name)
 dump(O/'conversion-manufacturing-map.json',{'parts':maps,'source':C['source'],'source_sha256':report['source_sha256'],'nominal_stock_mm':12,'reconstruction_difference_mm3':reconstruction,'holds':['Actual stock thickness','Coupon','Purchased hardware stack lengths','No production release']})
 import gzip
 with gzip.open(O/'conversion-mesh.json.gz','wt') as f:json.dump(meshes,f,separators=(',',':'))
 report['changes']=changes;report['part_count']=len(maps);report['stock_volume_gain_mm3']=sum(v['volume_delta_mm3'] for v in changes.values());report['mass_delta_kg']=sum(v['mass_delta_kg'] for v in changes.values());report['conversion_sha256']=hashlib.sha256((O/'conversion.FCStd').read_bytes()).hexdigest();report['promoted_breps']={n:v['installed_brep'] for n,v in changes.items() if not v.get('optional')};report['optional_breps']={n:v['installed_brep'] for n,v in changes.items() if v.get('optional')}
 ck('input source bytes unchanged',hashlib.sha256(src.read_bytes()).hexdigest()==report['source_sha256'])
 report['pass']=True;dump(O/'conversion-validation.json',report);print('V337_CONVERSION_PASS',flush=True)
try:main()
except Exception as e:report['error']=str(e);report['traceback']=traceback.format_exc();dump(O/'conversion-validation.json',report);print(report['traceback'],flush=True);raise
