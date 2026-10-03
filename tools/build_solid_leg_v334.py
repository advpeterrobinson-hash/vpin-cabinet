"""Current manufacturing overlay; preserves V33.1 as a historical audit. CERN-OHL-S-2.0."""
from pathlib import Path
import json,collections,csv,copy
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/solid-leg-v334';O.mkdir(exist_ok=True)
read=lambda f:json.loads((R/f).read_text())
def dump(n,v):(O/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
old=read('exports/generated/flatpack-v331/manufacturing-register.json');solid=read('exports/generated/solid-leg-v334/solid-members.json');ids={p['assembly_id'] for p in solid};removed=[p for p in old['parts'] if p['assembly_id'] in ids]
parts=[p for p in old['parts'] if p['assembly_id'] not in ids]+solid
# Do not inherit plywood CNC export paths or engraving from the retired layers.
for p in solid:
 for k in list(p):
  if k.endswith('_brep') and k!='finished_member_brep' or k in ('engraving','local_to_canonical_matrix','grain') :p.pop(k,None)
 p['CNC_required']=False;p['density_status']='SPECIES_DEPENDENT';p['shop_blank_volume_mm3']=54*54*126/2
 p['source']='CURRENT accepted B-rep; tools/solid_leg_v334.py exact replacement proof'
 p['grain_orientation']='Straight grain along126mm length; shop material qualification required'
 p['manufacturing_class']='SHOP_MADE_SOLID_WOOD_PART'
families=[f for f in old['families'] if f.get('manufacturing_part_id',f.get('id')) not in {p['manufacturing_part_id'] for p in removed}]
# Schema is deliberately explicit for the shop family; CNC family rows untouched.
families.append({'manufacturing_part_id':'SW01','quantity':4,'instances':[p['instance_id'] for p in solid],'manufacturing_class':'SHOP_MADE_SOLID_WOOD_PART','material_class':'STRUCTURAL_SOLID_WOOD','blank_dimensions_mm':[54,54,126],'section':'right-isosceles triangular prism','drilling_setups':['F','R'],'status':'PHYSICAL_HARDWARE_HOLD'})
assert len(parts)==106 and len(families)==62,(len(parts),len(families))
register={'version':'V33.4','supersedes':'flatpack-v331/manufacturing-register.json FOR CURRENT NESTING ONLY','installed_components':93,'manufacturing_pieces':106,'CNC_plywood_pieces':102,'shop_solid_wood_parts':4,'canonical_families':62,'CNC_families':61,'parts':parts,'families':families,'manufacturing_release':False}
dump('manufacturing-register.json',register)
manual=read('exports/generated/assembly-v333/assembly-manual.json');manual['version']='V33.4';manual['source_head']='f989d6cc9540247571a28e7f99f1499aacbfdd10';manual['assembly_screen']='../solid-leg-v334/jig-validation.json';manual['source_geometry_unchanged']=True
oldstep=manual['stages'][16]['steps'].pop(0)
newids=[p['instance_id'] for p in solid]
for s in manual['stages']:
 s['pieces']=[i for i in s['pieces'] if not any(i.startswith(pid+'-') for pid in ids)]
 for st in s['steps']:
  st['component_ids']=[i for i in st['component_ids'] if not any(i.startswith(pid+'-') for pid in ids)]
  if st['id']=='16.2':st['component_ids']=newids
  if 'validation' in st:
   st['validation']['pieces']=st['component_ids'];st['validation'].pop('both_face_normal_candidates_conflict',None)
# Explicit earlier checkpoint: drill before floor, PCBase and shelves obstruct the reference tool.
s=manual['stages'][2];s['pieces']+=newids
s['hardware']=list(dict.fromkeys(s['hardware']+['H18','B13','F37']))
st=copy.deepcopy(oldstep);st.update(id='02.0',component_ids=newids,hardware_ids=['H18','B13','F37'],animation_id='assembly-02.0')
def bi(en,pt):return {'en':en,'pt-BR':pt}
st['title']=bi('Position and qualify solid leg blocks before closing the shell','Posicione e qualifique os blocos maciços antes de fechar a caixa')
st['action']=bi('Shop-cut SW01 ×4 from dry, straight, stable knot-free solid wood:54×54×126mm square stock, then45° rip to the accepted triangular section. Check dimensions/squareness; register FL/FR/RL/RR to the documented cabinet datums. Before FLOOR, PC_BASE or SHELF_1 installation, fit the diagonal-face/top-stop jig, clamp, drill only with physically qualified hardware parameters, then test the real backing plate and bolts. Retain temporary support throughout.','Encomende SW01 ×4 de madeira maciça seca, reta, estável e sem nós: material quadrado54×54×126mm, depois corte longitudinal45° para a seção triangular aceita. Confira dimensões/esquadro; posicione FL/FR/RL/RR nos referenciais documentados. Antes de instalar FLOOR, PC_BASE ou SHELF_1, encaixe o gabarito na diagonal/topo, prenda, fure somente com parâmetros fisicamente qualificados e teste a chapa e parafusos reais. Mantenha apoio temporário.')
st['orientation']=bi('Diagonal backing face inward;126mm grain/height vertical. F uses14mm top spacer; R uses bare top stop. Front lower/upper axes42/100mm from bottom; rear28/86mm — reference only.','Face diagonal para dentro; altura/fibras126mm na vertical. F usa espaçador superior14mm; R usa batente sem espaçador. Eixos frontais42/100mm da base; traseiros28/86mm — somente referência.')
st['faces']=bi('SHOP DATUM A: diagonal backing face. TOP stop is datum B. No CNC and no plywood layer stack.','REFERÊNCIA A DE MARCENARIA: face diagonal. Batente SUPERIOR é referência B. Sem CNC e sem pilha de compensado.')
st['check']=bi('HOLD: real leg/backing/bolt pitch, diameter, drilling depth, selected drill and clamp envelope, printed registration and test bore.58mm vs57.15mm remains unresolved. No drilling through assembled shelves/floor; protect bore breakout and all neighboring surfaces.','PENDENTE: passo/diâmetro/profundidade reais, envelope da furadeira/grampos, registro impresso e furo de teste.58mm versus57,15mm continua pendente. Não fure através das prateleiras/piso montados; proteja saída e superfícies vizinhas.')
st['validation']={'id':'02.0','status':'VIRTUAL_AXIS_MATCH_EARLY_ASSEMBLY_SCREEN_PASS_PHYSICAL_HOLD','evidence':'jig-validation.json','physical_trajectory_validated':False,'removed_obstacles':['FLOOR','PC_BASE','SHELF_1']}
s['steps'].insert(0,st)
# Preparation cards for untouched CNC pieces remain byte-equivalent JSON objects.
prep=manual['part_preparation'];# The original per-piece preparation schema is retained.
if isinstance(prep,list):
 manual['part_preparation']=[p for p in prep if p.get('instance_id',p.get('id','')) not in {p['instance_id'] for p in removed}]
else:
 manual['part_preparation']={k:v for k,v in prep.items() if k not in {p['instance_id'] for p in removed}}
manual['solid_wood_preparation']=solid
manual['order_changes']=[{'from':'16.1','to':'02.0','reason':'Reference drill body conflicts with installed SHELF_1 / FLOOR / PC_BASE. Register/drill before closing shell; selected-tool/clamp/fixture physical hold remains.'}]
dump('assembly-manual.json',manual)
fields=['instance_id','manufacturing_part_id','assembly_id','description_en','description_pt_BR','quantity','material_class','manufacturing_class','nominal_stock_thickness_mm','finished_xy_size_mm','finished_reference_thickness_mm','manufacturing_status']
with (O/'manufacturing-bom.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");w.writeheader();w.writerows({k:p.get(k,1 if k=='quantity' else '') for k in fields} for p in parts)
for lang,filename in [('en','manufacturing-bom.md'),('pt_BR','manufacturing-bom.pt-BR.md')]:
 lines=['# V33.4 — '+('Manufacturing wood BOM' if lang=='en' else 'Lista de madeira para fabricação'),'','102 CNC +4 SHOP_MADE_SOLID_WOOD_PART =106;62 families / famílias. CNC RELEASE BLOCKED / LIBERAÇÃO BLOQUEADA.','','| ID | Family / Família | Description / Descrição | Qty | Stock / Material | Status |','|---|---|---|---:|---|---|']
 for p in parts:lines.append(f"| {p['instance_id']} | {p['manufacturing_part_id']} | {p['description_'+lang]} | 1 | {p['material_class']} / {p['nominal_stock_thickness_mm']} | {p['manufacturing_status']} |")
 (O/filename).write_text('\n'.join(lines)+'\n')
manifest={'version':'V33.4','head_before':'f989d6cc9540247571a28e7f99f1499aacbfdd10','current_register':str((O/'manufacturing-register.json').relative_to(R)),'current_BOM':str((O/'manufacturing-bom.csv').relative_to(R)),'CNC_filter':'manufacturing_class != SHOP_MADE_SOLID_WOOD_PART','superseded_leg_families':['M019','M020','M021','M022','M023'],'shop_family':'SW01','geometry_unchanged':True,'release':False}
(R/'config/manufacturing/flatpack_v334.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('V334_REGISTER_PASS',len(parts),len(families))

tooling={'class':'ASSEMBLY_TOOLING_NOT_CABINET_COMPONENT','status':'PHYSICAL_PRINT_AND_HARDWARE_QUALIFICATION_HOLD','cabinet_hardware_catalog_changed':False,'items':[
 {'id':'JIG-LEG-BODY','quantity':1,'description_en':'Universal printed guide body','description_pt_BR':'Corpo guia universal impresso','file':'GuideBody-REFERENCE.stl'},
 {'id':'JIG-LEG-TOP','quantity':1,'description_en':'Removable top registration saddle','description_pt_BR':'Batente superior removível','file':'TopSaddle-REFERENCE.stl'},
 {'id':'JIG-LEG-F14','quantity':1,'description_en':'Front-only14mm index spacer','description_pt_BR':'Espaçador14mm somente frontal','file':'FrontStop14-REFERENCE.stl'},
 {'id':'JIG-LEG-BUSHING','quantity':2,'description_en':'Preferred replaceable metal drill sleeve; dimensions unselected','description_pt_BR':'Bucha metálica substituível preferida; dimensões pendentes','mutually_exclusive_with':'JIG-LEG-SACRIFICIAL','purchase_hold':True},
 {'id':'JIG-LEG-SACRIFICIAL','quantity':2,'description_en':'Optional sacrificial printed guide','description_pt_BR':'Guia impressa sacrificial opcional','file':'Sacrificial1-REFERENCE.stl','mutually_exclusive_with':'JIG-LEG-BUSHING'},
 {'id':'JIG-LEG-CLAMP','quantity':None,'description_en':'Selected clamps and cabinet support fixture; full envelope to qualify','description_pt_BR':'Grampos e apoio da caixa selecionados; validar envelope completo','quantity_status':'SETUP_DEPENDENT_NOT_CABINET_BOM'}]}
dump('tooling-bom.json',tooling)

# Current installed-material metadata overlay; older V33 inventory remains audit history.
materials=read('config/wood_materials_v33.json')
for row in materials['parts']:
 if row['id'] in ids:
  p=next(p for p in solid if p['assembly_id']==row['id'])
  row.update(material='solid wood; species late-bound',material_class='STRUCTURAL_SOLID_WOOD',manufacturing_class='SHOP_MADE_SOLID_WOOD_PART',nominal_thickness_mm=None,description_en=p['description_en'],description_pt_BR=p['description_pt_BR'],manufacturing_family='SW01',notes='54×54×126mm triangular blank after45°shop rip; no CNC plywood lamination. Real leg/backing/bolt and drill-jig qualification HOLD.',assembly_stage='02.0')
materials['current_manufacturing_register']='exports/generated/solid-leg-v334/manufacturing-register.json'
materials['solid_leg_wood']={'quantity':4,'family':'SW01','density_kg_m3':None,'species':None,'nominal_planning_density_kg_m3':650,'condition':'dry, straight, stable, knot-free; selected lot qualification required','CNC_required':False}
(R/'config/wood_materials_v334.json').write_text(json.dumps(materials,indent=2,ensure_ascii=False)+'\n')
manifest['installed_material_map']='config/wood_materials_v334.json'
(R/'config/manufacturing/flatpack_v334.json').write_text(json.dumps(manifest,indent=2)+'\n')
