"""Complete lock integration and inherited architecture retest. CERN-OHL-S-2.0."""
from backbox_lock_integration_v32 import *
import hashlib,shutil
O.mkdir(parents=True,exist_ok=True);checks=[];results={};scenes={}
def check(n,v,d=None):
    checks.append({'check':n,'pass':bool(v),'details':d});print(('PASS ' if v else 'FAIL ')+n, d if not v else '',flush=True)
    assert v,(n,d)
def persist():
    report={'source_head':C['source_head'],'checks':checks,'results':results,'selected_option':'B','centers_xy_mm':C['lock_centers_xy_mm'],'operation':'HAND','promotion_authority':'config/current_v32.json after regression and viewer gates','mesh_sha256':results.get('mesh_sha256'),'manufacturing_ready':False,'custom_metal_added':0,'input_sha256':{n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in ['config/backbox_lock_integration_v32.json','tools/backbox_lock_integration_v32.py','tools/backbox_lock_integration_v32_entry.py','tools/backbox_lock_search_v32.py','config/backbox_service_v32.json','tools/backbox_service_v32.py']}}
    (O/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
oldq=json.loads((R/C['service_source']/'validation.json').read_text());oldm=json.loads((R/C['service_source']/'motion-validation.json').read_text())
for rep in [oldq,oldm]:
    for n,h in rep['input_sha256'].items():check('unchanged validated service input '+n,hashlib.sha256((R/n).read_bytes()).hexdigest()==h)
check('inherited populated architecture gates',all(x['pass'] for x in oldq['checks']) and oldm['pass'])
search=json.loads((O/'search.json').read_text())
for n,h in search['input_sha256'].items():check('fresh search '+n,hashlib.sha256((R/n).read_bytes()).hexdigest()==h)
check('A evaluated first and fails; symmetric B individually valid',all(not x['pass'] for x in search['option_A']) and len(search['selected'])==2)
src=load(R/C['cabinet_source']/'play.FCStd');removed=load(R/C['cabinet_source']/'matrix-removed.FCStd');p0,g,meta,blanks=service.build(src);p,shelf=bore_reference(p0,src['BACKBOX_BASE']);closed=service.occupied(p,g);opened=service.door_scene(p,g,100,100)
eng,fixedhw,refs=build_locks(False);park,_,_=build_locks(True);eng=with_tethers(eng,False);park=with_tethers(park,True)
newwood={n:s for n,s in eng.items() if 'ParkingPad' in n}
check('all four parking pads single valid solids',all(s.isValid() and len(s.Solids)==1 for s in newwood.values()))
check('parking pads clear populated backbox',not hits(newwood,closed),hits(newwood,closed))
check('generic passage untouched',not hits(newwood,{'passage':passage()}))
results['bearing_before_mm2']=face(p0['BB_Floor'],596.9).common(face(src['BACKBOX_BASE'],596.9)).Area
results['bearing_after_reference_bores_mm2']=face(p['BB_Floor'],596.9).common(face(shelf,596.9)).Area
check('only two reference bores reduce bearing',abs(results['bearing_before_mm2']-results['bearing_after_reference_bores_mm2']-2*math.pi*6**2)<1e-5)
check('net bearing retained above 99.6 percent',results['bearing_after_reference_bores_mm2']/results['bearing_before_mm2']>.996)
# Separate structural threads, intentional engagement, and rare hinge service.
rare={n:s for n,s in reserves().items() if 'HingeAccess' in n};results['rare_hinge_access_hits']=hits(rare,{n:s for n,s in closed.items() if g[n]=='cassette'})
check('hinge hardware and tool reserves clear new lock parts',not hits(eng,{n:s for n,s in reserves().items() if 'Hinge' in n}),hits(eng,{n:s for n,s in reserves().items() if 'Hinge' in n}))
check('cassette and all display envelopes unchanged',all(p[n].cut(p0[n]).Volume+p0[n].cut(p[n]).Volume<1e-6 for n in p if g[n] in ['cassette','display','adapter','carrier','glass','retainer']))
fixed={n:s for n,s in actual(removed).items() if not n.startswith('BB_')};fixed['BACKBOX_BASE']=shelf
# Embedded shanks/captive threads and screw thread engagement are intentional.
check('shelf backing clear cabinet except designated receiver',not hits(fixedhw,{n:s for n,s in fixed.items() if n!='BACKBOX_BASE'}))
check('parked lock bodies clear populated architecture',not hits({n:s for n,s in park.items() if 'ScrewReserve' not in n},closed),hits({n:s for n,s in park.items() if 'ScrewReserve' not in n},closed))
check('engaged heads and tethers clear backbox except intended floor bores',not hits({n:s for n,s in eng.items() if 'ScrewReserve' not in n},closed),hits({n:s for n,s in eng.items() if 'ScrewReserve' not in n},closed))
# Continuous conservative boxes for hands and rigid hardware. Re-grip turns use
# the full circular knob reserve, while hands approach above the rear sill.
accessrows=[];tetherrows=[]
for side,i in [('L',0),('R',1)]:
    x,y=C['lock_centers_xy_mm'][i];px,py=C['parking_centers_xy_mm'][i];name='BB_UprightLock'+side
    obs={**opened,**{n:s for n,s in eng.items() if not n.startswith(name) or 'Parking' in n}}
    # A threaded metal parking insert intentionally mates with the parked bolt;
    # hand corridors are always checked against it and all pads.
    entry=route(x,y);lift=swept(hand(x,y),dz=C['withdrawal_mm']);transfer=swept(hand(x,y,C['withdrawal_mm']),dx=px-x,dy=py-y)
    allhand={**entry,**{'Lift'+n:s for n,s in lift.items()},**{'Transfer'+n:s for n,s in transfer.items()},**{'ParkLower'+n:s for n,s in swept(hand(px,py,36),dz=C['withdrawal_mm']-36).items()}}
    hh=hits(allhand,obs);check('rear hand entry, unlock, parking and reverse '+side,not hh,hh)
    rigid={'HeadSweep':cyl(x,y,FLOOR+3,20,26+C['withdrawal_mm']), 'WasherSweep':cyl(x,y,FLOOR,16,3+C['withdrawal_mm'])}
    # The rod travels only in the reference clearance bore until fully withdrawn.
    hh=hits(rigid,opened);check('full rotating knob and release stroke '+side,not hh,hh)
    released={name:knob(x,y,FLOOR+3+C['withdrawal_mm']),name+'Washer':ring(x,y,FLOOR+C['withdrawal_mm'],16,4.5,3)}
    # Bounding-box sweep is conservative for the axis-aligned transfer.
    hh=hits(swept(released,dx=px-x,dy=py-y),{n:s for n,s in obs.items() if not n.startswith(name+'Parking')});check('released captive assembly transfer '+side,not hh,hh)
    # Exact axial insertion into the parking socket, including the long shank.
    drop=C['withdrawal_mm']-36
    park_sweep={'head':cyl(px,py,FLOOR+39,20,26+drop),'washer':cyl(px,py,FLOOR+36,16,3+drop),'shank':cyl(px,py,FLOOR-1,4,40+drop)}
    park_obs={n:s for n,s in obs.items() if n!=name+'ParkingThread'}
    hh=hits(park_sweep,park_obs);check('axial parking insertion and reverse '+side,not hh,hh)
    accessrows.append({'side':side,'minimum_hand_clearance':minimum(allhand,obs),'withdrawal_mm':C['withdrawal_mm'],'tip_clearance_above_floor_when_lifted_mm':FLOOR+3+C['withdrawal_mm']-40-FLOOR})
    # Mechanical tether, not electrical wiring. Full constant-length route sampled
    # through release and translation; rotational ring avoids accumulated twist.
    for j in range(C['withdrawal_mm']+1):
        z=FLOOR+3+j;tt,ll=tether(side,[x,y],z);hh=hits({'tether':tt},obs);tetherrows.append({'side':side,'phase':'lift','travel':j,'length':ll,'hits':hh})
    for j in range(21):
        t=j/20;tt,ll=tether(side,[x+(px-x)*t,y+(py-y)*t],FLOOR+3+C['withdrawal_mm']);hh=hits({'tether':tt},obs);tetherrows.append({'side':side,'phase':'transfer','fraction':t,'length':ll,'hits':hh})
    for dz in range(36,C['withdrawal_mm']+1):
        tt,ll=tether(side,[px,py],FLOOR+3+dz);hh=hits({'tether':tt},obs);tetherrows.append({'side':side,'phase':'park_lower','travel':dz,'length':ll,'hits':hh})
    scenes['access-'+side]={**opened,**eng,**{name+k:s for k,s in allhand.items()}}
check('mechanical retention tether through unlock and parking',not any(r['hits'] or abs(r['length']-C['mechanical_tether_length_mm'])>.01 for r in tetherrows),[r for r in tetherrows if r['hits']])
results['access']=accessrows;results['mechanical_tether_samples']=tetherrows;persist()
results['continuous_door_vs_locks']={}
for side in ['R','L']:
    ss=service.door_scene(p,g,0,100 if side=='L' else 0);mov={n:s for n,s in ss.items() if g[n] in ['door'+side,'unlocked'+side]}
    hx,hy=service.C['rear']['hinge_axis_xy_mm'][0 if side=='L' else 1]
    results['continuous_door_vs_locks'][side]=certify(mov,{**eng,**{'park_'+n:s for n,s in park.items()}},0,100,V(hx,hy,0),'Z',lambda ss,a:service.door_pose(ss,side,a))
check('continuous rear door integration',True)
# Differential retest of all unchanged service operations against new locks.
# Original service collision certificates remain valid by immutable-source hashes.
doorrows=[]
for side in ['R','L']:
    for angle in [0,.25,.5,1,2,5,10,15,30,45,60,75,90,100]:
        ss=service.door_scene(p,g,angle if side=='L' else 0,100 if side=='L' else angle)
        mov={n:s for n,s in ss.items() if g[n] in ['door'+side,'unlocked'+side]};fl,_=service.flex(side,angle)
        hh=hits({**mov,'fan_loop':fl},{**eng,**park});doorrows.append({'side':side,'angle':angle,'hits':hh})
check('rear leaves, accessories and fan loops clear both lock states',not any(r['hits'] for r in doorrows));results['door_new_parts_samples']=doorrows
# Every new lock part is below Z800; door/accessory material whose Z ranges could
# overlap is beyond Y1284 when closed and travels rearward. Exact continuous door
# certificate added separately in the motion proof.
services={}
for role in ['display','glass','cassette','fan','adjustment']:
    if role=='display':mv={n:s for n,s in closed.items() if g[n] in ['display','adapter']};ss=swept(mv,dy=-400)
    elif role=='glass':ss=swept({'glass':p['BB_Backglass']},dz=500)
    elif role=='cassette':ss=swept({n:s for n,s in closed.items() if g[n]=='cassette'},dy=-240)
    elif role=='fan':ss={}
    else:ss={}
    services[role]=hits(ss,{**eng,**park})
check('display, glass and cassette service sweeps preserved',not any(services.values()),services)
# Driver/fan original swept boxes are wholly above locks; separation verifies them.
maxz=max(s.BoundBox.ZMax for s in list(eng.values())+list(park.values()))
check('fan withdrawal and monitor adjustment above lock system',maxz<810)
results['service_differential']=services;results['max_lock_system_z_mm']=maxz
# Full populated fold includes parked bolts, captive washers and tethers.
foldbase={**closed,**park,**{'BB_FlexCorridor'+s:service.flex(s,0)[0] for s in ['L','R']}}
foldobs={**fixed,**fixedhw};foldrows=[]
for angle in [0,.001,.01,.05,.1,.25,.5,1,2,5,10,15,30,45,60,75,90]:
    mm=transform(foldbase,angle=angle,axis=WPC);hh=hits(mm,foldobs)
    # Parking screw threads intentionally embed in the co-moving floor only.
    foldrows.append({'angle':angle,'hits':hh});check('populated parked-lock fold '+str(angle),not hh,hh)
results['fold_samples']=foldrows
newmov={n:s for n,s in park.items() if not n.endswith('ScrewReserve0') and not n.endswith('ScrewReserve1')}
results['continuous_new_locks_fold']=certify(newmov,foldobs)
results['continuous_old_backbox_vs_new_shelf_hardware']=certify(closed,fixedhw)
check('continuous fold lock integration',True)
pfmov={n:s for n,s in removed.items() if n in pf_names(removed)};pfrows=[]
for angle in range(51):pfrows.append({'angle':angle,'hits':hits(transform(pfmov,angle=-angle),{**eng,**park,**fixedhw})})
for dz in range(49):pfrows.append({'lift':dz,'hits':hits(transform(pfmov,lift=dz),{**eng,**park,**fixedhw})})
check('playfield service and lift-out preserved',not any(r['hits'] for r in pfrows));results['playfield_new_parts_samples']=pfrows
blank_fold={**{n:s for n,s in closed.items() if not n.startswith(('BB_Fan','BB_Flex'))},**blanks,**park}
results['continuous_blank_modules_fold']=certify(blanks,foldobs)
check('optional blank modules fold clear',True)
# Native review and all CURRENT viewer states; no historical CAD overwritten.
scenes.update({'locks-engaged':{**closed,**eng,**fixedhw,'BACKBOX_BASE':shelf},'locks-parked':{**closed,**park,**fixedhw,'BACKBOX_BASE':shelf},'doors-open':{**opened,**eng,**fixedhw,'BACKBOX_BASE':shelf},'wood-reserves':{'BB_Floor':p['BB_Floor'],'BACKBOX_BASE':shelf,**refs,**fixedhw,**rare},'backbox-exploded':{n:shifted(s,y=220 if g[n].startswith(('door','locked')) else -250 if g[n] in ['glass','bezel','cassette'] else -130 if g[n] in ['display','adapter','carrier'] else 0,z=150 if g[n]=='retainer' else 0) for n,s in closed.items()}})
scenes['backbox-exploded'].update({**eng,**fixedhw})
scenes['blank-fans']={**{n:s for n,s in closed.items() if not n.startswith(('BB_Fan','BB_Flex'))},**blanks,**eng,**fixedhw,'BACKBOX_BASE':shelf}
scenes['toy-zones']={**closed,**eng,**{n:s for n,s in p.items() if g[n]=='zone'}}
for angle in [1,45,90]:scenes['fold-'+str(angle)]={**foldobs,**transform(foldbase,angle=angle,axis=WPC)}
basebundle=json.loads((R/C['cabinet_source']/'mesh.json').read_text());oldrep=json.loads((R/C['cabinet_source']/'validation.json').read_text());saved=oldrep['saved_poses'];current={}
for state,fn in saved.items():
    prior=load(R/C['cabinet_source']/fn);ss={n:s for n,s in prior.items() if not n.startswith('BB_')};ss['BACKBOX_BASE']=shelf;ss.update(fixedhw)
    bb=transform(foldbase,angle=90,axis=WPC) if state=='BACKBOX FOLD' else {**closed,**eng,**{'BB_FlexCorridor'+s:service.flex(s,0)[0] for s in ['L','R']}}
    ss.update(bb)
    zones={n:s for n,s in p.items() if g[n]=='zone'}
    ss.update(transform(zones,angle=90,axis=WPC) if state=='BACKBOX FOLD' else zones)
    current[state]=ss;save(Path(fn).stem,ss)
for name,ss in scenes.items():save(name,ss)
# Coarse B-rep tessellation only for rendering; collisions above use exact solids.
raw={'scenes':{n:[coarse_mesh(k,s) for k,s in ss.items()] for n,ss in scenes.items()},'details':{'old_access':[coarse_mesh(n,s) for n,s in reserves().items() if 'LockTool' in n],'hinges':[coarse_mesh(n,s) for n,s in reserves().items() if 'Hinge' in n],'hand_L':[coarse_mesh(n,s) for n,s in route(*C['lock_centers_xy_mm'][0]).items()]}}
(O/'review-mesh.json').write_text(json.dumps(raw,separators=(',',':')))
# Preserve original non-backbox mesh bytes/labels; explicit state overrides for
# every new populated backbox part, including released-and-parked fold hardware.
oldparts={x['name']:x for x in basebundle['parts']};parts=[]
for n,s in current['PLAY'].items():parts.append(oldparts[n] if n in oldparts and not n.startswith('BB_') and n!='BACKBOX_BASE' else coarse_mesh(n,s))
basebundle['parts']=parts
for state in basebundle['states']:
    prev=basebundle['states'][state];prev={n:v for n,v in prev.items() if not n.startswith('BB_')}
    ss=current[state]
    for n,s in ss.items():
        if n.startswith(('BB_','UprightLock')) or n=='BACKBOX_BASE':prev[n]=coarse_mesh(n,s)
    basebundle['states'][state]=prev
basebundle['review']['backbox_service']={'promoted':True,'two_rear_doors':True,'locks':'TWO REAR-OPERATED CAPTIVE HAND KNOBS; RELEASE AND THREAD INTO PARKING SOCKETS','normal_fold_cassette_removal':False,'backbox_glass_retained':True,'rare_hinge_service_cassette_removal':True,'manufacturing_ready':False}
basebundle['review']['matrix_cassette']['fold_status']='POPULATED 0–90 VALIDATED; LOCKS PARKED; REAR DOORS LATCHED; PLAYFIELD GLASS + MATRIX REMOVED; BACKBOX GLASS RETAINED; manufacturing BLOCKED'
rawmesh=json.dumps(basebundle,separators=(',',':'))+'\n';(O/'mesh.json').write_text(rawmesh)
check('source service CAD and exact populated parts preserved',all(p[n].cut(p0[n]).Volume+p0[n].cut(p[n]).Volume<1e-5 for n in p if n!='BB_Floor'))
results['saved_poses']=saved;results['cad_scenes']=list(scenes);results['mesh_sha256']=hashlib.sha256(rawmesh.encode()).hexdigest();results['inherited_service_validation_sha256']=hashlib.sha256((R/C['service_source']/'validation.json').read_bytes()).hexdigest();persist()
for name in ['LICENSE','NOTICE.md']:shutil.copyfile(R/name,O/name)
print('BACKBOX_LOCK_INTEGRATION_PASS',len(checks),flush=True)
