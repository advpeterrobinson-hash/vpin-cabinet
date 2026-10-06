"""Conservative V35.1 attachment, load-path and small-part audit. Original CAD only."""
from widebody_v351_common import *
p=load(O/'candidate.FCStd');reg=json.loads((O/'manufacturing-register.json').read_text());wa=json.loads((O/'width-audit.json').read_text());checks=[]
def ck(n,v,d=None):checks.append({'name':n,'pass':bool(v),'detail':d})
def contact(a,b):
 return sum(f.common(g).Area for f in a.Faces for g in b.Faces if f.BoundBox.intersect(g.BoundBox) and f.distToShape(g)[0]<1e-6)
def info(n):
 if n.startswith('SHELF_SUPPORT'):return ('SCREWED','SIDE_L/R','Shelf bearing and removable support','Broad42x150 support; spreads load without further thinning side; service screws remain accessible.')
 if n.startswith('CROSS_GUIDE'):return ('SCREWED','SIDE_L/R','Crossmember location and distributed bearing','145x60 backing; repeatable location and removable transverse members. Retain rather than deeper side routing.')
 if n.startswith('CROSS_'):return ('BOLTED','CROSS_GUIDE + sides','Structural transverse stiffness','Protected section and Y/Z. Width span regenerated; no loss of section.')
 if n.startswith('SHELF_'):return ('REMOVABLE','SHELF_SUPPORT pair','Equipment gravity bearing','Three intentional service shelves, supported at both sides; width matches widened supports.')
 if n.startswith('FLOOR_CLEAT'):return ('GLUED+SCREWED','FLOOR + SIDE','Continuous floor ledge','M006 protected; retained contact area and direct floor load path.')
 if n.startswith('CandidateLegBlock'):return ('SHOP-MADE','SIDE + FRONT/REAR','Leg bolt bearing into54x54x126 solid block','SW01 protected; load distribution and drill-jig architecture retained.')
 if n.startswith('FrontLanding'):return ('BOLTED','SIDE / SW02 interface','Closed playfield gravity and uplift restraint','SW02 protected, side-relative location; no merged plywood substitute.')
 if n.startswith('PF_OpenCradle'):return ('SCREWED','FLOOR + SIDE','Dowel seat to floor gravity load','Direct floor-bearing path; side screws retain against tipping;18mm seat profile unchanged.')
 if n=='PF_BasePlywood':return ('BOLTED','Wood dowel/straps + front landings','Playfield VESA load distribution','Horn-free base maintains landing bearing and lift-out.')
 if n.startswith('BB_UprightLock') and 'ParkingPad' in n:return ('SCREWED','BB_Floor; pad1 on pad0','Parking insert and released bolt capture','36mm stack keeps parked shaft above floor;18mm floor alone loses this depth. No reduced blind thread reserve.')
 if n.startswith('BB_MONITOR_STOP'):return ('SCREWED','BB_SideL/R','Vertical monitor plate reaction','12x18 actual plate overlap216mm2 per stop; integral4mm guide stop only72mm2. Separate block is replaceable without repairing side.')
 if n.startswith('BB_FanBlank'):return ('REMOVABLE','BB_DoorL/R upper fan station','Optional sealed unused upper station','Real dust/closed-station role for unpopulated build; not needed for grille-only airflow. Retain OPTIONAL, not required assembly.')
 if n.startswith('BB_HingeCleat'):return ('SCREWED','BB_RearFrame','Continuous hinge backing and door/fan load','23mm bearing width and14mm finished depth; preserves hinge axis and avoids driving into a weak edge.')
 if n=='BB_GLASS_BOTTOM_SEAT':return ('SCREWED','BB_SideL/R lower front','Padded acrylic lower-edge bearing','744x18 seat is replaceable and keeps acrylic separate from removable DMD panel; no thinner structural side pocket.')
 if n=='BB_GLASS_TOP_RETAINER':return ('REMOVABLE','BB_Top','Positive acrylic capture during fold','One simple removable strip; needed to remove acrylic from FRONT without shell-top removal.')
 if n=='BB_CenterAstragal':return ('SCREWED','BB_DoorL','Overlap seal and active lock reaction','No permanent center mullion. Replaceable gasket landing and latch reaction.')
 if n.startswith('BB_Door'):return ('REMOVABLE','Piano hinge + hinge cleat','Service leaf, fans; not shell shear','Both leaves give large rear access and retained100degree sweep.')
 if n=='BB_MONITOR_PLATE':return ('CAPTURED','BB_Side guides + stops + BB_Top','VESA loads into backbox sides','Permanent captured plate; monitor front-removable.')
 if n=='BB_DMD_SPEAKER_PANEL':return ('REMOVABLE','Backbox front side interfaces','DMD and speaker masses','One direct removable panel; no obsolete cassette or adapter stack.')
 if n.startswith('BB_'):return ('CAPTURED','Backbox shell joints + mechanical fasteners','Shell structure / racking / fold loads','Protected simplified backbox; no deletion proposed.')
 if n.startswith('MX_WoodSeat'):return ('SCREWED','BACKBOX_BASE','Matrix bearing and removal datum','Preserves accepted rocking/forward/lift path; attachment pilots follow centered matrix.')
 if n=='MatrixCarrier':return ('REMOVABLE','MX_WoodSeat pair','Matrix mechanical carrier','Same size; centered on new body, retained service path.')
 if n=='PC_BASE':return ('SCREWED','FLOOR','PC/chassis attachment base','Protected simple board; no drawer or additional tray.')
 if n=='SSF_BST_Carrier':return ('BOLTED','FLOOR','Tactile transducer coupling','Existing removable commodity device interface retained.')
 if n.startswith('RemovableIntakeFilter'):return ('REMOVABLE','FLOOR fan station','Filter media support','Downward service and existing12mm one-face construction.')
 if n=='Underfront_Plate':return ('REMOVABLE','FLOOR module bay','User controls; no structural replacement','12mm replaceable module, shared bay and four machine attachments; final controls held.')
 if n=='REAR_DOOR':return ('REMOVABLE','REAR / commercial hinges and lock','Routine service access','Current main service door unchanged apart from centerline placement.')
 if n=='BACKBOX_BASE':return ('CAPTURED','SIDE_L/R + retained mechanical fixing','Backbox broad shelf bearing and rear glass support','Same horizontal18mm stock; two small integral front lands add fixing edge distance, no separate rail.')
 if n in ['SIDE_L','SIDE_R','FRONT','REAR','FLOOR']:return ('GLUED+SCREWED','Captured shell joints','Primary shell loads','4mm captured-joint architecture; measured-stock/coupon holds retained.')
 raise RuntimeError('Unexplained wood '+n)
audit=[]
for a in reg['parts']:
 n=a['source_component'];attachment,parent,load_role,reason=info(n);bd=a['reference_bounds_3d_mm'];mx=max(bd[i+3]-bd[i] for i in range(3));area=a['outer_contour_area_mm2'];small=(area is not None and area<20000) or mx<150
 audit.append({'ID':a['manufacturing_part_id'],'instance':a['instance_id'],'name':n,'function':load_role,'parent':parent,'attachment':attachment,'load_or_location':load_role,'assembly_value':reason,'service_value':reason,'classification':'KEEP','small':small,'outer_area_mm2':area,'max_dimension_mm':mx,'rationale':reason})
protected=[n for n in p0 if n.startswith(('FLOOR_CLEAT','CandidateLegBlock','FrontLandingL_Block','FrontLandingR_Block','PF_OpenCradle','SHELF_SUPPORT','CROSS_GUIDE')) or n=='PC_BASE']
for n in protected:
 dx=wa[n]['translation_x_mm'];q=shift(p[n],x=-dx);e=q.cut(p0[n]).Volume+p0[n].cut(q).Volume;ck('protected exact '+n,e<.001,e)
for n in ['CROSS_1','CROSS_2','CROSS_3','SHELF_1','SHELF_2','SHELF_3','FLOOR_CLEAT_18','FLOOR_CLEAT_552']:
 ck('required structural presence '+n,n in p and p[n].Volume>=p0[n].Volume-.001)
for n in ['BB_MONITOR_STOP_L','BB_MONITOR_STOP_R']:
 area=contact(p[n],p['BB_MONITOR_PLATE']);ck('monitor stop bearing '+n,abs(area-216)<.01,{'current_mm2':area,'blind_guide_alternative_mm2':4*18,'decision':'KEEP: three times projected bearing; no cut into side'})
# Test12mm pilot engagement entirely in the two integral lands. No holes are drilled.
land=[];proof={}
for x in [33,W-33]:
 y=1125.125;z=(N0-1.5+y*sa)/ca;pt=V(x,y,z);axis=V(0,sa,-ca);pilot=Part.makeCylinder(1.5,12,pt,axis)
 missing=pilot.cut(p['BACKBOX_BASE']).Volume
 head=Part.makeCone(3,1.5,2.2,pt+V(0,-sa,ca)*.8,axis)
 proof['RearFixingPilot'+str(x)]=pilot;proof['RearFixingHead'+str(x)]=head
 land.append({'reference_x_mm':x,'reference_y_mm':y,'face_z_mm':z,'front_edge_mm':10,'side_edge_mm':10,'vertical_remaining_stock_mm':z-578.9,'pilot_embedment_reference_mm':12,'pilot_missing_wood_mm3':missing,'glass_intersection_mm3':head.common(p['CandidateGlass']).Volume,'status':'PACKAGING TEST POINT ONLY; count/diameter/centers NULL for production'})
ck('rear channel ordinary screw lands',all(a['pilot_missing_wood_mm3']<.001 and a['glass_intersection_mm3']<.001 for a in land),land)
# Body and clearances are planning reserves, not measured commercial CAD or a guessed latch trajectory.
obs={n:q for n,q in p.items() if n in actual(p) and not n.startswith('Receiver') and n!='LockdownReceiverReference'}
ck('receiver body and operating reserve',not hits({n:p[n] for n in ['LockdownReceiverReference','ReceiverLatchReserve','ReceiverToolReserve']},obs))
ck('commercial architecture not custom',C['commercial']['custom_lockdown'] is False)
ck('siderail optional regression',C['commercial']['siderail_optional'] is True)
ck('5mm primary',C['glass']['commercial_reference_mm'][2]==5)
fold=load(O/'fold-90.FCStd');tools={}
for a in land:
 pt=V(a['reference_x_mm'],a['reference_y_mm'],a['face_z_mm']);tools['Driver'+str(a['reference_x_mm'])]=Part.makeCylinder(6,80,pt+V(0,-sa,ca)*1,V(0,-sa,ca))
obstacles={n:q for n,q in fold.items() if n in actual(fold) and n not in ['CandidateGlass','PF_RearGlassChannel'] and not n.startswith(('Matrix','MX_Retainer'))}
ck('rear fixing tool access folded90',not hits(tools,obstacles),hits(tools,obstacles))
proof.update(tools)
save('fixing-reserves',proof);dump('attachment-audit',audit);dump('small-part-audit',[a for a in audit if a['small']]);dump('conservative-validation',{'checks':checks,'pass':all(a['pass'] for a in checks),'no_part_count_target':True,'no_reduced_load_path':True,'integrated':[],'retired':[],'added':[],'rear_land':land,'receiver_note':'Body520x42x40; additional388.65x42x15 free volume;90x42x85 hand/tool approach. Actual latch trajectory NULL, not a certification of the purchased receiver.'})
print('AUDIT',len(audit),'SMALL',sum(a['small'] for a in audit),'PASS',sum(a['pass'] for a in checks),'FAIL',[a for a in checks if not a['pass']]);assert all(a['pass'] for a in checks)
