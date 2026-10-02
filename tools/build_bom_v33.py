"""Generate bilingual inventory and procurement holds from canonical IDs.
CERN-OHL-S-2.0. Null means unresolved, never zero. No prices or wood mutations.
"""
from pathlib import Path
import json,collections,copy
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/hardware-v33';O.mkdir(parents=True,exist_ok=True)
C=json.loads((R/'config/hardware_catalog_v33.json').read_text());W=json.loads((R/'config/wood_materials_v33.json').read_text());A=C['classification_codes']['A'];B=C['classification_codes']['B'];D=C['classification_codes']['D'];E=C['classification_codes']['E']
hw=C['hardware'];rows=[]
def quantity(q):return 'TBD' if q is None else str(q)
def dump(name,data):(O/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def pt_note(it):
    n='Dimensões e ferragens provisórias; confirmar peça física e montagem antes da liberação.'
    if it['quantity'] is None:n+=' Quantidade não definida; não interpretar como zero.'
    if it['flatpack_classification']==D:n+=' Definido pelo adaptador/equipamento do usuário; não integra o kit básico.'
    if it['flatpack_classification']==C['classification_codes']['C']:n='Eletrônica futura, excluída do flatpack obrigatório; o volume CAD não seleciona um produto.'
    if it['flatpack_classification']==E:n='Reserva de espaço não física; não comprar nem fabricar.'
    specific={
      'F01':'6 parafusos4,5×30; posições atuais preservadas; Torx é candidato, não bit selecionado.',
      'F02':'8 parafusos; cilindro CAD Ø3,4×12. Ø3,5×12 comercial é apenas oportunidade, sem substituição.',
      'H01':'1 eixo de madeira Ø32×560; nenhuma barra metálica ou rolamento.',
      'B01':'4 abraçadeiras comerciais,2 parafusos por peça; medir ferragem real.',
      'F05':'24 posições:4 por guia,6 guias. Comprimento e retenção na lateral pendentes.',
      'F52':'12 posições:2 por cantoneira; as três alturas não multiplicam a quantidade.',
      'F09':'8 posições nas folhas das2 dobradiças principais; engajamento na porta de12 mm pendente.',
      'H11':'2 manípulos M8×40 em X130/X470,Y1260. Soltar pelas portas e rosquear nos alojamentos antes de dobrar.',
      'I05':'2 receptores M8 com apoio metálico; incluir a chapa, sem compra duplicada. Antirrotação pendente.',
      'I06':'2 insertos M8 em X185/X415,Y1268; guardam manípulos, não suportam a caixa.',
      'F17':'48 mm é reserva CAD; não trocar automaticamente por parafuso50 mm.',
      'H12':'2 cabos mecânicos200 mm; manter sobra presa. Não são cabos elétricos.',
      'H13':'Pode acompanhar H11; confirmar conteúdo do conjunto para evitar compra duplicada.',
      'H14':'2 dobradiças contínuas628 mm; passo dos furos não liberado. Não equivalem às dobradiças principais.',
      'H16':'2 ferrolhos na folha passiva, superior e inferior; não há montante central fixo.',
      'F20':'8 parafusos M4 opcionais; comprimento depende da porta12 mm, ventoinha25 mm e acessórios.',
      'F21':'8 fixadores das tampas básicas,4 por estação. Na montagem com ventoinha, substituem-se os parafusos.',
      'F24':'Reserva Ø6×30; cabeça e rosca cativa ainda não selecionadas. Vidro retido durante a dobra.',
      'F25':'72 mm é reserva do parafuso/corredor, não comprimento comercial congelado.',
      'F26':'4 grampos M6; cilindros Ø18×36 representam conjunto/arruela, não parafusos Ø18.',
      'F30':'4 fixadores positivos do cassete;65 mm é reserva. Sem alteração do cassete.',
      'F54':'6 parafusos planejados,3 por lado, com junta capturada e colada.',
      'B13':'Padrão atual58 mm difere da referência WPC57,15 mm; medir pés e chapas, sem corrigir furos nesta tarefa.',
      'H20':'Barra sob medida para caixa600 mm já aceita; V33 não cria nova fabricação metálica.',
      'H25':'Prateleira de brinquedos apenas acessória; não obrigatória nem instalada.',
      'W02':'Uma família Ø9×1 com folga4,5; separar quantidades obrigatórias e opcionais.',
      'W09':'16 arruelas planejadas para8 fixadores; confirmar eventual arruela integrada à cabeça.'}
    if it['id'] in ['H08','H09','H10','F14']:n='MEDIÇÃO FÍSICA OBRIGATÓRIA. Não substituir roscas WPC imperiais por métricas; nenhum furo CNC liberado.'
    return specific.get(it['id'],n)
for it in hw:
    base={k:copy.deepcopy(it[k]) for k in ['id','description_en','description_pt_BR','quantity','unit','material','nominal_dimensions','freeze_status','design_status','measurement_required','flatpack_classification','source','notes','assembly_stage','parent_assembly','price_BRL']}
    if 'material_class' in it:base['material_class']=it['material_class']
    base['status']=base['freeze_status'];base['notes_pt_BR']=pt_note(it);base['quantity_status']=it['quantity_status'];base['bom_layer']=2 if base['flatpack_classification']==A else 3 if base['flatpack_classification']==B else 5 if base['flatpack_classification']==D else 4;base['row_id']=it['id'];rows.append(base)
    for i,u in enumerate(it.get('additional_usages',[]),1):
        b=copy.deepcopy(base);b.update({'row_id':it['id']+'-use'+str(i),'quantity':u['quantity'],'flatpack_classification':u['flatpack_classification'],'assembly_stage':u['assembly_stage'],'notes':u['note'],'quantity_status':'ADDITIONAL_USAGE_PLANNING','bom_layer':2 if u['flatpack_classification']==A else 3});b['parent_assembly']=C['assembly_stages'][u['assembly_stage']]['assembly'];rows.append(b)
for p in W['parts']:
    b=copy.deepcopy(p);b.update({'row_id':p['id'],'bom_layer':1,'freeze_status':'PURCHASE_BEFORE_CNC','design_status':'PROVISIONAL','quantity_status':'LAMINATION_COUNT' if p['unit']=='lamination' else 'CURRENT_CAD_COMPONENT_COUNT','notes_pt_BR':'Madeira estrutural não pode ser rebaixada automaticamente.' if p['material_class']=='STRUCTURAL_PREMIUM' else 'Tentar primeiro compensado premium; alternativa secundária somente após análise de nesting e qualidade.'});
    if p['status']=='CNC_COMPONENT_BREAKDOWN_HOLD':b['notes_pt_BR']+=' Objeto fundido/em degraus: decomposição em peças CNC ou plano de espessura ainda pendente.'
    rows.append(b)
rows.sort(key=lambda r:(r['bom_layer'],r['assembly_stage'],r['row_id']))
stats={'catalog_families_including_electronics_and_reserves':len(hw),'classification_counts':dict(collections.Counter(i['flatpack_classification'] for i in hw)),'physical_hardware_consumable_adapter_families':sum(i['flatpack_classification'] not in [C['classification_codes']['C'],E] for i in hw),'purchase_before_cnc_families':sum(i['freeze_status']=='PURCHASE_BEFORE_CNC' for i in hw),'provisional_families':sum(i['design_status']=='PROVISIONAL' for i in hw),'wood_CAD_component_counts':dict(collections.Counter(p['material_class'] for p in W['parts'])),'wood_scheduled_piece_counts':{cl:sum(p['quantity'] for p in W['parts'] if p['material_class']==cl) for cl in ['STRUCTURAL_PREMIUM','MODULAR_SECONDARY']},'wood_decomposition_holds':[p['id'] for p in W['parts'] if p['status']=='CNC_COMPONENT_BREAKDOWN_HOLD'],'required_unknown_quantity_ids':[i['id'] for i in hw if i['quantity'] is None and i['flatpack_classification']==A],'fastener_washer_nut_insert_families_before':sum(i['id'][0] in 'FWI' for i in hw)+len(C['aliases']),'fastener_washer_nut_insert_families_after':sum(i['id'][0] in 'FWI' for i in hw),'all_CURRENT_objects_accounted_for':len(C['object_to_id']),'manufacturing_ready':False}
dump('bom.json',{'source_head':C['source_head'],'unit_policy':'Quantity null = unresolved, zero only for nonphysical reserves. One cabinet; no spares added. Optional fan/blank alternatives must not be added together.','layers':{'1':'FLATPACK_WOOD','2':'REQUIRED_MECHANICAL_HARDWARE','3':'OPTIONAL_MECHANICAL_ACCESSORIES','4':'FUTURE_ELECTRONICS_AND_REFERENCE','5':'USER_SPECIFIC_ADAPTER_PARTS'},'stats':stats,'rows':rows})
dump('assembly-dependencies.json',{'stages':C['assembly_stages'],'sequence_notes':['Basic mechanical kit includes backbox fan blanks and passive filter provisions; electronics are absent.','Do not install electronics before their replaceable adapters are confirmed.','Close/secure both doors and park locks before backbox fold; main glass and matrix removal remain prerequisites.','Stage grouping is planning metadata, not a validated assembly manual.'], 'family_ids_by_stage':{s:[i['id'] for i in hw if i['assembly_stage']==s] for s in C['assembly_stages']}})
dump('exploded-metadata.json',{'coordinate_system':'CURRENT V32 global mm; no viewer changes','installed_parts':[{k:i[k] for k in ['id','quantity','parent_assembly','assembly_stage','instances','installed_coordinate_status','service_removable','normal_assembly_removable','tool_family','model']} for i in hw],'wood_parts':W['parts']})
tools=[
 {'id':'T01','classification':'REQUIRED','en':'Hand screwdrivers or driver with interchangeable bits','pt_BR':'Chaves manuais ou parafusadeira com bits intercambiáveis','size':None,'families':'F screw families; size after purchase'},
 {'id':'T02','classification':'HARDWARE-DEPENDENT','en':'Torx, Phillips and/or hex bits','pt_BR':'Bits Torx, Phillips e/ou sextavados','size':None,'families':'F01 Torx candidate; do not claim T20 for an unselected local equivalent'},
 {'id':'T03','classification':'HARDWARE-DEPENDENT','en':'Sockets/spanners for nuts and leg/WPC bolts','pt_BR':'Soquetes/chaves para porcas e parafusos dos pés/WPC','size':None,'families':'M4/M5/M6/M8 and measured imperial interfaces'},
 {'id':'T04','classification':'REQUIRED','en':'Tape, square, clamps and soft mallet','pt_BR':'Trena, esquadro, sargentos e martelo de borracha','size':None,'families':'Wood assembly and laminated pads'},
 {'id':'T05','classification':'LIKELY','en':'Drill with depth stop for qualified shallow pilot completion','pt_BR':'Furadeira com limitador para finalizar pilotos qualificados','size':None,'families':'F01 current CNC pilot1 mm / finished13 mm; supplier coupon first'},
 {'id':'T06','classification':'HARDWARE-DEPENDENT','en':'Pilot bits and countersink for controlled touch-up only','pt_BR':'Brocas piloto e escareador somente para retoques controlados','size':None,'families':'Primary structural holes/countersinks are CNC-shop work; no freehand pattern layout'},
 {'id':'T07','classification':'HARDWARE-DEPENDENT','en':'Insert driver and retaining-ring pliers','pt_BR':'Chave para insertos e alicate para anéis de retenção','size':None,'families':'I families / W08/H13 after selection'},
 {'id':'T08','classification':'LIKELY','en':'Torque-controlled hand tool','pt_BR':'Ferramenta manual com controle de torque','size':None,'families':'Qualified structural clamps/legs/WPC; torque not yet specified'},
 {'id':'T09','classification':'REQUIRED','en':'Eye protection, sanding and adhesive cleanup supplies','pt_BR':'Proteção ocular, lixas e materiais para limpeza do adesivo','size':None,'families':'Flatpack finishing/assembly'}]
dump('tools.json',tools)
def esc(s):return str(s).replace('|','/').replace('\n',' ')
def dims(r):
    d=r['nominal_dimensions'];return json.dumps(d,ensure_ascii=False,separators=(',',':')) if d else 'TBD'
classpt={A:'A — obrigatório',B:'B — opcional',C['classification_codes']['C']:'C — eletrônica futura',D:'D — adaptador do usuário',E:'E — referência não congelada'}
statuspt={'PURCHASE_BEFORE_CNC':'COMPRAR/MEDIR ANTES DO CNC','PURCHASE_BEFORE_ASSEMBLY':'COMPRAR ANTES DA MONTAGEM','OPTIONAL':'OPCIONAL','PROVISIONAL':'PROVISÓRIO','DESIGN_GEOMETRY_ONLY':'GEOMETRIA DE PROJETO','CNC_COMPONENT_BREAKDOWN_HOLD':'DECOMPOSIÇÃO CNC PENDENTE'}
for lang in ['en','pt-BR']:
    pt=lang=='pt-BR';text=['# '+('V33 — Lista de materiais do flatpack' if pt else 'V33 — Flatpack bill of materials'),'',('Inventário de uma máquina. Fabricação BLOQUEADA. TBD significa não definido, nunca zero. O kit mecânico não exige eletrônica. Não somar tampas e ventoinhas alternativas. Sem preços.' if pt else 'One cabinet inventory. Manufacturing BLOCKED. TBD means unresolved, never zero. The mechanical kit needs no electronics. Do not sum alternative fan and blank configurations. No prices.'),'',('Dimensões de madeira são caixas envolventes instaladas, não retângulos para nesting. As93 linhas de madeira incluem conjuntos que precisam de decomposição. Fonte e nota técnica original estão preservadas no JSON.' if pt else 'Wood dimensions are installed bounding boxes, not nesting rectangles. The93 wood lines include assemblies awaiting decomposition. Full source and technical notes are retained in JSON.'),'']
    for layer in range(1,6):
        label=(['Madeira flatpack','Ferragens mecânicas obrigatórias','Acessórios mecânicos opcionais','Eletrônica futura / referências','Adaptadores específicos do usuário'] if pt else ['Flatpack wood','Required mechanical hardware','Optional mechanical accessories','Future electronics / references','User-specific adapters'])[layer-1]
        text+=['## BOM '+str(layer)+' — '+label,'']
        for stage in C['assembly_stages']:
            subset=[r for r in rows if r['bom_layer']==layer and r['assembly_stage']==stage]
            if not subset:continue
            text+=['### '+('Etapa ' if pt else 'Stage ')+stage+' — '+C['assembly_stages'][stage]['pt' if pt else 'en'],'','| ID | '+('Descrição | Qtd. | Material | Situação / classe |' if pt else 'Description | Qty | Material | Status / class |'),'| --- | --- | ---: | --- | --- |']
            for r in subset:
                mat=r.get('material_class',r['material']);st=statuspt.get(r['status'],r['status']) if pt else r['status'];cl=classpt[r['flatpack_classification']] if pt else r['flatpack_classification']
                text.append('| '+r['row_id']+' | '+esc(r['description_pt_BR'] if pt else r['description_en'])+' | '+quantity(r['quantity'])+' | '+esc(mat)+' | '+st+' / '+cl+' |')
            text+=['']
            for r in subset:
                text+=['- **'+r['row_id']+'** — '+('Dimensões nominais: ' if pt else 'Nominal dimensions: ')+esc(dims(r))+'. '+('Medição física: SIM. Fonte: ' if pt else 'Physical measurement: YES. Source: ')+esc('; '.join(r['source']))+'. '+(r['notes_pt_BR'] if pt else r['notes'])]
            text+=['']
    text+=['---','CERN-OHL-S-2.0 · Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet','']
    (O/('flatpack-bom-'+lang+'.md')).write_text('\n'.join(line.rstrip() for line in text).rstrip()+'\n')
for name,selected in [
 ('purchase-before-cnc',[i for i in hw if i['controls_permanent_cnc'] and i['flatpack_classification']!=E]),
 ('purchase-before-assembly',[i for i in hw if not i['controls_permanent_cnc'] and i['flatpack_classification']!=E and i['flatpack_classification']!=C['classification_codes']['C']]),
 ('optional-accessories',[i for i in hw if i['flatpack_classification']==B]),
 ('future-electronics',[i for i in hw if i['flatpack_classification'] in [C['classification_codes']['C'],D,E]])]:
    dump(name+'.json',{'not_a_shopping_release':True,'note':'Before-CNC items must also be on hand for assembly. Lists show obligations, not purchase authorization or stock availability. Unknown qty is not zero.','items':selected})
    lines=['# '+name.replace('-',' ').title(),'','Provisional inventory; no prices or manufacturing release. Before-CNC items are also required before their assembly stage. Optional/future classifications remain conditional.','','| ID | Description EN / PT-BR | Qty | Class | Hold |','| --- | --- | ---: | --- | --- |']
    for i in selected:lines.append('| '+i['id']+' | '+esc(i['description_en']+' / '+i['description_pt_BR'])+' | '+quantity(i['quantity'])+' | '+i['flatpack_classification']+' | '+esc(i['notes'])+' |')
    (O/(name+'.md')).write_text('\n'.join(lines)+'\n')
dump('summary.json',stats)
print('HARDWARE_V33_BOM_PASS',len(rows),'rows',stats,flush=True)
