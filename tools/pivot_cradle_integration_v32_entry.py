"""Validate then promote local relief + previously validated backbox; no new drilling.
CERN-OHL-S-2.0. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet
"""
from pathlib import Path
import sys,json,math,hashlib,shutil
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from pivot_cradle_integration_v32 import *
O=R/C['output_directory'];O.mkdir(parents=True,exist_ok=True);checks=[]
def check(n,v):
 assert v,n
 checks.append({'check':n,'pass':True})
def diff(a,b):return a.cut(b).Volume+b.cut(a).Volume
study=json.loads((O/'radius-study.json').read_text())
for row in study['candidates']:
 if 'rear_wall_width_at_seat_axis_mm' in row:row['rear_ear_nominal_width_before_relief_mm']=row.pop('rear_wall_width_at_seat_axis_mm')
 if 'support_side_contact_retained_percent' in row:row['support_volume_retained_percent']=row.pop('support_side_contact_retained_percent')
eligible=[q for q in study['candidates'] if q['pass']];selected=max(q['radius_mm'] for q in eligible)
source=R/C['source_directory'];play0=load(source/'play.FCStd');removed0=load(source/'matrix-removed.FCStd');original=play0['PF_OpenCradleL'];pair,cut=relief(original,selected);play={**play0,**pair};removed={**removed0,**pair};moving_ids=pf_names(removed);moving={n:removed[n] for n in moving_ids};back={n:s for n,s in removed.items() if n.startswith('BB_')};fixed={n:s for n,s in actual(removed).items() if n not in moving_ids and n not in back};hw=hardware();installed={n:s for n,s in hw.items() if n.startswith('WPC_')};arms={n:s for n,s in hw.items() if n.startswith('BB_')};tools=tools_for_pivot()
check('seven requested radii, no fallback mechanism',len(study['candidates'])==7)
check('largest screened radius selected',selected==12)
# Refresh access study with complete through-cradle tool corridor, not merely its inner exit.
for row in eligible:
 pp,_=relief(original,row['radius_mm']);obs={**fixed,**back,**pp};obs.pop('SIDE_L');obs.pop('SIDE_R')
 for state,ps in [('closed',moving),('service',transform(moving,angle=-50)),('lift',transform(moving,lift=48))]:row['cross_screen']['tool_'+state]=hits(tools,{**obs,**ps})
 row['tool_lift_clearance_mm']=minimum(tools,{**obs,**transform(moving,lift=48)})['mm']
 row['complete_packaging_pass']=not row['cross_screen']['hardware_closed'] and not row['cross_screen']['tool_lift'] and row['tool_lift_clearance_mm']>=2-1e-6
 row['selection_note']='local wood geometry passes; complete packaging needs installed hardware and through-cradle tool corridor with >=2 mm margin'
(O/'radius-study.json').write_text(json.dumps(study,indent=2)+'\n')
chosen=next(q for q in eligible if q['radius_mm']==selected);check('selected complete provisional packaging',chosen['complete_packaging_pass'])
check('one 18mm CNC solid per cradle',all(s.isValid() and len(s.Solids)==1 and abs(s.BoundBox.XLength-18)<1e-7 for s in pair.values()))
check('no material added; original cradle remains parent',all(pair[n].cut(play0[n]).Volume<1e-6 for n in pair))
check('dowel cylinder seat surface entirely unchanged',abs(seat_area(pair['PF_OpenCradleL'])-seat_area(original))<1e-7)
check('floor foot bearing unchanged',all(abs(face(pair[n],36).Area-face(play0[n],36).Area)<1e-6 for n in pair))
# The complete region below the seat center is byte-independent B-rep equivalent.
low=box(0,900,0,600,300,SEAT.z)
check('complete seat-to-floor wood path identical',all(diff(pair[n].common(low),play0[n].common(low))<1e-5 for n in pair))
# Screws, bores and countersinks are far below relief and remain copied unchanged.
mounts=BASE['support_mounting']['positions'];screwids=[r['id'] for r in mounts];screwgaps=[];driver={}
for row in mounts:
 n=row['id'];check('support screw unchanged '+n,diff(play[n],play0[n])<1e-7)
 side=n[-2];removedwood=play0['PF_OpenCradle'+side].cut(pair['PF_OpenCradle'+side]);screwgaps.append({'id':n,'relief_to_screw_mm':removedwood.distToShape(play[n])[0]})
 x,y,z=row['head_xyz_mm'];driver[n]=Part.makeCylinder(8,150,V(x,y,z),V(-row['axis'][0],0,0))
driverobs={n:s for n,s in actual(play).items() if n not in screwids and n not in pair and n!='CandidateGlass'};check('six support drivers clear',not hits(driver,driverobs))
check('installed WPC reserve clears internal components',not hits(installed,{n:s for n,s in actual(play).items() if n not in ['SIDE_L','SIDE_R']}))
check('upright backbox and relieved supports clear other components',not hits({**pair,**back},{n:s for n,s in actual(play).items() if n not in pair and n not in back and n not in screwids}))
check('pivot driver clear after accepted 48mm lift',not hits(tools,{**{n:s for n,s in fixed.items() if n not in ['SIDE_L','SIDE_R']},**back,**transform(moving,lift=48)}))
# Per-candidate motion was sampled by screen; subtraction makes all later relieved
# cradles subsets of the R5 candidate and cannot add any new interference.
for row in eligible:
 pp,_=relief(original,row['radius_mm']);p5,_=relief(original,5)
 check('monotone relief inclusion R'+str(row['radius_mm']),all(pp[n].cut(p5[n]).Volume<1e-6 for n in pp))
 check('candidate PF service and lift samples R'+str(row['radius_mm']),not row['cross_screen']['service'] and not row['cross_screen']['lift'])
# Independent combined playfield samples, including actual display envelope.
service=[];lift=[]
for kind,values in [('service',sorted(set([i/2 for i in range(101)]+[.01,.05,.1,.25]))),('lift',sorted(set(list(range(49))+[.01,.05,.1,.25,.5])) )]:
 rows=service if kind=='service' else lift
 for v in values:
  ps=transform(moving,angle=-v if kind=='service' else 0,lift=v if kind=='lift' else 0);hh=hits(ps,{**fixed,**back,**hw});check(kind+' combined '+str(v),not hh);rows.append({'value':v,'hits':hh})
 print('PF_SWEEP_PASS',kind,len(rows),flush=True)
# Continuous certificate for the changed interface against the moving playfield.
# Unchanged cradle contact and unchanged cabinet geometry retain their old motion
# authority; the new relief is a subtraction. Certify added backbox/hardware over
# every intervening angle, rather than treating endpoint tests as proof.
def certify(mov,obs,axis,start,end,sign=1,translation=False):
 radius=max(math.hypot(y-axis.y,z-axis.z) for s in mov.values() for y in [s.BoundBox.YMin,s.BoundBox.YMax] for z in [s.BoundBox.ZMin,s.BoundBox.ZMax]);stack=[(start,end)];out=[]
 while stack:
  lo,hi=stack.pop();mid=(lo+hi)/2;ps=transform(mov,lift=mid if translation else 0,angle=0 if translation else sign*mid,axis=axis);gap=minimum(ps,obs);bound=(hi-lo)/2 if translation else radius*math.radians((hi-lo)/2)
  if gap['mm']>bound+1e-6:out.append({'lo':lo,'hi':hi,'midpoint_clearance':gap,'motion_bound_mm':bound})
  else:
   check('adaptive interval converges',hi-lo>1e-7);stack.extend([(lo,mid),(mid,hi)])
 return {'radius_mm':radius,'intervals':out,'translation':translation,'range':[start,end]}
newobs={**back,**hw};pf_cert=certify(moving,newobs,PF,0,50,sign=-1);lift_cert=certify(moving,newobs,PF,0,48,translation=True);print('PF_NEW_INTERFACE_CERT_PASS',len(pf_cert['intervals']),len(lift_cert['intervals']),flush=True)
# Backbox floor and shelf bearing are unchanged. Existing whole-motion certificate
# remains valid against all unchanged obstacles; relieved cradles are subsets.
prior=json.loads((source/'validation.json').read_text());check('validated backbox eight parts retained',len(back)==8)
for n in back:check('validated backbox shape identical '+n,diff(back[n],play0[n])<1e-7)
check('upright shelf area preserved',abs(face(back['BB_Floor'],596.9).common(face(play['BACKBOX_BASE'],596.9)).Area-65672.4)<1e-5)
# New screen includes display/VESA occupied volumes omitted by old blanket envelope filter.
fold=[];foldfixed={**fixed,**moving,**installed};foldmoving={**back,**arms}
for a in sorted(set(list(range(91))+C['backbox_angles_deg']+[.001,.01,.05,.1])):
 ps=transform(foldmoving,angle=a,axis=WPC);hh=hits(ps,foldfixed);check('backbox combined fold '+str(a),not hh);gap=minimum({n:s for n,s in ps.items() if n in back},{n:s for n,s in fixed.items() if n.startswith('CandidateGlassChannel')});fold.append({'angle_deg':a,'hits':hh,'channel_gap_mm':gap['mm'],'floor_shelf_gap_mm':ps['BB_Floor'].distToShape(play['BACKBOX_BASE'])[0]})
print('BACKBOX_COMBINED_SWEEP_PASS',len(fold),flush=True)
# Exact new occupied display/hinge checks across the entire fold; old base wood
# certificate remains valid for the unchanged other components.
extra={n:s for n,s in {**moving,**installed}.items() if n in ['PLAYFIELD_ENVELOPE','PF_VESAEnvelope'] or n.startswith('WPC_')};bb_cert=certify(back,extra,WPC,0,90)
cabinet_x_slab=box(0,-2000,-2000,600,5000,5000)
# Trimmed surface BBoxes extend beyond real side wood; use exact outside volume.
outboard={n:s for n,s in {**fixed,**moving}.items() if s.cut(cabinet_x_slab).Volume>1e-6}
arm_cert=certify(arms,outboard,WPC,0,90) if outboard else {'intervals':[],'proof':'no outboard fixed obstacles'}
# Arms live outside the cabinet X planes and co-rotate rigidly with the backbox.
# All fixed occupied solids have X>=0 and X<=600; reference arms/flanges touch only
# these planes. This X-separation proof holds at all rotation angles about X.
check('exterior hinge corridor has invariant separation by X',all(s.BoundBox.XMax<=1e-7 or s.BoundBox.XMin>=600-1e-7 for s in arms.values()) and all(s.cut(cabinet_x_slab).Volume<1e-6 for n,s in {**fixed,**moving}.items() if n not in outboard))
# Save all established states with only the cradle replacements; backbox candidate
# source already includes the accepted proposed architecture and no final holes.
basebundle=json.loads((source/'mesh.json').read_text());saved=prior['saved_poses'];scenes={}
for state,fn in saved.items():
 d=A.openDocument(str(source/fn))
 for n,sh in pair.items():
  o=d.getObject(n)
  if o is not None:
   o.Shape=sh;o.addProperty('App::PropertyString','ReliefAuthority');o.ReliefAuthority='config/pivot_cradle_integration_v32.json; R12 packaging reserve + 2 mm allowance; hardware measurement required'
 if 'BackboxAuthority' in d.PropertiesList:d.BackboxAuthority='CURRENT V32 DESIGN CANDIDATE: local cradle relief + validated WPC wood fold; hardware provisional; no final drilling'
 for n in back:
  o=d.getObject(n)
  if o and 'DesignAuthority' in o.PropertiesList:o.DesignAuthority='CURRENT design geometry; WPC Y1066.8/Z508; physical hardware and CNC release pending'
 d.recompute();check('recompute promoted '+state,not any('Invalid' in o.State for o in d.Objects));d.saveAs(str(O/fn));scenes[state]={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape') and not o.Shape.isNull()};A.closeDocument(d.Name)
for a in [1,45]:
 d=A.openDocument(str(O/'matrix-removed.FCStd'))
 for n,sh in transform(back,angle=a,axis=WPC).items():d.getObject(n).Shape=sh
 d.recompute();d.saveAs(str(O/f'fold-{a}.FCStd'));A.closeDocument(d.Name)
# Source mesh labels and original unchanged entries preserved exactly.
bundle=basebundle
for i,p in enumerate(bundle['parts']):
 if p['name'] in pair:bundle['parts'][i]={**mesh(p['name'],pair[p['name']]),'label':p.get('label',p['name'])}
for state,over in bundle['states'].items():
 for n in pair:
  if n in over and over[n] is not None:over[n]=mesh(n,pair[n])
rev=bundle['review'];rev['backbox_structure_review'].update({'promoted':True,'hinge_installation_blocked':False,'hardware_reserve_status':'PROVISIONAL R12; installation tools require playfield lift-out/removal','manufacturing_ready':False});rev['matrix_cassette']['fold_status']='WOOD 0–90 VALIDATED; GLASS REMOVED + MATRIX REMOVED; WPC hardware provisional; manufacturing BLOCKED'
rev['pivot_cradle_integration']={'selected_radius_mm':selected,'profile':C['profile'],'radial_allowance_mm':2,'rear_top_z_mm':494,'seat_wrap_deg':180,'seat_web_mm':8.250619847179905,'floor_load_path_preserved':True,'six_screws_preserved':True,'promoted':True,'physical_hardware_required':True,'tool_access_prerequisites':['GLASS_REMOVED','MATRIX_REMOVED','PLAYFIELD_LIFT_OUT_OR_REMOVED'],'manufacturing_ready':False}
# Explicit current entry-point manifest; original source snapshots remain historical.
raw=json.dumps(bundle,separators=(',',':'))+'\n';(O/'mesh.json').write_text(raw)
report={'source_head':C['source_head'],'checks':checks,'selected_radius_mm':selected,'radius_study':study,'review':rev,'mesh_sha256':hashlib.sha256(raw.encode()).hexdigest(),'saved_poses':saved,'support_screw_relief_distances':screwgaps,'support_driver_hits':hits(driver,driverobs),'foot_contact_each_mm2':face(pair['PF_OpenCradleL'],36).Area,'seat_area_before_mm2':seat_area(original),'seat_area_after_mm2':seat_area(pair['PF_OpenCradleL']),'support_side_face_before_mm2':max(f.Area for f in original.Faces if abs(f.normalAt(0,0).x)>.99),'support_side_face_after_mm2':max(f.Area for f in pair['PF_OpenCradleL'].Faces if abs(f.normalAt(0,0).x)>.99),'playfield_service_samples':service,'lift_samples':lift,'backbox_fold_samples':fold,'continuous_new_interface':{'playfield_service':pf_cert,'playfield_lift':lift_cert,'backbox_extra_occupied_volumes':bb_cert,'exterior_arms_vs_outboard_components':arm_cert,'backbox_original_wood_certificate_source':'exports/generated/backbox-structure-v32/validation.json','backbox_original_wood_intervals':len(prior['continuous_certificate']['intervals']),'proof':'unchanged backbox wood/other fixed geometry; cradles strictly reduced; exterior reference arms remain outside cabinet X planes'},'promoted':True,'final_hinge_holes_frozen':False,'custom_metal_added':0,'manufacturing_ready':False}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
detail={'current':[mesh(n,play0[n]) for n in ['PF_OpenCradleL','PF_WoodDowel','PF_BasePlywood','SIDE_L','FLOOR']],'selected':[mesh(n,s) for n,s in pair.items()],'hardware':[mesh(n,s) for n,s in hw.items()],'tools':[mesh(n,s) for n,s in tools.items()],'drivers':[mesh(n,s) for n,s in driver.items()],'screws':[mesh(n,play[n]) for n in screwids],'radii':{str(q['radius_mm']):[mesh(n,s) for n,s in relief(original,q['radius_mm'])[0].items()] for q in study['candidates']},'wpc_axis':list(WPC),'dowel_axis':list(PF)}
(O/'detail-mesh.json').write_text(json.dumps(detail,separators=(',',':'))+'\n')
for n in ['LICENSE','NOTICE.md']:shutil.copyfile(R/n,O/n)
print('PIVOT_CRADLE_INTEGRATION_PASS',len(checks),'PROMOTED',True,flush=True)
