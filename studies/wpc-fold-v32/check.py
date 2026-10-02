"""Independent saved-solid, datum, scope and continuous-motion checks. CERN-OHL-S-2.0."""
from pathlib import Path
import json, hashlib, math, subprocess
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[2];C=json.loads((Path(__file__).parent/'parameters.json').read_text());O=R/C['output_directory'];r=json.loads((O/'validation.json').read_text());V=A.Vector;checks=[]
def check(n,v):
    assert v,n
    checks.append(n)
check('source head exists',subprocess.check_output(['git','rev-parse',C['source_head']],cwd=R,text=True).strip()==C['source_head'])
for p,h in r['source_hashes'].items():
    data=(R/p).read_bytes();check('unchanged '+p,hashlib.sha256(data).hexdigest()==h)
    # Compare actual bytes with the starting Git blob, not just a pre-run snapshot.
    expected=subprocess.check_output(['git','rev-parse',C['source_head']+':'+p],cwd=R,text=True).strip()
    check('starting blob '+p,hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==expected)
check('manufacturing not released',not r['manufacturing_ready'] and not r['production_geometry_changed'])
check('depth order obeyed; 180 never tested',r['v32']['side_depth_mm']==210)
check('single pure-rotation architecture',r['reference']['pure_rotation'] and r['reference']['axis']==[279.4,1066.8,508])
check('same source of incorrect datum reproduced',r['previous_P']['old_dz_dtheta_mm_per_rad']==-50 and abs(r['previous_P']['corrected_dz_dtheta_mm_per_rad']-153.2)<1e-7)
check('negative control is meaningful',r['reference']['negative_wrong_axis_hits'] and r['previous_P']['old_axis_one_degree_hits'] and not r['previous_P']['corrected_axis_one_degree_hits'])
for key in ['reference','v32']:
    a={q['angle_deg'] for q in r[key]['samples']};check(key+' required samples',all(t in a for t in C['angles_deg']+C['early_angles_deg']))
    check(key+' sampled clear',all(not q['hits'] and q['floor_shelf_penetration_mm3']<1e-6 for q in r[key]['samples']))
    check(key+' bearing release',r[key]['samples'][0]['floor_shelf_contact_area_mm2']>0 and all(q['floor_shelf_contact_area_mm2']<1e-6 and q['floor_shelf_minimum_separation_mm']>0 for q in r[key]['samples'][1:]))

def read(file):
    d=A.openDocument(str(R/file));d.recompute();check('recompute '+file,not any('Invalid' in o.State for o in d.Objects))
    ss={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape') and not o.Shape.isNull()};A.closeDocument(d.Name);return ss
ref=read(C['output_directory']+'/reference-0.FCStd');v32=read(C['output_directory']+'/v32-0.FCStd')
removed=read('exports/generated/matrix-cassette-v32/matrix-removed.FCStd')
allfixed={n:s for n,s in removed.items() if n!='PF_BackboxCheckEnvelope' and not any(k in n.upper() for k in ('ENVELOPE','RESERVE','RESERVED','CANDIDATEPAYLOAD'))}
allfixed['BACKBOX_BASE']=v32['Stationary_BACKBOX_BASE']
# Independently verify the full motion by a distance Lipschitz bound, not just samples.
# For midpoint angle a and interval half-width h, each moving point travels at
# most R*h radians. A separation exceeding that bound certifies the entire interval.
# Hardware silhouettes are not part of the clearance claim.
def minimum(moving,fixed):
    pairs=[]
    for n,s in moving.items():
        for m,t in fixed.items():
            b,c=s.BoundBox,t.BoundBox
            lb=math.sqrt(sum(max(0,getattr(b,k+'Min')-getattr(c,k+'Max'),getattr(c,k+'Min')-getattr(b,k+'Max'))**2 for k in 'XYZ'))
            pairs.append((lb,n,m,s,t))
    best=math.inf;pair=None
    for lb,n,m,s,t in sorted(pairs,key=lambda q:q[0]):
        if lb>=best:break
        d=s.distToShape(t)[0]
        if d<best:best=d;pair=[n,m]
    return best,pair
cert={}
for key,ss,ax in [('reference',ref,V(279.4,1066.8,508)),('v32',v32,V(300,1066.8,508))]:
    moving={n:s for n,s in ss.items() if n.startswith('MovingWood_')}
    fixed={n:s for n,s in ss.items() if n.startswith('Stationary_')} if key=='reference' else allfixed
    check(key+' valid single solid members',all(s.isValid() and len(s.Solids)==1 for s in moving.values()))
    # Mirror symmetry of every assembled moving wood volume.
    M=A.Matrix();M.A11=-1;M.A14=2*ax.x
    compound=Part.makeCompound(list(moving.values()));mirror=compound.transformGeometry(M)
    check(key+' moving wood symmetric',compound.cut(mirror).Volume+mirror.cut(compound).Volume<1e-4)
    radius=max(math.hypot(y-ax.y,z-ax.z) for s in moving.values() for y in [s.BoundBox.YMin,s.BoundBox.YMax] for z in [s.BoundBox.ZMin,s.BoundBox.ZMax])
    # At upright the only zero distances are floor/shelf and floor/cabinet-side
    # bearing. For 0..0.001 degrees their points remain Y>axisY and Z>=596.9,
    # while all stationary cabinet wood is Z<=596.9. All other pairs must be
    # separated by more than the maximum displacement on that tiny interval.
    initial=[];maxshift=radius*math.radians(.001)
    for n,s in moving.items():
        for m,t in fixed.items():
            # Cheap AABB lower bound then exact near-contact only.
            b,c=s.BoundBox,t.BoundBox
            lb=math.sqrt(sum(max(0,getattr(b,k+'Min')-getattr(c,k+'Max'),getattr(c,k+'Min')-getattr(b,k+'Max'))**2 for k in 'XYZ'))
            if lb>maxshift+1e-7:continue
            d=s.distToShape(t)[0]
            if d>maxshift+1e-7:continue
            check(key+' early bearing pair '+n+'/'+m,any(k in m for k in ['Shelf','Side','SIDE_','BACKBOX_BASE','REAR']))
            check(key+' early bearing z cap '+m,t.BoundBox.ZMax<=596.9+1e-7 and s.BoundBox.ZMin>=596.9-1e-7)
            check(key+' early bearing positive derivative '+n,s.BoundBox.YMin-maxshift>ax.y)
            check(key+' early rise over whole interval '+n,(s.BoundBox.YMin-ax.y)*math.cos(math.radians(.001))-(s.BoundBox.ZMax-ax.z)*math.sin(math.radians(.001))>0)
            initial.append([n,m])
    stack=[(.001,90.)];leaves=[];evaluated=0
    while stack:
        lo,hi=stack.pop();mid=(lo+hi)/2;sh={n:s.copy() for n,s in moving.items()}
        for s in sh.values():s.rotate(ax,V(1,0,0),mid)
        d,pair=minimum(sh,fixed);bound=radius*math.radians((hi-lo)/2);evaluated+=1
        if d>bound+1e-6:leaves.append({'lo_deg':lo,'hi_deg':hi,'minimum_midpoint_mm':d,'motion_bound_mm':bound,'pair':pair})
        else:
            check(key+' continuous interval does not collapse',hi-lo>1e-7)
            stack.extend([(lo,mid),(mid,hi)])
        if evaluated%50==0:print('CONTINUOUS',key,evaluated,'certified',len(leaves),'pending',len(stack),flush=True)
    cert[key]={'valid':True,'range_deg':[0,90],'method':'analytical bearing release 0..0.001; adaptive distance/Lipschitz certificate .001..90','radius_bound_mm':radius,'evaluations':evaluated,'early_contact_pairs':initial,'intervals':leaves}
    check(key+' complete continuous coverage',abs(sum(q['hi_deg']-q['lo_deg'] for q in leaves)-89.999)<1e-7)
    print('CONTINUOUS_PASS',key,evaluated,flush=True)
# Reopen fold endpoints and compare with the actual transform.
for a in [45,90]:
    ss=read(C['output_directory']+'/v32-'+str(a)+'.FCStd')
    for n,s in v32.items():
        if not n.startswith('MovingWood_'):continue
        expected=s.copy();expected.rotate(V(300,1066.8,508),V(1,0,0),a)
        check('saved rigid pose '+str(a)+' '+n,ss[n].cut(expected).Volume+expected.cut(ss[n]).Volume<1e-5)
(O/'regression-validation.json').write_text(json.dumps({'pass':True,'checks':checks,'continuous_motion':cert,'manufacturing_ready':False},indent=2)+'\n')
print('WPC_REGRESSION_PASS',len(checks),flush=True)
