"""V35.1 bilingual assembly/standard-interface authority, no final purchased dimensions."""
from pathlib import Path
import json,copy,re
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/widebody-v351';B=R/'exports/generated/backbox-v342'
def read(p):return json.loads(p.read_text())
def put(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def bi(en,pt):return {'en':en,'pt-BR':pt}
reg=read(O/'manufacturing-register.json');audit=read(O/'attachment-audit.json');manual=read(B/'assembly-manual.json');before=copy.deepcopy(manual);cat=read(R/'config/hardware_catalog_v342.json')
manual.update(version='V35.1',geometry_authority='exports/generated/widebody-v351/play.FCStd',current_manufacturing_register='config/manufacturing/flatpack_v351.json',source_geometry_unchanged=False,manufacturing_release=False,source_head='11822cb2dc9c7c7b511348df860cb76196d641be')
manual['widebody_authority']={'width_mm':628.65,'inside_nominal_mm':592.65,'centerline_mm':314.325,'length_mm':1308.1,'glass_nominal_mm':5,'hardware':'STANDARD COMMERCIAL ONLY','optional_siderail':True,'attachment_audit':'attachment-audit.json'}
for st in manual['stages']:
 for a in st['steps']:
  if a['id']=='08.28':a.update(title=bi('Install commercial widebody glass/lockdown interfaces','Instale interfaces comerciais widebody para vidro/lockdown'),hardware_ids=['H20','H21','B12','B21','G11','F36','F68'],action=bi('Purchase matching A-17996/A-16055 bar and A-16773-1 receiver (A-9174-4 alternative). Qualify the body/latch/access reserves before final holes. Install receiver on FRONT, with no plywood linkage. Screw the purchased rear channel onto the local angled lands of RearBearingShelf; use selected countersunk/flush heads entirely below the glass seat. Fit side polymer channels for actual5mm tempered glass. Slide glass from FRONT and latch lockdown. Optional siderails install last; glass works without them. Channel screw count/centers/pilots remain selected-hardware dependent.','Compre barra A-17996/A-16055 e receiver A-16773-1 compatível (alternativa A-9174-4). Qualifique reservas de corpo/trava/acesso antes dos furos. Instale receiver em FRONT sem mecanismo de madeira. Parafuse o canal traseiro nas áreas locais inclinadas da RearBearingShelf; cabeças selecionadas escareadas/niveladas devem ficar abaixo do apoio do vidro. Instale canais de polímero compatíveis com vidro temperado real5mm. Deslize vidro pela FRENTE e trave lockdown. Siderails opcionais por último; vidro funciona sem eles. Quantidade/centros/pilotos dependem da ferragem.'),check=bi('Confirm four-edge containment, smooth forward removal and no glass/head point contact. Test receiver operation with coin door open and verify no contact with playfield or coin equipment. Main glass/matrix removed before fold.','Confira retenção nas quatro bordas, retirada frontal livre e ausência de contato pontual com cabeças. Teste receiver com porta de moedas aberta e sem contato com playfield/mecanismos. Retire vidro principal/matriz antes da dobra.'),hold=bi('Purchased profiles, receiver trajectory, screw engagement, glass cut, stock and coupon HOLD. Rear-channel fastener access is verified before backbox assembly; future service may require folded backbox. No drilling from the reference test points.','Perfis comprados, trajetória receiver, engajamento, corte vidro, material/cupom PENDENTES. Acesso aos parafusos do canal antes da montagem do backbox; manutenção pode exigir backbox dobrado. Não furar pelos pontos de ensaio.'))
  if a['id']=='03.1':
   a['action']['en']+=' V35.1 preserves M006 and all bearing interfaces. Two small R2 integral front lands in the same18mm rear shelf provide rear-channel screw margins; no added rail.'
   a['action']['pt-BR']+=' V35.1 preserva M006 e interfaces de apoio. Duas áreas frontais locais integrais R2 na mesma prateleira18mm dão margem aos parafusos do canal; sem régua extra.'
  a['validation_note_v351']='Unchanged steps inherited; changed interface action requires purchased-part/coupon qualification. Schematic assembly trajectories remain schematic.'
# Current assembly coordinates override historical prose in both languages.
def update_text(v):
 if isinstance(v,str):
  for old,new in [('600 mm exterior width','628.65 mm exterior width'),('largura externa 600 mm','largura externa 628,65 mm'),('largura externa de 600 mm','largura externa de 628,65 mm'),('X72/X528','X72/X556.65'),('396 mm','424.65 mm'),('X130/Y1260','X144.325/Y1260'),('X470/Y1260','X484.325/Y1260')]:v=v.replace(old,new)
  return v
 if isinstance(v,dict):return {k:update_text(x) for k,x in v.items()}
 if isinstance(v,list):return [update_text(x) for x in v]
 return v
manual=update_text(manual)
for st in manual['stages']:
 for a in st['steps']:
  if a['id']=='16.2':a['action']=bi('Use matched commercial pinball legs, bolts, backing and levelers with protected SW01 blocks. The628.65mm body uses commercial A-17996/A-16055 lockdown and A-16773-1 receiver; no custom-width substitute. Final purchased interfaces remain held. Mobility skates are optional external accessories.','Use pés comerciais, parafusos, apoios e niveladores compatíveis com blocos SW01 preservados. O corpo628,65mm usa lockdown comercial A-17996/A-16055 e receiver A-16773-1; sem substituto sob medida. Interfaces compradas permanecem pendentes. Rodízios externos são opcionais.')
# No false quantity closure. IDs retain functional identity; exact purchased product remains held.
ids={a['id']:a for a in cat['hardware']}
for id,en,pt in [('H20','Commercial widebody lockdown A-17996 / A-16055','Lockdown comercial widebody A-17996 / A-16055'),('H21','Commercial receiver A-16773-1; A-9174-4 alternative','Receiver comercial A-16773-1; alternativa A-9174-4'),('B21','Commercial rear glass channel03-8091-2 class, screw mounted','Canal traseiro comercial03-8091-2, parafusado'),('B12','Commercial polymer side channel for actual5mm tempered glass','Canal lateral comercial de polímero para vidro temperado real5mm')]:
 a=ids[id];a.update(description_en=en,description_pt_BR=pt,freeze_status='PURCHASE_BEFORE_CNC',design_status='COMMERCIAL_ARCHITECTURE_SELECTED_EXACT_PART_HOLD',dimensional_authority='OWNER_V351_AND_PUBLIC_FAMILY_REFERENCE',notes='Commercial family only; final cut/holes/pockets/mounting pattern and actual fit NULL until purchased. No custom metal substitute.',source=['config/standard_interfaces_v351.json']);a['model']={'strategy':'ORIGINAL_REFERENCE_RESERVE_NOT_VENDOR_CAD','path':'exports/generated/widebody-v351/candidate.FCStd','detailed_threads':False}
ids['H01']['nominal_dimensions']['length_mm']=588.65
ids['H01']['model']={'strategy':'CURRENT_BREP_ENVELOPE','path':'exports/generated/widebody-v351/play.FCStd#PF_WoodDowel','parameters':{'diameter_mm':32,'length_mm':588.65},'detailed_threads':False}
ids['H01']['source']=['config/widebody_v351.json']
ids['H21']['measurement_fields'].update(receiver_external_envelope_mm=None,latch_travel_mm=None,mounting_pattern=None,withdrawal_clearance_mm=None)
ids['H20']['measurement_fields'].update(bar_width_mm=None,underside_engagement=None,glass_interface=None)
ids['G11'].update(nominal_dimensions={'reference_cut_mm':[603.25,1092.2,5],'final_cut_mm':None},notes='Local nominal5mm tempered; order size after purchased channel/lockdown and coupon. Not assumed compatible with3/16 channel.')
ids['F68'].update(parent_assembly='rear_bearing_shelf',notes='Ordinary screwed commercial rear channel. Reference lands screen12mm embedment and10mm edge distance; exact count/pilot/centers/head form and engagement held. No unsupported thread into thin skin.',quantity=None,quantity_formula='attachment count of selected rear-channel hardware; test points are NOT released holes')
nextid='B'+str(max(int(a['id'][1:]) for a in cat['hardware'] if a['id'].startswith('B'))+1)
opt=copy.deepcopy(ids['B21']);opt.update(id=nextid,description_en='Optional commercial slim WPC/widebody siderail pair',description_pt_BR='Par de siderails comerciais WPC/widebody opcionais',flatpack_classification='OPTIONAL_FLATPACK_HARDWARE',quantity=2,quantity_status='OPTIONAL_ARCHITECTURE_COUNT',notes='Not in minimum BOM. Reference ends before backbox. Purchased-part trimming/finish VERIFY SKU; no structural dependency.');cat['hardware'].append(opt)
cat['object_to_id'].pop('BB_PFRearChannel',None);cat['object_to_id'].update(PF_RearGlassChannel='B21',PF_LockdownGlassRetainer='H20',LockdownReceiverReference='H21',CommercialSiderailL=nextid,CommercialSiderailR=nextid)
cat.update(version='V35.1',source_head=manual['source_head'],authority='Standard-widebody commercial architecture; exact profiles/purchased measurements/CNC held',manufacturing_ready=False)
# Replace installed reference coordinates by current mesh bounds in final exporter; no hidden final drilling.
for a in cat['hardware']:
 for i in a['instances']:
  i['coordinate_authority']='V35.1 native source object; previous numeric coordinate superseded'
  i['coordinate_xyz_mm']=None;i['source']='exports/generated/widebody-v351/play.FCStd'
interfaces={'version':'V35.1','owner_hardware_class_locked':True,'custom_lockdown':False,'minimum_siderail_quantity':0,'final_drilling':None,'manufacturing_release':False,'sources':['https://www.tukkari.com/advisor/assembly-guide-widebody-vpin-cabinet-premium-flat-pack','https://www.pinballlife.com/williamsbally-lockdown-bar-lever-guide-receiver-assembly-wpcwpc-95.html','https://www.pinballspareparts.com.au/a-16055.html','https://www.pinballlife.com/widebody-playfield-glass-rear-plastic-channel.html'],'items':[{'id':id,'family':ids[id]['description_en'],'purchased':False,'final_drilling':None,'gate':'PURCHASE_BEFORE_CNC'} for id in ['H20','H21','B21','B12','G11']]+[{'id':nextid,'family':'Slim commercial WPC/widebody siderail','optional':True,'purchased':False,'modification':'PURCHASED-PART MODIFICATION / VERIFY SKU; not a cabinet redesign'}],'rear_channel':{'attachment':'SCREWED','exact_screw_count':None,'exact_centers':None,'exact_pilot_mm':None,'support':'same18mm rear bearing shelf, local angled lands; horizontal floor retained'},'receiver':{'reference_body_mm':[520,42,40],'operating_free_space_mm':[388.65,42,15],'hand_tool_approach_mm':[90,42,85],'actual_latch_motion':None,'status':'CONSERVATIVE_AVAILABLE_SPACE_SCREEN_NOT_A_MEASURED_RECEIVER'},'glass':{'nominal_mm':5,'final_cut_mm':None,'side_profile_sku':None}}
put(R/'config/standard_interfaces_v351.json',interfaces);put(R/'config/hardware_catalog_v351.json',cat);put(O/'assembly-manual.json',manual)
# Count explicit alignment/measurement action steps, not generic tools or inferred assembly minutes.
def align(m):return [s['id'] for st in m['stages'] for s in st['steps'] if re.search(r'\b(align|alignment|square|squareness|measure|leveling|centering)\b',s['action']['en'],re.I)]
complexity={'steps_before':sum(len(s['steps']) for s in before['stages']),'steps_after':sum(len(s['steps']) for s in manual['stages']),'manual_alignment_steps_before':align(before),'manual_alignment_steps_after':align(manual),'count_definition':'Explicit manual action steps containing alignment/measurement work; not an invented count of hand operations','hardware_change_count':'UNRESOLVED physical workflow; hardware families listed per step; no time claim','dry_fit':'SAME','labor':'SAME','piece_count_target':None,'retired':[],'integrated':[],'added':[]};put(O/'assembly-complexity.json',complexity)
for lang,file in [('en','ASSEMBLY_MANUAL.md'),('pt-BR','ASSEMBLY_MANUAL.pt-BR.md')]:
 lines=['# V35.1 '+('Assembly manual' if lang=='en' else 'Manual de montagem'),'','REFERENCE DESIGN — CNC RELEASE BLOCKED / LIBERAÇÃO CNC BLOQUEADA.','', '628.65mm body; commercial lockdown/receiver;5mm tempered glass; optional siderails.','']
 for st in manual['stages']:
  lines+=['## '+st['id']+' — '+st['title'][lang],'']
  for a in st['steps']:
   lines+=['### '+a['id']+' — '+a['title'][lang],'','Status: '+a['status'],'',('Parts: ' if lang=='en' else 'Peças: ')+', '.join(a['component_ids']),'',('Hardware: ' if lang=='en' else 'Ferragens: ')+', '.join(a['hardware_ids']),'',a['orientation'][lang],'',a['faces'][lang],'',a['action'][lang],'',a['check'][lang],'',a['hold'][lang],'','Viewer: '+a['next_state'],'']
 (O/file).write_text('\n'.join(line.rstrip() for line in lines).rstrip()+'\n')
print('V351 DOCUMENTATION',complexity['steps_after'],'steps',len(align(manual)),'alignment action steps')
