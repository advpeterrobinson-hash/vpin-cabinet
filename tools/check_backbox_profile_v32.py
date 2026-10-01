"""Independent saved-CAD, stop-gate and regression checks. CERN-OHL-S-2.0."""
from pathlib import Path
import hashlib,json,math,subprocess
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[1];c=json.loads((R/'config/backbox_profile_v32.json').read_text());O=R/c['output_directory'];r=json.loads((O/'validation.json').read_text());checks=[]
def check(n,v):
    assert v,n
    checks.append({'check':n,'pass':True})
def gates(report):
    assert report['selected_depth_mm'] is None
    assert report['coarse_envelope_authority']=='REFERENCE ONLY'
    assert report['manufacturing_ready'] is False
    assert [x['bottom_depth_mm'] for x in report['candidates']]==[210,200,190,180]
    for row in report['candidates']:
        valid=not row['zero_hits'] and row['channel_clearance_mm']>=3
        assert row['zero_valid']==valid
        assert not row['fold_performed'] and not row['fold_samples']
        assert row['fold_status']==('WARNING_BELOW_190_STOP' if row['bottom_depth_mm']==180 else 'REJECTED_ZERO')
gates(r);check('owner stop and no false fold/selection claims',True)
for change in ('select180','claim190valid','foldInvalidZero','manufacture'):
    bad=json.loads(json.dumps(r))
    if change=='select180':bad['selected_depth_mm']=180
    if change=='claim190valid':bad['candidates'][2]['zero_valid']=True
    if change=='foldInvalidZero':bad['candidates'][0]['fold_performed']=True
    if change=='manufacture':bad['manufacturing_ready']=True
    try:gates(bad)
    except AssertionError:pass
    else:raise AssertionError('negative gate failed '+change)
    check('negative control '+change,True)
tree=subprocess.check_output(['git','ls-tree','-r',c['source_head']],cwd=R,text=True)
blobs={s.split('\t',1)[1]:s.split('\t',1)[0].split()[2] for s in tree.splitlines()}
for p,h in r['source_hashes'].items():
    data=(R/p).read_bytes()
    check('accepted bytes '+p,hashlib.sha256(data).hexdigest()==h and hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blobs[p])
allowed={'README.md','config/backbox_profile_v32.json','tools/backbox_profile_v32_entry.py','tools/check_backbox_profile_v32.py','tools/render_backbox_profile_v32.py','docs/BACKBOX_PROFILE_V32.md'}
changed=subprocess.check_output(['git','diff',c['source_head'],'--name-only'],cwd=R,text=True).splitlines()
check('scope restricted to backbox study',all(p in allowed or p.startswith(c['output_directory']+'/') for p in changed))
play=A.openDocument(str(R/'exports/generated/matrix-cassette-v32/play.FCStd'))
M=A.Matrix();M.A11=-1;M.A14=600
for row in r['candidates']:
    depth=row['bottom_depth_mm'];d=A.openDocument(str(O/f'candidate-{depth}.FCStd'));d.recompute()
    wood=[o for o in d.Objects if hasattr(o,'Role') and o.Role=='WOOD_CANDIDATE']
    check(f'{depth} single solid members',len(wood)==8 and all(o.Shape.isValid() and len(o.Shape.Solids)==1 for o in wood))
    for i,a in enumerate(wood):
        for b in wood[i+1:]:check(f'{depth} internal pair {a.Name}/{b.Name}',a.Shape.common(b.Shape).Volume<1e-6)
    left=d.getObject('BackboxLeftSideV14').Shape;right=d.getObject('BackboxRightSideV14').Shape
    mirrored=left.transformGeometry(M)
    check(f'{depth} mirrored sides',right.cut(mirrored).Volume+mirrored.cut(right).Volume<1e-5)
    floor=d.getObject('BackboxFloorV14').Shape
    check(f'{depth} derived floor depth',abs(floor.BoundBox.YLength-(depth-6))<1e-6)
    clearance=min(floor.distToShape(play.getObject(n).Shape)[0] for n in ('CandidateGlassChannelL','CandidateGlassChannelR'))
    check(f'{depth} independent channel clearance',abs(clearance-row['channel_clearance_mm'])<1e-7)
    for hit in row['zero_hits']:
        val=d.getObject(hit['part']).Shape.common(play.getObject(hit['obstacle']).Shape).Volume
        check(f'{depth} exact rejection {hit["part"]}/{hit["obstacle"]}',abs(val-hit['volume_mm3'])<1e-5)
    if depth==180:
        for a in wood:
            for b in play.Objects:
                if not hasattr(b,'Shape') or b.Name=='PF_BackboxCheckEnvelope' or any(k in b.Name.upper() for k in ('ENVELOPE','RESERVE','RESERVED','CANDIDATEPAYLOAD')):continue
                if a.Shape.BoundBox.intersect(b.Shape.BoundBox):check(f'warning 180 zero {a.Name}/{b.Name}',a.Shape.common(b.Shape).Volume<1e-6)
    check(f'{depth} nominal stock',abs(floor.BoundBox.ZLength-18)<1e-7)
    check(f'{depth} side height',abs(left.BoundBox.ZLength-723.9)<1e-6)
    check(f'{depth} no invalid selected status','NO SELECTED PROFILE' in d.ApprovalStatus)
    z=596.9;bottom=[f for f in floor.Faces if abs(f.CenterOfMass.z-z)<1e-7 and abs(f.normalAt(0,0).z)>.99][0]
    shelf=play.getObject('BACKBOX_BASE').Shape
    top=Part.makeCompound([f for f in shelf.Faces if abs(f.CenterOfMass.z-z)<1e-7 and abs(f.normalAt(0,0).z)>.99])
    check(f'{depth} bearing independently measured',abs(bottom.common(top).Area-row['bearing_mm2'])<1e-6)
    holes=[w for w in bottom.Wires if not w.isSame(bottom.OuterWire)]
    web=min([w.distToShape(bottom.OuterWire)[0] for w in holes]+[holes[0].distToShape(holes[1])[0]])
    check(f'{depth} planar ligament',abs(web-row['minimum_planar_ligament_mm'])<1e-6)
    p=A.Vector(*r['shelf_kinematic_incompatibility']['point_xyz_mm'])
    check(f'{depth} shared bearing witness',floor.isInside(p+A.Vector(0,0,.001),1e-7,True) and shelf.isInside(p-A.Vector(0,0,.001),1e-7,True))
    for side,ps in row['fastener_positions_xyz_mm'].items():
        check(f'{depth} {side} fasteners avoid future hinge band',all(p[1]<=1177 and p[1]>=floor.BoundBox.YMin+25 for p in ps))
        check(f'{depth} {side} fastener pitch',all(ps[i+1][1]-ps[i][1]>=50 for i in range(len(ps)-1)))
    inv=row['mass']['inventory'];wm=sum(x['kg'] for x in inv if x['item'].startswith('Backbox'))
    check(f'{depth} CAD wood mass',abs(wm-sum(o.Shape.Volume for o in wood)*650/1e9)<1e-7)
    total=sum(x['kg'] for x in inv)
    cg=[sum(x['kg']*x['cg_xyz_mm'][j] for x in inv)/total for j in range(3)]
    check(f'{depth} mass budget sums',abs(total-row['mass']['total_kg'])<1e-9 and all(abs(cg[j]-row['mass']['cg_xyz_mm'][j])<1e-7 for j in range(3)))
    for q in row['mass']['loadcases']:
        check(f'{depth} force balance {q["angle_deg"]}',abs(q['upward_grip_force_N']+2*q['reaction_each_hinge_N']-total*9.80665)<1e-7)
    A.closeDocument(d.Name)
A.closeDocument(play.Name)
check('local derivative points down into shelf',r['shelf_kinematic_incompatibility']['dz_dtheta_mm_per_radian']==-50)
check('no unapproved successful fold files',not list(O.glob('*fold*.FCStd')))
(O/'regression-validation.json').write_text(json.dumps({'checks':checks,'all_pass':True,'selected_depth_mm':None,'manufacturing_ready':False},indent=2)+'\n')
print('BACKBOX_PROFILE_REGRESSION_PASS',len(checks),flush=True)
