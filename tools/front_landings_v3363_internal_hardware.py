"""Exact new-hardware compatibility gate. Original CERN-OHL-S-2.0.
No purchased internal foot geometry or thread profile is claimed.
"""
from pathlib import Path
import FreeCAD as A
import json, hashlib, itertools
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/front-landings-v3363'
g=json.loads((O/'geometry-validation.json').read_text())
hardware=g['new_hardware_names'];wood=g['new_wood_names']+['SIDE_L','SIDE_R','PF_BasePlywood']
foot={'ContactPad','SwivelDisc','SwivelJoint','AdjusterStem'}
intentional={frozenset(p) for p in [('ContactPad','SwivelJoint'),('SwivelDisc','SwivelJoint'),('SwivelJoint','AdjusterStem')]}
reports=[];checks=[]
for state in ['play','released']:
 d=A.openDocument(str(O/(state+'.FCStd')));sh={x.Name:x.Shape for x in d.Objects if hasattr(x,'Shape') and not x.Shape.isNull()}
 hits=[];accepted=[];manual=[];wood_hits=[];pairs=0
 for a,b in itertools.combinations(hardware,2):
  pairs+=1;s,t=sh[a],sh[b]
  if not s.BoundBox.intersect(t.BoundBox):continue
  v=s.common(t).Volume
  if v<1e-5:continue
  row={'a':a,'b':b,'volume_mm3':v}
  pa,sa=a.split('_',1);pb,sb=b.split('_',1)
  if pa==pb and frozenset([sa,sb]) in intentional:
   row['reason']='Explicit original envelope subparts of ONE H27 purchased articulated foot; not separate manufactured hardware';accepted.append(row)
  else:hits.append(row)
 for a in hardware:
  side=a[len('FrontLanding')];suffix=a.split('_',1)[1]
  for b in wood:
   s,t=sh[a],sh[b]
   if not s.BoundBox.intersect(t.BoundBox):continue
   v=s.common(t).Volume
   if v<1e-5:continue
   row={'hardware':a,'wood':b,'volume_mm3':v}
   allowed=(suffix.startswith('SideScrew') and b=='SIDE_'+side) or (suffix in ['RetentionBolt','RetentionReceiver'] and b=='PF_BasePlywood')
   if allowed:
    row['reason']='Explicit hardware-dependent pilot/receiver interface is uncut in protected original B-rep; mandatory guided manual operation, PURCHASE_BEFORE_CNC';manual.append(row)
   else:wood_hits.append(row)
 reports.append({'state':state,'hardware_pairs_tested':pairs,'unintended_hardware_intersections':hits,'intentional_single_foot_envelopes':accepted,'unreleased_original_wood_interfaces':manual,'unintended_wood_intersections':wood_hits})
 checks.append({'name':state+' distinct purchased hardware does not interpenetrate','pass':not hits})
 checks.append({'name':state+' hardware/wood only explicit uncut manual interfaces','pass':not wood_hits})
 A.closeDocument(d.Name)
out={'pass':all(x['pass'] for x in checks),'checks':checks,'source_sha256':hashlib.sha256((O/'play.FCStd').read_bytes()).hexdigest(),
 'states':reports,'side_screw_y_mm':[234,286],'minimum_body_center_edge_mm':9,
 'correction':'Initial new-support Y240/Y280 rows intersected the M8 adjuster insert/stem and M6 retention bolts. New-only rows234/286 eliminate those clashes; no original component changed.',
 'manufacturing_release':False,'purchased_internal_foot_geometry':'UNMEASURED; explicit envelope overlap only within H27; physical articulation and captive construction must be confirmed.'}
(O/'internal-hardware-validation.json').write_text(json.dumps(out,indent=2)+'\n')
assert out['pass'],reports
print('V3363_INTERNAL_HARDWARE_PASS',len(checks),flush=True)
