"""Isolated WPC positive control then V32 study. CERN-OHL-S-2.0.
Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet
Run: freecadcmd studies/wpc-fold-v32/build.py. Require WPC_STUDY_PASS.
OCC common-volume / distToShape matches tools/backbox_floor_v32_entry.py.
"""
from pathlib import Path
import json, math, hashlib, subprocess, shutil
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[2]; S=Path(__file__).parent
C=json.loads((S/'parameters.json').read_text()); O=R/C['output_directory'];O.mkdir(parents=True,exist_ok=True)
V=A.Vector; checks=[]; tol=C['volume_tolerance_mm3']
def check(n,v):
    assert v,n
    checks.append(n)
def box(x,y,z,w,d,h):return Part.makeBox(w,d,h,V(x,y,z))
def prism(x,w,points):
    p=[V(x,y,z) for y,z in points];return Part.Face(Part.makePolygon(p+[p[0]])).extrude(V(w,0,0))
def passage(p):return box(p['x_position']-p['width']/2,p['y_position']-p['depth']/2,570,p['width'],p['depth'],60)
def pose(ss,axis,a):
    out={n:s.copy() for n,s in ss.items()}
    for s in out.values():s.rotate(axis,V(1,0,0),a)
    return out
# Deliberately the same broad-phase and exact BRep collision test as V32.
def hits(moving,fixed):
    rows=[]
    for n,s in moving.items():
        for m,t in fixed.items():
            if s.BoundBox.intersect(t.BoundBox):
                vol=s.common(t).Volume
                if vol>tol:rows.append({'part':n,'obstacle':m,'volume_mm3':vol})
    return rows

def face(s,z):return Part.makeCompound([f for f in s.Faces if abs(f.CenterOfMass.z-z)<1e-7 and abs(f.normalAt(0,0).z)>.999])
def bounds(s):
    b=s.BoundBox;return [b.XMin,b.XMax,b.YMin,b.YMax,b.ZMin,b.ZMax]
def mesh(n,s):
    vs,fs=s.tessellate(.5);return {'name':n,'vertices':[list(v) for v in vs],'faces':[list(f) for f in fs]}
def read(path):
    d=A.openDocument(str(R/path));d.recompute()
    check('source recompute '+path,not any('Invalid' in o.State for o in d.Objects))
    ss={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape') and not o.Shape.isNull()}
    A.closeDocument(d.Name);return ss

def save(name,wood,fixed,hardware,axis,angle,status):
    d=A.newDocument(name.replace('-','_'))
    for role,ss in [('MovingWood',pose(wood,axis,angle)),('Stationary',fixed),('MovingHardwareSchematic',pose(hardware,axis,angle))]:
        for n,s in ss.items():
            o=d.addObject('PartDesign::Feature',role+'_'+n);o.Shape=s
            o.addProperty('App::PropertyString','Role');o.Role=role
    d.addProperty('App::PropertyString','StudyStatus');d.StudyStatus=status+'; MANUFACTURING BLOCKED; hardware schematic'
    d.recompute();check('saved valid solids '+name,all(o.Shape.isValid() for o in d.Objects if hasattr(o,'Shape')))
    d.saveAs(str(O/(name+'.FCStd')));A.closeDocument(d.Name)

# Hardware is topology, not a fabrication shape: single rigid bent arm per side,
# square-neck bolt keyed to arm and concentric barrel bushing in round cabinet bore.
# No extra joint/slot/translation is introduced by the bent arm.
def arms(width,axis):
    result={}
    for side,x,sgn in [('L',-6.35,-1),('R',width+3.175,1)]:
        web=prism(x,3.175,[(axis.y-12,axis.z-12),(axis.y+12,axis.z-12),(1285,593.725),(1166,593.725)])
        bore=Part.makeCylinder(6.35,8,V(x-2,axis.y,axis.z),V(1,0,0))
        web=web.cut(bore)
        flange=box(x-44.45 if sgn<0 else x,1166,593.725,47.625,119,3.175)
        result['HingeArm_'+side]=web.fuse(flange).removeSplitter()
        result['PivotBoltSchematic_'+side]=Part.makeCylinder(4.7625,19.05,V(x-8,axis.y,axis.z),V(1,0,0))
        result['ConcentricBushingSchematic_'+side]=Part.makeCylinder(6.35,19.05,V(x-8,axis.y,axis.z),V(1,0,0)).cut(Part.makeCylinder(4.7625,19.05,V(x-8,axis.y,axis.z),V(1,0,0)))
    return result

tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',C['source_head']],cwd=R,text=True).splitlines()
hashes={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in tracked if (R/p).is_file()}
angles=sorted(set(C['angles_deg']+C['early_angles_deg']+list(range(0,91,C['sweep_step_deg']))))
# Reference shell: nominal documented envelope. Interior joinery is partitioned;
# no imported third-party CAD and no unsupported exact hardware holes.
r=C['reference'];W=r['cabinet_width'];L=r['length'];z=r['rear_height'];t=r['stock'];cx=W/2
axis=V(cx,L-r['pivot_from_rear'],r['pivot_z']);p=passage(r['service_passage'])
shelf=box((W-r['shelf_width'])/2,L-r['shelf_depth'],z-t,r['shelf_width'],r['shelf_depth'],t).cut(p)
sideprofile=[(0,0),(L,0),(L,z),(L-r['shelf_depth'],z),(0,r['front_height'])]
fixed={'Shelf':shelf,'CabinetSideL':prism(0,t,sideprofile).cut(shelf),'CabinetSideR':prism(W-t,t,sideprofile).cut(shelf)}
bbw=r['backbox_width'];x0=cx-bbw/2;fh=z;low=z-9.525;top=low+r['backbox_height']
sp=[(L-r['side_lower_depth'],low),(L,low),(L,top),(L-r['side_upper_depth'],top)]
wood={'Floor':box(x0+9.525,r['floor_front_y'],fh,bbw-19.05,L-r['floor_front_y'],t).cut(p)}
for n,x in [('SideL',x0),('SideR',x0+bbw-t)]:wood[n]=prism(x,t,sp).cut(wood['Floor'])
wood['Top']=box(x0+t,L-254,top-t,bbw-2*t,254,t)
wood['Rear']=box(x0+t,L-12.7,fh+t,bbw-2*t,12.7,top-t-fh-t)
hw=arms(W,axis)
check('reference all single valid wood solids',all(s.isValid() and len(s.Solids)==1 for s in wood.values()))
check('reference moving joints no overlap',not [h for h in hits(wood,wood) if h['part']<h['obstacle']])

def sweep(label,wood,fixed,axis,floorname,shelfname):
    floor=wood[floorname];shelf=fixed[shelfname];bottom=face(floor,596.9);top=face(shelf,596.9);rows=[]
    for a in angles:
        moving=pose(wood,axis,a);f=moving[floorname];b=bottom.copy();b.rotate(axis,V(1,0,0),a)
        contact=b.common(top);h=hits(moving,fixed)
        row={'angle_deg':a,'hits':h,'floor_shelf_contact_area_mm2':contact.Area,
             'floor_shelf_penetration_mm3':f.common(shelf).Volume,
             'floor_shelf_minimum_separation_mm':f.distToShape(shelf)[0],
             'contact_bounds_mm':bounds(contact) if contact.Vertexes else None}
        rows.append(row)
        if a in C['angles_deg']:print(label,a,'hits',len(h),'bearing',round(contact.Area,5),'gap',round(row['floor_shelf_minimum_separation_mm'],5),flush=True)
        if label=='REFERENCE' and h:
            (O/'reference-failure.json').write_text(json.dumps(rows,indent=2))
            raise RuntimeError('REFERENCE FAILED: STOP before V32')
    return rows
refrows=sweep('REFERENCE',wood,fixed,axis,'Floor','Shelf')
check('reference control passes every sample',not any(q['hits'] for q in refrows))
check('reference bears then cleanly releases',refrows[0]['floor_shelf_contact_area_mm2']>0 and all(q['floor_shelf_penetration_mm3']<tol and q['floor_shelf_contact_area_mm2']<1e-6 and q['floor_shelf_minimum_separation_mm']>0 for q in refrows[1:]))
# A negative control proves the old axis reproduces the failure with the same engine.
negative=hits(pose(wood,V(cx,1270,508),.25),fixed)
check('wrong datum negative control detected',any(q['obstacle']=='Shelf' for q in negative))
for a in [0,.25,.5,1,2,15,45,90]:save('reference-'+str(a).replace('.','p'),wood,fixed,hw,axis,a,'REFERENCE WOOD KINEMATIC CONTROL PASS')
bundle={'reference':{'wood':[mesh(n,s) for n,s in wood.items()],'fixed':[mesh(n,s) for n,s in fixed.items()],'hardware':[mesh(n,s) for n,s in hw.items()],'axis':list(axis)}}
reference_bearing=face(wood['Floor'],z).common(face(shelf,z));bundle['reference']['bearing']=[mesh('Bearing',reference_bearing)]

# V32 work is below the passing reference gate. One deep-side study only.
v=C['v32'];axis32=V(*v['pivot_xyz'])
candidate=read('exports/generated/backbox-profile-v32/candidate-210.FCStd')
wood32={n:s for n,s in candidate.items() if n.startswith('Backbox')}
accepted=read('exports/generated/backbox-floor-v32/corrected-upright.FCStd')
play=read('exports/generated/matrix-cassette-v32/play.FCStd')
removed=read('exports/generated/matrix-cassette-v32/matrix-removed.FCStd')
floor=wood32['BackboxFloorV14'];b=floor.BoundBox
floor=floor.common(box(b.XMin-1,v['initial_floor_front_y'],z,b.XLength+2,b.YMax-v['initial_floor_front_y']+1,18))
# Fill the prior pair of passages locally before cutting ONE generic rectangle.
floor=floor.fuse(box(160,1158,z,280,60,18)).removeSplitter().cut(passage(v['service_passage'])).removeSplitter()
wood32['BackboxFloorV14']=floor
shelf0=play['BACKBOX_BASE'];shelf32=shelf0.cut(passage(v['service_passage'])).removeSplitter()
fixed32={n:s for n,s in removed.items() if n!='PF_BackboxCheckEnvelope' and not any(k in n.upper() for k in ('ENVELOPE','RESERVE','RESERVED','CANDIDATEPAYLOAD'))}
fixed32['BACKBOX_BASE']=shelf32
zero32={n:s for n,s in play.items() if n!='PF_BackboxCheckEnvelope' and not any(k in n.upper() for k in ('ENVELOPE','RESERVE','RESERVED','CANDIDATEPAYLOAD'))};zero32['BACKBOX_BASE']=shelf32
check('V32 eight valid single wood solids',len(wood32)==8 and all(s.isValid() and len(s.Solids)==1 for s in wood32.values()))
internal=[h for h in hits(wood32,wood32) if h['part']<h['obstacle']]
check('V32 nonoverlapping wood joints',not internal)
zero_hits=hits(wood32,zero32);gap=min(floor.distToShape(play[n])[0] for n in ['CandidateGlassChannelL','CandidateGlassChannelR'])
check('V32 upright passes with glass and matrix installed',not zero_hits and gap>=5)
# Preserve established material reserves, not the invalid pivot-related keepout.
zone_rows=[]
for name,x,wid in [('HingeL',-78,96),('HingeR',582,96)]:
    zone=box(x,1197,z,wid,105.1,18)
    retained=candidate['BackboxFloorV14'].common(zone).cut(floor).Volume
    check('V32 material reserve '+name,retained<tol);zone_rows.append({'name':name,'removed_mm3':retained})
for x in [120,480]:
    zone=Part.makeCylinder(30.7,18,V(x,1188,z))
    check('V32 lock material floor '+str(x),abs(floor.common(zone).Volume-zone.Volume)<tol)
    lower=zone.copy();lower.translate(V(0,0,-18));check('V32 lock material shelf '+str(x),abs(shelf32.common(lower).Volume-lower.Volume)<tol)
rows32=sweep('V32_INITIAL',wood32,fixed32,axis32,'BackboxFloorV14','BACKBOX_BASE')
first=next((q for q in rows32 if q['hits']),None)
# Refine first contact, keeping all later required samples as diagnostics.
refine=[]
if first:
    prior=max(q['angle_deg'] for q in rows32 if q['angle_deg']<first['angle_deg'] and not q['hits'])
    lo=prior;hi=first['angle_deg']
    for i in range(20):
        a=(lo+hi)/2;h=hits(pose(wood32,axis32,a),fixed32)
        refine.append({'angle_deg':a,'hits':h})
        if h:hi=a
        else:lo=a
    bracket=[lo,hi]
else:bracket=None
baseline={'samples':rows32,'first_collision':first,'first_collision_bracket_deg':bracket,'refinement':refine}
hw32=arms(600,axis32)
bundle['v32_initial']={'wood':[mesh(n,s) for n,s in wood32.items()], 'fixed':[mesh(n,fixed32[n]) for n in ['SIDE_L','SIDE_R','BACKBOX_BASE','CandidateGlassChannelL','CandidateGlassChannelR']], 'axis':list(axis32)}
if first:save('v32-initial-bottleneck',wood32,{n:fixed32[n] for n in set(['SIDE_L','BACKBOX_BASE']+[q['obstacle'] for q in first['hits']])},hw32,axis32,first['angle_deg'],'INITIAL FLOOR COLLISION DIAGNOSTIC; INVALID POSE')
floor=floor.common(box(-100,v['floor_front_y'],z,1000,400,18)).removeSplitter()
wood32['BackboxFloorV14']=floor
check('final floor one valid solid',floor.isValid() and len(floor.Solids)==1)
zero_hits=hits(wood32,zero32);gap=min(floor.distToShape(play[n])[0] for n in ['CandidateGlassChannelL','CandidateGlassChannelR'])
check('final upright and preferred channel gap',not zero_hits and gap>=5)
rows32=sweep('V32_SELECTED',wood32,fixed32,axis32,'BackboxFloorV14','BACKBOX_BASE')
first=next((q for q in rows32 if q['hits']),None)
check('selected deep side complete sampled fold',first is None)
channel_gaps=[]
for a in angles:
    moving=pose(wood32,axis32,a)
    channel_gaps.append({'angle_deg':a,'gap_mm':min(s.distToShape(fixed32[n])[0] for s in moving.values() for n in ['CandidateGlassChannelL','CandidateGlassChannelR'])})
check('selected preferred channel clearance throughout samples',min(q['gap_mm'] for q in channel_gaps)>=5)
refine=[];bracket=None

for a in [0,.25,.5,1,2,15,45,90]:
    if first and a>=first['angle_deg']:continue
    save('v32-'+str(a).replace('.','p'),wood32,{n:s for n,s in fixed32.items() if n in ['SIDE_L','SIDE_R','REAR','BACKBOX_BASE','CandidateGlassChannelL','CandidateGlassChannelR','PF_BasePlywood'] or n.startswith('MX_')},hw32,axis32,a,'ISOLATED V32 WOOD STUDY; VALID THROUGH SHOWN SAMPLED ANGLE')
if first:save('v32-first-bottleneck',wood32,{n:fixed32[n] for n in set(['SIDE_L','BACKBOX_BASE']+[q['obstacle'] for q in first['hits']])},hw32,axis32,first['angle_deg'],'COLLISION DIAGNOSTIC; INVALID POSE')
bearing=face(floor,z).common(face(shelf32,z));oldbearing=face(floor,z).common(face(shelf0,z))
context=['SIDE_L','SIDE_R','REAR','BACKBOX_BASE','CandidateGlassChannelL','CandidateGlassChannelR','PF_BasePlywood']
bundle['v32']={'wood':[mesh(n,s) for n,s in wood32.items()], 'fixed':[mesh(n,fixed32[n]) for n in context], 'hardware':[mesh(n,s) for n,s in hw32.items()], 'axis':list(axis32),'bearing':[mesh('Bearing',bearing)]}
# Old accepted floor witness, independent of the new generic passage.
acceptedfloor=accepted['BackboxFloorV32'];point=V(300,1220,z)
check('P is actual accepted floor and shelf bearing',acceptedfloor.isInside(point+V(0,0,.001),1e-7,True) and shelf0.isInside(point-V(0,0,.001),1e-7,True))
check('P is inside the final generic passage',not floor.isInside(point+V(0,0,.001),1e-7,True) and not shelf32.isInside(point-V(0,0,.001),1e-7,True))
old1=hits(pose({'AcceptedFloor':acceptedfloor},V(*v['accepted_pivot_xyz']),1),{'AcceptedShelf':shelf0})
new1=hits(pose({'AcceptedFloor':acceptedfloor},axis32,1),{'AcceptedShelf':shelf0})
check('accepted floor failure removed by axis interpretation alone',bool(old1) and not new1)
# Continuous shelf-release certificate: during possible Y-overlap, floor bottom
# lies on z=z0+(y-axisY)*tan(a)+(z0-axisZ)*(sec(a)-1), strictly above z0
# when y>=shelfYmin>axisY and 0<a<90. At 90 all floor lies forward of shelf.
certificates={}
for name,f,sh,ax in [('reference',wood['Floor'],shelf,axis),('v32',floor,shelf32,axis32)]:
    check(name+' continuous shelf certificate',sh.BoundBox.YMin>ax.y and f.BoundBox.ZMin>ax.z)
    f90=pose({'f':f},ax,90)['f'];check(name+' 90 floor ahead of shelf',f90.BoundBox.YMax<sh.BoundBox.YMin)
    certificates[name]={'release_begins_deg':0,'completely_clear_for':'every angle >0 through 90 degrees; infimum 0, not a finite delay',
       'last_contact':'entire upright bearing face at 0 degrees; simultaneous release, no rolling edge',
       'shelf_front_minus_axis_y_mm':sh.BoundBox.YMin-ax.y,'at_90_y_gap_mm':sh.BoundBox.YMin-f90.BoundBox.YMax}
check('every original tracked file unchanged',all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in hashes.items()))
report={'head_before':C['source_head'],'head_after':'commit containing this study; resolve with git log -1 -- studies/wpc-fold-v32',
 'engine':{'FreeCAD':A.Version(),'OpenCASCADE':Part.OCC_VERSION,'volume_threshold_mm3':tol,'distance_is_unsigned':True},
 'checks':checks,'source_hashes':hashes,'reference':{'upright_valid':True,'sampled_0_to_90_valid':True,'axis':list(axis),'pure_rotation':True,'samples':refrows,'negative_wrong_axis_hits':negative,'continuous_shelf_certificate':certificates['reference']},
 'v32_initial':baseline,
 'v32':{'channel_gaps':channel_gaps,'side_depth_mm':210,'floor_front_y_mm':v['floor_front_y'],'upright_valid':not zero_hits,'channel_gap_mm':gap,'sampled_0_to_90_valid':first is None,'samples':rows32,'first_collision':first,'first_collision_bracket_deg':bracket,'refinement':refine,'floor_shelf_bearing_mm2':bearing.Area,'bearing_before_generic_shelf_cut_mm2':oldbearing.Area,'shelf_top_area_before_mm2':face(shelf0,z).Area,'shelf_top_area_after_mm2':face(shelf32,z).Area,'material_reserves':zone_rows,'continuous_shelf_certificate':certificates['v32']},
 'previous_P':{'classification':'actual accepted V32 floor / shelf bearing; final isolated generic passage contains P; axis-only test below uses original accepted wood','old_dz_dtheta_mm_per_rad':-50,'corrected_dz_dtheta_mm_per_rad':1220-axis32.y,'old_axis_one_degree_hits':old1,'corrected_axis_one_degree_hits':new1,'conclusion':'INCOMPLETE: valid for erroneous axis; invalid as unavoidable WPC architecture conclusion'},
 'hardware':'topology validated from installation documentation; silhouettes schematic, holes/offsets require physical hardware',
 'production_geometry_changed':False,'production_pivot_changed':False,'study_pivot_interpretation_corrected':True,'generic_service_passage':True,'connector_disconnect_designed':False,'manufacturing_ready':False}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');(O/'mesh.json').write_text(json.dumps(bundle,separators=(',',':'))+'\n')
for n in ['LICENSE','NOTICE.md']:shutil.copyfile(R/n,O/n)
(O/'build-complete.json').write_text(json.dumps({'pass':True,'checks':len(checks)}))
print('WPC_STUDY_PASS',len(checks),'V32_FULL',first is None,'FIRST',first['angle_deg'] if first else None,flush=True)
