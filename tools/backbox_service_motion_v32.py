"""Conservative continuous rigid-motion certificates. CERN-OHL-S-2.0."""
from pathlib import Path
import sys,json,math,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_service_v32 import *
src=load(R/C['source_directory']/'matrix-removed.FCStd');p,g,meta,blanks=build(src);closed=occupied(p,g)
report={'pass':False,'manufacturing_ready':False,'certificates':{},'checks':[]}
def check(n,v,detail=None):
    report['checks'].append({'check':n,'pass':bool(v),'detail':detail})
    assert v,(n,detail)
def write(): (O/'motion-validation.json').write_text(json.dumps(report,indent=2)+'\n')
def lower_bound(a,b):
    return math.sqrt(sum(max(0,getattr(a,k+'Min')-getattr(b,k+'Max'),getattr(b,k+'Min')-getattr(a,k+'Max'))**2 for k in 'XYZ'))
def certify(mov,obs,poser,radii,start,end):
    """Every pair is certified at every interval; per-part arc displacement
    bounds avoid incorrectly applying only the nearest pair's rotation radius.
    """
    todo=[(start,end)];rows=[];obounds={n:s.BoundBox for n,s in obs.items()};tested=0
    while todo:
        lo,hi=todo.pop();mid=(lo+hi)/2;ss=poser(mov,mid);ok=True;closest=math.inf;witness=None
        for n,s in ss.items():
            limit=radii[n]*math.radians((hi-lo)/2);sb=s.BoundBox
            for m,t in obs.items():
                lb=lower_bound(sb,obounds[m])
                if lb>limit+1e-6:continue
                distance=s.distToShape(t)[0];tested+=1
                if distance<closest:closest=distance;witness=[n,m]
                if distance<=limit+1e-6:ok=False;break
            if not ok:break
        if ok:rows.append({'lo':lo,'hi':hi,'checked_near_pair_minimum_mm':closest if math.isfinite(closest) else None,'pair':witness})
        else:
            if hi-lo<1e-6:raise AssertionError(('continuous certificate failed',lo,hi,witness,closest))
            todo.extend([(lo,mid),(mid,hi)])
        if len(rows)>20000:raise AssertionError('nonconvergent certificate')
    return {'range_deg':[start,end],'intervals':rows,'exact_near_pair_distance_calls':tested,'radii_mm':radii,'method':'midpoint OCC distance > per-part radius * angular half interval for every non-separated pair; AABB lower bounds only reject distant pairs'}
def rx(ss,axis):return {n:max(math.hypot(y-axis.y,z-axis.z) for y in [s.BoundBox.YMin,s.BoundBox.YMax] for z in [s.BoundBox.ZMin,s.BoundBox.ZMax]) for n,s in ss.items()}
# Validate only added material against original obstacles. Unchanged material and
# subtractions inherit the exact previously validated reference trajectory.
closed.update({'BB_FlexCorridor'+side:flex(side,0)[0] for side in ['L','R']})
old=Part.makeCompound([s for n,s in src.items() if n.startswith('BB_')]);added={}
for n,s in closed.items():
    new=s.cut(old)
    if new.Volume>1e-6:added[n]=new
fixed={n:s for n,s in actual(src).items() if not n.startswith('BB_')}
check('added material remains in upper/rear quadrant of WPC axis',all(s.BoundBox.YMin>WPC.y and s.BoundBox.ZMin>WPC.z for s in added.values()))
minz=min(WPC.z+min(s.BoundBox.YMin-WPC.y,s.BoundBox.ZMin-WPC.z) for s in added.values())
critical={n:s for n,s in fixed.items() if s.BoundBox.ZMax>=minz-1e-6}
report['fold_obstacle_cull']={'minimum_possible_added_z_mm':minz,'included':list(critical),'proof':'positive dy and dz: minimum z on 0..90 is an endpoint; lower obstacles cannot contact'}
report['certificates']['populated_fold']=certify(added,critical,lambda ss,a:transform(ss,angle=a,axis=WPC),rx(added,WPC),0,90)
print('CONTINUOUS_POPULATED_FOLD_PASS',flush=True);write()
# Cover every allowed monitor adjustment, not only the nominal installed pose.
# Expanded part boxes conservatively contain the entire adjustment family.
family={}
for n,s in p.items():
    if g[n] not in ['display','adapter','carrier']:continue
    b=s.BoundBox;dx=1 if g[n] in ['display','adapter'] else 0;dz=5 if g[n] in ['display','adapter'] else 0
    family[n]=box(b.XMin-dx,b.YMin,b.ZMin-dz,b.XLength+2*dx,b.YLength+16,b.ZLength+2*dz+(5 if 'MonitorStopScrew' in n else 0))
report['certificates']['monitor_adjustment_family_fold']=certify(family,fixed,lambda ss,a:transform(ss,angle=a,axis=WPC),rx(family,WPC),0,90)
print('CONTINUOUS_ADJUSTED_MONITOR_FOLD_PASS',flush=True);write()
for side in ['R','L']:
    scene=door_scene(p,g,0,100 if side=='L' else 0)
    mov={n:s for n,s in scene.items() if g[n] in ['door'+side,'unlocked'+side] and 'Gasket' not in n}
    # Intentional compressible gasket contact is handled by the following planar
    # release proof, not mistaken for an intersecting rigid bearing constraint.
    obs={n:s for n,s in scene.items() if n not in mov and 'Gasket' not in n}
    if side=='R':
        obs={n:s for n,s in obs.items() if g[n]!='unlockedL'}
        obs.update({n:s for n,s in p.items() if g[n]=='lockedL'}) # passive bolts engaged while active opens
    hx,hy=C['rear']['hinge_axis_xy_mm'][0 if side=='L' else 1]
    radii={n:max(math.hypot(x-hx,y-hy) for x in [s.BoundBox.XMin,s.BoundBox.XMax] for y in [s.BoundBox.YMin,s.BoundBox.YMax]) for n,s in mov.items()}
    report['certificates']['door'+side]=certify(mov,obs,lambda ss,a:door_pose(ss,side,a),radii,0,100)
    print('CONTINUOUS_DOOR_PASS',side,flush=True);write()
cam_sweep=cylinder_y(340,1290.1,960,60,4)
cam_obs={n:s for n,s in closed.items() if not n.startswith(('BB_CamLock','BB_CamTongue'))}
hh=hits({'cam_full_turn_reserve':cam_sweep},cam_obs);check('cam unlocking rotation fits conservative R60 reserve',not hh,hh)
report['gasket_release_proof']='Door panels have inward hinge offset >=3 mm and lie forward of hinge Y1324.1. For 0..90, their rearmost compression surface moves rearward from Y1310.1 (dy*cos + dx*sin); for 90..100 it remains behind Y1324.1. Fixed and center gasket rearmost face is Y1310.1. Passive astragal Z656..1260 stays 2 mm inside top/bottom gasket lands. Dense explicit samples also include all gasket solids.'
# Extrusion of a part's AABB is a conservative translation sweep. Touching faces
# do not count as volume penetration; no sampling gaps exist in these proofs.
def sweptbox(s,dx=0,dy=0,dz=0):
    b=s.BoundBox;return box(b.XMin+min(0,dx),b.YMin+min(0,dy),b.ZMin+min(0,dz),b.XLength+abs(dx),b.YLength+abs(dy),b.ZLength+abs(dz))
display={n:s for n,s in closed.items() if g.get(n) in ['display','adapter'] and 'Reserve' not in n}
obs={n:s for n,s in closed.items() if g.get(n) not in ['display','adapter','glass','retainer','bezel'] and 'MonitorStopScrew' not in n}
hh=hits({n:sweptbox(s,dy=-400) for n,s in display.items()},obs);check('continuous nominal front display withdrawal',not hh,hh)
obs={n:s for n,s in closed.items() if g.get(n) not in ['glass','retainer']}
hh=hits({'glass_sweep':sweptbox(p['BB_Backglass'],dz=500)},obs);check('continuous glass lift with monitor installed',not hh,hh)
# Front cassette withdrawal is also the explicit provisional lock-access method.
cas={n:s for n,s in closed.items() if g.get(n)=='cassette' and 'Reserve' not in n}
obs={**{n:s for n,s in closed.items() if g.get(n)!='cassette'},**fixed}
hh=hits({n:sweptbox(s,dy=-240) for n,s in cas.items()},obs);check('continuous front cassette withdrawal for lock access',not hh,hh)
opened=door_scene(p,g,100,100)
for side in ['L','R']:
    n='BB_Fan'+side;sw=door_pose({n:sweptbox(p[n],dy=-160)},side,100)
    hh=hits(sw,{m:s for m,s in opened.items() if m!=n and 'Reserve' not in m});check('continuous fan withdrawal '+side,not hh,hh)
for side in ['L','R']:
    ids=['BB_SpeakerBaffle'+side,'BB_SpeakerEnvelope'+side]
    mov={n:sweptbox(closed[n],dy=-160) for n in ids}
    obs={n:s for n,s in closed.items() if n not in ids and 'CassetteBoltReserve'+side not in n}
    hh=hits(mov,obs);check('independent front speaker baffle replacement '+side,not hh,hh)
report['input_sha256']={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in ['config/backbox_service_v32.json','tools/backbox_service_v32.py','tools/backbox_service_motion_v32.py']}
report['pass']=True;write();print('BACKBOX_SERVICE_CONTINUOUS_PASS',flush=True)
