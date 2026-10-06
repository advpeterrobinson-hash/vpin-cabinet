"""Promotion guard and mutation regressions; CNC authorization always false."""
from pathlib import Path
import json,copy,hashlib,sys
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/widebody-v351'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
C=read(R/'config/widebody_v351.json');reg=read(O/'manufacturing-register.json');names={a['source_component'] for a in reg['parts']}
required={'CROSS_1','CROSS_2','CROSS_3','SHELF_1','SHELF_2','SHELF_3','FLOOR_CLEAT_18','FLOOR_CLEAT_552','CandidateLegBlockFL','CandidateLegBlockFR','CandidateLegBlockRL','CandidateLegBlockRR','FrontLandingL_Block','FrontLandingR_Block','PF_OpenCradleL','PF_OpenCradleR','PC_BASE'}
def contract(c,names,rows):
 return (required<=names and c['body']['outside_width_mm']==628.65 and c['body']['length_mm']==1308.1 and c['backbox']['width_mm']==780 and c['backbox']['height_mm']==723.9 and c['backbox']['local_geometry']=='PRESERVE' and c['commercial']['custom_lockdown'] is False and c['commercial']['siderail_optional'] is True and c['glass']['commercial_reference_mm'][2]==5 and c['glass']['final_cut_mm'] is None and c['glass']['slot_width_mm'] is None and c['glass']['slot_depth_mm'] is None and not c['manufacturing_release'] and not c['production_nesting'] and not c['LED_mandatory'] and c['playfield']['angle_difference_deg']==0 and c['playfield']['selected_planning_gap_mm']<=10 and {a['nominal_stock_thickness_mm'] for a in rows if a['nominal_stock_thickness_mm'] is not None}=={12,18})
checks=[]
def ck(n,p):checks.append({'name':n,'pass':bool(p)});assert p,n
ck('candidate contract',contract(C,names,reg['parts']))
for n in sorted(required):ck('reject deletion '+n,not contract(C,names-{n},reg['parts']))
for path,v in [(('body','outside_width_mm'),600),(('body','outside_width_mm'),630),(('body','outside_width_mm'),635),(('backbox','width_mm'),808.65),(('commercial','custom_lockdown'),True),(('commercial','siderail_optional'),False),(('playfield','selected_planning_gap_mm'),50),(('playfield','angle_difference_deg'),1)]:
 cc=copy.deepcopy(C);cc[path[0]][path[1]]=v;ck('reject '+'.'.join(path)+'='+str(v),not contract(cc,names,reg['parts']))
rr=copy.deepcopy(reg['parts']);rr[0]['nominal_stock_thickness_mm']=6;ck('reject third plywood stock',not contract(C,names,rr))
for n in ['geometry','validation','continuous-motion','conservative-validation','browser-validation']:
 d=read(O/(n+'.json'));ck('evidence '+n,d['pass'] and all(a['pass'] for a in d['checks']))
ck('browser evidence matches viewer',read(O/'browser-validation.json')['viewer_sha256']==sha(O/'viewer.html'))
ck('zero reconstruction',max(a['reconstruction_difference_mm3'] for a in reg['parts'])<1e-6)
ck('32 review images',len(list(O.glob('[0-9][0-9]-review.png')))==32)
ck('all bundles <=25 HIGH',all(a['high_gross_kg']<=25 for a in read(O/'packaging.json')['bundles']))
for t,n in read(O/'nesting.json').items():ck('nesting '+t,n['pass'] and n['release'] is False)
files=[R/C['source'],R/'config/widebody_v351.json',R/'config/standard_interfaces_v351.json',R/'config/hardware_catalog_v351.json']+sorted((R/'tools').glob('*v351*.*'))+[O/n for n in ['candidate.FCStd','play.FCStd','manufacturing-register.json','viewer.html','geometry.json','validation.json','continuous-motion.json','conservative-validation.json','browser-validation.json','nesting.json','mass-counts.json','assembly-manual.json']]+sorted(O.glob('*.brep'))
# Do not self-include the seal/check output; a changed source or model requires rebuilding and resealing.
hashes={str(p.relative_to(R)):sha(p) for p in files}
seal=O/'promotion-validation.json'
if '--seal' in sys.argv:
 seal.write_text(json.dumps({'version':'V35.1','pass':True,'manufacturing_release':False,'checks':checks,'hashes':hashes},indent=2)+'\n')
else:
 saved=read(seal);ck('sealed source/geometry/evidence hashes',saved['hashes']==hashes)
print('V351_PROMOTION_GUARD_PASS',len(checks),'CNC BLOCKED')
