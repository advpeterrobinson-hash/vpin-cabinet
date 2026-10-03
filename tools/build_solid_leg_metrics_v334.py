"""Derived V33.4 material, mass, packaging and manual audit. CERN-OHL-S-2.0."""
from pathlib import Path
import json,math,hashlib,collections,html,subprocess
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/solid-leg-v334';O.mkdir(exist_ok=True,parents=True)
read=lambda p:json.loads((R/p).read_text())
C=read('config/assembly_planning_v333.json');S=read('config/manufacturing/profiles/peter_supplier_v1.json')
reg=read('exports/generated/solid-leg-v334/manufacturing-register.json');ps=reg['parts'];byid={p['instance_id']:p for p in ps}
metrics={p['instance_id']:p for p in read('exports/generated/assembly-v333/brep-metrics.json') if p['instance_id'] in byid}
SC=read('config/solid_leg_blocks_v334.json')
for p in ps:
 if p.get('manufacturing_class')=='SHOP_MADE_SOLID_WOOD_PART':
  metrics[p['instance_id']]={'instance_id':p['instance_id'],'volume_mm3':p['shop_blank_volume_mm3'],'center_of_mass_local_mm':[18,18,63]}
cnc=[p for p in ps if p.get('manufacturing_class')!='SHOP_MADE_SOLID_WOOD_PART']
def partmass(p,scenario=1):
 density=SC['density_kg_m3'][scenario] if p.get('manufacturing_class')=='SHOP_MADE_SOLID_WOOD_PART' else C['densities_kg_m3']['plywood'][scenario]
 return metrics[p['instance_id']]['volume_mm3']*density/1e9
def highmass(b):return sum(partmass(byid[a['instance_id']],2) for l in b['layers'] for a in l['pieces'])

cat=read('config/hardware_catalog_v33.json')['hardware'];hw={h['id']:h for h in cat}
manual=read('exports/generated/solid-leg-v334/assembly-manual.json');stagemap={i:s['id'] for s in manual['stages'] for i in s['pieces']}
old=read('exports/generated/flatpack-v331/preliminary-layout.json')
closure={h['id']:h for h in read('exports/generated/flatpack-v331/hardware-quantity-closure.json')['rows']}
def dump(n,x):(O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def md(n,x):(O/n).write_text('\n'.join(x)+'\n')
def fit(cells,w,h):
 fits=[(min(c[2]-w,c[3]-h),c[2]*c[3]-w*h,i) for i,c in enumerate(cells) if w<=c[2]+1e-6 and h<=c[3]+1e-6]
 return min(fits)[2] if fits else None
def place(cells,idx,w,h):
 x,y,cw,ch=cells.pop(idx)
 # Disjoint guillotine residuals, preserve larger contiguous offcuts.
 if cw-w>ch-h:
  fresh=[(x+w,y,cw-w,ch),(x,y+h,w,ch-h)]
 else:fresh=[(x+w,y,cw-w,h),(x,y+h,cw,ch-h)]
 cells.extend(c for c in fresh if min(c[2:])>1e-7)
 return x,y
stocks=[];sheets=[]
for t in sorted({p['nominal_stock_thickness_mm'] for p in cnc},reverse=True):
 group=[p for p in ps if p['nominal_stock_thickness_mm']==t]
 attempts=[]
 for sort in ('area','height','width'):
  local=[]
  for p in sorted(group,key=lambda p: -(math.prod(p['finished_xy_size_mm']) if sort=='area' else min(p['finished_xy_size_mm']) if sort=='height' else max(p['finished_xy_size_mm']))):
   w,h=sorted(p['finished_xy_size_mm'],reverse=True);chosen=None
   for sh in local:
    idx=fit(sh['free'],w+15,h+15)
    if idx is not None:chosen=(sh,idx);break
   if chosen is None:
    sh={'id':f'T{t:g}-N{len(local)+1}','thickness_mm':t,'free':[(20,20,2460,1560)],'placements':[]};local.append(sh);chosen=(sh,0)
   sh,idx=chosen;x,y=place(sh['free'],idx,w+15,h+15)
   sh['placements'].append({'instance_id':p['instance_id'],'id':p['manufacturing_part_id'],'x':x,'y':y,'w':w,'h':h,'rotated':p['finished_xy_size_mm'][1]>p['finished_xy_size_mm'][0]})
  attempts.append(local)
 local=min(attempts,key=lambda ss:(len(ss),-sum(c[2]*c[3] for sh in ss for c in sh['free'] if min(c[2:])>=150)))
 sheets+=local;n=len(local);outer=sum(metrics[p['instance_id']]['outer_area_mm2'] for p in group);net=sum(metrics[p['instance_id']]['projected_material_area_mm2'] for p in group)
 box=sum(math.prod(p['finished_xy_size_mm']) for p in group);alloc=sum((a['w']+15)*(a['h']+15) for sh in local for a in sh['placements']);free=n*2460*1560-alloc
 reusable=sum(c[2]*c[3] for sh in local for c in sh['free'] if min(c[2:])>=150)
 purchase=[]
 for sh in local:
  l=math.ceil((max(p['x']+p['w'] for p in sh['placements'])+20)/50)*50
  w=math.ceil((max(p['y']+p['h'] for p in sh['placements'])+20)/50)*50
  purchase.append([l,w])
 old_offcut=0
 for sh in old['sheets']:
  if sh['nominal_stock_mm']!=t:continue
  for r in sh['rows']:
   ww=2480-r['next_x'];hh=r['height'];old_offcut+=ww*hh if min(ww,hh)>=150 else 0
  yy=20+sum(r['height']+15 for r in sh['rows']);old_offcut+=2460*(1580-yy) if 1580-yy>=150 else 0
 stocks.append({'thickness_mm':t,'pieces':len(group),'outer_contour_area_mm2':outer,'projected_material_area_mm2':net,'cutout_area_mm2':outer-net,
 'current_preliminary_sheets':next(s['conservative_row_layout_sheets'] for s in old['stock'] if s['nominal_thickness_mm']==t),
 'improved_study_sheets':n,'previous_row_layout_reusable_offcut_mm2':old_offcut,'purchased_full_sheet_area_mm2':n*4e6,'usable_area_mm2':n*2460*1560,'hold_down_area_mm2':n*(4e6-2460*1560),
 'spacing_reserved_area_mm2':alloc-box,'bounding_rectangle_contour_loss_mm2':box-outer,'unallocated_usable_area_mm2':free,
 'reusable_rectangular_offcut_area_mm2':reusable,'small_unallocated_area_mm2':free-reusable,
 'utilization_percent_outer':outer/(n*4e6)*100,'utilization_percent_net':net/(n*4e6)*100,'waste_percent_gross_including_offcuts':100-net/(n*4e6)*100,
 'practical_stock_rectangles_mm':purchase,'practical_purchase':'Qualified premium offcut/small stock; do not buy full sheet solely for these pieces' if t in (4,6,8) else 'Premium stock first; quoted cut-to-size rectangles or full sheets subject to supplier holding approval',
 'material_removed_volume_mm3':sum(metrics[p['instance_id']]['removed_stock_volume_mm3'] for p in group)})
# Separate purchased-small-stock search. Keep the confirmed supplier full-sheet
# dimensions unchanged; these are procurement envelopes, subject to shop holding.
for stock in stocks:
 if stock['improved_study_sheets']!=1:continue
 group=[p for p in ps if p['nominal_stock_thickness_mm']==stock['thickness_mm']]
 minL=math.ceil((max(max(p['finished_xy_size_mm']) for p in group)+55)/50)*50
 minW=math.ceil((max(min(p['finished_xy_size_mm']) for p in group)+55)/50)*50
 candidates=[]
 for L in range(minL,2501,50):
  for W in range(minW,min(1600,L)+1,50):
   if (L-40)*(W-40)<sum((max(p['finished_xy_size_mm'])+15)*(min(p['finished_xy_size_mm'])+15) for p in group):continue
   candidates.append((L*W,L,W))
 for _,L,W in sorted(candidates):
  success=False
  for mode in ['area','height','width']:
   cells=[(20,20,L-40,W-40)];placements=[]
   for p in sorted(group,key=lambda p:-(math.prod(p['finished_xy_size_mm']) if mode=='area' else min(p['finished_xy_size_mm']) if mode=='height' else max(p['finished_xy_size_mm']))):
    w,h=sorted(p['finished_xy_size_mm'],reverse=True);i=fit(cells,w+15,h+15)
    if i is None:break
    x,y=place(cells,i,w+15,h+15);placements.append({'instance_id':p['instance_id'],'id':p['manufacturing_part_id'],'x':x,'y':y,'w':w,'h':h,'rotated':p['finished_xy_size_mm'][1]>p['finished_xy_size_mm'][0]})
   else:success=True;break
  if success:
   stock['practical_stock_rectangles_mm']=[[L,W]]
   stock['practical_purchase_area_mm2']=L*W
   stock['practical_utilization_percent_net']=stock['projected_material_area_mm2']/(L*W)*100
   stock['practical_small_stock_layout']={'placements':placements,'free':cells,'status':'PROCUREMENT_ENVELOPE_NOT_SUPPLIER_HOLDING_APPROVAL'}
   break
material={'status':'PRELIMINARY_NOT_FOR_CNC','optimized':False,'method':'best of three deterministic guillotine rectangle heuristics; actual contours overlaid; no interlocking; grain long axis along sheet long axis',
 'area_authority':'B-rep outer face and net horizontal projection. Spacing is reserved rectangle allocation, NOT actual kerf. Cutout islands and profile scraps are not counted reusable. Disjoint free rectangles >=150×150 are potential reusable offcuts, subject to holding/tabs/defects.',
 'stocks':stocks,'sheets':sheets,'production_authorized':False}
dump('material-utilization.json',material)
# Mass: no envelope metal masses. All unweighed physical hardware stays estimated/unknown.
woodvol=sum(p['volume_mm3'] for p in metrics.values());wood=[sum(partmass(p,i) for p in ps) for i in range(3)]
vols={p['id']:p for p in read('exports/generated/assembly-v333/hardware-volumes.json')};known=[];unknown=[]
for h in cat:
 if h['flatpack_classification']!='REQUIRED_FLATPACK_HARDWARE':continue
 v=vols.get(h['id']);q=h['quantity']
 if v and isinstance(q,(int,float)) and h['unit'] in ['piece','pieces','each','pc','un','unit']:
  density=C['densities_kg_m3']['hardwood_dowel'][1] if h['id']=='H01' else C['densities_kg_m3']['steel']
  known.append({'id':h['id'],'quantity':q,'volume_each_mm3':v['volume_mm3'],'mass_kg':v['volume_mm3']*density*q/1e9,'status':'ESTIMATED','density_kg_m3':density,'source':v['model_status']})
 else:unknown.append({'id':h['id'],'quantity':q,'mass_kg':None,'status':'UNKNOWN','reason':'unmeasured assembly/envelope, unknown quantity, or non-piece unit'})
# Unit names are read from the catalog, never fabricate a conversion.
est=sum(h['mass_kg'] for h in known);est_range=[est*.8,est,est*1.2]
glassrows=read('exports/generated/assembly-v333/glass-volumes.json');glass=sum(p['volume_mm3'] for p in glassrows)*C['densities_kg_m3']['glass']/1e9
elec=[sum(v[i] for v in C['future_electronics_scenarios_kg'].values()) for i in range(3)]
mechanical=[wood[i]+est_range[i]+C['unknown_required_hardware_allowance_kg'][i] for i in range(3)]
mass={'units':'kg','scenario_order':['LOW','NOMINAL','HIGH'],'wood_volume_mm3':woodvol,'wood_flatpack_kg':wood,'wood_status':'EXACT_REFERENCE_BREP_VOLUME_TIMES_ASSUMED_DENSITY',
 'known_measured_hardware_mass_kg':None,'known_measured_items':0,'known_quantity_nominal_model_subtotal_kg':est,'known_quantity_model_status':'ESTIMATED_NOT_WEIGHED','estimated_hardware_items':known,'unknown_hardware_items':unknown,
 'unknown_required_hardware_allowance_kg':C['unknown_required_hardware_allowance_kg'],'mechanical_scenario_kg':mechanical,'mechanical_exact_total_kg':None,
 'glass_reference_kg':glass,'glass_items':glassrows,'glass_status':'ESTIMATED_REFERENCE_THICKNESS_AND_DENSITY','future_electronics_kg':elec,
 'full_planning_build_kg':[mechanical[i]+glass+elec[i] for i in range(3)],'full_planning_status':'ILLUSTRATIVE_SCENARIO_NOT_GUARANTEED_BOUNDS; unknown hardware is an explicit allowance, optional electronics vary','assumptions':C}
dump('mass-budget.json',mass)
# Counted hardware dashboard with quantity overlay.
req=lambda h:h['flatpack_classification']=='REQUIRED_FLATPACK_HARDWARE'
f=[h for h in cat if h['id'].startswith('F')];rf=[h for h in f if req(h)]
dashboard={'total_hardware_families':len(cat),'fastener_families':len(f),'required_Fxx_models':len(rf),'optional_Fxx_models':sum(h['flatpack_classification']=='OPTIONAL_FLATPACK_HARDWARE' for h in f),'user_adapter_Fxx_models':sum(h['flatpack_classification']=='USER_ADAPTER_HARDWARE' for h in f),
 'known_required_Fxx_minimum':sum(h['quantity'] for h in rf if isinstance(h['quantity'],(int,float))),
 'formula_driven_Fxx':[h['id'] for h in rf if closure.get(h['id'],{}).get('classification')=='FORMULA_FROM_SELECTED_HARDWARE'],
 'TBD_Fxx':[h['id'] for h in rf if h['quantity'] is None and closure.get(h['id'],{}).get('classification')!='FORMULA_FROM_SELECTED_HARDWARE'],
 'required_groups':{}}
for prefix,label in [('W','washers'),('I','nuts_inserts'),('H','hinges_locks_dowel_legs'),('B','straps_brackets_fittings'),('G','gaskets_consumables')]:
 a=[h for h in cat if h['id'].startswith(prefix) and req(h)]
 dashboard['required_groups'][label]={'models':len(a),'items':[{'id':h['id'],'quantity':h['quantity'],'unit':h['unit'],'formula':closure.get(h['id'],{}).get('formula'),'status':h['freeze_status']} for h in a]}
dump('hardware-dashboard.json',dashboard)
# Packaging: one real piece per padded layer, smaller pieces co-pack into a layer
# only with same finished thickness. Largest panels define each protected footprint.
pkg=C['packaging'];packing=[]
def allowance(b):
 L,W=b['L']+40,b['W']+40;H=sum(l['t']+2 for l in b['layers'])+20
 m=.6*2*(L*W+L*H+W*H)/1e6+.15*b['L']*b['W']*(len(b['layers'])+1)/1e6+.3
 return [L,W,H],m
def repack_layers(b):
 items=[p for l in b['layers'] for p in l['pieces']];layers=[]
 for a in sorted(items,key=lambda a:(-byid[a['instance_id']]['finished_reference_thickness_mm'],-math.prod(byid[a['instance_id']]['finished_xy_size_mm']))):
  p=byid[a['instance_id']];w,h=sorted(p['finished_xy_size_mm'],reverse=True);t=p['finished_reference_thickness_mm'];chosen=None
  for l in layers:
   if abs(l['t']-t)>1e-6:continue
   i=fit(l['free'],w+5,h+5)
   if i is not None:chosen=(l,i);break
  if chosen is None:
   l={'t':t,'free':[(0,0,b['L'],b['W'])],'pieces':[]};layers.append(l);chosen=(l,0)
  l,i=chosen;x,y=place(l['free'],i,w+5,h+5);l['pieces'].append({**a,'x':x,'y':y})
 b['layers']=layers
for target in pkg['targets_kg']:
 bundles=[]
 for p in sorted(ps,key=lambda p:-math.prod(p['finished_xy_size_mm'])):
  w,h=sorted(p['finished_xy_size_mm'],reverse=True);t=p['finished_reference_thickness_mm'];massp=partmass(p)
  candidates=[]
  for idx,b in enumerate(bundles):
   if w>b['L'] or h>b['W']:continue
   for li,l in enumerate(b['layers']):
    if abs(l['t']-t)>1e-6:continue
    ci=fit(l['free'],w+5,h+5)
    if ci is not None:candidates.append((0 if b['stage']==stagemap[p['instance_id']] else 1,idx,li,ci));break
   else:candidates.append((2 if b['stage']==stagemap[p['instance_id']] else 3,idx,None,None))
  chosen=None
  for _,bi,li,ci in sorted(candidates):
   b=bundles[bi];dims,am=allowance(b)
   extra=(t+2)*2*(b['L']+b['W']+80)*.6/1e6+.15*b['L']*b['W']/1e6 if li is None else 0
   if (highmass(b)+partmass(p,2))+am+extra<=target:chosen=(b,li,ci);break
  if chosen is None:
   b={'id':f'P{target}-{len(bundles)+1:02}','L':max(w+5,300),'W':max(h+5,200),'layers':[],'wood_mass_kg':0,'stage':stagemap[p['instance_id']]};bundles.append(b);chosen=(b,None,None)
  b,li,ci=chosen
  if li is None:b['layers'].append({'t':t,'free':[(0,0,b['L'],b['W'])],'pieces':[]});li=len(b['layers'])-1;ci=0
  l=b['layers'][li];x,y=place(l['free'],ci,w+5,h+5);l['pieces'].append({'instance_id':p['instance_id'],'id':p['manufacturing_part_id'],'x':x,'y':y,'rotated':p['finished_xy_size_mm'][1]>p['finished_xy_size_mm'][0],'mass_kg':massp});b['wood_mass_kg']+=massp
 # Consolidate low-mass residual packages, allowing the larger of their two
 # protected footprints. This avoids a separate box for every leftover strip.
 while True:
  merges=[]
  for ai,a in enumerate(bundles):
   for bi,b in enumerate(bundles[ai+1:],ai+1):
    q={**a,'L':max(a['L'],b['L']),'W':max(a['W'],b['W']),'layers':a['layers']+b['layers'],'wood_mass_kg':a['wood_mass_kg']+b['wood_mass_kg']}
    repack_layers(q);dd,aa=allowance(q)
    if highmass(q)+aa<=target:merges.append((dd[0]*dd[1],ai,bi,q))
  if not merges:break
  _,ai,bi,q=min(merges,key=lambda v:v[:3]);bundles[ai]=q;bundles.pop(bi)
 for bi,b in enumerate(bundles):
  b['id']=f'P{target}-{bi+1:02}'
  dims,am=allowance(b);z=10;moment=[0,0,0];seps=[8]
  for li,l in enumerate(b['layers']):
   l['z']=z;l['order']=li+1
   for p in l['pieces']:
    q=byid[p['instance_id']];cx,cy,cz=metrics[p['instance_id']]['center_of_mass_local_mm'];xmin,ymin,_,_=q['finished_xy_bounds_mm']
    if p['rotated']:cx,cy=cy-ymin,q['finished_xy_size_mm'][0]-(cx-xmin)
    else:cx,cy=cx-xmin,cy-ymin
    cg=[20+p['x']+cx,20+p['y']+cy,z+cz];p['center_of_mass_package_mm']=cg
    moment=[moment[i]+cg[i]*p['mass_kg'] for i in range(3)]
   z+=l['t']+2;seps.append(z-2)
  b.update(external_LWH_mm=dims,packaging_allowance_kg=am,gross_nominal_kg=b['wood_mass_kg']+am,
   gross_high_density_kg=highmass(b)+am,wood_center_of_gravity_mm=[v/b['wood_mass_kg'] for v in moment],separator_z_mm=seps,
   estimated_gross_center_of_gravity_mm=[(moment[i]+am*dims[i]/2)/(b['wood_mass_kg']+am) for i in range(3)],
   handling='Two-person carry recommended for long/wide panels even below mass target; density sensitivity target is not ergonomic certification',
   protection='Full-footprint rigid separator each layer; pad cavities and narrow strips; edge/corner protectors, straps over spreader boards. Compression/drop qualification pending.')
  assert b['gross_high_density_kg']<=target+1e-6
 packing.append({'target_kg':target,'bundles':bundles,'bundle_count':len(bundles)})
dump('packaging.json',{'preferred_target_kg':25,'candidates':packing,'hardware_box':{'separate':True,'mass_kg':None,'dimensions_mm':None,'status':'SIZE_AFTER_PURCHASE; no hardware hidden in wood bundles'},'glass_electronics_in_wood_bundles':False,'status':'HIGH_DENSITY_SENSITIVITY_MASS_TARGET_NOT_TRANSIT_QUALIFIED'})

# Separate solid species sensitivity and undrilled shipping stock from installed volume.
solid=[p for p in ps if p.get('manufacturing_class')=='SHOP_MADE_SOLID_WOOD_PART']
oldmetrics=read('exports/generated/assembly-v333/brep-metrics.json')
oldleg=[p for p in oldmetrics if p['instance_id'].split('-')[0] in {'P029','P030','P031','P032'}]
oldvol=sum(p['volume_mm3'] for p in oldleg)
installed=[wood[i]-sum(partmass(p,i) for p in solid)+sum(p['volume_mm3'] for p in solid)*SC['density_kg_m3'][i]/1e9 for i in range(3)]
mass.update(wood_flatpack_kg=wood,installed_wood_kg=installed,plywood_only_kg=[sum(partmass(p,i) for p in cnc) for i in range(3)],solid_undrilled_shop_blanks_kg=[sum(partmass(p,i) for p in solid) for i in range(3)],solid_density_kg_m3=SC['density_kg_m3'],solid_density_status=SC['density_status'],wood_status='CNC BREP VOLUME + FOUR UND RILLED TRIANGULAR SHOP BLANKS; ASSUMED SEPARATE MATERIAL DENSITIES'.replace('UND RILLED','UNDRILLED'))
# Mechanical mass is the finished installed mass, not shipping stock before bores.
mass['mechanical_scenario_kg']=[mechanical[i]-wood[i]+installed[i] for i in range(3)]
mass['full_planning_build_kg']=[mass['mechanical_scenario_kg'][i]+glass+elec[i] for i in range(3)]
dump('mass-budget.json',mass)
summary={'manufacturing_pieces':len(ps),'CNC_pieces':len(cnc),'shop_solid_pieces':len(solid),'canonical_families':len(reg['families']),'wood_mass_kg':wood[1],'preliminary_sheets':sum(s['improved_study_sheets'] for s in stocks),'known_fastener_minimum':dashboard['known_required_Fxx_minimum'],'hardware_models':len(cat),'manufacturing_status':'BLOCKED','coupon_status':S['coupon']['validation_status']}
dump('project-metrics.json',summary)
savings={'retired_CNC_pieces':len(oldleg),'old_plywood_volume_mm3':oldvol,'finished_outer_area_saved_mm2':sum(p['outer_area_mm2'] for p in oldleg),'projected_net_area_saved_mm2':sum(p['projected_material_area_mm2'] for p in oldleg),'bounding_stock_area_saved_mm2':28*54*54,'purchased_full_sheet_count_reduction':next(s['current_preliminary_sheets']-s['improved_study_sheets'] for s in stocks if s['thickness_mm']==18),'note':'Finished contour saving is not a whole sheet saving; no production nesting.'}
dump('plywood-savings.json',savings)
dump('packing-metrics.json',list(metrics.values()))
print('V334_METRICS_PASS',summary)

# SVG review atlas, actual contours inside study placements. No production layers/export.
preview_sheets=sheets+[{'id':f"T{s['thickness_mm']:g}-SMALL-STOCK",'placements':s['practical_small_stock_layout']['placements'],'preview_dims':s['practical_stock_rectangles_mm'][0]} for s in stocks if 'practical_small_stock_layout' in s]
for sh in preview_sheets:
 svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2540 1700"><rect width="2540" height="1700" fill="white"/><g transform="translate(20,70)"><rect width="2500" height="1600" fill="#eee" stroke="#333"/><rect x="20" y="20" width="2460" height="1560" fill="white" stroke="#777"/>']
 if 'preview_dims' in sh:
  ll,ww=sh['preview_dims'];svg.append(f'<rect width="{ll}" height="{ww}" fill="#edf3f5" stroke="#173d59" stroke-width="6"/><text x="{ll+25}" y="50" font-size="27">SMALL STOCK {ll} × {ww} mm — procurement study</text>')
 for a in sh['placements']:
  p=byid[a['instance_id']];xmin,ymin,_,_=p['finished_xy_bounds_mm'];pts=[]
  for x,y in p['review_outline']:
   xx,yy=(y-ymin,p['finished_xy_size_mm'][0]-(x-xmin)) if a['rotated'] else (x-xmin,y-ymin)
   pts.append(f'{a["x"]+xx:.3f},{a["y"]+yy:.3f}')
  svg.append(f'<polygon points="{" ".join(pts)}" fill="#dbc59b" stroke="#344955" stroke-width="2"/><text x="{a["x"]+5}" y="{a["y"]+18}" font-size="16">{a["id"]}</text>')
 svg.append(f'</g><text x="20" y="40" font-family="sans-serif" font-size="26">{sh["id"]} · PRELIMINARY — NOT FOR CNC · 20 mm border / 15 mm spacing</text></svg>')
 (O/(sh['id']+'.svg')).write_text(''.join(svg))
