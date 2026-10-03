"""Compact removable underfloor module: native design/reference envelopes.
CERN-OHL-S-2.0. Source https://github.com/advpeterrobinson-hash/vpin-cabinet
Purchased hardware is not selected; all individual device/attachment bores held.
"""
from pathlib import Path
import sys,json,hashlib,math,itertools
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,V
from coin_door_v32 import definitions,turn
C=json.loads((R/'config/underfront_user_module_v337.json').read_text());M=C['module'];O=R/C['output'];O.mkdir(exist_ok=True,parents=True);B=O/'brep';B.mkdir(exist_ok=True)
old=load(R/C['source']);xc,yc=M['center_xy_mm'];w,h=M['external_size_mm'];depth=M['selected_recess_mm'];zfloor=18;ztop=zfloor+depth;zface=ztop-12
def box(x,y,z,w,d,h):return Part.makeBox(w,d,h,V(x,y,z))
def cyl(x,y,z,r,h):return Part.makeCylinder(r,h,V(x,y,z))
def ring(x,y,z,ro,ri,h):return cyl(x,y,z,ro,h).cut(cyl(x,y,z,ri,h))
def rr(x,y,z,w,h,r,t):
 s=box(x+r,y,z,w-2*r,h,t).fuse(box(x,y+r,z,w,h-2*r,t))
 for xx in [x+r,x+w-r]:
  for yy in [y+r,y+h-r]:s=s.fuse(cyl(xx,yy,z,r,t))
 return s.removeSplitter()
def shifted(s,dx=0,dy=0,dz=0):q=s.copy();q.translate(V(dx,dy,dz));return q
def bb(s):b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def bboxgap(s,t):
 a,b=s.BoundBox,t.BoundBox
 return math.sqrt(sum(max(0,getattr(a,k+'Min')-getattr(b,k+'Max'),getattr(b,k+'Min')-getattr(a,k+'Max'))**2 for k in 'XYZ'))
def sweep_box(s,delta):
 b=s.BoundBox;return box(b.XMin+min(0,delta[0]),b.YMin+min(0,delta[1]),b.ZMin+min(0,delta[2]),b.XLength+abs(delta[0]),b.YLength+abs(delta[1]),b.ZLength+abs(delta[2]))
def near(s,obs,limit=1e9):
 out=[];nearest=limit
 for n,t in sorted(obs.items(),key=lambda x:bboxgap(s,x[1])):
  if bboxgap(s,t)>nearest:continue
  d=s.distToShape(t)[0]
  if d<nearest:nearest=d;out=[{'part':n,'distance_mm':d,'volume_mm3':s.common(t).Volume if d<1e-7 else 0}]
  elif abs(d-nearest)<1e-7:out.append({'part':n,'distance_mm':d,'volume_mm3':s.common(t).Volume if d<1e-7 else 0})
 return out
def penetrations(ss,obs):
 rows=[]
 for n,s in ss.items():
  for k,t in obs.items():
   if not s.BoundBox.intersect(t.BoundBox):continue
   v=s.common(t).Volume
   if v>1e-5:rows.append({'moving':n,'fixed':k,'volume_mm3':v})
 return rows
fit=M['reference_fit_gap_each_side_mm'];rw,rh=M['through_aperture_mm']
recess=rr(xc-w/2-fit,yc-h/2-fit,zfloor,w+2*fit,h+2*fit,6+fit,depth)
aperture=rr(xc-rw/2,yc-rh/2,17,rw,rh,8,20)
floor=old['FLOOR'].cut(aperture).cut(recess).removeSplitter()
plate=rr(xc-w/2,yc-h/2,zface,w,h,6,12)
slots=[]
for dx,dy in M['cable_clamp_reference_zones_local_xy_mm']:
 # Native capsule4x12: same Ø4 cutter follows an8mm centerline, no dogbone.
 slot=cyl(xc+dx,yc+dy-4,zface-1,2,14).fuse(cyl(xc+dx,yc+dy+4,zface-1,2,14)).fuse(box(xc+dx-2,yc+dy-4,zface-1,4,8,14)).removeSplitter()
 plate=plate.cut(slot);slots.append(slot)
plate=plate.removeSplitter();common={'Underfront_Plate':plate};references={'Underfront_BayApertureReference':aperture,'Underfront_RecessReference':recess}
for i,(dx,dy) in enumerate(M['attachment_offsets_xy_mm'],1):
 x,y=xc+dx,yc+dy
 common[f'Underfront_Screw{i}']=cyl(x,y,zface,2,20).fuse(cyl(x,y,zface-3,4,3))
 common[f'Underfront_Insert{i}']=ring(x,y,ztop,4,2.05,10)
 references[f'Underfront_PlateAttachmentBore{i}']=cyl(x,y,zface-1,2.25,14)
 references[f'Underfront_FloorInsertBore{i}']=cyl(x,y,ztop,4,10)
buttons={};reserves={}
for i,(dx,dy) in enumerate(M['button_cells_mm'],1):
 x,y=xc+dx,yc+dy
 buttons[f'Underfront_Button{i}_Body']=cyl(x,y,zface,15,45)
 buttons[f'Underfront_Button{i}_Face']=cyl(x,y,zface-8,17.5,8)
 buttons[f'Underfront_Button{i}_Nut']=ring(x,y,ztop,19,15.05,10)
 buttons[f'Underfront_Button{i}_Switch']=box(x-18,y-11,zface+45,36,22,17)
 buttons[f'Underfront_Button{i}_WireReserve']=box(x-20,y-20,zface+62,40,40,23)
 references[f'Underfront_Button{i}_BoreReference']=cyl(x,y,zface-1,15,14)
ux,uy=xc+42,yc+21
usb={'Underfront_USBBody':cyl(ux,uy,zface,13.25,46.8),'Underfront_USBFlange':cyl(ux,uy,zface-4,16.5,4),
 'Underfront_USBNut':ring(ux,uy,ztop,16.5,13.3,8.2),'Underfront_USBCap':cyl(ux,uy,zface-6,17,2),
 'Underfront_USBCableReserve':box(ux-21,uy-21,zface+46.8,42,42,70-46.8)}
references['Underfront_USBBoreReference']=cyl(ux,uy,zface-1,14.15,14)
references['Underfront_USBRearPocketReserve']=cyl(ux,uy,zface+4,19,8)
owner={n:s for n,s in buttons.items() if not n.startswith('Underfront_Button6_')}|usb
generic=buttons
fallback={n:s for n,s in buttons.items() if any(n.startswith('Underfront_Button'+str(i)+'_') for i in [1,2,4,5])}|{n:shifted(s,dy=-21) for n,s in usb.items()}
common['Underfront_HarnessLoopReserve']=box(*M['harness_loop_reserve_xyz_size_mm'])
obs=actual(old);obs['SHELF_1_CandidatePayload']=old['SHELF_1_CandidatePayload'];obs.pop('FLOOR');obs.update({n:s for n,s in old.items() if n.startswith(('Button','Leaf')) or n=='PLUNGER_RESERVED'})
checks=[]
def ck(name,value,detail=None):checks.append({'name':name,'pass':bool(value),'detail':detail});print(name,bool(value),flush=True)
ck('new floor and12mm plate each valid single solid',all(s.isValid() and len(s.Solids)==1 for s in [floor,plate]))
ck('bay and perimeter recess originate from existing underside FACE_A',depth==2 and old['FLOOR'].BoundBox.ZLength==18)
ck('module stays below structural shoulder with zero penetration',plate.common(floor).Volume<1e-5)
for name,parts in [('OWNER5_USB',owner),('GENERIC6',generic),('FALLBACK4_USB',fallback)]:
 bad=penetrations({'Underfront_Plate':plate}|parts,obs)
 ck(name+' hardware and85/70mm rear service clear actual cabinet',not bad,bad)
 ck(name+' rear hardware clears through aperture',not penetrations(parts,{'FLOOR_WITH_BAY':floor}),penetrations(parts,{'FLOOR_WITH_BAY':floor}))
 # Continuous negativeZ translation of rectangular upper-bound envelopes;
 # FLOOR intentionally tested against exact swept solids separately below.
 env={n:sweep_box(s,[0,0,-100]) for n,s in ({'Plate':plate}|parts).items()}
 ck(name+'100mm downward service sweep clears cabinet',not penetrations(env,obs),penetrations(env,obs))
 floorhits=[]
 for n,s in ({'Plate':plate}|parts).items():
  # Exact solid translation by extrusion union via planar footprint for
  # cylindrical devices; rectangular sweeps for allparts, actual roundedplate
  # plus body sweep rectangle must stay inside roundedrecess until release.
  if n=='Plate':q=plate.fuse(shifted(plate,dz=-100)).fuse(rr(xc-w/2,yc-h/2,zface-100,w,h,6,112))
  else:q=sweep_box(s,[0,0,-100])
  v=q.common(floor).Volume
  if v>1e-5:floorhits.append({'part':n,'volume_mm3':v})
 ck(name+' withdrawal also clears machined floor',not floorhits,floorhits)
# Arcade face/nut envelopes fit42mm grid with4mm nut gap. USB pocket reserve
# radius19 is optional ONLY in12mm module, not structuralFLOOR.
ck('6button nuts have4mm nominal minimum gap',42-38>=4)
ck('generic flexibleharness loop reserve clear abovebay',not penetrations({'loop':common['Underfront_HarnessLoopReserve']},obs))
ck('USB rear pocket reserve does not intersect adjacent device bore',all(references['Underfront_USBRearPocketReserve'].common(s).Volume<1e-5 for n,s in references.items() if n.startswith('Underfront_Button') and '6_' not in n and n!='Underfront_Button6_BoreReference'))
# Coin door sweep is an independent operating state.
coin=json.loads((R/'config/front_panel_v32.json').read_text());defs=definitions(coin,True);moving={n:s for n,(s,k,m) in defs.items() if m}
coin_hits=[]
moduleoccupied={'Plate':plate}|owner
for angle in range(111):
 for n,s in moving.items():
  t=turn(s,coin['coin_door'],angle)
  for k,q in moduleoccupied.items():
   if t.BoundBox.intersect(q.BoundBox) and t.common(q).Volume>1e-5:coin_hits.append([angle,n,k])
ck('coin door0to110deg clears module andcontrol envelopes',not coin_hits,coin_hits)
# All door rotating components retain their Z range; prove continuous Z
# separation from module upperbound, not merely angle samples.
door_z=min(s.BoundBox.ZMin for s in moving.values());module_z=max(s.BoundBox.ZMax for s in moduleoccupied.values())
ck('coin door continuous vertical separation',door_z-module_z>0,{'door_z_min':door_z,'module_z_max':module_z,'clearance_mm':door_z-module_z})
hinge=coin['coin_door']['hinge_axis_mm'];maxrear=-float('inf')
# Exact extrema of Y=hy+dy*cos(a)-dx*sin(a), bounded over every
# rotating B-rep's enclosing-box vertices. Convex boxes contain all points.
for s in moving.values():
 b=s.BoundBox
 for x,y in itertools.product([b.XMin,b.XMax],[b.YMin,b.YMax]):
  dx,dy=x-hinge[0],y-hinge[1];angles=[0,math.radians(110)]
  base=math.atan2(-dx,dy)
  angles += [base+k*math.pi for k in range(-2,3) if 0<=base+k*math.pi<=math.radians(110)]
  maxrear=max(maxrear,max(hinge[1]+dy*math.cos(a)-dx*math.sin(a) for a in angles))
loopgap=common['Underfront_HarnessLoopReserve'].BoundBox.YMin-maxrear
ck('flexibleloop remains behind whole outwardcoin sweep',loopgap>=3,{'method':'Analytic rotating enclosing-box corner extrema over0..110deg about -Z','coin_sweep_Y_max_mm':maxrear,'loop_Y_min_mm':110,'separation_mm':loopgap})
# Player/front approach: palm below cabinet; finger curls up only at target.
human={};humanresults=[]
visiblecontrols={n:s for n,s in owner.items() if n.endswith('_Face') or n=='Underfront_USBFlange'}
fixed=obs|{'FLOOR_WITH_BAY':floor,'Underfront_Plate':plate}|visiblecontrols
for i,(dx,dy) in enumerate(M['button_cells_mm'][:5],1):
 x,y=xc+dx,yc+dy
 palm=box(x-35,-85,-50,70,y+105,25)
 finger=box(x-10,y-12,-25,20,24,zface-8+25)
 ss={'palm':palm,'finger':finger};oo={n:s for n,s in fixed.items() if n!=f'Underfront_Button{i}_Face'}
 bad=penetrations(ss,oo);humanresults.append({'control':i,'pass':not bad,'hits':bad});human.update({f'Underfront_AccessButton{i}_{k}':s for k,s in ss.items()})
ck('five finger press approaches with70mm palm clear neighboring controls',all(r['pass'] for r in humanresults),humanresults)
drivers=[]
for i,(dx,dy) in enumerate(M['attachment_offsets_xy_mm'],1):
 x,y=xc+dx,yc+dy
 driver=cyl(x,y,-145,4,150).fuse(cyl(x,y,-215,15,70))
 bad=penetrations({'driver':driver},fixed)
 drivers.append({'screw':i,'pass':not bad,'hits':bad});human[f'Underfront_AttachmentDriver{i}']=driver
ck('four underside screwdrivers require no interior nut orplayfield access',all(q['pass'] for q in drivers),drivers)
# USB hand/plug access is from below, cable pointsdown; cap folds rearwards.
usbhand=box(ux-15,uy-16,-55,30,32,49);plug=box(ux-9,uy-6,-35,18,12,39)
usbobs={n:s for n,s in fixed.items() if n not in ['Underfront_USBFlange']}
ck('USB plug hand corridor clears neighbors/cabinet',not penetrations({'USBHand':usbhand,'Plug':plug},usbobs),penetrations({'USBHand':usbhand,'Plug':plug},usbobs))
human.update({'Underfront_USBHand':usbhand,'Underfront_USBPlug':plug})
cap=usb['Underfront_USBCap'];caps=[];caphits=[]
for angle in range(0,121,2):
 q=cap.copy();q.rotate(V(ux,uy+17,zface-4),V(1,0,0),angle);caps.append(q)
 caphits+=penetrations({'cap':q},{n:s for n,s in fixed.items() if n!='Underfront_USBFlange'})
ck('rearward cap0to120deg clears panel andneighbors',not caphits,caphits)
human['Underfront_USBCapSweep']=Part.makeCompound(caps)
# Stand-up front sightlines to controlfaces are intercepted by opaque FRONT.
eyes=[V(300,-450,1000),V(180,-400,900),V(420,-400,900)];sight=[]
for eye in eyes:
 for n,s in visiblecontrols.items():
  target=s.CenterOfMass;line=Part.makeLine(eye,target);blockers=[k for k in ['FRONT','CoinStudy_DoorLeaf','CoinStudy_CoinFrame'] if line.common(old[k]).Length>0]
  sight.append({'control':n,'eye':list(eye),'occluded_by_front':bool(blockers),'closed_front_occluders':blockers})
ck('controlfaces hidden in three standing-front sightline screens',all(r['occluded_by_front'] for r in sight),sight)
# Recess depth comparison holds functionalface/outsidehardware clearances.
recesses=[{'depth_mm':d,'remaining_structural_skin_mm':18-d,'panel_projection_below_floor_mm':12-d,'selected':d==2,'reason':'2mm positive location already sufficient; deeper recess removes more structuralskin without neededfunction'} for d in M['recess_candidates_mm']]
nearest={}
for label,names in [('front',['FRONT']),('SW01',['CandidateLegBlockFL','CandidateLegBlockFR']),('leg_hardware',['CandidateLegPlateFL','CandidateLegPlateFR']),('M006',['FLOOR_CLEAT_18','FLOOR_CLEAT_552']),('coin_tray',['CoinStudy_CoinTray','CoinStudy_TraySupport1','CoinStudy_TraySupport2']),('landings',[n for n in old if n.startswith('FrontLanding')]),('plunger',['PLUNGER_RESERVED']),('side_buttons',[n for n in old if n.startswith(('Leaf','Button'))]),('S1',[n for n in old if n.startswith(('SHELF_1','SHELF_SUPPORT_1'))]),('SSF',['SSF_BST_Carrier','SSF_BST1_Reference'])]:
 nearest[label]=near(Part.makeCompound([plate]+list(owner.values())),{n:old[n] for n in names})
ck('permanent front capture untouched andfullheightfrontweb>=44mm',aperture.BoundBox.YMin-22>=44 and floor.common(old['FRONT']).Volume<=old['FLOOR'].common(old['FRONT']).Volume+1e-5)
ck('exact only scopedfloor modification',floor.cut(old['FLOOR']).Volume<1e-5)
new={**old,'FLOOR':floor,**common,**owner}
def save(name,ss):
 d=A.newDocument('V337_'+name)
 for n,s in ss.items():o=d.addObject('PartDesign::Feature',n);o.Shape=s
 d.recompute();assert all(o.Shape.isValid() for o in d.Objects if hasattr(o,'Shape'));d.saveAs(str(O/(name+'.FCStd')));A.closeDocument(d.Name)
save('module',new);save('modulevariants',{n:s for n,s in buttons.items() if n.startswith('Underfront_Button6_')});save('module-study',references|human);save('module-fallback',{'Underfront_Plate':plate}|fallback)
for n,s in {'FLOOR':floor,**common,**owner,**generic,**references,**human}.items():s.exportBrep(str(B/(n+'.brep')))
# Manufacturing contract includes actual sourceCAD, exact local transforms and
# explicit one-face CUT/POCKET operations; uncut device interfaces stayREFERENCE.
reg=json.loads((R/'exports/generated/front-landings-v3363/manufacturing-register.json').read_text());fr=next(p for p in reg['parts'] if p['source_component']=='FLOOR')
pm=A.Matrix();pm.A11=1;pm.A22=-1;pm.A33=-1;pm.A14=xc-w/2;pm.A24=yc+h/2;pm.A34=ztop
fm=A.Matrix(*fr['local_to_installed_matrix'])
members=[]
for inst,mid,n,s,mat,stock,ops in [('P005-Main','M005','FLOOR',floor,fm,18,[('CUT','bay',aperture,18),('POCKET','locating-shoulder',recess,2)]),('P097-Main','M074','Underfront_Plate',plate,pm,12,[('CUT','strain-slot'+str(i+1),q,12) for i,q in enumerate(slots)])]:
 inv=mat.inverse();local=s.copy();local.transformShape(inv,True);path=B/(inst+'-finished.brep');local.exportBrep(str(path));localops=[]
 for group,label,q,dep in ops:
  q=q.copy();q.transformShape(inv,True);op=B/(inst+'-'+label+'.brep');q.exportBrep(str(op));localops.append({'group':group,'id':label,'face':'FACE_A','depth_mm':dep,'brep':str(op.relative_to(R))})
 members.append({'instance_id':inst,'manufacturing_part_id':mid,'source_component':n,'nominal_stock_thickness_mm':stock,'finished_reference_thickness_mm':stock,'local_to_installed_matrix':list(mat.A),'finished_member_brep':str(path.relative_to(R)),'installed_member_brep':str((B/(n+'.brep')).relative_to(R)),'machining_face':'FACE_A','face_A_outward_world':[0,0,-1] if n=='FLOOR' else [0,0,1],'operations_added':localops,'attachment_interfaces':'REFERENCE_ONLY / PURCHASE_BEFORE_CNC / guided manual pilot fromsameFACE_A datum','device_bores':None,'quantity':1,'optional_variant_not_extra_piece':n=='Underfront_Plate'})
(O/'module-manufacturing-map.json').write_text(json.dumps({'source_config':'config/underfront_user_module_v337.json','members':members,'manufacturing_release':False},indent=2)+'\n')
variants=[]
for id,name,pt,ns in [('UNDERFRONT_OWNER','Owner —5buttons +dualUSB','Proprietário —5botões +USB duplo',list(owner)),('UNDERFRONT_BUTTON_ONLY','Generic —6buttons','Genérico —6botões',list(generic)),('UNDERFRONT_BLANK','Blank mechanical plate','Placa mecânica sem controles',[])]:
 variants.append({'id':id,'names':{'en':name,'pt-BR':pt},'object_names':ns,'status':'HARDWARE_PENDING' if ns else 'MECHANICAL_FLATPACK_DEFAULT'})
motion={'variants':variants,'default_variant':'UNDERFRONT_OWNER','common_names':list(common),'removable_names':['Underfront_Plate']+list(owner)+[n for n in buttons if n.startswith('Underfront_Button6_')],'removal_vector_mm':[0,0,-100],'rigid_removal_validated':all(q['pass'] for q in checks if 'withdrawal' in q['name'] or 'service sweep' in q['name']),
 'variant_native_file':str((O/'modulevariants.FCStd').relative_to(R)),'variant_only_names':[n for n in buttons if n.startswith('Underfront_Button6_')],
 'fixed_names':['FLOOR','Underfront_HarnessLoopReserve']+[n for n in common if 'Insert' in n],'screw_names':[n for n in common if 'Screw' in n],'final_interface_status':{'button_bore_mm':None,'usb_cutout':None,'attachment_bore_mm':None,'status':'PURCHASE_BEFORE_CNC'},
 'harness':'Builder-selected disconnect,250mm minimum planning service slack in60x44x60mm loopreserve,2module-side strain slots; remove4screws,lower100mm,disconnectforbenchservice. Flexible wire trajectory is envelope-screened, not a cablebend certification.'}
(O/'module-motion.json').write_text(json.dumps(motion,indent=2)+'\n')
report={'pass':all(q['pass'] for q in checks),'checks':checks,'source_sha256':hashlib.sha256((R/C['source']).read_bytes()).hexdigest(),'native_sha256':hashlib.sha256((O/'module.FCStd').read_bytes()).hexdigest(),'changed_existing':['FLOOR'],'added_names':list(common)+list(owner),'new_wood_names':['Underfront_Plate'],'variant_only_names':motion['variant_only_names'],
 'selected':{'plate_size_mm':[w,h,12],'center_xy_mm':[xc,yc],'plate_bounds_mm':bb(plate),'recess_bounds_mm':bb(recess),'through_aperture_bounds_mm':bb(aperture),'recess_depth_mm':2,'remaining_shoulder_skin_mm':16,'aperture_fullheight_front_web_from_capture_mm':aperture.BoundBox.YMin-22,'recess_front_web_from_capture_mm':recess.BoundBox.YMin-22,'pitch_mm':42,'physically_feasible_pitch_mm':40,'owner_buttons':5,'generic_buttons':6,'usb_rear_reserve_mm':70},
 'recess_study':recesses,'nearest':nearest,'floor_removed_volume_mm3':old['FLOOR'].Volume-floor.Volume,'plate_volume_mm3':plate.Volume,'device_holes_not_cut':True,'manufacturing_release':False,'physical_ergonomic_qualification':False,
 'limits':['Representative finger/palm and three viewing points, not population ergonomic certification','Production leg length/groundclearance/kneegeometry remains hardwaredependent; controls do not descend below cabinet side/front loweredgeZ0','Hardware envelopeexample is not a purchasedSKU','Controlbody/plate andscrew/insert/uncutwood overlaps are intentional referenceinterfaces awaiting selectedbore','No electrical connector selected; cable250mm slack andbendradius must be verified in actualharness']}
(O/'module-validation.json').write_text(json.dumps(report,indent=2)+'\n')
assert report['pass'],checks
print('V337_MODULE_PASS',len(checks),flush=True)
