"""Differential service certificates for V33.5 only. CERN-OHL-S-2.0."""
from pathlib import Path
import sys,json,gzip,re,math
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import certify,load,transform,actual,pf_names,WPC,PF,V,box,service,swept,route,hand
O=R/'exports/generated/structural-v335';old=load(R/'exports/generated/backbox-lock-integration-v32/play.FCStd');new=load(O/'play.FCStd')
D=json.loads(gzip.decompress((R/'exports/generated/solid-leg-v334/viewer-data.json.gz').read_bytes()));groups={p['key']:p['meta']['group'] for p in D['installed']}
Q=json.loads(re.search(r'<script id="v333-data"[^>]*>(.*?)</script>',(R/'exports/generated/viewer-v32/index.html').read_text(),re.S).group(1));roles=Q['motions']['groups']
report={'checks':[],'certificates':{},'samples':{},'manufacturing_release':False}
def check(n,v,d=None):report['checks'].append({'name':n,'pass':bool(v),'detail':d});assert v,(n,d)
def hits(a,b):
 out=[]
 for n,s in a.items():
  for m,t in b.items():
   if s.BoundBox.intersect(t.BoundBox):
    vol=s.common(t).Volume
    if vol>1e-4:out.append([n,m,vol])
 return out
rail={n:s for n,s in new.items() if n.startswith(('BB_MonitorStopRail','BB_Stop'))}
fixed={n:s for n,s in actual(new).items() if not n.startswith('BB_') and n!='CandidateGlass' and groups.get(n)!='matrix'}
report['certificates']['rail_populated_fold']=certify(rail,fixed,0,90)
print('FOLD_CERT_PASS',flush=True)
angles=[0,.25,.5,1,2,5,10,15,30,45,60,75,90]
report['samples']['rail_fold']=[{'angle':a,'hits':hits(transform(rail,angle=a,axis=WPC),fixed)} for a in angles]
check('new monitor rail and hardware clear cabinet throughout fold',not any(r['hits'] for r in report['samples']['rail_fold']))
# Datum transfer does not add occupied shell volume; only the eight withdrawn
# fan bores add wood. Check that difference against accepted service trajectories.
# Explicit disjoint new cylinders avoid a degenerate Boolean between the
# compound side-tab difference and touching side faces. Each is verified inside
# the new rear and empty in the old rear independently.
plugs=[Part.makeCylinder(2.25,18,V(x,1290.1,z),V(0,1,0)) for x in [177.5,282.5,317.5,422.5] for z in [447.5,552.5]]
for i,p in enumerate(plugs):
 check('withdrawn fan clearance bore '+str(i),old['REAR'].common(p).Volume<1e-5 and abs(new['REAR'].common(p).Volume-p.Volume)<1e-5)
filled=Part.makeCompound(plugs)
pf={n:s for n,s in actual(new).items() if n in pf_names(new)}
report['certificates']['PF_vs_withdrawn_fan_bores']=certify(pf,{'rear_new_wood':filled},0,50,PF,poser=lambda ss,a:transform(ss,angle=-a,axis=PF))
check('playfield lift-out clears newly restored fan pilot material',not hits(swept(pf,dz=48),{'rear_new_wood':filled}))
# Doors are unchanged. Only added rail / hardware need differential retesting.
for side in ['L','R']:
 mov={n:s for n,s in new.items() if roles.get(n) in ['door'+side,'unlocked'+side]}
 hx,hy=service.C['rear']['hinge_axis_xy_mm'][0 if side=='L' else 1]
 report['certificates']['door_'+side]=certify(mov,rail,0,100,V(hx,hy,0),'Z',lambda ss,a:service.door_pose(ss,side,a))
# Main display and adapter approach from the front; installed top contact is
# permitted but positive volume anywhere along the removal is not.
display={n:s for n,s in new.items() if roles.get(n) in ['display','adapter'] and n not in rail}
check('front display/adapter removal preserved',not hits(swept(display,dy=-400),rail),hits(swept(display,dy=-400),rail))
check('glass top removal preserved',not hits(swept({'glass':new['BB_Backglass']},dz=500),rail))
cas={n:s for n,s in new.items() if roles.get(n)=='cassette'}
check('lower cassette removal preserved',not hits(swept(cas,dy=-240),rail))
# Rear screw corridors R8 x90; carriers and screw hosts intentionally excluded.
obs={n:s for n,s in new.items() if n.startswith('BB_') and n not in rail and roles.get(n) not in ['doorL','doorR','lockedL','lockedR','unlockedL','unlockedR'] and not n.startswith('BB_MonitorCarrier')}
for i,x in enumerate([160,440]):
 access=Part.makeCylinder(8,90,V(x,1261,926),V(0,1,0))
 check('rail retention rear driver '+str(i),not hits({'driver':access},obs),hits({'driver':access},obs))
# Knob release/parking paths are below the rail and are exactly unchanged.
for side,x in [('L',130),('R',470)]:check('upright lock rear approach '+side,not hits(route(x,1260),rail))
# Adjustment moves the entire carrier/rail together in Y; adapter follows the
# existing +/-5Z, +/-1X alignment range. Rail stays below lowest plate underside.
check('rail allows -5 vertical adapter adjustment',935 < new['BB_ReplaceableVESAPlate'].BoundBox.ZMin-5)
report['adjustment']={'rearward_positions_mm':[0,16],'vertical_mm':[-5,5],'centering_large_display_mm':[-1,1],'adjuster_tip_top_required_mm':[944,954],'adjuster_physical_stroke':'PURCHASE_BEFORE_CNC','rail_top_mm':935,'through_bolts_unchanged':True}
# Native retained cradle seat and six screws; contour subtraction cannot create
# a new collision in any original service state. No move of T3/S3 is promoted.
report['inherited_proof']={'source':'exports/generated/backbox-lock-integration-v32/validation.json','fixed_shell_union':'exact, except restored obsolete fan bores screened above','cradles':'entire original B-rep retained; trimmed candidate not promoted','main_fan_body':'unchanged; screw insertion hardware-dependent','new_rail':'continuous rotation certificates + exact swept service envelopes','underfront_controls':'unlocated schematic, not a fit validation'}
# Shelf bearing is reassigned from side top to shelf tabs; assembled top datum
# and occupied union stay fixed. Report the changed part attribution explicitly.
from backbox_structure_review_v32 import face
report['bearing']={'top_z_mm':596.9,'old_shelf_contact_mm2':face(old['BACKBOX_BASE'],596.9).common(face(old['BB_Floor'],596.9)).Area,'new_shelf_contact_mm2':face(new['BACKBOX_BASE'],596.9).common(face(new['BB_Floor'],596.9)).Area,'added_tab_shoulder_area_mm2':2*4*162.975}
check('existing shelf contact preserved, tab bearing added',report['bearing']['new_shelf_contact_mm2']>=report['bearing']['old_shelf_contact_mm2']-1e-5)
study=load(O/'study.FCStd')
reserves={n:s for n,s in new.items() if n.startswith('WPC_') or 'UprightLock' in n}
for n,s in study.items():
 if n.startswith('BACKBOX_BASE_') and ('Screw' in n or 'Driver' in n):check(n+' WPC/lock reserve clearance',not hits({n:s},reserves),hits({n:s},reserves))
plunger={n:s for n,s in new.items() if n.startswith('Plunger')}
check('provisional exterior plunger clears cabinet wood',not hits(plunger,{n:s for n,s in new.items() if n in ['FRONT','SIDE_L','SIDE_R','FLOOR']}))
diag={n:s for n,s in study.items() if n.startswith('Diagnostic_')}
obs={n:s for n,s in actual(new).items() if n not in ['CROSS_3','CROSS_GUIDE_3L','CROSS_GUIDE_3R']}
report['T3_diagnostic']={'offset_y_mm':-20,'hits_at_proposed_static_position':hits(diag,obs),'meaningful_cradle_simplification':False,'promoted':False,'service_qualification':'Not pursued: no geometric benefit; CURRENT T3 and all service paths remain unchanged.'}
report['pass']=all(c['pass'] for c in report['checks']);(O/'motion-validation.json').write_text(json.dumps(report,indent=2)+'\n');print('V335_MOTION_PASS',len(report['checks']),flush=True)
