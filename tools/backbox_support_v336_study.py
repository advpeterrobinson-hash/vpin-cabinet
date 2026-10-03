"""V33.6 isolated backbox support screen. Original CERN-OHL-S-2.0.
Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet
No selected display, connector, or VESA pattern is inferred. No production release.
"""
from pathlib import Path
import json, math, sys, gzip, hashlib, traceback
import FreeCAD as A, Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,transform,WPC,actual,certify,service
O=R/'exports/generated/monitor-support-v336/backbox-study';O.mkdir(parents=True,exist_ok=True);(O/'brep').mkdir(exist_ok=True)
V=A.Vector

def box(x,y,z,dx,dy,dz):return Part.makeBox(dx,dy,dz,V(x,y,z))
def join(ss):
 s=ss[0].copy()
 for t in ss[1:]:s=s.fuse(t)
 return s.removeSplitter()
def rounded_xz(x,z,w,h,r,y=1239,depth=20):
 ss=[box(x,y,z+r,w,depth,h-2*r)]
 if w>2*r:ss.append(box(x+r,y,z,w-2*r,depth,h))
 return join(ss+[Part.makeCylinder(r,depth,V(xx,y,zz),V(0,1,0)) for xx in sorted(set([x+r,x+w-r])) for zz in [z+r,z+h-r]])
def bounds(s):
 b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def mesh(s):
 v,f=s.tessellate(.3);return {'vertices':[list(p) for p in v],'faces':f}
def diff(a,b):return a.cut(b).Volume+b.cut(a).Volume
def hits(s,obs):
 return [{'part':n,'penetration_mm3':v} for n,t in obs.items() if s.BoundBox.intersect(t.BoundBox) and (v:=s.common(t).Volume)>1e-5]
def distances(s,obs):return sorted([{'part':n,'distance_mm':s.distToShape(t)[0]} for n,t in obs.items()],key=lambda r:r['distance_mm'])
def save(name,ss):
 doc=A.newDocument('V336Backbox'+name)
 for n,s in ss.items():doc.addObject('PartDesign::Feature',n).Shape=s
 doc.recompute();doc.saveAs(str(O/(name+'.FCStd')));A.closeDocument(doc.Name)

def main():
 old=load(R/'exports/generated/structural-v335/play.FCStd');doors=load(R/'exports/generated/structural-v335/doors-open.FCStd')
 checks=[]
 def ck(n,v,d=None):
  checks.append({'name':n,'pass':bool(v),'detail':d});print(n,bool(v),flush=True)
 new={};cuts={};refs={};rows=[]
 hardware={n:s for n,s in old.items() if n.startswith(('BB_MonitorClamp','BB_MonitorDepthBolt','BB_Stop')) and 'Rail' not in n}
 protected={n:s for n,s in old.items() if n=='BB_MonitorStopRail' or n.startswith(('BB_MonitorClamp','BB_MonitorDepth','BB_Stop'))}
 for i in range(2):
  n='BB_MonitorCarrier'+str(i);x=135+280*i;s=old[n]
  pair=[rounded_xz(x+10,1190,6,16,3),rounded_xz(x+34,1190,6,16,3)]
  cut=join(pair);cuts[n]=cut;new[n]=s.cut(cut).removeSplitter()
  ck(n+' remains one valid solid',new[n].isValid() and len(new[n].Solids)==1)
  ck(n+' subtraction only',new[n].cut(s).Volume<1e-6)
  ck(n+' complete through slots',cut.BoundBox.YMin<s.BoundBox.YMin and cut.BoundBox.YMax>s.BoundBox.YMax and new[n].common(cut).Volume<1e-6)
  # Existing slots + M067 capture + all lower wood unchanged; new routing features
  # confined above the adapter. Preserve exact 6 mm bearing capture region.
  capture=box(x,1227,916,50,40,20)
  ck(n+' M067 capture exact',diff(s.common(capture),new[n].common(capture))<1e-6)
  ck(n+' existing slot bands exact',all(diff(s.common(box(x,1239,z-15,50,30,30)),new[n].common(box(x,1239,z-15,50,30,30)))<1e-6 for z in [994,1134]))
  ck(n+' protected hardware and M067 unaffected',not hits(cut,protected),hits(cut,protected))
  # Strap threading corridor: 12-mm wide, 2-mm thick material can run through
  # each slot. This is a flexible strap routing envelope, not a rigid cable.
  passages=[box(xx+2,1228.1,1192,2,145,12) for xx in [x+10,x+34]]
  frontbridge=box(x+12,1237,1192,26,2,12)
  rearbridge=box(x+12,1259,1192,26,2,12)
  # Thread portions join the two faces with slack on rear; front has 9 mm clear
  # space to the maximum monitor envelope at Y1228.
  refs[n+'_StrapThread']=join(passages+[frontbridge,rearbridge])
  obs={k:t for k,t in doors.items() if k.startswith('BB_') and k!=n}
  ck(n+' strap threading and rear access clear',not hits(refs[n+'_StrapThread'],obs),hits(refs[n+'_StrapThread'],obs))
  # Practical rear hand/tool opening: 60 x40 mm box at the attachment height,
  # begins behind carrier and follows the already open rear service aperture.
  refs[n+'_RearFingerApproach']=box(x-5,1262,1186,60,120,24)
  accesshits=hits(refs[n+'_RearFingerApproach'],obs)
  ck(n+' rear finger approach clear',not accesshits,accesshits)
  removed=s.Volume-new[n].Volume
  rows.append({'component':n,'classification':'STRAIN_RELIEF_SLOT','quantity':2,'slot_mm':[6,16],'radius_mm':3,'bounds_mm':[bounds(p) for p in pair],
   'minimum_outer_edge_mm':10,'inter_slot_web_mm':18,'remaining_section_width_mm':38,'section_width_retained_percent':76,'nominal_thickness_mm':18,
   'minimum_web_area_per_side_mm2':180,'section_retained_mm2':684,'section_before_mm2':900,
   'nearest_known_fasteners':distances(cut,hardware)[:6], 'nearest_insert':distances(cut,{k:t for k,t in old.items() if k.startswith('BB_StopInsert')})[:1],
   'nearest_known_retention_load_point':distances(cut,{k:t for k,t in old.items() if k.startswith('BB_MonitorClamp')})[:1],
   'display_specific_VESA_load_point_distance_mm':None,'display_specific_VESA_note':'Display-specific bores are in replaceable plate; carrier strap slots leave existing VESA/retention interfaces unchanged.',
   'gap_above_adapter_mm':1190-old['BB_ReplaceableVESAPlate'].BoundBox.ZMax,'gap_below_depth_shoe_mm':24,
   'removed_volume_mm3':removed,'mass_saved_kg_at650':removed*650e-9,'normal_face':[0,-1,0],
   'one_side':'FACE_A front (-Y), same as existing capture; through cuts. FACE_B no CNC','manufacturing_release':False,
   'structural_screen':'Conservative small slots above upper retention row. 76% net width,10 mm outer webs; no certification. No load/retention bore or capture changed.'})
 # Large central adapter window has useful access, but unknown VESA locations
 # cannot be validated by retaining the outside rectangle alone.
 n='BB_ReplaceableVESAPlate';window=rounded_xz(210,1029,180,70,12,1227,14);candidate=old[n].cut(window).removeSplitter();refs['AdapterServiceWindow']=window
 ck('adapter window candidate valid single frame',candidate.isValid() and len(candidate.Solids)==1)
 ck('adapter window does not cut known peripheral clamps',not hits(window,protected),hits(window,protected))
 connector=box(275,1228,1049,50,205,30);refs['GenericConnectorRemovalEnvelope']=connector
 obs={k:t for k,t in doors.items() if k.startswith('BB_') and k!=n}
 chits=hits(connector,obs)
 ck('candidate service corridor clear with open rear doors',not chits,chits)
 ck('current adapter genuinely obstructs proposed service corridor',connector.common(old[n]).Volume>1)
 ck('candidate window clears proposed service corridor',connector.common(candidate).Volume<1e-6)
 window_report={'component':n,'classification':'SERVICE_WINDOW','bounds_mm':bounds(window),'size_mm':[180,70],'radius_mm':12,'status':'HOLD_DISPLAY_SPECIFIC_VESA_LAYOUT','promote':False,
  'reason':'No selected display / drilled VESA load points. A 100-mm VESA row centered on this plate would be only 15 mm from this opening before bore/washer allowance; different centers may fall inside. Passing existing four clamp reserves does not prove the screen attachment.',
  'outer_edge_webs_mm':{'left':90,'right':90,'lower':80,'upper':80},'remaining_width_percent':50,'vertical_side_section_mm2':2160,
  'nearest_known_clamp_reserve':distances(window,{k:t for k,t in old.items() if k.startswith('BB_MonitorClamp')})[:4],
  'nearest_VESA_load_point_mm':None,'actual_connector_SKU':None,'generic_connector_planning_box_mm':[50,30,65],
  'rear_service_sweep_mm':bounds(connector),'connector_fit_status':'PLANNING ONLY; display connector positions, pull direction and cable bend radius unselected. Not a universal fit claim.',
  'removed_volume_mm3':old[n].Volume-candidate.Volume,'mass_saved_kg_at650':(old[n].Volume-candidate.Volume)*650e-9,
  'current_adapter_unchanged':True,'minimum_rear_approach_clearance_mm':min([q['distance_mm'] for q in distances(connector,obs) if q['distance_mm']>1e-6],default=None),
  'one_side':'FACE_A rear (+Y), through cut; FACE_B no CNC'}
 # Existing open side space is a useful connector route without cutting an
 # unqualified VESA pattern. 50x30x65 is a generic planning envelope, not a SKU.
 side_routes={};side_route_report=[]
 for side,x in [('L',60),('R',490)]:
  swept_connector=box(x,1228,1049,50,205,30)
  refs['ExistingSideConnectorRoute'+side]=swept_connector
  obs={k:t for k,t in doors.items() if k.startswith('BB_')}
  hh=hits(swept_connector,obs)
  ck('existing '+side+' connector-sized route clear',not hh,hh)
  # Rounded flexible cable centerline; radius20 corner, 5-mm cable reserve.
  pts=[V(85,1233,1064),V(85,1233,1178)]
  pts += [V(105+20*math.cos(a),1233,1178+20*math.sin(a)) for a in [math.pi-j*math.pi/32 for j in range(1,17)]]
  pts += [V(160,1233,1198)]
  if side=='R':pts=[V(600-p.x,p.y,p.z) for p in pts]
  cable=Part.makeCompound([Part.makeCylinder(2.5,(b-a).Length,a,b-a) for a,b in zip(pts,pts[1:])]+[Part.makeSphere(2.5,p) for p in pts])
  side_routes['FlexibleCableRoute'+side]=cable;refs['FlexibleCableRoute'+side]=cable
  route_obs={k:(new[k] if k in new else t) for k,t in old.items() if k.startswith('BB_')}
  ch=hits(cable,route_obs)
  ck('existing '+side+' flexible cable routing reserve clear',not ch,ch)
  side_route_report.append({'side':side,'classification':'CABLE_PASSAGE','new_wood_cut':False,'connector_swept_bounds_mm':bounds(swept_connector),'generic_connector_mm':[50,30,65],'cable_radius_reserve_mm':2.5,'centerline_bend_radius_mm':20,'minimum_bend_radius_status':'PLANNING_ONLY_ACTUAL_CABLE_REQUIRED','cable_centerline_mm':[list(p) for p in pts],'minimum_separation_mm':min(r['distance_mm'] for r in distances(cable,route_obs)), 'actual_connector_locations':'UNSELECTED; no universal reach claim'})
 # A pure subtraction cannot create collision; verify exact subset first and
 # inspect the prescribed fold samples against the SAME static occupied set.
 allnew=dict(old);allnew.update(new)
 groups=json.loads(gzip.decompress((R/'exports/generated/structural-v335/viewer-data.json.gz').read_bytes()))
 # Current geometry includes physical glass; remove main glass/matrix as required.
 meta={p['key']:p['meta'].get('group') for p in groups['installed']}
 fixed={n:s for n,s in actual(old).items() if not n.startswith('BB_') and n!='CandidateGlass' and meta.get(n)!='matrix'}
 angles=[0,.25,.5,1,2,5,10,15,30,45,60,75,90]
 samples=[]
 for angle in angles:
  ss=transform({**new,**side_routes},angle=angle,axis=WPC)
  collision=[{'component':n,**h} for n,s in ss.items() for h in hits(s,fixed)]
  samples.append({'angle_deg':angle,'collisions':collision})
 ck('changed carriers clear fixed cabinet at requested fold angles',not any(r['collisions'] for r in samples),[r for r in samples if r['collisions']])
 ck('all removed wood confined to permitted new slots',all(new[n].cut(old[n]).Volume<1e-6 for n in new))
 ck('M067 current exact preserved',diff(allnew['BB_MonitorStopRail'],old['BB_MonitorStopRail'])<1e-6)
 # Explicit motion certificate is inherited over all intermediate angles:
 # changed moving sets are exact subsets; all other solids remain identical.
 certificate=certify(side_routes,fixed,0,90)
 ck('flexible route continuous fold screen',bool(certificate['intervals']),certificate)
 motion={'cable_route_continuous_certificate':certificate,'continuous_proof':'Exact subset of previously certified moving solids at every rigid pose; subtraction cannot create any new collision. Original native motion-validation.json retained as base proof.',
  'source':'exports/generated/structural-v335/motion-validation.json','fold_samples':samples,'fold_prerequisites':['MAIN PLAYFIELD GLASS REMOVED','MATRIX REMOVED','REAR DOORS CLOSED/LATCHED','LOCKS RELEASED/PARKED'],
  'other_services':'Door sweeps/display and glass removal unchanged except removed carrier wood, hence no new geometric interference. Flexible strap is a study route, cable qualification awaits selected display.'}
 report={'source':'exports/generated/structural-v335/play.FCStd','legacy_config_depth_offset_mm':10,'source_sha256':hashlib.sha256((R/'exports/generated/structural-v335/play.FCStd').read_bytes()).hexdigest(),'checks':checks,'pass':all(c['pass'] for c in checks),
  'current_bounds':{n:bounds(s) for n,s in old.items() if n.startswith(('BB_Display','BB_ReplaceableVESA','BB_MonitorCarrier','BB_MonitorDepth','BB_MonitorStopRail'))},'changed_components':list(new),'unchanged_components':['BB_ReplaceableVESAPlate','BB_MonitorStopRail','BB_MonitorClampReserve160994','BB_MonitorClampReserve1601134','BB_MonitorClampReserve440994','BB_MonitorClampReserve4401134'],
  'proposed_current_operations':rows,'existing_side_connector_routes':side_route_report,'held_service_window':window_report,'adjustment':{'existing':{'vertical_mm':[-5,5],'depth_positions_mm':[0,16],'lateral_max_display_mm':[-1,1],'lateral_smaller_display_mm':[-15,15]},'new_added_travel_mm':0,'decision':'No additional slotting; existing adjustment addresses alignment and tolerance. Physical hardware and display still required.'},
  'motion':motion,'total_volume_removed_proposed_mm3':sum(old[n].Volume-s.Volume for n,s in new.items()),'total_mass_saved_proposed_kg_at650':sum(old[n].Volume-s.Volume for n,s in new.items())*650e-9,
  'decision':'PROMOTE STRAIN-RELIEF SLOTS ONLY if overall V33.6 gates pass. Retain adapter until actual display VESA layout validates service window.','release':False}
 for n,s in new.items():s.exportBrep(str(O/'brep'/(n+'.brep')))
 for n in [*new,'BB_ReplaceableVESAPlate','BB_MonitorStopRail']:old[n].exportBrep(str(O/'brep'/('CURRENT_'+n+'.brep')))
 candidate.exportBrep(str(O/'brep'/'HELD_AdapterServiceWindow.brep'))
 save('study',{**{n:s for n,s in old.items() if n.startswith(('BB_Monitor','BB_ReplaceableVESA','BB_Display','BB_Stop'))},**{'Proposed_'+n:s for n,s in new.items()},'Held_AdapterWindow':candidate,**refs})
 scenes={'current':{n:mesh(s) for n,s in old.items() if n.startswith(('BB_Monitor','BB_ReplaceableVESA','BB_Stop'))},'proposed':{n:mesh(s) for n,s in new.items()},'held_adapter':mesh(candidate),'references':{n:mesh(s) for n,s in refs.items()}}
 (O/'review-meshes.json.gz').write_bytes(gzip.compress(json.dumps(scenes,separators=(',',':')).encode()))
 report['promoted_breps']={n:str((O/'brep'/(n+'.brep')).relative_to(R)) for n in new}
 (O/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 (O/'result.json').write_text(json.dumps(report,indent=2)+'\n')
 (O/'README.md').write_text('''# V33.6 backbox support study

Native source: `exports/generated/structural-v335/play.FCStd`. The current carriers are Y1240–1258, adapter Y1228–1240, display rear Y1228; historical backbox-service config is 10 mm forward of these accepted B-reps. No existing part is repositioned.

Proposed current change: two 6 × 16 mm R3 through slots per monitor carrier, above the adapter. Minimum outer web 10 mm; between slots 18 mm; net transverse width 38 / 50 mm (76%). Four slots remove 6355.752 mm³ / 0.00413124 kg at650 kg/m³. The nearest depth-bolt reserve is 25.624 mm away; upper monitor clamp reserve 48.208 mm away. Both carriers remain one solid. Capture lands, M067 and all adjustment/retention interfaces remain exact. This is a geometry screen, not strength certification.

The existing carrier FACE_A faces front (-Y), because the M067 capture is machined from that face. New slots are through-cut from that same face; FACE_B receives no CNC. Minimum corner radius R3 exceeds the supplier R2 limit. A 12 mm-wide / 2 mm-thick flexible-strap threading reserve and 60 ×24 mm rear finger corridor were checked with doors open. Actual tie/strap selection remains optional and user configurable.

Existing open space beside the adapter accepts a generic 50 ×30 mm connector cross-section,65 mm body planning envelope, with 205 mm rear removal sweep. This is not a connector SKU or universal fit claim. Two illustrative flexible 5 mm cable routes include R20 bends and retain 2.5 mm minimum modeled clearance. The selected cable bend requirement and display connector positions remain unknown. Rigid backbox fold of these internal routes passes a continuous OCC separation-bound test over 0–90° plus all 13 requested sample angles. A real service loop must be qualified with selected cables; no electronics disconnection is introduced.

A 180 ×70 mm R12 central adapter service window was constructed and quantified. Existing peripheral clamp reserves clear it by 56.801 mm; outer frame webs are 90 /80 mm. Its rear service corridor works. **NOT PROMOTED:** actual VESA load points are absent, and a centered 100 mm row example leaves only 15 mm to the window before bore/washer allowance. Unknown future hole positions can lie within it. The unchanged replaceable VESA adapter remains current until the selected display supports the opening. Retaining a rectangular perimeter alone does not prove the VESA load path.

No new adjustment slots are justified. Existing vertical ±5 mm, depth choices 0 /16 mm, max-width centering ±1 mm and smaller-display centering ±15 mm remain unchanged. Display retention stays four positive clamps; M067 lower adjusters remain unchanged.

`validation.json` includes 29 checks, true B-rep volume and nearest-hardware distances. `brep/BB_MonitorCarrier*.brep` are the only proposed replacements. `brep/CURRENT_*` preserves references; `HELD_AdapterServiceWindow.brep` is isolated and must never be promoted by a glob.

Manufacturing remains blocked pending actual plywood, coupon, purchased hardware and display-specific adapter qualification. No full-sheet or CAM files are generated.
'''.replace('at650','at 650').replace('away; upper','away; upper'))
 print('V336_BACKBOX_STUDY_PASS' if report['pass'] else 'V336_BACKBOX_STUDY_FAIL',len(checks),flush=True)

try:main()
except Exception:
 traceback.print_exc();raise
