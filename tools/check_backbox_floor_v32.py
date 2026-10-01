"""Reopen floor integration; enforce immutable V32 and motion gates. CERN-OHL-S-2.0."""
from pathlib import Path
import hashlib,json,subprocess
import FreeCAD as A
import Part

R=Path(__file__).resolve().parents[1]; c=json.loads((R/'config/backbox_floor_v32.json').read_text());O=R/c['output_directory'];r=json.loads((O/'validation.json').read_text());checks=[]
def check(name,value):
    assert value,name
    checks.append({'check':name,'pass':True})
def same(a,b):return a.cut(b).Volume+b.cut(a).Volume<1e-6
def validate_gates(report):
    f=report['fold'];z=report['zero']
    assert z['valid'] and not z['new_hits'] and z['new_unintended_volume_mm3']==0
    assert report['floor']['minimum_channel_clearance']['mm']>=5
    assert f['performed'] and len(f['samples'])==91 and [p['angle_deg'] for p in f['samples']]==list(range(91))
    assert f['prerequisites']==['GLASS_REMOVED','MATRIX_REMOVED']
    for angle in (45,90):
        clear=not any(p['angle_deg']<=angle and (p['A_wood_cabinet_wood'] or p['B_wood_glass_channels'] or p['other_physical_components']) for p in f['samples'])
        assert f['review_45_90_eligible'][str(angle)]==clear
    if not f['baseline_clear']:
        assert f['matrix_supports_evaluated'] is False and f['matrix_supports_new_conflict'] is None and not f['matrix_support_samples']
    assert report['coarse_envelope_authority']=='REFERENCE ONLY' and report['manufacturing_ready'] is False
validate_gates(r);check('explicit zero, baseline fold and support sequencing gates',True)
for key,value in [('zero',False),('45',True),('matrix',False),('prerequisite',[])]:
    wrong=json.loads(json.dumps(r))
    if key=='zero':wrong['zero']['valid']=value
    elif key=='45':wrong['fold']['review_45_90_eligible']['45']=value
    elif key=='matrix':wrong['fold']['matrix_supports_new_conflict']=value
    else:wrong['fold']['prerequisites']=value
    try:validate_gates(wrong)
    except AssertionError:pass
    else:raise AssertionError('Negative gate control failed: '+key)
    check('negative false motion approval rejected: '+key,True)

tree=subprocess.check_output(['git','ls-tree','-r',c['source_head']],cwd=R,text=True)
blobids={line.split('\t',1)[1]:line.split('\t',1)[0].split()[2] for line in tree.splitlines() if '\t' in line}
check('repository object format for byte verification',subprocess.check_output(['git','rev-parse','--show-object-format'],cwd=R,text=True).strip()=='sha1')
for p,h in r['source_hashes'].items():
    data=(R/p).read_bytes()
    check('accepted bytes preserved: '+p,hashlib.sha256(data).hexdigest()==h)
    check('accepted requested-HEAD blob: '+p,hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blobids[p])
allowed={'README.md','config/backbox_floor_v32.json','docs/BACKBOX_FLOOR_V32.md','tools/backbox_floor_v32_entry.py','tools/check_backbox_floor_v32.py','tools/render_backbox_floor_v32.py'}
changed=subprocess.check_output(['git','diff',c['source_head'],'--name-only'],cwd=R,text=True).splitlines()
check('only scoped floor integration and associated records changed',all(p in allowed or p.startswith(c['output_directory']+'/') for p in changed))

old=A.openDocument(str(R/c['source_play']));new=A.openDocument(str(O/'corrected-upright.FCStd'));new.recompute()
for obj in old.Objects:
    if hasattr(obj,'Shape'):
        check('accepted CAD component unchanged: '+obj.Name,same(obj.Shape,new.getObject(obj.Name).Shape))
check('accepted wooden pivot remains live',bool(new.getObject('PF_WoodDowel').ExpressionEngine))
check('coarse reference explicit in proposed CAD',new.getObject('PF_BackboxCheckEnvelope').CollisionAuthority=='REFERENCE ONLY')
floor=new.getObject('BackboxFloorV32').Shape
check('saved corrected floor single valid 18 mm solid',floor.isValid() and len(floor.Solids)==1 and abs(floor.BoundBox.ZLength-18)<1e-7)
for n in ('CandidateGlassChannelL','CandidateGlassChannelR'):
    s=old.getObject(n).Shape
    check('saved floor-channel positive-volume zero: '+n,floor.common(s).Volume<1e-6)
    check('saved floor-channel clearance meets 5 mm: '+n,floor.distToShape(s)[0]>=5)
    ad=A.openDocument(str(R/c['source_backbox']));original=ad.getObject('BackboxFloorV14').Shape
    check('negative old floor reproduces rejected overlap: '+n,original.common(s).Volume>937)
    A.closeDocument(ad.Name)
check('saved glass pane itself clear',floor.common(old.getObject('CandidateGlass').Shape).Volume<1e-6)
ww=r['floor']['minimum_channel_clearance_witness_xyz_mm']
check('review section shifted witness lies on actual floor and channel',
      Part.Vertex(A.Vector(13,ww[0][1],ww[0][2])).distToShape(floor)[0]<1e-7
      and Part.Vertex(A.Vector(13,ww[1][1],ww[1][2])).distToShape(old.getObject('CandidateGlassChannelL').Shape)[0]<1e-7)
lower=floor.copy();lower.translate(A.Vector(0,0,-.1))
check('negative lowering rejects unintended shelf penetration',lower.common(old.getObject('BACKBOX_BASE').Shape).Volume>1)
advance=floor.copy();advance.translate(A.Vector(0,-1,0))
check('negative forward floor shift fails channel margin',advance.distToShape(old.getObject('CandidateGlassChannelL').Shape)[0]<5)

# Independent bottom-face loop measurement (not the generator's passport boxes).
bottom=[f for f in floor.Faces if abs(f.CenterOfMass.z-596.9)<1e-7 and abs(f.normalAt(0,0).z)>.99]
check('single planar floor bottom face',len(bottom)==1)
outer=bottom[0].OuterWire;holes=[w for w in bottom[0].Wires if not w.isSame(outer)]
check('two unchanged actual cable passports',len(holes)==2)
web=min([w.distToShape(outer)[0] for w in holes]+[holes[0].distToShape(holes[1])[0]])
check('minimum planar ligament independently measured',abs(web-44.5)<1e-6)
top=Part.makeCompound([f for f in old.getObject('BACKBOX_BASE').Shape.Faces if abs(f.CenterOfMass.z-596.9)<1e-7 and abs(f.normalAt(0,0).z)>.99])
check('saved actual bearing area independently measured',abs(bottom[0].common(top).Area-r['floor']['bearing_new_mm2'])<1e-6)

ad=A.openDocument(str(R/c['source_backbox']))
for o in ad.Objects:
    if hasattr(o,'AuditRole') and o.AuditRole=='wood' and o.Name!='BackboxFloorV14':
        check('other reconstructed backbox member unchanged: '+o.Name,same(o.Shape,new.getObject(o.Name).Shape))
for n in ('PF_BasePlywood','PF_WoodDowel','FloorIntakeFanL','RemovableIntakeFilterL','LeafButton_primary_L','SHELF_2','PC_BASE','REAR_DOOR','SSF_Exciter2L'):
    before=old.getObject(n).Shape;wrong=before.copy();wrong.translate(A.Vector(.1,0,0))
    check('negative accepted-system geometry mutation rejected: '+n,not same(before,wrong))
A.closeDocument(ad.Name);A.closeDocument(old.Name);A.closeDocument(new.Name)

d=A.openDocument(str(O/'first-bottleneck.FCStd'));d.recompute()
check('first bottleneck explicitly labeled collision',d.PoseStatus=='COLLISION DIAGNOSTIC' and d.Prerequisites=='GLASS_REMOVED, MATRIX_REMOVED')
first=r['fold']['first_structural_collision']
check('first collision is actual floor/shelf at 1 degree',first['angle_deg']==1 and any(p['part']=='BackboxFloorV32' and p['obstacle']=='BACKBOX_BASE' for p in first['A_wood_cabinet_wood']))
for row in first['A_wood_cabinet_wood']:
    mm3=d.getObject(row['part']).Shape.common(d.getObject(row['obstacle']).Shape).Volume
    check('first saved collision independently reproduced: '+row['obstacle'],abs(mm3-row['volume_mm3'])<1e-5)
for angle in (45,90):
    check(f'no invalid {angle} degree success CAD generated',not (O/f'valid-through-{angle}.FCStd').exists())
A.closeDocument(d.Name)
(O/'regression-validation.json').write_text(json.dumps({'checks':checks,'all_pass':True,'zero_valid':True,'fold_clear':False,'manufacturing_ready':False},indent=2)+'\n')
print('BACKBOX_FLOOR_REGRESSION_PASS',len(checks),flush=True)
