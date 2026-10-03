"""Extend the committed offline V33.2 atlas; never rewrite engineering geometry."""
from pathlib import Path
import json,subprocess,hashlib,math
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/assembly-v333'
read=lambda f:json.loads((R/f).read_text())
HEAD=read('config/assembly_planning_v333.json')['head_before']
manual=read('exports/generated/viewer-v332/assembly-manual.json');motions=read('exports/generated/assembly-v333/motion-authority.json')
clips=[]
for stage in manual['stages']:
 for step in stage['steps']:
  clips.append({'id':'assembly-'+step['id'],'type':'assembly','title':{k:step['id']+' · '+v for k,v in step['title'].items()},'stage':stage['id'],'step':step['id'],'first_stage_step':step==stage['steps'][0],
   'status':'SCHEMATIC_ASSEMBLY_ANIMATION','duration_s':8,'piece_ids':step['component_ids'],'hardware_ids':step['hardware_ids'],'action':step['action'],'check':step['check'],
   'note':{'en':'SCHEMATIC ASSEMBLY ANIMATION — exploded highlight → fade/seat. No physical insertion path claim. Repeated stage steps inspect the same kit, not another quantity. Hardware/fixture/tool holds remain.',
   'pt-BR':'ANIMAÇÃO ESQUEMÁTICA DE MONTAGEM — destaque explodido → transição/assentamento. Não valida trajetória física. Etapas repetidas inspecionam o mesmo kit, sem duplicar quantidades. Ferragens/gabaritos/ferramentas pendentes.'}})
services=[
 ('pf-service','Playfield service opening','Abertura de serviço do playfield','PF','Main glass and matrix removed. Support/load qualification remains; never work below an unsupported playfield.','Vidro principal e matriz removidos. Validação de apoio/carga pendente; nunca trabalhe sob playfield sem apoio.'),
 ('pf-lift','Playfield lift-out 48 mm','Retirada do playfield 48 mm','PF_LIFT','Main glass/matrix removed; complete assembly lifts48mm from its open cradles. Provide external manual support.','Vidro principal/matriz removidos; conjunto sobe48mm dos berços abertos. Sustente manualmente.'),
 ('matrix','Matrix removal','Remoção da matriz','MATRIX','Main glass removed; release retainers, rock26°, translate forward68mm, lift100mm. Electrical interface remains builder-configurable; secure any moving leads.','Vidro principal removido; solte retentores, gire26°, avance68mm, eleve100mm. Interface elétrica configurável; acomode os cabos móveis.'),
 ('doors','Backbox rear doors','Portas traseiras do backbox','DOORS','UPRIGHT only. Release active cam and passive bolts; active leaf opens first, then passive. Latch operation shown schematically; door rotation0–100° uses accepted axes.','Somente VERTICAL. Solte fecho ativo e ferrolhos passivos; abra ativa antes da passiva. Fechos esquemáticos; rotação0–100° nos eixos aceitos.'),
 ('unlock','Unlock → PARK','Destravar → GUARDAR','LOCK','UPRIGHT, both rear doors open. Release L then R, lift80mm, transfer to parking sockets, lower44mm. Knob turning and flexible tether are schematic; rigid clearance route validated.','VERTICAL, portas abertas. Solte E e D, eleve80mm, transfira aos alojamentos, abaixe44mm. Giro e tirante flexível esquemáticos; trajeto rígido validado.'),
 ('fold','Backbox fold0–90°','Dobra do backbox0–90°','FOLD','Locks already released/parked; doors closed/latched; MAIN PLAYFIELD GLASS and MATRIX removed. Backbox glass/cassette retained. No routine electronics disconnection.','Travas soltas/guardadas; portas fechadas/travadas; VIDRO PRINCIPAL e MATRIZ removidos. Vidro do backbox/cassete mantidos. Sem desconexão elétrica de rotina.'),
 ('glass','Backbox glass removal','Remoção do vidro do backbox','GLASS','Support glass; release/remove top retainer (schematic), lift glass500mm. Monitor remains installed.','Sustente o vidro; solte/remova retentor superior (esquemático), eleve vidro500mm. Monitor permanece instalado.'),
 ('display','Front display removal','Retirada frontal do monitor','DISPLAY','Front glass, top retainer and bezel removed; release clamps and stop screws, support display/adapter; withdraw400mm toward front. Release operations schematic.','Vidro frontal, retentor e moldura removidos; solte fixações/batentes, sustente monitor/adaptador; retire400mm para frente. Liberação esquemática.'),
 ('cassette','DMD / speaker cassette removal','Remoção do cassete DMD / alto-falantes','CASSETTE','Support cassette, release its four attachments; withdraw240mm toward front. Rare service, NOT a normal fold prerequisite.','Sustente cassete, solte quatro fixações; retire240mm para frente. Serviço raro, NÃO exigido na dobra normal.'),
 ('fan','Fan replacement on open doors','Troca de ventoinha nas portas abertas','FAN','Both doors open100°; release fan screws and local accessory stack; withdraw each fan160mm normal to open door. Accessories schematic; fan-body corridor validated. Fan wiring is builder-configurable.','Portas abertas100°; solte parafusos e acessórios; retire cada ventoinha160mm normal à porta. Acessórios esquemáticos; trajeto do corpo validado. Fiação configurável.'),
 ('shelf','Shelf removal','Remoção de prateleira','SHELF','SCHEMATIC SERVICE — remove playfield for access, release top screws; shelf highlighted then faded. No continuous shelf removal path is validated by this task.','SERVIÇO ESQUEMÁTICO — remova playfield para acesso, solte parafusos superiores; destaque/transição da prateleira. Trajetória contínua não validada nesta tarefa.')]
for id,en,pt,mode,ne,np in services:clips.append({'id':'service-'+id,'type':'service','mode':mode,'title':{'en':en,'pt-BR':pt},'duration_s':12,'status':'SCHEMATIC_SERVICE_ANIMATION' if mode=='SHELF' else 'INHERITED_VALIDATED_RIGID_PATH_WITH_SCHEMATIC_RELEASE_DETAILS','note':{'en':ne,'pt-BR':np}})
for mode,en,pt in [('PACK','Flatpack packing','Embalagem do flatpack'),('UNPACK','Unpack / identify parts','Desembalar / identificar peças')]:clips.append({'id':mode.lower(),'type':'packing','mode':mode,'title':{'en':en,'pt-BR':pt},'duration_s':35,'status':'DOCUMENTATION_PACKING_SEQUENCE_NOT_TRANSIT_QUALIFICATION','note':{'en':'Layer-by-layer actual manufacturing pieces. IDs identify the current layer. Full rigid separators and edge padding required. Hardware box separate; no glass/electronics.','pt-BR':'Peças reais de fabricação por camada. IDs identificam a camada atual. Separadores rígidos inteiros e proteção nas bordas. Caixa de ferragens separada; sem vidro/eletrônica.'}})
# Matrix moving wood follows its saved historical route, not obsolete backbox axis.
f=motions['matrix']['carrier_front_xyz_mm'];a=math.radians(25)
motions['matrix_axis']=[300,f[1]+95.375*math.cos(a),f[2]+95.375*math.sin(a)]
reg=read('exports/generated/flatpack-v331/manufacturing-register.json')['parts']
payload={'metrics':read('exports/generated/assembly-v333/project-metrics.json'),'material':read('exports/generated/assembly-v333/material-utilization.json')['stocks'],'mass':read('exports/generated/assembly-v333/mass-budget.json'),
 'hardware':read('exports/generated/assembly-v333/hardware-dashboard.json'),'packaging':read('exports/generated/assembly-v333/packaging.json'),'validation':read('exports/generated/assembly-v333/assembly-validation.json'),
 'motions':motions,'clips':clips,'pieces':{p['instance_id']:{k:p[k] for k in ['local_to_installed_matrix','finished_xy_size_mm','finished_xy_bounds_mm','manufacturing_part_id']} for p in reg}}
(O/'animations.json').write_text(json.dumps({'clips':clips,'motion_authority':'motion-authority.json','manufacturing_release':False},indent=2,ensure_ascii=False)+'\n')
base=subprocess.check_output(['git','show',HEAD+':exports/generated/viewer-v32/index.html'],cwd=R,text=True)
ext=(R/'tools/viewer-v333/extension.js').read_text()
base=base.replace('</body>', '<script id="v333-data" type="application/json">'+json.dumps(payload,separators=(',',':'),ensure_ascii=False).replace('</','<\\/')+'</script><script>'+ext+'</script></body>')
base=base.replace('V33.2','V33.3')
(R/'exports/generated/viewer-v32/index.html').write_text(base)
# Versioned manual audit overlay and crosslinks preserve all original preparation cards.
manual['version']='V33.3';manual['assembly_screen']='../assembly-v333/assembly-validation.json';manual['status']='SCREENED_FRAMEWORK_PHYSICAL_ASSEMBLY_QUALIFICATION_HOLD'
for s in manual['stages']:
 for step in s['steps']:
  step['animation_id']='assembly-'+step['id'];step['validation']=next(v for v in payload['validation']['steps'] if v['id']==step['id'])
(O/'assembly-manual.json').write_text(json.dumps(manual,indent=2,ensure_ascii=False)+'\n')
for fn,pt in [('ASSEMBLY_MANUAL.md',False),('ASSEMBLY_MANUAL.pt-BR.md',True)]:
 old=subprocess.check_output(['git','show',HEAD+':docs/'+fn],cwd=R,text=True)
 intro=('V33.3: 19 etapas /31passos auditados geometricamente; montagem física e trajetórias contínuas novas NÃO validadas. Animações de montagem são esquemáticas. [Resultados por passo](../exports/generated/assembly-v333/assembly-validation.json). [Reproduzir montagem](../exports/generated/viewer-v32/index.html?animation=assembly-02.1&lang=pt-BR).' if pt else 'V33.3: 19 stages /31steps geometrically screened; physical assembly and new continuous insertion paths remain UNVALIDATED. Assembly clips are schematic. [Per-step evidence](../exports/generated/assembly-v333/assembly-validation.json). [Play assembly](../exports/generated/viewer-v32/index.html?animation=assembly-02.1).')
 for s in manual['stages']:
  for step in s['steps']:
   title=f"### {step['id']} — {step['title']['pt-BR' if pt else 'en']}"
   old=old.replace(title,title+'\n\n['+('Reproduzir animação esquemática' if pt else 'Play schematic assembly animation')+'](../exports/generated/viewer-v32/index.html?animation='+step['animation_id']+('&lang=pt-BR' if pt else '')+')')
 (R/'docs'/fn).write_text(intro+'\n\n'+old)
print('V333_VIEWER_PASS',len(clips),'clips',len(base),'bytes')
