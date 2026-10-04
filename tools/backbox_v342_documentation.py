"""V34.2 bilingual evidence/manual/BOM. CERN-OHL-S-2.0."""
from pathlib import Path
import json,copy
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/backbox-v342';B=R/'exports/generated/backbox-v34'
def read(p):return json.loads(p.read_text())
def put(n,x):(O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def bi(e,p):return {'en':e,'pt-BR':p}
g=read(O/'geometry-validation.json');reg=read(O/'manufacturing-register.json');cat=read(R/'config/hardware_catalog_v342.json');delta=read(O/'manufacturing-delta.json');mass=read(O/'mass-counts.json')
sources=[{'id':'TCL','url':'https://tclelectronics.co.nz/downloads/brochures/32S5K_Product_Specification_NZ.pdf','publisher':'TCL','evidence':'Official indexed manufacturer specification:715x422x75mm without stand;3.15kg;VESA100x100;M4x10 reference. Assembled screw length is NOT released from this value.','status':'DOCUMENTED; actual bosses, VESA offset, connectors and active image not established','access':'Official indexed PDF extract inspected; direct PDF request timed out. No proprietary document copied.'},{'id':'TUKKARI_GUIDE','url':'https://www.tukkari.com/advisor/assembly-guide-widebody-vpin-cabinet-premium-flat-pack','evidence':'One monitor plate; combined lower panel; ordinary side and rear plastic playfield-glass channels. Public assembly architecture only.'},{'id':'TUKKARI_PRODUCT','url':'https://www.tukkari.com/p/ultra-widebody-virtual-pinball-cabinet-vpin-premium-flat-pack-kit','evidence':'3mm clear acrylic, routed channels,120mm fan interfaces and combined DMD/speaker panel. Functional adaptation; no source CAD copied.'}]
put('sources.json',sources)
audit=[]
for name,adopt,conflict,deviation in [
 ('MONITOR','One fixed monitor plate;front monitor service;spacer depth adjustment.','Owner mandates captured top-inserted plate, supplier one-face CNC; public bracket construction differs.','Existing4mm guides,2 stops and top capture retained. Fixed planeY1209 and4VESA100 slots independently dimensioned.'),
 ('ACRYLIC','3mm acrylic and simple front channels; no wooden bezel.','Actual TCL image and acrylic stock/liner unknown; owner requires front removal without top disassembly.','Existing front tilt seat +one removable strip retained. Rear mask687x356 is provisional and crops assumed image to cover30mm travel.'),
 ('VENTILATION','Ordinary120mm fan-size openings.','Our twin doors, locks and90mm speaker depth constrain location.','TwoØ116 lower openings in existing doors atX155/445 Z738; no added panel or duct. Grille-only default; optional fans.'),
 ('DMD_SPEAKERS','One combined front panel.','Public bent metal does not translate directly to one-face plywood; owner already accepts V34 direct-front arrangement.','Existing18mm one-panel architecture retained.90mm rear speaker reserve replaces60mm after baffle deletion.'),
 ('PLAYFIELD_GLASS','Continuous side plastic channels, rear plastic channel, front lockdown retention.','Extending fixed side channels to the folding rear stop creates sweep interference. Existing WPC fold/main cabinet protected.','Retain1100mm side profiles; rear U at1142mm local glass length.32mm side-edge transition to rear support. Local top-face floor bevel follows derived9.906669deg. Physical edge support/channel/lockdown qualification HOLD.')]:
 audit.append({'subsystem':name,'equivalent_found':True,'public_sources':[sources[1]['url'],sources[2]['url']],'functional_architecture_adopted':adopt,'our_measured_or_owner_conflict':conflict,'minimum_deviation':deviation,'source_CAD_imported':False})
put('tukkari-first-audit.json',audit)
manual=read(B/'assembly-manual.json');ret=set(delta['retired_instances'])|set(g['retired']);retH=set(delta['retired_hardware_ids'])
# Preserve unrelated stages; update affected authoritative service text and remove obsolete identifiers.
replacements={'backbox front glass':'backbox front acrylic','vidro frontal do backbox':'acrílico frontal do backbox','backbox-v34/':'backbox-v342/','BB_Backglass':'BB_AcrylicFront','BB_GlassTopScrew':'BB_AcrylicRetainerScrew','Backglass':'Acrylic front','backglass glass':'backbox acrylic','+/-5mm':'+/-15mm','+5mm':'+15mm','5mm above':'15mm above','60mm rear':'90mm rear','<=60mm':'<=90mm','one75 or100 pattern':'primary100x100 pattern','padrão75 ou100':'padrão100x100','vidro/tira':'acrílico/tira','Vidro/tira':'Acrílico/tira','glass/strip':'acrylic/strip','Glass/strip':'Acrylic/strip','glass seating':'acrylic seating','vidro do backbox':'acrílico do backbox'}
def walk(x):
 if isinstance(x,str):
  for a,b in replacements.items():x=x.replace(a,b)
  return x
 if isinstance(x,list):return [walk(a) for a in x if not isinstance(a,str) or a not in ret|retH]
 if isinstance(x,dict):return {k:walk(v) for k,v in x.items()}
 return x
manual=walk(manual);manual.update(version='V34.2',source_head='8d951bc37a38d5e3820cbde93700f1161ff32fb1',geometry_authority='config/current_v32.json',current_manufacturing_register='config/manufacturing/flatpack_v342.json',manufacturing_release=False)
for st in manual['stages']:
 for s in st['steps']:
  if s['id']=='00.1':s['action']=bi('Inventory production lot and qualify coupon before full-sheet release. Plywood is12/18mm only. Acrylic is separate purchased3mm reference stock; playfield glass is purchased5mm tempered. No wood monitor bezel. SW01/SW02 remain solid wood.','Identifique lote e valide cupom antes de chapas completas. Compensado somente12/18mm. Acrílico comprado separado, referência3mm; vidro do playfield temperado5mm. Sem moldura de madeira do monitor. SW01/SW02 permanecem maciços.')
  if s['id']=='08.12':s['action']=bi('Remove acrylic/upper strip. Support monitor at+15mm; bring from FRONT; rear access installs VESA bolts. Plate and shell top remain fixed.','Retire acrílico/tira superior. Sustente monitor a+15mm; entre pela FRENTE; parafusos VESA por trás. Placa e topo fixos.')
  if s['id']=='08.14':s['action']=bi('Four primary100x100 slots allow±15mm. Verify LOW/NOMINAL/HIGH. Actual TCL VESA offset and active image remain unmeasured; final mask follows selected alignment.','Quatro rasgos100x100 permitem±15mm. Confira BAIXO/NOMINAL/ALTO. Posição VESA e imagem TCL não medidas; máscara final conforme alinhamento real.')
  if s['id']=='08.15':s['action']=bi('Plate frontY1209; planning12mm spacers clear75/65 and80/70 body/boss cases.80/55 fails. Measure actual bosses, connectors and thread engagement before selecting bolts.','Frente da placaY1209; espaçadores12mm liberam corpo/boss75/65 e80/70.80/55 falha. Meça bosses, conectores e engate antes de selecionar parafusos.')
  if s['id']=='11.1':
   s.update(title=bi('Fit simple lower fan stations','Monte estações inferiores simples'),component_ids=['BB_DoorL','BB_DoorR'],hardware_ids=['B20','F66','H28','F67'],action=bi('Fit two commodity grilles directly to lower door openings. Optional120mm fans replace passive stacks; no intake frames or plywood baffles.','Fixe duas grades comerciais diretamente nas aberturas inferiores das portas. Fans120mm opcionais substituem pilhas passivas; sem molduras ou defletores.'),check=bi('Verify grille safety, fan clearances, locks and100degree door sweep.','Confira proteção, folgas, travas e giro100graus.'),hold=bi('Fan/grille/bolt dimensions and flexible lead routing pending physical purchase.','Dimensões fan/grade/parafusos e fios flexíveis pendem da compra.'))
  if s['id']=='11.2':
   s['action']=bi('Upper exhaust stations retain fan/blank choice. Lower stations use grille-only or fan+grille. Builder chooses wiring and flexible lead routing; no universal wooden anchors.','Estações superiores mantêm fan/tampa. Inferiores usam grade ou fan+grade. Usuário escolhe fios e trajeto flexível; sem ancoragem universal de madeira.')
  if s['id'].startswith('08.'):
   for field in ['title','action','check','hold']:
    for lang in ['en','pt-BR']:s[field][lang]=s[field][lang].replace('glass','acrylic').replace('Glass','Acrylic').replace('vidro','acrílico').replace('Vidro','Acrílico')
  if s['id'].startswith('08.'):
   s['review_view']='exports/generated/backbox-v342/index.html';s['hold']=bi('Reference geometry only: actual monitor/DMD/speakers, acrylic/channel, fasteners, material/coupon and physical load qualification required.','Geometria de referência: monitor/DMD/alto-falantes reais, acrílico/canal, fixadores, material/cupom e qualificação física obrigatórios.')
# Explicit new simple ventilation, acrylic, main-glass operation cards.
template=copy.deepcopy(manual['stages'][8]['steps'][0])
extra=[('08.26','Fit passive lower grilles or optional intake fans','Instale grades passivas ou ventoinhas inferiores opcionais',['BB_DoorL','BB_DoorR'],['F66','B20','F67','H28'],'Two lowerØ116 stations share105mm pitch. Passive:F66+grille. Active:F67 replaces F66,120x120x25 fan+grille. No filter frames, ducts or universal cable anchors. Builder qualifies flexible wiring with doors0–100°.','Duas estaçõesØ116, passo105mm. Passivo:F66+grade. Ativo:F67 substitui F66, fan120x120x25+grade. Sem molduras, dutos ou ancoragem universal. Usuário qualifica fios flexíveis no giro0–100°.'),('08.27','Fit and mask acrylic','Instale e pinte o acrílico',['BB_AcrylicFront','BB_GLASS_TOP_RETAINER'],['G10','G08','G09','F65'],'Reference752x459x3 sheet: lower padded seat, side rebates, one2-screw upper strip. Paint REAR face only after actual screen alignment.687x356 fixed window covers±15mm but crops assumed697x392 image. Remove strip, lift1mm, tilt10°, lift6mm and withdraw FRONT.','Chapa referência752x459x3: assento inferior acolchoado, rebaixos laterais, tira superior com2 parafusos. Pinte face TRASEIRA após alinhamento real. Janela687x356 cobre±15mm, mas recorta imagem assumida697x392. Retire tira, eleve1mm, incline10°, eleve6mm e retire pela FRENTE.'),('08.28','Fit main playfield glass system','Monte o sistema de vidro do playfield',['CandidateGlass','BB_PFRearChannel','PF_LockdownGlassRetainer'],['G11','B21','F68'],'5mm TEMPERED glass; lined side channels; angled rear U; lockdown front stop. Glass slides forward after lockdown removal. Reference575x1142, final cut NULL until actual profiles/clearances. Rear local floor bevel9.906669° is derived from side channels; whole floor stays horizontal.32mm side-edge transition requires physical glass qualification. Before fold remove main glass and matrix; close doors, release/park locks. Backbox acrylic and lower panel remain.','Vidro TEMPERADO5mm; canais laterais revestidos, U traseiro inclinado, lockdown frontal. Retire lockdown e deslize vidro à frente. Referência575x1142, corte finalNULL até perfis/folgas reais. Rebaixo local9,906669° deriva dos canais; fundo não inclinado. Transição lateral32mm exige ensaio físico. Antes da dobra retire vidro principal e matrix; feche portas, solte/estacione travas. Acrílico e painel inferior ficam.')]
for id,en,pt,parts,hw,enact,ptact in extra:
 s=copy.deepcopy(template);s.update(id=id,title=bi(en,pt),component_ids=parts,hardware_ids=hw,action=bi(enact,ptact),check=bi('Check retention, unobstructed service and selected hardware fit. No full-sheet CNC release.','Confira retenção, acesso e encaixe real. Sem liberação de chapas completas.'),checkpoint=True,animation_id='assembly-'+id,next_state='PLAY',review_view='exports/generated/backbox-v342/index.html');manual['stages'][8]['steps'].append(s)
manual['part_preparation']=reg['parts'];manual['hardware_quantity_overlay']={'source':'config/hardware_catalog_v342.json','status':'Numeric quantities only where known; optional active fixings REPLACE passive ones.'};put('assembly-manual.json',manual)
for lang,suffix in [('en',''),('pt-BR','.pt-BR')]:
 lines=['# '+('Assembly manual — V34.2' if lang=='en' else 'Manual de montagem — V34.2'),'','**CNC RELEASE BLOCKED / LIBERAÇÃO CNC BLOQUEADA**','', '[CAD reviews](../exports/generated/backbox-v342/index.html) · [Offline viewer](../exports/generated/viewer-v32/index.html)','']
 for st in manual['stages']:
  lines+=['## '+st['id']+' — '+st['title'][lang],'']
  for s in st['steps']:
   lines+=['### '+s['id']+' — '+s['title'][lang],'','Status: '+s['status'],'','Parts: '+', '.join(s['component_ids'])+' | Hardware: '+', '.join(s['hardware_ids']),'',s['action'][lang],'',s['orientation'][lang]+' '+s['faces'][lang],'',s['tools'][lang],'','**CHECK:** '+s['check'][lang],'','**HOLD:** '+s['hold'][lang],'','Viewer: '+s['next_state']+' / '+s['animation_id'],'']
 (R/('docs/ASSEMBLY_MANUAL'+suffix+'.md')).write_text('\n'.join(x.rstrip() for x in lines).rstrip()+'\n')
 bom=['# Manufacturing wood BOM V34.2 — NOT FOR CNC','','|ID|Instance|Description|Stock mm|Material|Status|','|---|---|---|---|---|---|']
 for a in reg['parts']:bom.append('|'+ '|'.join(str(x) for x in [a['manufacturing_part_id'],a['instance_id'],a['description_en' if lang=='en' else 'description_pt_BR'],a['nominal_stock_thickness_mm'] or 'SOLID',a['material_class'],a['manufacturing_status']])+'|')
 (O/('manufacturing-bom'+suffix+'.md')).write_text('\n'.join(bom)+'\n')
(R/'assembly-manual.json').write_text(json.dumps(manual,indent=2,ensure_ascii=False)+'\n')
wood={'version':'V34.2','parts':[{k:a[k] for k in ['manufacturing_part_id','instance_id','source_component','material_class','nominal_stock_thickness_mm']} for a in reg['parts']],'premium_first':True,'secondary_substitution_requires_review':True,'structural_premium_never_automatically_downgraded':True};(R/'config/wood_materials_v342.json').write_text(json.dumps(wood,indent=2)+'\n')
# Purpose/attachment audit references the actual manufacturing register; no hidden L assemblies.
prior={a['name']:a for a in read(B/'attachment-audit.json')};audit=[]
for a in reg['parts']:
 n=a['source_component']
 if not n.startswith('BB_'):continue
 item=copy.deepcopy(prior[n]);item['ID']=a['manufacturing_part_id']
 for key in ['purpose','load','why_needed']:
  if isinstance(item.get(key),str):item[key]=item[key].replace('glass','acrylic').replace('Glass','Acrylic')
 item['status']='RETAINED_CURRENT_V342';audit.append(item)
put('small-wood-audit.json',audit)
print('V342_DOCUMENTATION',sum(len(s['steps']) for s in manual['stages']))
