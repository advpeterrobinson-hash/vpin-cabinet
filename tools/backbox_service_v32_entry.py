"""B-rep service validation and review artifacts; no manufacturing release.
CERN-OHL-S-2.0. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet
"""
from pathlib import Path
import sys,json,math,hashlib,shutil
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_service_v32 import *
O.mkdir(parents=True,exist_ok=True);checks=[];results={}
def check(n,v,details=None):
    checks.append({'check':n,'pass':bool(v),'details':details})
    if not v: print('FAIL',n,details,flush=True)
def persist():
    (O/'validation.json').write_text(json.dumps({'source_head':C['source_head'],'checks':checks,'results':results,'input_sha256':{n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in ['config/backbox_service_v32.json','tools/backbox_service_v32.py','tools/backbox_service_v32_entry.py']},'promoted':False,'manufacturing_ready':False},indent=2)+'\n')
def delta(a,b):return a.cut(b).Volume+b.cut(a).Volume
src=R/C['source_directory'];play=load(src/'play.FCStd');removed=load(src/'matrix-removed.FCStd');p,g,meta,blanks=build(play)
closed=occupied(p,g);fixed={n:s for n,s in actual(removed).items() if not n.startswith('BB_')};sourcebb={n:s for n,s in play.items() if n.startswith('BB_')}
check('validated transverse WPC axis retained',list(WPC)==[300,1066.8,508])
check('all new physical parts valid single solids',all(s.isValid() and len(s.Solids)==1 for s in p.values()),[n for n,s in p.items() if not s.isValid() or len(s.Solids)!=1])
check('Y1146 floor and generic passage unchanged',delta(p['BB_Floor'],play['BB_Floor'])<1e-6)
check('side profiles only lose upper glass rebate material',all(p[n].cut(play[n]).Volume<1e-6 for n in ['BB_SideL','BB_SideR']))
low=box(-100,1000,580,800,400,240)
check('210 lower sides entirely unchanged below Z820',all(delta(p[n].common(low),play[n].common(low))<1e-6 for n in ['BB_SideL','BB_SideR']))
check('shelf bearing unchanged',abs(face(p['BB_Floor'],596.9).common(face(play['BACKBOX_BASE'],596.9)).Area-65672.4)<1e-5)
wood={n:s for n,s in p.items() if meta[n]['material']=='plywood' and g[n]!='optional'}
wh=[]
for i,(n,s) in enumerate(wood.items()):wh+=hits({n:s},dict(list(wood.items())[i+1:]))
check('no wood self penetration',not wh,wh)
check('center meeting gap has continuous gasket backing including astragal ends',box(299,1308.1,654,2,2,608).cut(p['BB_CenterGasket']).Volume<1e-7)
payload={n:s for n,s in p.items() if n in ['BB_Display32','BB_DMDEnvelope','BB_SpeakerEnvelopeL','BB_SpeakerEnvelopeR']}
hh=hits(payload,{n:s for n,s in closed.items() if n not in payload and 'Reserve' not in n})
check('occupied display and speaker envelopes clear structure',not hh,hh)
hardware_bodies={n:s for n,s in p.items() if 'PassiveBoltBody' in n or 'CamLockBody' in n}
hh=hits(hardware_bodies,wood);check('provisional door hardware bodies do not embed in wood',not hh,hh)
zones={n:s for n,s in p.items() if g[n]=='zone'}
hh=hits(zones,{n:s for n,s in closed.items() if 'Reserve' not in n});check('four side toy mounting volumes unoccupied',not hh,hh)
check('full rear aperture without a center post',p['BB_RearFrame'].common(box(-12,1290.1,654,624,18,608)).Volume<1e-6)
results['rear_aperture_mm']=[684,608];results['aperture_percent_of_clear_internal_rectangle']=100*684*608/(744*(1302.8-614.9))
# Locks and hinge floor installation routes remain independent of lower electronics.
from backbox_structure_review_v32 import reserves
access={n:s for n,s in reserves().items() if 'LockTool' in n or 'HingeAccess' in n}
results['installed_lock_hinge_access_hits']=hits(access,{n:s for n,s in closed.items() if n not in sourcebb and 'Reserve' not in n})
hh=hits(access,{n:s for n,s in closed.items() if n not in sourcebb and g[n]!='cassette' and 'Reserve' not in n});check('original lock and hinge floor tool corridors restored with front cassette removed',not hh,hh)
results['upright_hits']=hits(closed,fixed);check('complete service architecture upright clear of current cabinet',not results['upright_hits'],results['upright_hits'])
persist();print('STATIC_SCREEN_FINISHED',flush=True)
# Door motion: active right opens first; then passive left. Its bolts and cam are
# explicitly retracted. Never certify the mechanically interlocked wrong sequence.
doorrows=[];looprows=[];maxrear=0;minloop=math.inf
for side in ['R','L']:
    for a in sorted(set([i*2 for i in range(51)]+[.1,.25,.5,1,5,15,45,75])):
        ss=door_scene(p,g,a if side=='L' else 0,100 if side=='L' else a)
        mov={n:s for n,s in ss.items() if g[n] in ['door'+side,'unlocked'+side]}
        obs={n:s for n,s in ss.items() if n not in mov}
        hh=hits(mov,obs);doorrows.append({'side':side,'angle_deg':a,'hits':hh})
        maxrear=max(maxrear,max(s.BoundBox.YMax for s in mov.values()))
        f,met=flex(side,a)
        obsloop={**{n:s for n,s in ss.items() if n!='BB_FanStrainReliefReserve'+side},**zones}
        hh=hits({'flex':f},obsloop);gap=minimum({'flex':f},obsloop)
        looprows.append({'side':side,'angle_deg':a,**met,'clearance':gap,'hits':hh});minloop=min(minloop,met['minimum_centerline_bend_radius_mm'])
    print('DOOR_LOOP_SAMPLED',side,flush=True);persist()
results['door_samples']=doorrows;results['loop_samples']=looprows
results['rear_service_space_from_original_rear_mm']=maxrear-1308.1
check('both door sequences 0 to 100 sampled clear',not any(r['hits'] for r in doorrows))
check('constant 160 mm loop corridor clear at all door samples',not any(r['hits'] for r in looprows))
check('flex loop bend screen and constant length',minloop>=C['fan_flex']['minimum_bend_radius_screen_mm'] and all(abs(r['length_mm']-160)<.01 for r in looprows))
persist()
# Display front extraction, glass upward extraction and rear accessible adjustment.
frontobs={n:s for n,s in closed.items() if g[n] not in ['display','adapter','glass','retainer','bezel'] and 'MonitorClampReserve' not in n and 'MonitorStopScrew' not in n}
displaymov={n:s for n,s in closed.items() if g[n] in ['display','adapter'] and 'MonitorClampReserve' not in n}
frontrows=[]
for y in range(0,401,10):
    mm={n:shifted(s,y=-y) for n,s in displaymov.items()};hh=hits(mm,frontobs);frontrows.append({'withdrawal_mm':y,'hits':hh})
results['front_removal']=frontrows;check('32 display and replaceable adapter withdraw through front',not any(r['hits'] for r in frontrows))
glassrows=[];glassobs={n:s for n,s in closed.items() if g[n] not in ['glass','retainer']}
for z in range(0,501,10):glassrows.append({'lift_mm':z,'hits':hits({'glass':shifted(p['BB_Backglass'],z=z)},glassobs)})
results['glass_removal']=glassrows;check('backbox glass lifts 500 without monitor removal',not any(r['hits'] for r in glassrows))
adjust=[]
for depth in C['display']['depth_positions_mm']:
    for z in C['display']['vertical_adjustment_mm']+[0]:
        for x in C['display']['centering_at_max_width_mm']+[0]:
            moved={n:shifted(s,x=x if g[n] in ['display','adapter'] else 0,y=depth,z=z if g[n] in ['display','adapter'] else 0) for n,s in closed.items() if g[n] in ['display','adapter','carrier'] and 'Reserve' not in n}
            obs={n:s for n,s in closed.items() if g[n] not in ['display','adapter','carrier'] and 'Reserve' not in n}
            hh=hits(moved,obs);adjust.append({'depth_mm':depth,'z_mm':z,'centering_mm':x,'hits':hh})
results['monitor_adjustment']=adjust;check('maximum display fits all stated adjustment extrema',not any(r['hits'] for r in adjust),[r for r in adjust if r['hits']])
opened=door_scene(p,g,100,100);drivers={}
for x in C['display']['adjustment_bolt_x_mm']:
    for z in C['display']['adjustment_bolt_z_mm']:drivers[f'clamp{x}_{z}']=cylinder_y(x,1258,z,8,200)
    drivers[f'depth_low{x}']=Part.makeCylinder(6,140,V(x,1277,877))
    drivers[f'depth_high{x}']=Part.makeCylinder(6,140,V(x,1277,1229),V(0,0,-1))
driverobs={n:s for n,s in opened.items() if 'Reserve' not in n}
hh=hits(drivers,driverobs);results['rear_driver_hits']=hh;check('rear adjustment drivers reachable with both doors open',not hh,hh)
# Fan replacement requires no monitor/DMD/door removal. Accessories unbolt through
# common mounting pattern; occupied fan translates away from the open door.
fanrows=[]
for side in ['L','R']:
    name='BB_Fan'+side;others={n:s for n,s in opened.items() if n!=name and 'Reserve' not in n}
    for travel in range(0,161,10):
        sh=door_pose({name:shifted(p[name],y=-travel)},side,100)
        fanrows.append({'side':side,'withdrawal_mm':travel,'hits':hits(sh,others)})
results['fan_service']=fanrows;check('each fan replaceable on open attached door',not any(r['hits'] for r in fanrows))
results['optional_shelf_hits']=hits({'shelf':p['BB_OptionalToyShelfStudy']},closed)
results['optional_shelf_decision']='NOT INSTALLED: central shelf would obstruct lower-to-upper air and hand/cable routes; retain as removable accessory study only'
persist();print('SERVICE_SCREEN_FINISHED',flush=True)
# Full combined fold: playfield glass and matrix removed, doors secured, backbox
# glass and all monitor/cassette parts retained. Original cabinet is untouched.
foldrows=[]
foldclosed={**closed,**{'BB_FlexCorridor'+side:flex(side,0)[0] for side in ['L','R']}}
for a in sorted(set([0,.001,.01,.05,.1,.25,.5,1,2,5,10,15,30,45,60,75,90])):
    mm=transform(foldclosed,angle=a,axis=WPC);hh=hits(mm,fixed)
    foldrows.append({'angle_deg':a,'hits':hh})
    print('FOLD_SAMPLE',a,'HITS',hh,flush=True)
results['fold_samples']=foldrows;check('complete populated backbox 0 to 90 sampled',not any(r['hits'] for r in foldrows),[r for r in foldrows if r['hits']])
pfmov={n:removed[n] for n in pf_names(removed)};pfrows=[]
for a in range(51):pfrows.append({'angle_deg':a,'hits':hits(transform(pfmov,angle=-a),closed)})
for z in range(49):pfrows.append({'lift_mm':z,'hits':hits(transform(pfmov,lift=z),closed)})
results['playfield_new_interface']=pfrows;check('playfield service and lift preserved',not any(r['hits'] for r in pfrows))
persist();print('COMBINED_MOTION_SCREEN_FINISHED',flush=True)
# Record mass as a planning inventory, not certified capacities. Envelopes are not
# solid lumps of plywood; electronic masses are explicit assumptions.
wood_volume=sum(s.Volume for n,s in p.items() if meta[n]['material']=='plywood' and g[n]!='optional')
results['planning_mass']={'plywood_volume_mm3':wood_volume,'density_kg_m3':650,'wood_kg':wood_volume*650e-9,'display_kg':7,'dmd_kg':2,'speaker_pair_kg':3.2,'glass_kg':p['BB_Backglass'].Volume*2500e-9,'accessories_hardware_wiring_kg':3,'certified':False}
results['planning_mass']['total_kg']=sum(v for k,v in results['planning_mass'].items() if k.endswith('_kg'))
results['net_intake_planning_mm2']=2*C['ventilation']['intake_width_mm']*80*C['ventilation']['mesh_free_area_planning_fraction']
results['fan_opening_pair_mm2']=2*math.pi*58**2
persist()
# Save only actual geometry, including independent optional/zone objects hidden
# from occupied states. Review CAD is distinct from the production/master model.
scenes={'rear-closed':closed,'rear-active-open':door_scene(p,g,0,100),'rear-both-open':opened,
        'glass-removal':{**{n:s for n,s in closed.items() if g[n]!='retainer'},'BB_Backglass':shifted(p['BB_Backglass'],z=500)},
        'monitor-removal':{**frontobs,**{n:shifted(s,y=-400) for n,s in displaymov.items()}},
        'blank-fans':{**{n:s for n,s in closed.items() if not n.startswith(('BB_Fan','BB_PianoLeaf')) or n.startswith('BB_PianoLeaf')},**blanks}}
scenes['toy-zones']={**closed,**zones};scenes['optional-shelf']={**closed,'BB_OptionalToyShelfStudy':p['BB_OptionalToyShelfStudy']}
scenes['cassette-exploded']={n:shifted(s,y=-180 if g[n]=='cassette' else 0) for n,s in closed.items()}
for n in list(scenes['cassette-exploded']):
    if any(k in n for k in ['Baffle','Bezel']):scenes['cassette-exploded'][n]=shifted(scenes['cassette-exploded'][n],y=-80)
scenes['mechanical-exploded']={n:shifted(s,y=220 if g[n].startswith(('door','locked')) else -250 if g[n] in ['glass','bezel','cassette'] else -130 if g[n] in ['display','adapter','carrier'] else 0,z=150 if g[n]=='retainer' else 0) for n,s in closed.items()}
for a in [1,15,45,90]:scenes[f'fold-{a}']={**{n:s for n,s in removed.items() if not n.startswith('BB_')},**transform(foldclosed,angle=a,axis=WPC)}
scenes['complete-upright']={**{n:s for n,s in play.items() if not n.startswith('BB_')},**closed}
for side in ['L','R']:
    f,_=flex(side,100);scenes['rear-both-open']['BB_FlexCorridor'+side]=f
    f,_=flex(side,0);scenes['rear-closed']['BB_FlexCorridor'+side]=f
cadfiles={}
for state,ss in scenes.items():
    doc=A.newDocument('BackboxService');doc.addProperty('App::PropertyString','Authority');doc.Authority='DESIGN STUDY; hardware unmeasured; manufacturing BLOCKED'
    for n,s in ss.items():
        ob=doc.addObject('PartDesign::Feature',n);ob.Shape=s
        ob.addProperty('App::PropertyString','SourceAuthority');ob.SourceAuthority=meta.get(n,{}).get('authority','unchanged current V32 cabinet')
    doc.recompute();check('CAD recompute '+state,not any('Invalid' in ob.State for ob in doc.Objects));fn=state+'.FCStd';doc.saveAs(str(O/fn));A.closeDocument(doc.Name);cadfiles[state]=fn
base={n:mesh(n,s) for n,s in closed.items()};state_mesh={}
for state,ss in scenes.items():state_mesh[state]=[mesh(n,s) for n,s in ss.items()]
detail={'parts':list(base.values()),'states':state_mesh,'groups':g,'metadata':meta,'blanks':[mesh(n,s) for n,s in blanks.items()],'zones':[mesh(n,s) for n,s in zones.items()],'drivers':[mesh(n,s) for n,s in drivers.items()]}
(O/'review-mesh.json').write_text(json.dumps(detail,separators=(',',':'))+'\n')
results['cad_files']=cadfiles;persist()
for n in ['LICENSE','NOTICE.md']:shutil.copyfile(R/n,O/n)
print('BACKBOX_SERVICE_SCREEN_COMPLETE',len(checks),'ALL_PASS',all(q['pass'] for q in checks),flush=True)
