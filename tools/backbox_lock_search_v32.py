"""OCC access map, evaluated in owner A/B priority order. CERN-OHL-S-2.0."""
from backbox_lock_integration_v32 import *
O.mkdir(parents=True,exist_ok=True)
src=load(R/C['cabinet_source']/'play.FCStd');p,g,meta,blanks=service.build(src);opened=service.door_scene(p,g,100,100)
obs={n:s for n,s in opened.items() if n!='BB_Floor'}
hinge={n:s for n,s in reserves().items() if 'Hinge' in n};floor=p['BB_Floor'];shelf=src['BACKBOX_BASE']
# First preference: test real occupied heads, axial release and hand/tool routes.
optionA=[]
for x,y in [(120,1188),(480,1188)]:
    tests={'hand_knob':cyl(x,y,FLOOR+3,20,26),'wing_head':cyl(x,y,FLOOR+3,22,18),'compact_socket':cyl(x,y,FLOOR+3,10,24)}
    tests.update({'released_'+n:shifted(s,z=C['withdrawal_mm']) for n,s in list(tests.items())})
    rows={n:hits({n:s},obs) for n,s in tests.items()}
    optionA.append({'center':[x,y],'head_and_release_hits':rows,'hand_route_hits':hits(route(x,y),obs),'pass':not any(rows.values())})
assert not any(r['pass'] for r in optionA)
rows=[]
for x in range(46,301,4):
    for y in range(1172,1265,4):
        wood=cyl(x,y,578.9,26,36);need_floor=wood.common(box(-100,1100,596.9,800,300,18));need_shelf=wood.common(box(-100,1100,578.9,800,300,18))
        if need_floor.cut(floor).Volume>1e-5 or need_shelf.cut(shelf).Volume>1e-5:reason='wood'
        elif hits({'reserve':wood},hinge):reason='hinge'
        elif hits({'knob':cyl(x,y,FLOOR+3,20,26+C['withdrawal_mm'])},obs):reason='head_or_release'
        elif hits(route(x,y),obs):reason='hand_approach'
        else:reason='PASS'
        rows.append({'x':x,'y':y,'result':reason})
    print('SEARCH_X',x,flush=True)
selected=[]
for x,y in C['lock_centers_xy_mm']:
    wood=cyl(x,y,578.9,26,36)
    fv=wood.common(box(-100,1100,596.9,800,300,18));sv=wood.common(box(-100,1100,578.9,800,300,18))
    hh=hits(route(x,y),obs);kh=hits({'knob_release':cyl(x,y,FLOOR+3,20,26+C['withdrawal_mm'])},obs)
    row={'center':[x,y],'floor_reserve_missing_mm3':fv.cut(floor).Volume,'shelf_reserve_missing_mm3':sv.cut(shelf).Volume,'hand_hits':hh,'release_hits':kh,'hand_minimum':minimum(route(x,y),obs),'cable_passage_gap_mm':wood.distToShape(passage())[0],'hinge_reserve_gap_mm':minimum({'wood':wood},hinge)['mm'],'floor_reserve_area_mm2':math.pi*26**2,'shelf_rear_edge_center_distance_mm':1290.1-y}
    assert row['floor_reserve_missing_mm3']<1e-5 and row['shelf_reserve_missing_mm3']<1e-5 and not hh and not kh,row
    selected.append(row)
import hashlib
report={'input_sha256':{n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in ['config/backbox_lock_integration_v32.json','tools/backbox_lock_integration_v32.py','tools/backbox_lock_search_v32.py']},'option_A':optionA,'grid_mm':4,'search_domain_half_floor_mm':[46,300,1172,1264],'mirror_about_x_mm':300,'rows':rows,'selected':selected,'selected_option':'B','note':'Grid cells are sampled centers, not an interpolated manufacturing-safe region. Both selected centers are independently checked with exact B-reps. Hardware holes are reference-only.'}
(O/'search.json').write_text(json.dumps(report,indent=2)+'\n')
save('option-a',{**opened,**{'OldLock'+str(i):cyl(x,1188,FLOOR+3,20,26+C['withdrawal_mm']) for i,x in enumerate([120,480])}})
save('search-map',{**{'BB_Floor':floor,'BACKBOX_BASE':shelf},**hinge,**{'ClearCenter'+str(i):cyl(r['x'],r['y'],616,1.4,1) for i,r in enumerate(rows) if r['result']=='PASS'}})
print('LOCK_SEARCH_PASS',len(rows),sum(r['result']=='PASS' for r in rows),selected,flush=True)
