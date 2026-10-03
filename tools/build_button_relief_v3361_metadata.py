"""V33.6.1 corrected front ergonomic authority and bilingual manual/BOM overlay.
CERN-OHL-S-2.0. No purchased hardware dimensions or counts are invented.
"""
from pathlib import Path
import json,copy,csv
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/button-relief-v3361'
def read(p):return json.loads((R/p).read_text())
def dump(p,v):(R/p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def bi(en,pt):return {'en':en,'pt-BR':pt}
def fmt(x):
 if x is None:return 'HOLD'
 if isinstance(x,(int,float)):return f'{x:.3f}'.rstrip('0').rstrip('.') or '0'
 if isinstance(x,list):return ' / '.join(fmt(v) for v in x)
 return str(x)
C=read('config/button_relief_v3361.json');reg=read('exports/generated/button-relief-v3361/manufacturing-register.json');parts=reg['parts'];by={p['instance_id']:p for p in parts}
manual=read('exports/generated/monitor-support-v336/assembly-manual.json');base=read('exports/generated/structural-v335/assembly-manual.json');cat=read('config/hardware_catalog_v335.json')
manual['version']='V33.6.1';manual['source_head']=C['head_before'];manual['source_geometry_unchanged']=False
steps={t['id']:t for s in manual['stages'] for t in s['steps']};base_steps={t['id']:t for s in base['stages'] for t in s['steps']}
notes={
 '06.1':bi('Use CURRENT M025 with the clean relief open to the front edge: narrowed straight sides and rounded return to full width, with no horn, front bridge or hooked projection. Keep the V33.6 rear 180 × 110 mm R8 service window and two strain-relief slots. Preserve the VESA load region, dowel, four straps and eight F02 coordinates. Button clearance is derived from the restored front leaf-body, terminal, wire and tool reserves. Do not move buttons to fit the plywood. Final display/button hardware and stiffness qualification remain HOLD.',
 'Use M025 CURRENT com alívio limpo aberto até a borda frontal: laterais retas recuadas e retorno arredondado à largura total, sem ponta, ponte frontal ou gancho. Mantenha a janela traseira V33.6 de 180 × 110 mm R8 e dois rasgos para alívio de tração. Preserve região de carga VESA, cavilha, quatro abraçadeiras e oito coordenadas F02. A folga é derivada das reservas frontais de corpo leaf, terminais, fios e ferramenta. Não mova os botões para acomodar a madeira. Ferragens finais do monitor/botões e qualificação de rigidez permanecem PENDENTES.'),
 '18.1':bi('CURRENT OWNER BUTTON AUTHORITY: primary Y89, secondary Y127, both 65 mm below the actual local side-top profile (currently Z350.593661971831 and Z357.2302816901408). Mirror both sides. This restores owner ergonomic correction87d63825; V33.6 rearward Y255/Y310 Z270 was an erroneous temporary restoration and is SUPERSEDED. Reference Ø15.875 bore and Ø25 ×3 nut pocket are REFERENCE_ONLY_NOT_RELEASED. Actual leaf buttons and all final bores/recesses/leaf mounting holes are PURCHASE_BEFORE_CNC. Service requires main playfield glass and matrix removed, with playfield raised. Under-front220 ×55 controls remain a separate unlocated schematic.',
 'AUTORIDADE ATUAL DO PROPRIETÁRIO PARA BOTÕES: primário Y89, secundário Y127, ambos 65 mm abaixo do topo local real da lateral (atualmente Z350,593661971831 e Z357,2302816901408). Espelhe nos dois lados. Restaura a correção ergonômica87d63825; Y255/Y310 Z270 da V33.6 foi restauração temporária incorreta e está SUPERADA. Furo Ø15,875 e rebaixo Ø25 ×3 são SOMENTE REFERÊNCIA, NÃO LIBERADOS. Compre botões leaf antes de liberar furos/rebaixos/fixações: PURCHASE_BEFORE_CNC. Serviço requer vidro principal e matriz removidos, com playfield levantado. Controles inferiores220 ×55 continuam esquema separado sem localização.')}
for sid,note in notes.items():
 # Start from pre-V33.6 action to remove, not append to, the wrong positional
 # instruction. All unrelated V33.6 monitor/cable steps remain verbatim.
 steps[sid]['action']={lang:base_steps[sid]['action'][lang]+' '+txt for lang,txt in note.items()};steps[sid]['status']='WAITING_FOR_PHYSICAL_MEASUREMENT'
manual['current_manufacturing_register']='exports/generated/button-relief-v3361/manufacturing-register.json';manual['geometry_authority']='config/button_relief_v3361.json'
prepkeys=list(manual['part_preparation'][0]);manual['part_preparation']=[{k:by[p['instance_id']].get(k) for k in prepkeys} if by[p['instance_id']].get('version')=='V33.6.1' else p for p in manual['part_preparation']]
dump('exports/generated/button-relief-v3361/assembly-manual.json',manual)
# Reuse presentation only, leaving every historical builder/config unchanged.
source=(R/'tools/build_structural_v335_metadata.py').read_text();source=source[source.index("fields=['instance_id'"):source.index("manifest={'version'")].replace('V33.5','V33.6.1')
source=source.replace("'CNC FACE_A · '+op.get('id','')", "(('REFERENCE ONLY / PURCHASE BEFORE CNC — final bore/recess unselected · ' if lang=='en' else 'SOMENTE REFERÊNCIA / COMPRAR ANTES DO CNC — furo/rebaixo finais indefinidos · ') if op.get('production_export_policy') or op.get('hardware_interface_status')=='PURCHASE_BEFORE_CNC' else 'CNC FACE_A · ')+op.get('id','')")
exec(compile(source,'V3361 manual/BOM presentation','exec'),globals())
manifest={'version':'V33.6.1','head_before':C['head_before'],'current_register':'exports/generated/button-relief-v3361/manufacturing-register.json','current_BOM':'exports/generated/button-relief-v3361/manufacturing-bom.csv','CNC_filter':'manufacturing_class != SHOP_MADE_SOLID_WOOD_PART','shop_family':'SW01','installed_material_map':'config/wood_materials_v335.json','release':False,'hardware_catalog':'config/hardware_catalog_v335.json','button_positional_authority':'config/button_relief_v3361.json','button_final_bore_mm':None,'button_final_recess_mm':None}
dump('config/manufacturing/flatpack_v3361.json',manifest)
print('V3361_METADATA_PASS',len(parts))
