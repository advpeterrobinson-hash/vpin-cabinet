"""Independent inventory reconciliation and geometry-preservation gates.
CERN-OHL-S-2.0. Does not promote catalog dimensions to manufacturing authority.
"""
from pathlib import Path
import json,hashlib,subprocess,csv,copy
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/hardware-v33'
C=json.loads((R/'config/hardware_catalog_v33.json').read_text());W=json.loads((R/'config/wood_materials_v33.json').read_text());B=json.loads((O/'bom.json').read_text());audit=json.loads((R/'library/hardware/current-object-audit.json').read_text());L=json.loads((O/'cad-library-validation.json').read_text())
checks=[]
def check(name,value):
    checks.append({'check':name,'pass':bool(value)});assert value,name
def validate(c,w):
    assert len({i['id'] for i in c['hardware']})==len(c['hardware'])
    for i in c['hardware']:
        assert i['flatpack_classification'] in c['classification_codes'].values()
        assert i['price_BRL'] is None and i['design_status']=='PROVISIONAL'
        assert not i['model']['detailed_threads'] and i['measurement_required']
        if i['controls_permanent_cnc']:assert i['freeze_status']=='PURCHASE_BEFORE_CNC'
        if i['flatpack_classification']=='REFERENCE_ONLY_NOT_FROZEN':assert i['quantity']==0
        else:assert i['quantity'] is None or i['quantity']>0
        if i['quantity_status']=='UNRESOLVED_NOT_ZERO':assert i['quantity'] is None
        if i.get('reference_part'):assert i['measurement_fields'] and all(v is None for v in i['measurement_fields'].values())
    assert not c['manufacturing_ready'] and w['policy']['structural_premium_never_auto_downgrade'] and w['policy']['strategy']=='PREMIUM_FIRST'
validate(C,W);check('Classification, uncertain quantities, prices and CNC holds',True)
names={i['object'] for i in audit['objects']};ids={i['id'] for i in C['hardware']}|{p['id'] for p in W['parts']}
check('All438 CURRENT and blank-state B-reps classified exactly once',len(names)==438 and set(C['object_to_id'])==names and all(v in ids for v in C['object_to_id'].values()))
H={i['id']:i for i in C['hardware']}
check('Wood pivot1 dowel /4 straps /8 strap screws /6 support screws',all(H[id]['quantity']==q for id,q in [('H01',1),('B01',4),('F02',8),('F01',6)]))
check('Two CNC cradles preserved',sum(p['object'].startswith('PF_OpenCradle') for p in W['parts'])==2)
check('Purchased subcomponents not double counted',all(H[id]['quantity']==q for id,q in [('H02',2),('H03',1),('H14',2),('H15',1),('H16',2),('I05',2)]))
check('No invented metal shaft bearings or legacy prop hardware',not any('metal shaft' in i['description_en'].lower() or 'bearing' in i['description_en'].lower() or 'prop ' in i['description_en'].lower() for i in C['hardware'] if i['flatpack_classification']=='REQUIRED_FLATPACK_HARDWARE'))
check('WPC family exact references and physical holds',set(H[i]['reference_part'] for i in ['H08','H09','H10','F14'])=={'01-9011-L','01-9011-R','02-4352','4322-01139-12B'})
check('Canonical washer aliases do not create buy rows',not any(i['id'] in C['aliases'] for i in C['hardware']) and C['aliases']=={'W05':'W02','W04':'W02'})
# Independent B-rep metrology supports consolidation, independent of catalog labels.
byname={i['object']:i for i in audit['objects']}
for n in ['CandidateHandleBolt1Washer','CandidateFixedSupportScrew1L1Washer','CandidateFanBolt230_1OuterWasher']:
    row=byname[n];check('Washer equivalence '+n,sorted(round(c['radius_mm'],6) for c in row['cylinders'])==[2.25,4.5] and sorted(round(v,6) for v in row['size_world_mm'])==[1,9,9])
check('No electronics in required hardware layer',all(r['flatpack_classification']=='REQUIRED_FLATPACK_HARDWARE' and not r['id'].startswith('E') for r in B['rows'] if r['bom_layer']==2))
check('Blank and fan bolt alternatives explicit',H['F21']['quantity']==H['F20']['quantity']==8 and H['F21']['flatpack_classification']!=H['F20']['flatpack_classification'])
check('Wood component map preserves structural load-bearing parts',all(p['material_class']=='STRUCTURAL_PREMIUM' for p in W['parts'] if p['object'].startswith(('SIDE_','PF_OpenCradle','BB_Side','BB_MonitorCarrier')) or p['object'] in ['FLOOR','BACKBOX_BASE','PF_BasePlywood','BB_Floor','BB_ReplaceableVESAPlate','BB_LowerCassetteFrame']))
check('Known fused/stepped wood objects expose CNC decomposition holds',all(p['status']=='CNC_COMPONENT_BREAKDOWN_HOLD' for p in W['parts'] if p['object'].startswith(('BB_IntakeDownBaffle','BB_GlassTopRetainer','BB_HingeCleat'))))
check('All current CAD valid at read-only audit',all(i['valid'] for i in audit['objects']))
check('One valid lightweight model per canonical family',L['pass'] and {i['id'] for i in L['models']}==set(H) and all(i['valid'] and i['solid_count']>0 for i in L['models']))
for i in L['models']:check('Saved model '+i['id'],hashlib.sha256((R/i['file']).read_bytes()).hexdigest()==i['sha256'])
check('Every assembly stage dependency resolves and is acyclic',all(all(int(p)<int(s) and p in C['assembly_stages'] for p in row['depends_on']) for s,row in C['assembly_stages'].items()))
for name,digest in audit['input_sha256'].items():check('CURRENT byte preservation '+name,hashlib.sha256((R/name).read_bytes()).hexdigest()==digest)
# Full source-HEAD audit catches changes to any current source, state or viewer,
# including objects outside the small metrology input list. New V33 paths only.
base=C['source_head'];tracked=subprocess.check_output(['git','ls-tree','-r','-z',base],cwd=R).split(b'\0');verified=0
for line in tracked:
    if not line:continue
    info,name=line.split(b'\t');mode,kind,sha=info.split();p=R/name.decode()
    if kind!=b'blob':continue
    data=p.read_bytes();actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode();assert actual==sha,('Changed accepted source',name)
    verified+=1
check('Every source-HEAD file byte identical',verified>0)
for title,mut in [('Reject false frozen WPC',lambda c,w:c['hardware'][next(i for i,x in enumerate(c['hardware']) if x['id']=='H08')].update(freeze_status='FROZEN')),('Reject unknown quantity converted to zero',lambda c,w:c['hardware'][next(i for i,x in enumerate(c['hardware']) if x['id']=='F06')].update(quantity=0)),('Reject automatic structural material downgrade',lambda c,w:w['policy'].update(structural_premium_never_auto_downgrade=False))]:
    c=copy.deepcopy(C);w=copy.deepcopy(W);mut(c,w);rejected=False
    try:validate(c,w)
    except AssertionError:rejected=True
    check(title,rejected)
with (O/'bom.csv').open(encoding='utf-8-sig',newline='') as f:csvrows=list(csv.DictReader(f))
check('CSV row/ID roundtrip',len(csvrows)==len(B['rows']) and {r['row_id'] for r in csvrows}=={r['row_id'] for r in B['rows']})
for a,b in zip(csvrows,B['rows']):assert a['quantity']==('' if b['quantity'] is None else str(b['quantity'])) and a['price_BRL']==''
check('CSV null quantities and prices preserved',True)
review=json.loads((O/'review-views.json').read_text());check('All15 requested real-CAD views',len(review)==15 and all((O/x['cad']).is_file() and (O/(x['number']+'-review.png')).is_file() for x in review))
inputs=['config/hardware_catalog_v33.json','config/wood_materials_v33.json','library/hardware/current-object-audit.json','tools/check_hardware_v33.py','tools/build_hardware_library_v33.py','tools/build_bom_v33.py','tools/define_hardware_v33.py','tools/export_bom_v33.mjs','studies/hardware-v33/render.py']
(O/'validation.json').write_text(json.dumps({'pass':True,'source_head':base,'checks':checks,'unchanged_source_head_files':verified,'manufacturing_ready':False,'structural_certification':False,'input_sha256':{n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in inputs}},indent=2)+'\n')
print('HARDWARE_V33_VALIDATION_PASS',len(checks),'gates;',verified,'source files byte-identical')
