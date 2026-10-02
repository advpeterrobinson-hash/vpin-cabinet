"""Independent saved-CAD and preserved-system regression. CERN-OHL-S-2.0."""
from pathlib import Path
import sys,json,hashlib,subprocess
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_service_v32 import *
q=json.loads((O/'validation.json').read_text());motion=json.loads((O/'motion-validation.json').read_text());checks=[]
def check(n,v):
    assert v,n
    checks.append(n)
def difference(a,b):
    # The cable corridor is an overlapping compound of swept cylinders and
    # spheres, not one manufactured solid. Compare corresponding primitives;
    # a compound-wide Boolean would subtract overlapping tools from one another.
    if a.ShapeType=='Compound' and b.ShapeType=='Compound' and len(a.Solids)>1:
        aa,bb=a.childShapes(),b.childShapes()
        assert len(aa)==len(bb)
        return sum(difference(x,y) for x,y in zip(aa,bb))
    return a.cut(b).Volume+b.cut(a).Volume
check('all service screens pass',all(x['pass'] for x in q['checks']))
check('continuous certificates complete',motion['pass'] and all(x['pass'] for x in motion['checks']))
for rep in [q,motion]:
    for n,h in rep['input_sha256'].items():check('current input '+n,hashlib.sha256((R/n).read_bytes()).hexdigest()==h)
for name,cert in motion['certificates'].items():
    end=cert['range_deg'][0]
    for row in sorted(cert['intervals'],key=lambda r:r['lo']):
        check(name+' contiguous '+str(end),abs(row['lo']-end)<1e-8);end=row['hi']
    check(name+' full domain',abs(end-cert['range_deg'][1])<1e-8)
old=load(R/C['source_directory']/'play.FCStd');now=load(O/'complete-upright.FCStd')
for n,s in old.items():
    if not n.startswith('BB_'):check('unchanged current component '+n,n in now and difference(s,now[n])<1e-5)
base=load(O/'rear-closed.FCStd');rebuilt,groups,meta,blanks=build(old)
for n,s in occupied(rebuilt,groups).items():check('saved B-rep matches parametric build '+n,n in base and difference(s,base[n])<1e-5)
for state,fn in q['results']['cad_files'].items():
    ss=load(O/fn)
    check('saved valid shapes '+state,all(s.isValid() for s in ss.values()))
    if state.startswith('fold-'):
        a=float(state.split('-')[1]);expected=transform({n:s for n,s in base.items() if n.startswith('BB_')},angle=a,axis=WPC)
        for n,s in expected.items():check('rigid glass-retained fold '+state+' '+n,n in ss and difference(s,ss[n])<1e-4)
        check('playfield glass and matrix absent '+state,'CandidateGlass' not in ss and 'MatrixCarrier' not in ss)
        for n,s in load(R/C['source_directory']/'matrix-removed.FCStd').items():
            if not n.startswith('BB_'):check('fold fixed cabinet unchanged '+state+' '+n,difference(s,ss[n])<1e-5)
# Current geometry and viewer are intentionally not promoted. Prove that the
# complete previous package and offline viewer bytes are unchanged from HEAD.
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',C['source_head'],C['source_directory'],'exports/generated/viewer-v32'],cwd=R,text=True).splitlines()
for name in paths:
    raw=(R/name).read_bytes();blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    expected=subprocess.check_output(['git','rev-parse',C['source_head']+':'+name],cwd=R,text=True).strip();check('accepted package unchanged '+name,blob==expected)
current=json.loads((R/'config/current_v32.json').read_text())
check('no promotion with lock-service tradeoff',current['geometry_directory']==C['source_directory'] and not q['promoted'])
check('no final hinge drilling or manufacturing release',not C['final_hinge_drilling_released'] and not C['manufacturing_ready'])
(O/'regression-validation.json').write_text(json.dumps({'pass':True,'checks':checks,'input_sha256':{str(path.relative_to(R)):hashlib.sha256(path.read_bytes()).hexdigest() for path in [O/'validation.json',O/'motion-validation.json',R/'tools/check_backbox_service_v32.py']},'promoted':False,'manufacturing_ready':False},indent=2)+'\n')
print('BACKBOX_SERVICE_REGRESSION_PASS',len(checks),flush=True)
