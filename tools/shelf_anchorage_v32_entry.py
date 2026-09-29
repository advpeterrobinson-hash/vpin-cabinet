"""Separate side-anchorage candidate. Original material: CERN-OHL-S-2.0."""
import hashlib,json
from pathlib import Path
import FreeCAD as A
import Part
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'exports/generated/side-panel-v32'
cp=ROOT/'config/shelf_anchorage_v32.json';c=json.loads(cp.read_text())
rp=OUT/'retention-validation.json';prior=json.loads(rp.read_text());mp=OUT/'motion-validation.json';motion=json.loads(mp.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if not all(x['pass'] for x in prior['checks']):raise RuntimeError('Retention audit failed')
for name,h in prior['source_hashes'].items():
    if digest(ROOT/name)!=h:raise RuntimeError('Stale retention input: '+name)
source=ROOT/prior['saved_proposal']['path']
if digest(source)!=prior['saved_proposal']['sha256']:raise RuntimeError('Stale retention CAD')
inputs=[cp,rp,mp,source,Path(__file__).resolve()];hashes={str(p.relative_to(ROOT)):digest(p) for p in inputs}
doc=A.openDocument(str(source));doc.recompute()
scene={o.Name:o.Shape.copy() for o in doc.Objects if hasattr(o,'Shape')};original={n:s.copy() for n,s in scene.items()}
checks=[];axes=[];hardware={}
def check(n,v):checks.append({'check':n,'pass':bool(v)})
def cylinder(x,y,z,r,length,direction):return Part.makeCylinder(r,length,A.Vector(x,y,z),A.Vector(direction,0,0))
def hits(moving,obstacles):
    out=[]
    for n,s in moving.items():
        for k,t in obstacles.items():
            if s.BoundBox.intersect(t.BoundBox):
                v=s.common(t).Volume
                if v>c['collision_threshold_mm3']:out.append({'moving':n,'obstacle':k,'mm3':v})
    return out
def sweep_box(s,v):
    b=s.BoundBox
    return Part.makeBox(b.XLength+abs(v.x),b.YLength+abs(v.y),b.ZLength+abs(v.z),A.Vector(b.XMin+min(0,v.x),b.YMin+min(0,v.y),b.ZMin+min(0,v.z)))
for i in (1,2,3):
    for side,direction in [('L',1),('R',-1)]:
        sn=f'SHELF_SUPPORT_{i}{side}';wall='SIDE_'+side;b=scene[sn].BoundBox
        face=b.XMin if side=='L' else b.XMax
        inward=b.XMax if side=='L' else b.XMin
        z=(b.ZMin+b.ZMax)/2
        for j,offset in enumerate(c['anchor_y_offsets_mm'],1):
            y=b.YMin+offset;name=f'CandidateSupportAnchor{i}{side}{j}'
            scene[sn]=scene[sn].cut(cylinder(face-direction,y,z,c['support_bore_diameter_mm']/2,b.XLength+2,direction))
            scene[wall]=scene[wall].cut(cylinder(face,y,z,c['side_blind_bore_diameter_mm']/2,c['side_blind_depth_mm'],-direction))
            insert=cylinder(face,y,z,c['insert_diameter_mm']/2,c['insert_length_mm'],-direction).cut(cylinder(face+direction,y,z,c['shaft_diameter_mm']/2,c['insert_length_mm']+2,-direction))
            washer=cylinder(inward,y,z,c['washer_diameter_mm']/2,c['washer_thickness_mm'],direction).cut(cylinder(inward-direction,y,z,c['support_bore_diameter_mm']/2,c['washer_thickness_mm']+2,direction))
            head=inward+direction*c['washer_thickness_mm'];tip=head-direction*c['shaft_length_mm']
            bolt=cylinder(tip,y,z,c['shaft_diameter_mm']/2,c['shaft_length_mm'],direction).fuse(cylinder(head,y,z,c['head_diameter_mm']/2,c['head_length_mm'],direction)).removeSplitter()
            hardware[name]=bolt;hardware[name+'Washer']=washer;hardware[name+'Insert']=insert
            axes.append({'name':name,'support':sn,'wall':wall,'side':side,'direction':direction,'xyz_mm':[face,y,z],
                         'support_inner_face_mm':inward,'head_start_x_mm':head,'tip_x_mm':tip,
                         'nominal_shaft_insert_overlap_mm':c['shaft_length_mm']-b.XLength-c['washer_thickness_mm'],
                         'remaining_outer_skin_mm':original[wall].BoundBox.XLength-c['side_blind_depth_mm']})
scene.update(hardware)
check('12 support anchors',len(axes)==12)
check('all candidate solids valid',all(s.isValid() and len(s.Solids)==1 for s in scene.values()))
changed={n for n,s in original.items() if s.cut(scene[n]).Volume+scene[n].cut(s).Volume>1e-4}
check('only six supports and two side shapes changed',changed=={'SIDE_L','SIDE_R'}|{f'SHELF_SUPPORT_{i}{s}' for i in (1,2,3) for s in ('L','R')})
mirror=A.Matrix();mirror.A11=-1;mirror.A14=600
for left,right in [('SIDE_L','SIDE_R')]+[(f'SHELF_SUPPORT_{i}L',f'SHELF_SUPPORT_{i}R') for i in (1,2,3)]:
    reflected=scene[left].transformGeometry(mirror)
    check(left+' mirrored geometry',reflected.cut(scene[right]).Volume+scene[right].cut(reflected).Volume<1e-4)
installed=hits(hardware,{n:s for n,s in scene.items() if n not in hardware})
check('anchor hardware clears installed scene',not installed)
items=list(hardware.items());internal=[]
for index,(name,shape) in enumerate(items):internal+=hits({name:shape},dict(items[index+1:]))
check('anchor hardware mutually clear',not internal)
# Verify blind bottoms by probing the entire remaining outside skin at each axis.
for a in axes:
    face,y,z=a['xyz_mm'];direction=a['direction'];thick=original[a['wall']].BoundBox.XLength
    x=face-direction*thick
    skin=cylinder(x,y,z,c['side_blind_bore_diameter_mm']/2,a['remaining_outer_skin_mm'],direction)
    check(a['name']+' retained 7.5mm outer skin',abs(scene[a['wall']].common(skin).Volume-skin.Volume)<1e-4)
# Support replacement only after unloading/removing that shelf. Check normal
# shelf release still works with these new anchor heads retained underneath.
removed=motion['config']['monitor_assembly']+motion['config']['crossmembers']
service={n:s for n,s in scene.items() if n not in removed};shelf_routes=[]
for spec in motion['config']['shelf_routes']:
    name=spec['object'];moving_names=[name,name+'_CandidatePayload']+spec['removed_payload']
    released=[n for a in prior['axes'] if a['shelf']==name for n in (a['bolt'],a['washer'])]
    obstacles={n:s for n,s in service.items() if n not in moving_names+released}
    moving={n:scene[n].copy() for n in moving_names};conflicts=[]
    for v in (A.Vector(0,spec['stage_y_mm']-scene[name].BoundBox.YMin,0),A.Vector(0,0,max(o.BoundBox.ZMax for o in obstacles.values())+motion['config']['top_exit_margin_mm']-scene[name].BoundBox.ZMin)):
        conflicts+=hits({n:sweep_box(s,v) for n,s in moving.items()},obstacles)
        for s in moving.values():s.translate(v)
    check(name+' loaded removal retained',not conflicts)
    shelf_routes.append({'shelf':name,'conflicts':conflicts})
# New side anchors must preserve the already-approved shelf release direction.
retention_access=[]
pc=prior['config']
for a in prior['axes']:
    x,y,z=a['xyz_mm'];obs={n:s for n,s in service.items() if n not in (a['bolt'],a['washer'])}
    driver=Part.makeCylinder(pc['driver_radius_mm'],pc['driver_length_mm'],A.Vector(x,y,a['head_top_z_mm']))
    dh=hits({'driver':driver},obs)
    hz=z+pc['washer_thickness_mm'];travel=pc['bolt_withdrawal_mm']
    bolt=Part.makeCylinder(pc['shaft_diameter_mm']/2,pc['shaft_length_mm']+travel,A.Vector(x,y,hz-pc['shaft_length_mm'])).fuse(
        Part.makeCylinder(pc['head_diameter_mm']/2,pc['head_height_mm']+travel,A.Vector(x,y,hz)))
    washer=Part.makeCylinder(pc['washer_diameter_mm']/2,pc['washer_thickness_mm']+travel,A.Vector(x,y,z)).cut(
        Part.makeCylinder(pc['clearance_bore_diameter_mm']/2,pc['washer_thickness_mm']+travel+2,A.Vector(x,y,z-1)))
    wh=hits({'bolt':bolt,'washer':washer},obs)
    check(a['bolt']+' prior driver access preserved',not dh)
    check(a['bolt']+' prior withdrawal preserved',not wh)
    retention_access.append({'bolt':a['bolt'],'driver_conflicts':dh,'withdrawal_conflicts':wh})
cover_access=[]
for index,entry in enumerate(prior['cover_access'],1):
    axis=entry['axis'];probe=Part.makeCylinder(pc['cover_driver_radius_mm'],pc['cover_driver_length_mm'],A.Vector(*axis['xyz_mm']),A.Vector(0,0,-1))
    conflict=hits({'driver':probe},scene)
    check('cover '+str(index)+' prior driver access preserved',not conflict)
    cover_access.append({'axis':axis,'conflicts':conflict})
access=[];support_routes=[];insert_access=[]
for i in (1,2,3):
    name=f'SHELF_{i}';spec=motion['config']['shelf_routes'][i-1]
    absent=[name,name+'_CandidatePayload']+spec['removed_payload']+[n for a in prior['axes'] if a['shelf']==name for n in (a['bolt'],a['washer'])]
    obstacles={n:s for n,s in service.items() if n not in absent}
    for a in (a for a in axes if a['support'].startswith(f'SHELF_SUPPORT_{i}')):
        _,y,z=a['xyz_mm'];d=a['direction'];head=a['head_start_x_mm'];tip=a['tip_x_mm'];travel=c['withdrawal_mm']
        exclude=[a['name'],a['name']+'Washer'];obs={n:s for n,s in obstacles.items() if n not in exclude}
        driver=cylinder(head+d*c['head_length_mm'],y,z,c['driver_radius_mm'],c['driver_length_mm'],d)
        driver_hits=hits({'driver':driver},obs)
        screw_sweep=cylinder(tip,y,z,c['shaft_diameter_mm']/2,c['shaft_length_mm']+travel,d).fuse(cylinder(head,y,z,c['head_diameter_mm']/2,c['head_length_mm']+travel,d))
        wstart=a['support_inner_face_mm']
        washer_sweep=cylinder(wstart,y,z,c['washer_diameter_mm']/2,c['washer_thickness_mm']+travel,d).cut(cylinder(wstart-d,y,z,c['support_bore_diameter_mm']/2,c['washer_thickness_mm']+travel+2,d))
        withdrawal_hits=hits({'screw':screw_sweep,'washer':washer_sweep},obs)
        check(a['name']+' inward driver access',not driver_hits)
        check(a['name']+' inward complete withdrawal',not withdrawal_hits)
        check(a['name']+' tip clears support',d*(tip+d*travel-wstart)>0)
        access.append({'anchor':a['name'],'driver_conflicts':driver_hits,'withdrawal_conflicts':withdrawal_hits})
    for side,d in [('L',1),('R',-1)]:
        sn=f'SHELF_SUPPORT_{i}{side}';moving_names=[sn,f'CandidateNutCover{i}{side}']+[a['nut'] for a in prior['axes'] if a['support']==sn]
        local=[a for a in axes if a['support']==sn];released=[n for a in local for n in (a['name'],a['name']+'Washer')]
        obs={n:s for n,s in obstacles.items() if n not in moving_names+released}
        moving={n:scene[n].copy() for n in moving_names};conflicts=[]
        legs=(A.Vector(d*c['support_inward_release_mm'],0,0),A.Vector(0,spec['stage_y_mm']-scene[sn].BoundBox.YMin,0),A.Vector(0,0,max(o.BoundBox.ZMax for o in obs.values())+motion['config']['top_exit_margin_mm']-min(s.BoundBox.ZMin for s in moving.values())))
        for v in legs:
            conflicts+=hits({n:sweep_box(s,v) for n,s in moving.items()},obs)
            for s in moving.values():s.translate(v)
        check(sn+' replacement route',not conflicts)
        retained_stop=scene[sn].translated(A.Vector(d,0,0)).common(scene[local[0]['name']+'Washer']).Volume
        check(sn+' retained anchor blocks inward movement',retained_stop>c['collision_threshold_mm3'])
        support_routes.append({'support':sn,'moving':moving_names,'translations_mm':[[v.x,v.y,v.z] for v in legs],'conflicts':conflicts,'retained_washer_stop_mm3':retained_stop})
        for a in local:
            face,y,z=a['xyz_mm']
            probe=cylinder(face,y,z,c['driver_radius_mm'],c['driver_length_mm'],d)
            conflict=hits({'insert_driver':probe},obs)
            check(a['name']+' insert access after support removal',not conflict)
            insert_access.append({'anchor':a['name'],'conflicts':conflict})
# Negative control: drill-through mutation must destroy the retained skin.
a=axes[0];face,y,z=a['xyz_mm'];wall=scene[a['wall']];mutant=wall.cut(cylinder(face,y,z,c['side_blind_bore_diameter_mm']/2,19,-1))
skin=cylinder(0,y,z,c['side_blind_bore_diameter_mm']/2,7.5,1)
check('negative control rejects through-drilled side',mutant.common(skin).Volume<1e-5)
check('inputs unchanged',all(digest(ROOT/n)==h for n,h in hashes.items()))
proposal=A.newDocument('ShelfSideAnchorageV32')
proposal.Comment='CERN-OHL-S-2.0; Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet; NOT manufacturing release'
for name,s in scene.items():
    o=proposal.addObject('PartDesign::Feature',name);o.Shape=s;o.addProperty('App::PropertyString','PartCode')
    o.PartCode=getattr(doc.getObject(name),'PartCode','') if doc.getObject(name) else ''
    o.Label=(o.PartCode or 'PROVISIONAL '+name)+' / anchorage study'
proposal.recompute();path=OUT/'shelf-anchorage-proposal.FCStd';proposal.saveAs(str(path));A.closeDocument(proposal.Name)
proposal=A.openDocument(str(path));proposal.recompute();actual={o.Name:o.Shape for o in proposal.Objects if hasattr(o,'Shape')}
check('saved identity set',set(actual)==set(scene))
check('saved permanent part codes preserved',all(proposal.getObject(n).PartCode==getattr(doc.getObject(n),'PartCode','') for n in original))
check('saved valid solids',all(s.isValid() and len(s.Solids)==1 for s in actual.values()))
check('saved exact shapes',all(actual[n].cut(s).Volume+s.cut(actual[n]).Volume<1e-4 for n,s in scene.items()))
report={'status':c['status'],'manufacturing_ready':False,'config':c,'source_hashes':hashes,'checks':checks,'axes':axes,
        'retention_access':retention_access,'cover_access':cover_access,'insert_access':insert_access,'installed_conflicts':installed,'hardware_conflicts':internal,'access':access,'shelf_routes':shelf_routes,'support_routes':support_routes,
        'changed_original_objects':sorted(changed),'saved_proposal':{'path':str(path.relative_to(ROOT)),'sha256':digest(path),'solids':len(scene)},
        'limitations':['No selected insert or verified side pilot; no thread/installation/load certification','Side bores only in separate proposal; actual stock/cutter/relief and pullout/vibration tests required','Support replacement requires unloaded removed shelf and monitor/crossmember teardown prerequisites','Axial probes do not prove hand access or whole-tool insertion','Continuous conservative swept boxes for shelf/support assemblies; exact coaxial sweeps for bolts/washers']}
(OUT/'anchorage-validation.json').write_text(json.dumps(report,indent=2)+'\n')
assert all(x['pass'] for x in checks),[x for x in checks if not x['pass']]
print('SHELF_ANCHORAGE_PASS',len(checks),'checks;',len(scene),'saved solids; CNC BLOCKED')
A.closeDocument(proposal.Name);A.closeDocument(doc.Name)
