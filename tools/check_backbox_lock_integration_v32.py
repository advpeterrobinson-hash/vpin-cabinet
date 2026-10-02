"""Independent saved-CAD regression for complete backbox promotion. CERN-OHL-S-2.0."""
from backbox_lock_integration_v32 import *
import hashlib,subprocess
q=json.loads((O/'validation.json').read_text());checks=[]
def check(n,v):
    assert v,n
    checks.append(n)
def delta(a,b):
    if a.ShapeType=='Compound' and b.ShapeType=='Compound' and len(a.Solids)>1:
        aa,bb=a.childShapes(),b.childShapes();assert len(aa)==len(bb)
        return sum(delta(x,y) for x,y in zip(aa,bb))
    return a.cut(b).Volume+b.cut(a).Volume
check('all integration checks passed',all(c['pass'] for c in q['checks']))
for n,h in q['input_sha256'].items():check('fresh '+n,hashlib.sha256((R/n).read_bytes()).hexdigest()==h)
for key in ['continuous_new_locks_fold','continuous_old_backbox_vs_new_shelf_hardware']:
    c=q['results'][key];end=c['range_deg'][0]
    for lo,hi in c['intervals']:check('continuous interval '+key+' '+str(lo),abs(end-lo)<1e-8);end=hi
    check('full 90 degrees '+key,end==90)
for side,c in q['results']['continuous_door_vs_locks'].items():
    end=0
    for lo,hi in c['intervals']:check('continuous door '+side+' '+str(lo),abs(end-lo)<1e-8);end=hi
    check('full 100 degree door '+side,end==100)
old=load(R/C['cabinet_source']/'play.FCStd');p0,g,meta,blanks=service.build(old);p,shelf=bore_reference(p0,old['BACKBOX_BASE']);eng,fix,_=build_locks();eng=with_tethers(eng,False);park=with_tethers(build_locks(True)[0],True)
expected={**service.occupied(p,g),**eng,**fix,**{'BB_FlexCorridor'+s:service.flex(s,0)[0] for s in ['L','R']},'BACKBOX_BASE':shelf}
now=load(O/'play.FCStd')
for n,s in expected.items():check('saved current matches source '+n,n in now and delta(s,now[n])<1e-5)
for n,s in old.items():
    if not n.startswith('BB_') and n!='BACKBOX_BASE':check('current fixed systems unchanged '+n,n in now and delta(s,now[n])<1e-5)
for n,s in p0.items():
    if n!='BB_Floor' and g[n] not in ['optional','zone','unlockedL','unlockedR']:check('accepted service part unchanged '+n,delta(s,now[n])<1e-5)
for state,fn in q['results']['saved_poses'].items():
    ss=load(O/fn);base=load(R/C['cabinet_source']/fn)
    check('all valid saved solids '+state,all(s.isValid() for s in ss.values()))
    for n,s in base.items():
        if not n.startswith('BB_') and n!='BACKBOX_BASE':check('state fixed component preserved '+state+' '+n,delta(s,ss[n])<1e-5)
    if state=='BACKBOX FOLD':
        fold={**service.occupied(p,g),**park,**{'BB_FlexCorridor'+s:service.flex(s,0)[0] for s in ['L','R']}}
        for n,s in transform(fold,angle=90,axis=WPC).items():check('retained populated fold '+n,delta(s,ss[n])<1e-4)
        check('only required main glass and matrix removed','CandidateGlass' not in ss and 'MatrixCarrier' not in ss)
# Keep immutable historical reports and source CAD; viewer is intentionally updated.
for folder in [C['service_source'],C['cabinet_source']]:
    for n in subprocess.check_output(['git','ls-tree','-r','--name-only',C['source_head'],folder],cwd=R,text=True).splitlines():
        b=(R/n).read_bytes();expectedhash=subprocess.check_output(['git','rev-parse',C['source_head']+':'+n],cwd=R,text=True).strip();check('historical artifact unchanged '+n,hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==expectedhash)
check('current mesh hash',hashlib.sha256((O/'mesh.json').read_bytes()).hexdigest()==q['results']['mesh_sha256'])
check('WPC datum and two independent locks',list(WPC)==[300,1066.8,508] and C['lock_centers_xy_mm']==[[130,1260],[470,1260]])
for x,y in C['lock_centers_xy_mm']:
    for part,key in [('BB_Floor','reference_floor_bore_diameter_mm'),('BACKBOX_BASE','reference_shelf_bore_diameter_mm')]:
        fs=[f for f in now[part].Faces if isinstance(f.Surface,Part.Cylinder) and abs(f.CenterOfMass.x-x)<1e-5 and abs(f.CenterOfMass.y-y)<1e-5]
        check('reference bore matches declared diameter '+part+str(x),any(abs(f.Surface.Radius-C[key]/2)<1e-7 for f in fs))
for side in ['L','R']:
    pad=now['BB_UprightLock'+side+'ParkingPad0'].BoundBox
    check('stock parking pads match parameters '+side,abs(pad.XLength-C['parking_block_size_mm'][0])<1e-7 and abs(pad.YLength-C['parking_block_size_mm'][1])<1e-7 and abs(2*pad.ZLength-C['parking_block_size_mm'][2])<1e-7)
search=json.loads((O/'search.json').read_text())
check('wood reserve matches declared radius',all(abs(row['floor_reserve_area_mm2']-math.pi*C['wood_reserve_radius_mm']**2)<1e-5 for row in search['selected']))
check('no manufacturing or hardware release',not C['manufacturing_ready'] and not C['final_hinge_drilling_released'])
(O/'regression-validation.json').write_text(json.dumps({'pass':True,'checks':checks,'input_sha256':{'exports/generated/backbox-lock-integration-v32/validation.json':hashlib.sha256((O/'validation.json').read_bytes()).hexdigest(),'tools/check_backbox_lock_integration_v32.py':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},'manufacturing_ready':False},indent=2)+'\n')
print('BACKBOX_LOCK_REGRESSION_PASS',len(checks),flush=True)
