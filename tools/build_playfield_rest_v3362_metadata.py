"""V33.6.2 documentation for requested front relief and unresolved PLAY support.
CERN-OHL-S-2.0. No new rests or purchased hardware are added by this overlay.
"""
from pathlib import Path
import json,copy,csv
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/playfield-rest-v3362'
def read(p):return json.loads((R/p).read_text())
def dump(p,v):(R/p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def bi(en,pt):return {'en':en,'pt-BR':pt}
def fmt(x):
 if x is None:return 'HOLD'
 if isinstance(x,(int,float)):return f'{x:.3f}'.rstrip('0').rstrip('.') or '0'
 if isinstance(x,list):return ' / '.join(fmt(v) for v in x)
 return str(x)
C=read('config/playfield_rest_v3362.json');reg=read('exports/generated/playfield-rest-v3362/manufacturing-register.json');parts=reg['parts'];by={p['instance_id']:p for p in parts}
manual=read('exports/generated/button-relief-v3361/assembly-manual.json');cat=read('config/hardware_catalog_v335.json')
manual['version']='V33.6.2';manual['source_head']=C['head_before'];manual['source_geometry_unchanged']=False
steps={t['id']:t for s in manual['stages'] for t in s['steps']}
hold=bi('CLOSED_POSITION_SUPPORT_BLOCKED. The rear dowel contacts its two open cradles, but CURRENT contains no front landing/rest or closed-position latch. The base is22 mm above T1, T2 and T3. PLAY is a reference pose and cannot be treated as a self-supporting operating assembly. Do not use unqualified pivot friction or electronics/buttons as a stop. A dedicated rest/support design and load/retention validation are still required; no new rest parts are included in this BOM.',
'CLOSED_POSITION_SUPPORT_BLOCKED. A cavilha traseira apoia nos dois berços abertos, mas CURRENT não contém apoio/batente frontal nem trava da posição fechada. A base está22 mm acima de T1, T2 e T3. PLAY é posição de referência e não representa montagem operacional com apoio próprio. Não use atrito não qualificado do pivô ou eletrônicos/botões como batente. Projeto de apoio e validação de carga/retenção continuam necessários; esta BOM não inclui novas peças de apoio.')
manual['engineering_blockers']=[{'id':'CLOSED_POSITION_SUPPORT_BLOCKED','status':'OPEN','description':hold,'geometry_scope':'No new closed rest geometry; existing collision-free paths do not prove static support.'}]
for sid in ['00.1','05.1','06.1','06.2','17.1','17.2']:
 t=steps[sid];t['hold']={lang:hold[lang]+' '+t['hold'][lang] for lang in hold};t['engineering_blockers']=['CLOSED_POSITION_SUPPORT_BLOCKED']
 t.setdefault('validation',{})['closed_position_support']='BLOCKED'
relief=read('exports/generated/playfield-rest-v3362/geometry-validation.json')['relief']
length=fmt(relief['length_mm'])
note=bi(f'Owner-requested V33.6.2 relief extends30 mm farther inward on EACH side: total inset52 mm, remaining front width396 mm, retained length{length} mm and R8 transition. Buttons stay atY89/Y127, local side top minus65 mm. Rear window, strain slots, VESA region, dowel and straps remain unchanged. This clearance edit does not add front support.',
f'O alívio V33.6.2 solicitado avança mais30 mm para dentro em CADA lateral: recuo total52 mm, largura frontal restante396 mm, comprimento{length} mm e transiçãoR8 mantidos. Os botões permanecem emY89/Y127,65 mm abaixo do topo local. Janela traseira, rasgos de alívio de tração, região VESA, cavilha e abraçadeiras permanecem iguais. Esta alteração de folga não cria apoio frontal.')
steps['06.1']['action']={lang:steps['06.1']['action'][lang]+' '+note[lang] for lang in note}
steps['06.2']['action']={lang:hold[lang]+' '+steps['06.2']['action'][lang] for lang in hold}
steps['06.2']['check']=bi('STOP: qualify closed-position rests and retention before an unsupported PLAY or service demonstration. The retained50° service/48 mm lift paths establish geometric clearance only; handling/support/load qualification is separate.',
'PARE: qualifique os apoios e a retenção da posição fechada antes de demonstrar PLAY ou serviço sem apoio externo. As trajetórias50°/48 mm mantidas estabelecem apenas folga geométrica; qualificação de manuseio/apoio/carga é separada.')
manual['current_manufacturing_register']='exports/generated/playfield-rest-v3362/manufacturing-register.json';manual['geometry_authority']='config/playfield_rest_v3362.json'
prepkeys=list(manual['part_preparation'][0]);manual['part_preparation']=[{k:by[p['instance_id']].get(k) for k in prepkeys} if by[p['instance_id']].get('version')=='V33.6.2' else p for p in manual['part_preparation']]
dump('exports/generated/playfield-rest-v3362/assembly-manual.json',manual)
source=(R/'tools/build_structural_v335_metadata.py').read_text();source=source[source.index("fields=['instance_id'"):source.index("manifest={'version'")].replace('V33.5','V33.6.2')
source=source.replace("'CNC FACE_A · '+op.get('id','')", "(('REFERENCE ONLY / PURCHASE BEFORE CNC — final bore/recess unselected · ' if lang=='en' else 'SOMENTE REFERÊNCIA / COMPRAR ANTES DO CNC — furo/rebaixo finais indefinidos · ') if op.get('production_export_policy') or op.get('hardware_interface_status')=='PURCHASE_BEFORE_CNC' else 'CNC FACE_A · ')+op.get('id','')")
exec(compile(source,'V3362 manual/BOM presentation','exec'),globals())
manifest={'version':'V33.6.2','head_before':C['head_before'],'current_register':'exports/generated/playfield-rest-v3362/manufacturing-register.json','current_BOM':'exports/generated/playfield-rest-v3362/manufacturing-bom.csv','CNC_filter':'manufacturing_class != SHOP_MADE_SOLID_WOOD_PART','shop_family':'SW01','installed_material_map':'config/wood_materials_v335.json','release':False,'hardware_catalog':'config/hardware_catalog_v335.json','button_positional_authority':'config/button_relief_v3361.json','button_final_bore_mm':None,'button_final_recess_mm':None,'closed_position_support':'CLOSED_POSITION_SUPPORT_BLOCKED'}
dump('config/manufacturing/flatpack_v3362.json',manifest)
print('V3362_METADATA_PASS',len(parts))
