"""V33.8 exact SW02 shop-block manufacturing replacement. CERN-OHL-S-2.0.
Runs only on a final validated native candidate. No plywood geometry changes,
no drill diameter release, no production CNC output or invented jig geometry.
"""
from pathlib import Path
import sys,json,copy,hashlib,gzip,collections,math
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from validate_plywood_stock_v338 import validate_stock_policy,negative_controls
O=R/'exports/generated/service-productization-v338';BASE=R/'exports/generated/two-stock-user-module-v337';V=A.Vector
CONFIG=R/'config/service_productization_v338.json';POLICY=R/'config/manufacturing/stock_policy_v338.json'
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(n,v):(O/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def load(p):
 d=A.openDocument(str(p));s={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')};A.closeDocument(d.Name);return s

def union(ss):
 s=ss[0].copy()
 for q in ss[1:]:s=s.fuse(q)
 return s.removeSplitter()
def diff(a,b):return a.cut(b).Volume+b.cut(a).Volume
def center(s):return sum((q.CenterOfMass*q.Volume for q in s.Solids),V())/sum(q.Volume for q in s.Solids)
def export(inst,label,s):
 p=O/'brep'/f'{inst}-{label}.brep';p.parent.mkdir(exist_ok=True);s.exportBrep(str(p));return str(p.relative_to(R))
def bbox(s):
 b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
inputs=[O/'play.FCStd',O/'geometry-validation.json',CONFIG,POLICY,R/'config/solid_front_landings_v338.json',R/'tools/validate_plywood_stock_v338.py',BASE/'play.FCStd',BASE/'manufacturing-register.json']
hashes={str(p.relative_to(R)):sha(p) for p in inputs};g=read(O/'geometry-validation.json');assert g['pass'] and not g['manufacturing_release']
old=load(BASE/'play.FCStd');new=load(O/'play.FCStd');reg=read(BASE/'manufacturing-register.json');oldparts=copy.deepcopy(reg['parts']);assert (len(oldparts),len(reg['families']))==(108,66)
retired=[p for p in oldparts if p['source_component'] in [f'FrontLanding{s}_Layer{i}' for s in 'LR' for i in range(1,4)]];assert len(retired)==6
parts=[p for p in oldparts if p not in retired];assert len(parts)==102
retired_ids={p['manufacturing_part_id'] for p in retired};assert retired_ids=={f'M{i:03}' for i in range(68,74)}
assert all(p['source_component'] not in new for p in retired)
assert all(f'FrontLanding{s}_LaminationScrew{i}' not in new for s in 'LR' for i in (1,2))
unchanged=[]
for p in parts:
 n=p['source_component']
 if n in old and n in new:
  error=0 if old[n].exportBrepToString()==new[n].exportBrepToString() else diff(old[n],new[n])
  assert error<1e-4,(n,'unrelated wood geometry changed',error)
  unchanged.append({'source_component':n,'difference_mm3':error})
newrows=[];metrics=[];meshes={};audits=[];mapping={};canonical=[]
for side,assembly,originx in [('L','P095',18),('R','P096',582)]:
 name=f'FrontLanding{side}_Block';inst=assembly+'-Solid';s=new[name];assert s.isValid() and len(s.Solids)==1
 oldunion=union([old[f'FrontLanding{side}_Layer{i}'] for i in range(1,4)]);b=oldunion.BoundBox
 size=[b.XLength,b.YLength,b.ZLength];assert all(abs(a-c)<1e-6 for a,c in zip(size,[68,70,54]))
 blank=Part.makeBox(*size,V(b.XMin,b.YMin,b.ZMin));assert diff(Part.makeBox(s.BoundBox.XLength,s.BoundBox.YLength,s.BoundBox.ZLength,V(s.BoundBox.XMin,s.BoundBox.YMin,s.BoundBox.ZMin)),blank)<1e-4
 assert s.cut(blank).Volume<1e-4
 removed=oldunion.cut(s);restored=s.cut(oldunion);obsolete=union([old[f'FrontLanding{side}_LaminationScrew{i}'] for i in (1,2)])
 assert removed.Volume<1e-4 and restored.cut(obsolete).Volume<1e-4,(side,'non-binder functional geometry changed')
 # Canonical shop coordinates: U inward from cabinet-side face, V rearward
 # from front face, W upward from block bottom. Right is explicitly mirrored.
 matrix=A.Matrix();matrix.A11=1 if side=='L' else -1;matrix.A14=originx;matrix.A24=b.YMin;matrix.A34=b.ZMin
 local=s.copy();local.transformShape(matrix.inverse(),True);rebuilt=local.copy();rebuilt.transformShape(matrix,True);error=diff(rebuilt,s);assert error<1e-4
 canonical.append(local);localblank=Part.makeBox(*size);assert local.cut(localblank).Volume<1e-4
 features=[]
 for f in local.Faces:
  if type(f.Surface).__name__ in ('Cylinder','Cone'):
   q=f.Surface;row={'surface':type(q).__name__,'axis_local':list(q.Axis),'center_local_mm':list(q.Center),'radius_reference_mm':getattr(q,'Radius',None),'bounds_local_mm':bbox(f)}
   if row not in features:features.append(row)
 # Physical receiver/side interfaces remain unchanged. Centers come from the
 # exact CURRENT source hardware axes, verified against cylinder surfaces.
 paths=[]
 for label,u,v,axis,entry,length,diam in [
  ('M8 adjuster clearance',54,20,[0,0,-1],[54,20,54],54,9),
  ('M8 receiver pilot reference',54,20,[0,0,-1],[54,20,54],16,12),
  ('M6 captive retention passage',54,50,[0,0,-1],[54,50,54],54,7)]:
  assert any(q['surface']=='Cylinder' and abs(abs(q['axis_local'][2])-1)<1e-6 and abs(q['center_local_mm'][0]-u)<1e-5 and abs(q['center_local_mm'][1]-v)<1e-5 and abs(q['radius_reference_mm']-diam/2)<1e-5 for q in features),(inst,label)
  paths.append({'interface':label,'entry_local_uvw_mm':entry,'axis_local':axis,'reference_depth_mm':length,'reference_diameter_mm':diam,'final_diameter_mm':None,'final_depth_mm':None,'status':'PURCHASE_BEFORE_ASSEMBLY / QUALIFIED_GUIDE_AND_COUPON_HOLD'})
 for v in (9,61):
  for w in (9,45):
   assert any(q['surface']=='Cylinder' and abs(abs(q['axis_local'][0])-1)<1e-6 and abs(q['center_local_mm'][1]-v)<1e-5 and abs(q['center_local_mm'][2]-w)<1e-5 and abs(q['radius_reference_mm']-2.5)<1e-5 for q in features),(inst,v,w)
   paths.append({'interface':'Side attachment clearance/head reference','entry_local_uvw_mm':[68,v,w],'axis_local':[-1,0,0],'reference_depth_mm':68,'reference_diameter_mm':5,'reference_head_diameter_mm':9,'reference_head_depth_mm':2,'final_diameter_mm':None,'final_depth_mm':None,'status':'PURCHASE_BEFORE_ASSEMBLY / QUALIFIED_GUIDE_AND_COUPON_HOLD'})
 row={'manufacturing_part_id':'SW02','instance_id':inst,'source_component':name,'assembly_id':assembly,
 'description_en':f'Solid-wood front playfield landing {side}','description_pt_BR':'Apoio frontal maciço do playfield '+('esquerdo' if side=='L' else 'direito'),
 'material_class':'STRUCTURAL_SOLID_WOOD','nominal_stock_thickness_mm':None,'finished_reference_thickness_mm':54,'quantity':1,
 'machining_face':'SHOP_DATUM_A_TOP','opposite_face':'NO CNC; manual inner-side datum B per qualified guide',
 'face_A_outward_world':[0,0,1],'local_to_installed_matrix':list(matrix.A),'local_to_canonical_matrix':list(A.Matrix().A),
 'local_datum':'U inward from side-wall mating face; V rearward from front; W upward from bottom. TOP A at W54, INNER B at U68. R is mirrored, not a second CNC face.',
 'finished_xy_bounds_mm':[0,0,68,70],'finished_xy_size_mm':[68,70],
 'finished_member_brep':export(inst,'finished-reference',local),'installed_member_brep':export(inst,'installed-reference',s),'shop_blank_brep':export(inst,'shop-blank',localblank),
 'through_cuts':[],'pockets':[],'reference_features':features,'reference_drill_paths':paths,
 'manual_finish':[{'operation':'SHOP_CUT_RECTANGULAR_SOLID_WOOD_BLANK','face_datum':'TOP A / INNER B / FRONT','instruction':'Woodshop supplies68×70×54 mm rectangular dry, stable, straight, knot-free structural solid wood. Qualify species, moisture, grain and squareness; no plywood lamination, glue-up or binder screws. Grain along68 mm U/X cantilever axis is provisional.'},
 {'operation':'QUALIFIED_PORTABLE_DRILL_GUIDE_HOLD','face_datum':'TOP A and INNER B, each indexed from FRONT and side/bottom datum','tool':'clamped commercial90° portable drill guide, ordinary drill/driver, selected pilot/countersink, depth stop, clamps and scale-verified paper template',
 'instruction':'Paper locates centers only. It cannot guide54/68 mm drill paths. Clamp a qualified perpendicular guide and test the selected pilot/insert/head stack on scrap of the same wood. No precise freehand drilling. Final drill diameters, depths, drill-point allowance and template release await purchased hardware; no new printed jig is required unless the commercial guide fails qualification.'},
 {'operation':'CABINET_INTERFACE_HOLD','instruction':'Preserve eight side screw locations and the two held M025 receivers. No new side/M025 bores are cut in CURRENT. Use the existing qualified cabinet template/depth-stop process; do not glue SW02 to the side wall. Keep positive support/retention and reset stop after permitted leveling.'}],
 'blockers':[],'manufacturing_status':'SHOP_MADE_SOLID_WOOD_PART','manufacturing_class':'SHOP_MADE_SOLID_WOOD_PART','CNC_required':False,
 'facing_reduction_mm':0,'fit_dependent':True,'coupon_dependent':True,'fit_expression':'Measured solid blank, selected receiver/pilots and qualified drill guide; no nominal plywood thickness expression',
 'corner_classes':['B_OPEN_EDGE_NO_RELIEF_NEEDED'],'rotation_90_allowed_geometrically':True,'arbitrary_rotation_90_for_packing':False,'opposite_face_cnc':False,
 'mirror_relation':'One SW02 rectangular blank family×2; handed placement and drilling orientation explicitly labeled L/R',
 'grain_orientation':'Straight grain along68 mm U/X cantilever direction, dry and defect-free; species/splitting/load qualification pending',
 'projected_area_mm2':4760,'volume_mm3':s.Volume,'shop_blank_volume_mm3':localblank.Volume,'blank_outside_error_mm3':s.cut(blank).Volume,
 'review_outline':[[0,0],[68,0],[68,70],[0,70],[0,0]],'source':[str((O/'play.FCStd').relative_to(R)),name],
 'joinery':'One shop-cut block per side; four existing removable side screws, no glue to wall; no lamination adhesive or binder screws',
 'assembly_stage':'05','version':'V33.8','manufacturing_release':False,'density_status':'SPECIES_DEPENDENT','release_hold':'PURCHASED_HARDWARE + QUALIFIED_DRILL_GUIDE + SAME_WOOD_COUPON + STRUCTURAL_QUALIFICATION',
 'engraving':{'optional':True,'text':'SW02 '+side,'status':'LABEL_OR_HIDDEN_SHOP_MARK','note':'TOP / FRONT / INNER orientation on removable labels; no CNC engraving required'}}
 newrows.append(row);parts.append(row);mapping[name]={'instance_id':inst,'assembly_id':assembly,'manufacturing_part_id':'SW02','group':'PLAYFIELD_LANDINGS'}
 audits.append({'instance_id':inst,'dimensions_mm':size,'blank_volume_mm3':localblank.Volume,'finished_volume_mm3':s.Volume,'old_union_volume_mm3':oldunion.Volume,'obsolete_binder_holes_filled_mm3':restored.Volume,'old_functional_wood_removed_mm3':removed.Volume,'restored_outside_obsolete_binder_corridors_mm3':restored.cut(obsolete).Volume,'installed_reconstruction_difference_mm3':error,'reference_drill_paths':paths})
 metrics.append({'instance_id':inst,'volume_mm3':localblank.Volume,'finished_volume_mm3':local.Volume,'center_of_mass_local_mm':[34,35,27],'finished_center_of_mass_local_mm':list(center(local)),'outer_area_mm2':4760,'projected_material_area_mm2':4760,'removed_stock_volume_mm3':localblank.Volume-local.Volume,'shipping_geometry_authority':row['shop_blank_brep']})
 vv,ff=local.tessellate(.15);meshes[inst]={'vertices':[list(v) for v in vv],'faces':ff}
assert diff(canonical[0],canonical[1])<1e-4,'SW02 mirrored canonical geometry differs'
assert len(parts)==104 and sum(p==q for p,q in zip([p for p in parts if p not in newrows],[p for p in oldparts if p not in retired]))==102
families=[f for f in reg['families'] if f.get('id',f.get('manufacturing_part_id')) not in retired_ids]+[{'id':'SW02','quantity':2,'instances':['P095-Solid','P096-Solid'],'class':'STRUCTURAL_SOLID_WOOD','stock':None,'manufacturing_status':'SHOP_MADE_SOLID_WOOD_PART'}]
assert len(families)==61
reg.update(version='V33.8',supersedes='two-stock-user-module-v337/manufacturing-register.json FOR CURRENT NESTING ONLY',parts=parts,families=families,manufacturing_pieces=104,CNC_plywood_pieces=98,shop_solid_wood_parts=6,canonical_families=61,CNC_families=59,installed_components=len({p['source_component'] for p in parts}),manufacturing_release=False,stock_policy='config/manufacturing/stock_policy_v338.json',retired_current_landing_families=sorted(retired_ids))
policy=read(POLICY);validate_stock_policy(parts,policy);dump('manufacturing-register.json',reg)
negative=negative_controls(parts,policy);negative.update(version='V33.8',native_sha256=sha(O/'play.FCStd'),register_sha256=sha(O/'manufacturing-register.json'),validator_sha256=sha(R/'tools/validate_plywood_stock_v338.py'),policy_sha256=sha(POLICY));dump('stock-policy-negative-control.json',negative)
dump('manufacturing-audit.json',{'version':'V33.8','pass':True,'native_geometry_sha256':sha(O/'play.FCStd'),'native_configuration_sha256':sha(CONFIG),'geometry_validation_sha256':sha(O/'geometry-validation.json'),'input_sha256':hashes,'changed_audits':audits,'unchanged_piece_rows_retained':102,'unchanged_wood_geometry':unchanged,'retired_instances':[p['instance_id'] for p in retired],'canonical_families':61,'counts':dict(collections.Counter(p['manufacturing_status'] for p in parts)),'stock_mm':[12,18],'solid_families':['SW01','SW02'],'manufacturing_release':False})
dump('changed-piece-metrics.json',metrics);dump('sw02-manufacturing-map.json',mapping);(O/'manufacturing-mesh.json.gz').write_bytes(gzip.compress(json.dumps(meshes).encode(),mtime=0))
materials=read(R/'config/wood_materials_v337.json');materials['parts']=[p for p in materials['parts'] if p['object'] not in {r['source_component'] for r in retired}]
for p in newrows:
 materials['parts'].append({'id':p['instance_id'],'assembly_id':p['assembly_id'],'object':p['source_component'],'description_en':p['description_en'],'description_pt_BR':p['description_pt_BR'],'quantity':1,'unit':'shop-made block','material':'dry stable structurally suitable solid wood, species pending','material_class':'STRUCTURAL_SOLID_WOOD','nominal_thickness_mm':None,'nominal_dimensions':{'finished_mm':[68,70,54]},'source':p['source'],'status':'DESIGN_GEOMETRY_ONLY','measurement_required':True,'flatpack_classification':'REQUIRED_FLATPACK_HARDWARE','assembly_stage':'05','parent_assembly':'playfield_landings','price_BRL':None,'service_removable':True,'normal_assembly_removable':True})
materials['solid_front_landing_wood']={'family':'SW02','quantity':2,'shop_blank_dimensions_mm':[68,70,54],'grain_direction':'U/X68 mm cantilever direction, provisional','material_authority':'config/solid_front_landings_v338.json','purchased_hardware_and_qualification_pending':True}
materials.update(version='V33.8',current_manufacturing_register=str((O/'manufacturing-register.json').relative_to(R)),stock_policy='config/manufacturing/stock_policy_v338.json')
(R/'config/wood_materials_v338.json').write_text(json.dumps(materials,indent=2,ensure_ascii=False)+'\n')
for path,digest in hashes.items():assert sha(R/path)==digest,('Concurrent native input writer',path)
print('V338_MANUFACTURING_PASS',len(parts),len(families),flush=True)
