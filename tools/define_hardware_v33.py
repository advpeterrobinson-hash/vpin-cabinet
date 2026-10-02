"""Canonical V33 inventory decisions, not geometry mutations. CERN-OHL-S-2.0.
IDs are permanent: append new IDs; never renumber or reuse retired IDs.
"""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1]
audit=json.loads((R/'library/hardware/current-object-audit.json').read_text()); objects={x['object']:x for x in audit['objects']}
A='REQUIRED_FLATPACK_HARDWARE';B='OPTIONAL_FLATPACK_HARDWARE';C='FUTURE_ELECTRONICS_HARDWARE';D='USER_ADAPTER_HARDWARE';E='REFERENCE_ONLY_NOT_FROZEN'
items=[]; assigned={};wood=[]
def add(id,en,pt,cl,stage,pattern='',qty=None,dims=None,kind='envelope',source='',note='',material='steel; finish/grade TBD',cnc=True,components=1,direction=None):
    names=[n for n in objects if pattern and re.fullmatch(pattern,n)]
    for n in names:
        assert n not in assigned,(n,id,assigned.get(n));assigned[n]=id
    if qty is None and names:qty=len(names)//components
    instances=[]
    for n in names:
        ob=objects[n]
        instances.append({'object':n,'coordinate_xyz_mm':ob['center_xyz_mm'],'coordinate_meaning':'CURRENT B-rep bounding-box center, not a drilling datum','installation_direction':direction,'direction_status':'DESIGN_REFERENCE' if direction else 'HARDWARE_DEPENDENT; not inferred from bounding box','source':ob['source'],'mirrored_pair':bool(re.search(r'[LR](?:\d|$)',n))})
    it={'id':id,'description_en':en,'description_pt_BR':pt,'flatpack_classification':cl,'assembly_stage':stage,'parent_assembly':stages[stage]['assembly'],'quantity':qty,'quantity_status':'CURRENT_OBJECT_COUNT' if names and qty is not None else 'ARCHITECTURE_COUNT' if qty is not None else 'UNRESOLVED_NOT_ZERO','unit':'piece','material':material,'nominal_dimensions':dims or {},'dimensional_authority':'PROVISIONAL_CURRENT_DESIGN' if names or dims else 'UNSPECIFIED','freeze_status':'PURCHASE_BEFORE_CNC' if cnc else 'OPTIONAL' if cl==B else 'PURCHASE_BEFORE_ASSEMBLY','design_status':'PROVISIONAL','measurement_required':True,'controls_permanent_cnc':cnc,'source':[source or 'CURRENT V32 B-reps / owner V33 inventory instruction'],'source_license':'CERN-OHL-S-2.0 original geometry; external links are citations only','supplier':None,'price_BRL':None,'notes':note,'instances':instances,'model':{'strategy':'CURRENT_BREP_ENVELOPE' if names else 'ORIGINAL_PARAMETRIC' if dims else 'UNRESOLVED_MARKER_NOT_FIT_GEOMETRY','kind':kind,'parameters':dims or {},'detailed_threads':False},'service_removable':True,'normal_assembly_removable':True,'tool_family':'hand' if kind in ['knob','dowel','gasket','mesh'] else 'hardware-dependent drive/socket; size not selected'}
    items.append(it);return it
stages={
 '01':{'assembly':'cabinet_shell','en':'Cabinet shell and legs','pt':'Caixa principal e pés','depends_on':[]},
 '02':{'assembly':'shelves_supports','en':'Shelf supports and crossmembers','pt':'Apoios, prateleiras e travessas','depends_on':['01']},
 '03':{'assembly':'playfield_pivot','en':'Wooden playfield pivot','pt':'Pivô de madeira do playfield','depends_on':['01','02']},
 '04':{'assembly':'main_rear_door','en':'Main rear service door','pt':'Porta traseira da caixa principal','depends_on':['01']},
 '05':{'assembly':'main_ventilation','en':'Main ventilation and filter interfaces','pt':'Ventilação e filtros da caixa principal','depends_on':['01']},
 '06':{'assembly':'backbox_shell_wpc','en':'Backbox shell and WPC interface','pt':'Caixa superior e interface WPC','depends_on':['01','03']},
 '07':{'assembly':'backbox_upright_locks','en':'Upright locks and parking','pt':'Travas verticais e alojamentos','depends_on':['06']},
 '08':{'assembly':'backbox_doors','en':'Twin backbox doors','pt':'Portas duplas da caixa superior','depends_on':['06']},
 '09':{'assembly':'backbox_ventilation','en':'Backbox blanks, filters and optional fans','pt':'Tampas, filtros e ventoinhas opcionais','depends_on':['08']},
 '10':{'assembly':'display_glass_interfaces','en':'Display carrier and glass retention','pt':'Suporte de monitor e retenção do vidro','depends_on':['06']},
 '11':{'assembly':'lower_cassette','en':'DMD/speaker cassette','pt':'Cassete DMD/alto-falantes','depends_on':['06','07']},
 '12':{'assembly':'matrix_front_interfaces','en':'Matrix and front interfaces','pt':'Matriz e interfaces frontais','depends_on':['01','03']},
 '13':{'assembly':'future_electronics','en':'Later electronics and adapters','pt':'Eletrônica e adaptadores futuros','depends_on':['02','03','10','11','12']}}
# F = fastener, W = washer, I = captive thread/nut, H = mechanism, B = fitting,
# G = gasket/glass/consumable, E = electronic reference. Purchasable assemblies
# own their CAD subcomponents; the same hinge/lock is never counted three times.
add('F01','Cradle support wood screw','Parafuso de madeira do apoio do pivô',A,'03',r'PF_SupportMountScrew[LR][123]',dims={'diameter_mm':4.5,'length_mm':30,'head_diameter_mm':9,'head':'countersunk'},kind='screw',source='config/wood_dowel_pivot_v32.json#fixing',note='6 unchanged coordinates. Torx candidate; exact bit/hardness and pilots await purchase.',direction=[1,0,0])
add('F02','Saddle-strap wood screw','Parafuso da abraçadeira do eixo de madeira',A,'03',r'PF_StrapScrew\d_[13]',dims={'diameter_mm':3.4,'length_mm':12,'head_diameter_mm':6.4,'head_height_mm':2,'head':'pan'},kind='screw',source='tools/wood_dowel_pivot_v32_entry.py: saddle strap loop',note='CURRENT cylinder is Ø3.4 ×12, not a selected standard screw. Candidate Ø3.5 ×12 requires strap/pilot/engagement check; NO substitution made.')
add('H01','Wooden pivot dowel','Cavilha/eixo de madeira do playfield',A,'03','PF_WoodDowel',dims={'diameter_mm':32,'length_mm':560},kind='dowel',material='straight sound hardwood; species/moisture TBD',source='config/wood_dowel_pivot_v32.json',direction=[1,0,0])
add('B01','Commercial saddle strap for Ø32 wooden dowel','Abraçadeira comercial para eixo de madeira Ø32',A,'03',r'PF_CommercialStrap\d',source='tools/wood_dowel_pivot_v32_entry.py',note='4 straps, 2 screws each. No bearing, metal shaft, custom journal or custom plate.')
add('F03','Shelf top-release M5 screw','Parafuso M5 de liberação superior da prateleira',A,'02',r'SimpleShelfBolt\d[LR]\d',dims={'diameter_mm':5,'length_mm':25,'head_diameter_mm':9,'head_height_mm':4,'head':'pan'},kind='screw',source='config/simple_shelves_v32.json',direction=[0,0,-1])
add('W01','M5 load-spreading washer, current Ø12 ×1','Arruela M5, reserva atual Ø12 ×1',A,'02',r'SimpleShelfBolt\d[LR]\dWasher',dims={'inner_diameter_mm':5.5,'outer_diameter_mm':12,'thickness_mm':1},kind='washer',cnc=False)
add('I01','M5 shelf captive insert','Inserto roscado M5 da prateleira',A,'02',r'SimpleShelfBolt\d[LR]\dInsert',dims={'thread':'M5','outer_diameter_mm':8,'length_mm':10},kind='insert',source='config/simple_shelves_v32.json',note='Bore Ø8.5 is an existing design candidate, not a generic M5-insert standard.')
add('F04','Fixed shelf-support wood screw','Parafuso de madeira do apoio fixo de prateleira',A,'02',r'CandidateFixedSupportScrew\d[LR]\d',dims={'diameter_mm':4,'length_mm':55,'head_diameter_mm':8,'head_height_mm':3,'head':'pan'},kind='screw',source='config/support_leg_machining_v32.json#anchor')
add('W02','Ø4 clearance washer, Ø9 ×1','Arruela para folga Ø4, Ø9 ×1',A,'02',r'CandidateFixedSupportScrew\d[LR]\dWasher',dims={'inner_diameter_mm':4.5,'outer_diameter_mm':9,'thickness_mm':1},kind='washer',cnc=False,note='Same nominal family as rear M4 fan washers; additional optional quantities listed separately.')
add('B02','Commodity support angle, 40 ×40 ×50 ×3 reserve','Cantoneira comercial de apoio, reserva 40 ×40 ×50 ×3',A,'02',r'CROSS_BRACKET_\d[LR]',source='exports/generated/cabinet-v32/build_v32.py',note='6 fittings. Rated commodity part and attachment pattern unselected; do not fabricate custom brackets from envelope.')
add('F05','Crossmember guide attachment screws','Parafusos das guias das travessas',A,'02',qty=24,source='exports/generated/cabinet-v32/build_v32.py: guide anchoring loop',note='4 existing anchor holes per guide ×6; shank/head/length and wall thread retention unresolved.')
add('F52','M5-family crossmember support-angle bolts','Parafusos M5 das cantoneiras das travessas',A,'02',qty=12,dims={'diameter_mm':5,'length_mm':None},kind='screw',source='exports/generated/cabinet-v32/build_v32.py: support-angle loop',note='2 installed bolts per angle ×6; three height choices are NOT6 bolts per angle.')
add('I14','Crossmember angle captive-thread/retention set','Conjunto de rosca cativa das cantoneiras',A,'02',qty=12,dims={'thread':'M5'},kind='insert',note='Guide12 mm remaining web; purchased thread/washer strategy unselected.')
add('F06','Cabinet shell/floor/cleat joint fasteners','Fixadores das juntas da caixa, fundo e sarrafos',A,'01',source='CURRENT SIDE/FRONT/REAR/FLOOR/FLOOR_CLEAT interfaces',note='Captured joinery exists; permanent mechanical reinforcement schedule is not specified. Quantity and family HOLD; not replaced by guessed dense screws.')
add('G01','Plywood joint adhesive','Adesivo para juntas de compensado',A,'01',kind='consumable',material='wood adhesive; specification/coverage TBD',cnc=False,note='At least lock parking laminations require glue; volume depends on final joint schedule. Not a structural screw substitute.')
add('F07','PCBase flush M5 floor anchors','Fixadores M5 escareados da PCBase ao fundo',A,'02',qty=4,dims={'diameter_mm':5,'length_mm':None,'head':'countersunk','clearance_mm':5.5},kind='screw',source='config/consolidated_audio_v32.json#pc_base',note='4 holes exist; bolt length/nut/washer stack not modeled. 36 mm combined boards. Future chassis mounting is separate.')
add('I02','PCBase M5 retaining nuts','Porcas M5 dos fixadores da PCBase',A,'02',qty=4,dims={'thread':'M5'},kind='nut',cnc=False,note='Captive or locking form and length stack pending; no chosen torque.')
add('W03','PCBase M5 underside backing washers','Arruelas inferiores M5 da PCBase',A,'02',qty=4,dims={'thread':'M5','outer_diameter_mm':None},kind='washer',cnc=False)
add('H02','Main rear door hinge assembly','Dobradiça da porta traseira principal',A,'04',r'CandidateHinge(?:Fixed|Moving|Pin)[12]',qty=2,components=3,source='config/rear_door_v32.json',note='Two short hinges, not the backbox piano-hinge family. Each consists of two leaves and one pin.')
add('H03','Main rear keyed cam-lock assembly','Fechadura de lingueta com chave da porta principal',A,'04',r'CandidateKeyLock(?:Body|Shaft|Cam)',qty=1,components=3,source='config/rear_door_v32.json')
add('B03','Main rear lock keeper','Contra-fecho da porta traseira principal',A,'04','CandidateLockKeeper',note='Ordinary flat strike; selection and fixing require measurement.')
add('H04','Main rear door handle','Puxador da porta traseira principal',A,'04','CandidateRearHandle',source='config/rear_hardware_v32.json#handle')
add('F08','M4 ×20 handle screw','Parafuso M4 ×20 do puxador',A,'04',r'CandidateHandleBolt[12]',dims={'diameter_mm':4,'length_mm':20,'head':'pan','head_diameter_mm':8,'head_height_mm':3},kind='screw')
add('W04','Handle washer','Arruela do puxador',A,'04',r'CandidateHandleBolt[12]Washer',kind='washer',cnc=False,note='Do not assume this historical shape matches W02 until measured; CAD dimensions remain in object audit.')
add('F09','Main rear hinge fixing screws','Parafusos das dobradiças traseiras principais',A,'04',qty=8,source='tools/rear_door_v32_entry.py: hinge leaf loop',note='2 holes per leaf ×2 leaves ×2 hinges; length/diameter and12 mm door engagement unselected.')
add('F53','Main rear keeper fixing screws','Parafusos do contra-fecho traseiro principal',A,'04',note='Keeper attachment count and stack unresolved.')
add('G02','Main rear door contact felt','Feltro de contato da porta traseira',B,'04',kind='gasket',material='adhesive furniture felt',cnc=False,note='Owner adds at actual contact; not a restraint. Quantity/size determined at assembly.')
add('H05','Optional main rear door limiter set','Conjunto limitador opcional da porta principal',B,'04',qty=1,cnc=False,note='Accessory only; no new mechanism designed.')
add('H06','Optional main rear slide bolt','Ferrolho opcional da porta principal',B,'04',qty=1,cnc=False)
add('F10','M4 ×55 main rear fan bolt','Parafuso M4 ×55 da ventoinha traseira principal',B,'05',r'CandidateFanBolt(?:230|370)_[1-4]',dims={'diameter_mm':4,'length_mm':55,'head':'pan','head_diameter_mm':8,'head_height_mm':3},kind='screw',source='config/fixed_rear_services_v32.json',cnc=False)
add('W05','M4 fan washer, Ø9 ×1','Arruela M4 da ventoinha, Ø9 ×1',B,'05',r'CandidateFanBolt(?:230|370)_[1-4](?:Outer|Inner)Washer',dims={'inner_diameter_mm':4.5,'outer_diameter_mm':9,'thickness_mm':1},kind='washer',cnc=False,note='Consolidated into canonical W02 during catalog normalization; ID retained as alias, not a second buy line.')
add('I03','M4 fan nut','Porca M4 da ventoinha',B,'05',r'(?:CandidateFanBolt(?:230|370)_[1-4]Nut|FloorFanNut[LR][1-4])',dims={'thread':'M4','outer_diameter_mm':8,'length_mm':3.2},kind='nut',cnc=False)
add('F11','M4 ×50 floor fan bolt','Parafuso M4 ×50 da ventoinha do fundo',B,'05',r'FloorFanBolt[LR][1-4]',dims={'diameter_mm':4,'length_mm':50,'head':'pan','head_diameter_mm':8,'head_height_mm':3},kind='screw',source='config/notch_floor_fans_v32.json',cnc=False)
add('F12','M4 ×16 floor-filter screw','Parafuso M4 ×16 do filtro do fundo',A,'05',r'FloorFilterScrew[LR][1-4]',dims={'diameter_mm':4,'length_mm':16,'head':'pan','head_diameter_mm':8,'head_height_mm':3},kind='screw')
add('I04','M4 blind floor-filter insert','Inserto cego M4 do filtro do fundo',A,'05',r'FloorFilterInsert[LR][1-4]',dims={'thread':'M4','outer_diameter_mm':6,'length_mm':8},kind='insert',source='config/notch_floor_fans_v32.json',note='10 mm remaining floor skin in nominal 18 mm stock; purchased insert must fit existing reserve.')
add('H07','120 mm main/floor optional fan','Ventoinha opcional 120 mm da caixa/fundo',B,'05',r'(?:FAN_(?:230|370)|FloorIntakeFan[LR])',dims={'width_mm':120,'height_mm':120,'depth_mm':25,'pitch_mm':105},material='fan assembly; no electrical interface selected',cnc=False,note='4 optional fans. Passive floor filtration remains possible; thermal qualification is separate.')
add('B04','120 mm main rear fan finger guard','Grade de proteção 120 mm da ventoinha traseira',B,'05',r'CandidateFanGuard(?:230|370)(?:Inner|Outer)',cnc=False,note='4 guards; purchased finger protection/free area not certified.')
add('B05','Floor intake lower guard','Grade inferior da entrada de ar do fundo',A,'05',r'FloorCommercialGuardReserve[LR]',cnc=True,note='Retained for passive intake protection even without fan. Current lower guard is a rotated packaging box, not a solid air-blocking plate.')
add('B06','Floor fan upper finger guard','Grade superior da ventoinha do fundo',B,'05',r'FloorUpperGuardReserve[LR]',cnc=False)
add('F13','Short floor lower-guard attachment screws','Parafusos curtos da grade inferior do filtro',A,'05',qty=8,source='config/notch_floor_fans_v32.json#fans.lower_guard_fixing',note='4 per guard on rotated105 mm pitch; diameter/head/length unselected; 8 mm frame prevents using long screws blindly.')
add('G03','Floor intake replaceable filter media','Mídia filtrante substituível do fundo',A,'05',r'FloorFilterMediaReserve[LR]',kind='mesh',material='serviceable mesh/filter; permeability TBD',cnc=False)
# WPC identity is mandatory. Installed axis is authoritative; no arm/drilling dimensions inferred.
for id,ref,side,qty in [('H08','01-9011-L','left',1),('H09','01-9011-R','right',1),('H10','02-4352','bushing',2),('F14','4322-01139-12B','pivot bolt',2)]:
    it=add(id,'WPC '+ref+' '+side,'WPC '+ref+' '+{'left':'esquerda','right':'direita','bushing':'bucha','pivot bolt':'parafuso do pivô'}[side],A,'06',qty=qty,source='config/wpc_kinematics_v32.json; studies/wpc-fold-v32/README.md',note='PHYSICAL MEASUREMENT HOLD. No metric substitution of a mating imperial thread. No CNC drilling released.')
    it['reference_part']=ref;it['measurement_fields']={k:None for k in (['arm_thickness_mm','bend_angles_deg','bend_offsets_mm','floor_holes_xyz_mm_3','floor_hole_diameters_mm_3','pivot_hole_diameter_mm'] if side in ['left','right'] else ['bushing_od_mm','bushing_id_mm','bushing_length_mm','flange_diameter_mm','flange_thickness_mm'] if side=='bushing' else ['shank_diameter_mm','thread_diameter_mm','thread_pitch_mm_or_tpi','thread_standard','square_neck_width_mm','square_neck_length_mm','head_diameter_mm','head_height_mm','under_head_length_mm','total_length_mm','washer_nut_stack_mm'])}
add('F15','WPC floor attachment fasteners','Fixadores WPC no piso da caixa superior',A,'06',qty=6,note='3 per arm; measured hole/thread/head/length and access needed. Rare cassette removal allowed for hinge maintenance only.')
add('W06','WPC pivot/floor washer and nut stack','Conjunto de arruelas e porcas WPC',A,'06',note='Unresolved content and count; do not add metric nuts to unknown WPC threads.')
add('F16','Backbox shell/frame/rail joint screws','Parafusos das juntas da caixa superior',A,'06',note='Shell, rear frame, hinge cleats, monitor rail cleats and cassette cleats require joint schedule. Counts/pilots not implied by envelopes.')
add('F54','Backbox side-to-floor joint screws','Parafusos da junta lateral/piso superior',A,'06',qty=6,dims={'diameter_mm_max_planning':4,'floor_thread_reach_mm':20},source='config/backbox_structure_review_v32.json#joint_planning',note='3 per side provisional planning; glued captured joint. Separate from remaining shell joints F16.')
add('B16','WPC floor backing plate','Chapa de apoio dos fixadores WPC no piso',A,'06',qty=2,source='studies/wpc-fold-v32/README.md',note='Documented backing relationship; purchased plate dimensions/holes/material unmeasured, not a custom fabricated design.')
add('H11','M8 ×40 captive upright-lock hand knob','Manípulo cativo M8 ×40 da trava vertical',A,'07',r'BB_UprightLock[LR]Knob',dims={'diameter_mm':8,'length_mm':40,'head_diameter_mm':40,'head_height_mm':26},kind='knob',source='config/backbox_lock_integration_v32.json',note='L130/R470,Y1260. Architecture family only; rotating loss-protection ring purchased with compatible shaft.',direction=[0,0,-1])
add('W07','Captive upright-lock load washer','Arruela cativa de carga da trava vertical',A,'07',r'BB_UprightLock[LR]Washer',dims={'inner_diameter_mm':9,'outer_diameter_mm':32,'thickness_mm':3},kind='washer',source='config/backbox_lock_integration_v32.json')
add('I05','M8 metal-backed shelf captive receiver','Receptor roscado metálico M8 da prateleira traseira',A,'07',r'UprightLock[LR]Shelf(?:Thread|Backing)',qty=2,components=2,dims={'thread':'M8','outer_diameter_mm':12,'length_mm':12,'backing_diameter_mm':32,'backing_thickness_mm':3},kind='insert',note='Backing is included in receiver assembly; do not buy separate duplicate backing. Anti-rotation/retention unresolved.')
add('I06','M8 metal parking insert','Inserto metálico M8 para guardar o manípulo',A,'07',r'BB_UprightLock[LR]ParkingThread',dims={'thread':'M8','outer_diameter_mm':12,'length_mm':12},kind='insert',note='X185/X415,Y1268; parking only, not structural backbox clamping.')
add('F17','Parking-pad countersunk wood screw','Parafuso escareado dos blocos de estacionamento',A,'07',r'BB_UprightLock[LR]ParkingScrewReserve[01]',dims={'diameter_mm':4,'length_mm':48,'head_diameter_mm':9,'head':'countersunk'},kind='screw',note='48 mm modeled envelope, not a chosen stock SKU; two screws per laminated block.')
add('H12','Mechanical knob tether, 200 mm','Cabo mecânico de retenção do manípulo, 200 mm',A,'07',r'BB_UprightLock[LR]Tether',dims={'length_mm':200},material='flexible loss-protection tether',cnc=False,note='Not electrical wiring. Installed shape includes stored corridor, not exact strand geometry.')
add('W08','Captive washer retention ring','Anel de retenção da arruela cativa',A,'07',qty=2,cnc=False,note='Compatible ordinary retaining hardware required; groove/stack not frozen. Loose washers not allowed.')
add('H13','Rotating loss-protection ring','Anel giratório de proteção contra perda',A,'07',qty=2,cnc=False,note='May be supplied with H11; included flag must suppress duplicate purchase.')
add('B07','Positive tether slack keeper','Presilha positiva da sobra do cabo de retenção',A,'07',qty=2,cnc=False,note='Reusable mechanical cord keeper. Fold requires slack secured around knob.')
add('B08','Parking-block tether anchor','Ancoragem do cabo no bloco de estacionamento',A,'07',qty=2,note='Ordinary eye/clamp with positive mounting; selected stack and screws unresolved.')
add('H14','628 mm continuous backbox door hinge','Dobradiça contínua de 628 mm da caixa superior',A,'08',r'BB_(?:PianoHingeReserve|PianoLeafFixed|PianoLeafDoor)[LR]',qty=2,components=3,source='config/backbox_service_v32.json#rear',note='628 mm envelope; leaf widths23/20,1.5 thick,knuckleØ5 provisional. Final hole pitch not frozen.')
add('H15','Backbox active-door keyed cam lock','Fechadura de lingueta da porta ativa superior',A,'08',r'BB_Cam(?:LockBodyReserve|LockBarrelReserve|TongueClosedReserve)',qty=1,components=3,note='One purchased mechanism incl tongue; does not substitute main rear door lock without fit review.')
add('H16','Backbox passive-leaf retaining bolt','Ferrolho da folha passiva superior',A,'08',r'BB_PassiveBolt(?:BodyReserve|ClosedReserve)[01]',qty=2,components=2,note='Upper and lower bolt. Purchased strike/attachment stack included but unmeasured.')
add('F18','Backbox piano-hinge fixing screws','Parafusos das dobradiças contínuas superiores',A,'08',note='Quantity from purchased hole pitch on both leaves of both hinges; maximum engagement limited by12 mm door.')
add('F19','Backbox latch/astragal fasteners','Fixadores dos ferrolhos e sobreposição central',A,'08',note='Count/length pending hardware and joint schedule; no permanent center mullion.')
add('G04','Backbox perimeter door gasket','Vedação perimetral das portas superiores',A,'08',r'BB_DoorPerimeterGasket[LR]',kind='gasket',material='replaceable closed-cell foam / EPDM',cnc=False,note='2 cut sets; supply length includes waste only after supplier selection. 2 mm compressed reserve.')
add('G05','Backbox center meeting-line gasket','Vedação central das portas superiores',A,'08','BB_CenterGasket',kind='gasket',material='replaceable closed-cell foam / EPDM',cnc=False)
add('H17','Optional 120 mm backbox door fan','Ventoinha opcional 120 mm da porta superior',B,'09',r'BB_Fan[LR]',dims={'width_mm':120,'height_mm':120,'depth_mm':25,'pitch_mm':105},cnc=False,material='fan assembly',note='Fan state replaces blank; no manufacturer/connector required.')
add('B09','Backbox fan finger guard','Grade da ventoinha superior',B,'09',r'BB_FanGuard[LR]',cnc=False)
add('G06','Backbox fan dust mesh/filter','Tela/filtro da ventoinha superior',B,'09',r'BB_FanMeshReserve[LR]',kind='mesh',material='mesh/filter',cnc=False,note='Exhaust pressure loss unresolved; no zero-restriction assumption.')
add('G07','Backbox low-intake filter/mesh','Filtro/tela da entrada inferior superior',A,'09',r'BB_IntakeMeshReserve[LR]',kind='mesh',material='serviceable insect mesh/filter',cnc=False)
add('F20','M4 backbox fan-station bolt, length pending','Parafuso M4 da ventoinha superior, comprimento pendente',B,'09',qty=8,dims={'diameter_mm':4,'length_mm':None,'head':'pan'},kind='screw',cnc=False,note='12 mm door +25 mm fan +accessories; do not copy main55 mm bolt automatically.')
add('F21','M4 backbox blank-station fixing','Fixador M4 da tampa cega superior',A,'09',qty=8,dims={'diameter_mm':4,'length_mm':None,'head':'pan'},kind='screw',note='4 per existing blank; same105 mm pitch as fan. Basic kit includes blanks; fan bolts replace these, not additive at same station.')
add('I07','M4 station captive nut/insert','Porca/inserto cativo M4 da estação superior',A,'09',qty=8,dims={'thread':'M4'},kind='insert',note='Captive form must preserve interchangeable fan/blank and12 mm leaf. No insert bore invented.')
add('F22','Backbox intake frame/baffle/filter fixings','Fixadores do quadro, defletor e filtro superior',A,'09',note='2 serviceable intakes; count/length and mesh clamping not defined by current assembly.')
add('B10','Flexible fan-cable clamp/strain relief','Abraçadeira/alívio de tração do cabo flexível',B,'09',r'BB_FanStrainReliefReserve[LR]',qty=4,note='Two fixed and two door attachment points; only two door reserves modeled. Connector choice remains builder-defined.')
add('F23','Fan-loop clamp screws','Parafusos das abraçadeiras dos cabos',B,'09',note='Clamp SKU controls number and screw length; electrical connectors excluded.')
add('B11','Optional downward fan dust hood','Capa opcional de ventilação voltada para baixo',B,'09',qty=2,dims={'width_mm':140,'depth_mm':19,'height_mm':140},cnc=False,note='Owner-accepted accessory reserve in service source; not installed CURRENT geometry.')
add('F55','Optional dust-hood service screws','Parafusos de serviço da capa antipoeira',B,'09',qty=4,cnc=False,note='Two per optional hood in service concept; hole and screw geometry remain unselected.')
add('F24','Backglass top-retainer M6-family fastener','Fixador M6 da barra superior do vidro',A,'10',r'BB_GlassRetainerFastenerReserve[01]',dims={'diameter_mm':6,'length_mm':30,'head':'unselected'},kind='screw',note='Ø6×30 reserve only, head/captive thread not selected. No unretained glass during fold.')
add('I08','Top-retainer captive metal thread','Rosca metálica cativa da barra superior',A,'10',qty=2,dims={'thread':'M6'},kind='insert',note='Repeated removal; purchased retention/stock engagement unresolved.')
add('G08','Backglass side U-liners','Perfis U de revestimento lateral do vidro superior',A,'10',r'BB_GlassLiner[LR]',kind='gasket',material='felt/EPDM/U liner',cnc=False)
add('G09','Backglass lower and top pads','Apoios macios inferior e superior do vidro',A,'10',r'BB_Glass(?:Lower|Top)Pad',kind='gasket',material='felt/EPDM',cnc=False)
add('G10','User-supplied backbox tempered glass','Vidro temperado superior fornecido pelo usuário',D,'10','BB_Backglass',material='tempered glass',kind='glass',note='752×465×4 current reserve; supplier confirms3–4 mm, edges and channel/liner fit before order.')
add('F25','Monitor depth-position M6 through bolt','Parafuso passante M6 de profundidade do monitor',A,'10',r'BB_MonitorDepthBoltReserve\d\d',dims={'diameter_mm':6,'length_mm':72,'head':'unselected'},kind='screw',note='72 mm is corridor/shank envelope, not stock SKU length. Rail/shoe retention independent of display.')
add('F26','Monitor alignment M6 clamp bolt','Parafuso M6 de alinhamento do monitor',A,'10',r'BB_MonitorClampReserve\d+',dims={'diameter_mm':6,'length_mm':None,'head':'unselected'},kind='screw',note='4 clamps; existing Ø18×36 objects are washer/tool stack reserves, NOT Ø18 bolts.')
add('W09','Monitor M6 large clamping washer','Arruela larga M6 do suporte de monitor',A,'10',qty=16,dims={'thread':'M6','outer_diameter_mm':18,'thickness_mm':None},kind='washer',cnc=False,note='Planning2 per8 through clamps/depth bolts; final bolt head may integrate washer. Not a selected DIN dimension.')
add('I09','Monitor M6 positive-retention nuts','Porcas M6 de retenção do monitor',A,'10',qty=8,dims={'thread':'M6'},kind='nut',cnc=False)
add('F27','Monitor M6 adjustable lower stop','Parafuso M6 do batente inferior regulável',A,'10',r'BB_MonitorStopScrewReserve[01]',dims={'diameter_mm':6,'length_mm':46,'head':'unselected'},kind='screw',note='46 mm reference cylinder, not final screw length; positive stop with locknut.')
add('I10','M6 stop captive thread','Rosca cativa M6 do batente',A,'10',qty=2,dims={'thread':'M6'},kind='insert')
add('I11','M6 stop locknut','Contraporca M6 do batente',A,'10',qty=2,dims={'thread':'M6'},kind='nut',cnc=False)
add('F28','Monitor ladder/stop/cleat wood joints','Fixadores de madeira da estrutura do monitor',A,'10',note='Carrier shoes, stop blocks, contact pads and fixed rail cleats need attachment schedule; quantity unresolved.')
add('F29','Display VESA mounting screws and spacers','Parafusos e espaçadores VESA do monitor',D,'13',note='Exact display thread, insertion depth and count from selected monitor; not automatically M6.',cnc=False)
add('F30','Lower cassette M4 positive attachment','Fixador positivo M4 do cassete inferior',A,'11',r'BB_CassetteBoltReserve[LR][01]',dims={'diameter_mm':4,'length_mm':65,'head':'unselected'},kind='screw',note='4 attachments,65 mm reference envelope; selected bolt/washer/thread stack must fit. No cassette geometry change.')
add('I12','Cassette M4 captive receiver','Receptor cativo M4 do cassete',A,'11',qty=4,dims={'thread':'M4'},kind='insert')
add('W10','Cassette M4 load washer','Arruela M4 do cassete',A,'11',qty=4,dims={'thread':'M4'},kind='washer',cnc=False)
add('F31','Replaceable baffle/bezel and DMD-adapter fixings','Fixadores dos defletores, molduras e adaptador DMD',A,'11',note='Retention of blank modules required even without electronics. Counts/lengths unresolved; cannot assume four cassette bolts also secure inserts.')
add('F32','Selected speaker mounting screws','Parafusos dos alto-falantes escolhidos',D,'13',cnc=False,note='Speaker-specific holes only in replaceable baffles.')
add('F33','Selected DMD mounting hardware','Fixadores do DMD escolhido',D,'13',cnc=False,note='VESA/non-VESA adapters; no permanent model-specific pattern.')
add('F34','M4 ×20 matrix thumb screw','Parafuso manual M4 ×20 da matriz',A,'12',r'MX_Retainer[LR]',dims={'diameter_mm':4,'length_mm':20,'head_diameter_mm':12,'head_height_mm':4},kind='knob',source='config/matrix_cassette_v32.json')
add('I13','M4 matrix support insert','Inserto M4 do suporte da matriz',A,'12',r'MX_Insert[LR]',kind='insert',source='tools/matrix_cassette_v32_entry.py')
add('F35','4 ×50 countersunk matrix-support screw','Parafuso escareado4 ×50 do suporte da matriz',A,'12',r'MX_FixedScrew[LR][12]',dims={'diameter_mm':4,'length_mm':50,'head':'countersunk','head_diameter_mm':8},kind='screw',source='config/matrix_cassette_v32.json')
add('B12','Playfield glass side channel','Canaleta lateral do vidro do playfield',A,'12',r'CandidateGlassChannel[LR]',material='replaceable channel; material/SKU TBD',note='Separate from backglass liners; do not infer stock channel from envelope.')
add('G11','User-supplied playfield glass','Vidro do playfield fornecido pelo usuário',D,'12','CandidateGlass',kind='glass',material='tempered glass',source='config/panel_closure_v32.json#glass_study',note='575×1100×5 study, not glass order; front/rear capture remains lockdown-dependent.')
add('G12','Playfield glass channel liner/seal','Revestimento/vedação da canaleta do playfield',A,'12',qty=2,kind='gasket',cnc=False,material='replaceable soft liner',note='2 side runs; lengths and front/rear pads from selected channel/bar.')
add('F36','Playfield channel/lockdown fixing hardware','Fixadores da canaleta e receiver da lockdown',A,'12',note='Permanent holes depend on channel and actual receiver; count unresolved.')
add('H18','Real pinball leg','Pé de pinball real',A,'01',qty=4,source='config/panel_closure_v32.json#legs',note='Reference A-19514,28.5 in; actual revision required. Not modeled as fabricated wood/steel substitute.')
add('B13','Metal threaded leg backing plate','Placa roscada metálica interna do pé',A,'01',r'CandidateLegPlate(?:FL|FR|RL|RR)',note='4 existing envelopes; measured matched bolts mandatory.58 mm candidate differs from57.15 mm WPC reference; HOLD.')
add('F37','Matched pinball leg bolts','Parafusos compatíveis com os pés de pinball',A,'01',qty=8,note='Thread, shoulder, length and head unselected. No M10 substitution into imperial backing thread.')
add('H19','Leg leveler and jam-nut assembly','Nivelador do pé com contraporca',A,'01',qty=4,note='Purchased matched thread; height/foot load unqualified.')
add('F38','Leg backing plate retention screws','Parafusos de retenção das placas dos pés',A,'01',note='Quantity/pitch supplied by purchased backing; not primary leg bolts.')
add('H20','600 mm body lockdown bar','Barra lockdown para caixa de600 mm',A,'12',qty=1,source='config/panel_closure_v32.json#lockdown',note='Existing accepted custom-width outsourced bar strategy. V33 adds no custom metal; no fabrication drawing generated.')
add('H21','WPC-compatible lockdown receiver','Receiver compatível WPC da lockdown',A,'12',qty=1,source='config/panel_closure_v32.json#lockdown',note='A-16673-1 / A-9174-4 references, not two purchases. Pattern/lever service/width to measure.')
add('H22','Front coin-door/frame/keyed access assembly','Conjunto de porta frontal, moldura e fechadura',A,'12',r'CoinStudy_(?:CoinFrame|DoorLeaf|DoorLock|ReturnButton[12])',qty=1,note='Closure/interface required; coin mechanisms/electrics optional. Front reserve is a study, not selected purchased door.')
add('F39','Front-door frame fixing set','Conjunto de fixação da moldura frontal',A,'12',note='Count/thread from selected front door; no historical mounting count assumed.')
add('H23','Coin mechanism/tray mounting set','Conjunto de mecanismos e bandeja de moedas',B,'12',r'CoinStudy_(?:Mechanism[12]|MechanismMount[12]_[12]|CoinTray|TraySupport[12])',qty=1,cnc=False,note='Optional1 set of2 mechanisms/tray/supports; no duplicate part purchase for CAD components.')
add('H24','Optional pinball button mechanical set','Conjunto mecânico opcional de botões de pinball',B,'12',r'(?:Leaf(?:Button|Nut|Bracket)_(?:primary|secondary)_[LR]|CandidateFrontButton[1-4])',qty=8,note='4 side +4 front bodies, side nuts/brackets included. Hole shapes remain existing references; builder may choose later buttons.')
add('F40','Button bracket mounting fasteners','Fixadores dos suportes de botões',B,'12',note='4 side brackets, exact number of screws unselected.')
add('H26','Optional mobility skate set','Conjunto opcional de patins externos de transporte',B,'01',qty=1,cnc=False,note='External removable PinSkates-style only; no integrated wheels.')
# Future electronics are explicitly excluded from mandatory flatpack.
for id,en,pt,pattern,qty in [
 ('E01','Playfield display','Monitor do playfield','PLAYFIELD_ENVELOPE',None),('E02','Backglass display','Monitor superior','BB_Display32',None),('E03','DMD display','Tela DMD','BB_DMDEnvelope',None),('E04','Backbox speakers','Alto-falantes superiores',r'BB_SpeakerEnvelope[LR]',None),('E05','PC open chassis and computer','Gabinete aberto e computador','PC_ENVELOPE',None),('E06','SSF exciter','Excitador SSF',r'SSF_Exciter[12][LR]',None),('E07','Bass shaker','Transdutor de graves','SSF_BST1_Reference',None),('E08','Subwoofer','Subwoofer','SSF_Subwoofer_DCS165_Reference',None),('E09','Amplifier','Amplificador','SSF_AmplifierReserve',None),('E10','Protected power supply','Fonte protegida','SSF_PSUReserve',None),('E11','USB sound interface','Interface de áudio USB','SSF_USBReserve',None),('E12','Matrix LED panel','Painel LED da matriz',r'MatrixPanel[1-6]',None),('E13','Button switches/contacts','Contatos/interruptores dos botões',r'(?:LeafContacts_(?:primary|secondary)_[LR]|CoinStudy_LightSwitch[12])',None),('E14','Optional toys/controllers/LED/relays','Brinquedos, controladores, LEDs e relés opcionais','',None)]:
    add(id,en,pt,C,'13',pattern,qty=qty,cnc=False,material='electronic reference; model selected later',note='Not in mandatory flatpack; dimensions from CURRENT occupied envelope only.')
add('B14','Protected mains inlet enclosure reference','Reserva de invólucro protegido da entrada de rede',C,'13','CandidateMainsEnclosure',material='insulating/protective enclosure',note='Safety-critical electrical interface, not general low-voltage hardware. No exposed terminals; no wiring design in V33.')
for id,en,pt,qty in [('F42','Subwoofer floor mounting bolts','Parafusos do subwoofer ao fundo',8),('F43','Bass-shaker carrier floor anchors','Fixadores da base do transdutor ao fundo',4),('F44','Bass-shaker to carrier fasteners','Fixadores do transdutor à base',None),('F45','Exciter IMS mounting fasteners','Fixadores IMS dos excitadores',None),('F46','PC chassis/base and component restraints','Fixadores do PC e retenção dos componentes',None),('F47','Electronics board shelf standoffs and screws','Espaçadores e parafusos de placas eletrônicas',None),('F48','Matrix panel mounting fasteners','Fixadores dos painéis da matriz',None),('F49','Toy mounting board fasteners','Fixadores de placas de brinquedos',None),('F50','Mains/network flange and enclosure fasteners','Fixadores das flanges e invólucros de rede/energia',None)]:
    add(id,en,pt,D,'13',qty=qty,cnc=(id in ['F42','F43','F45','F50']),note='Selected equipment controls thread/length/retention. Existing holes/reserves remain provisional; not included in basic flatpack.')
add('B15','Playfield replaceable VESA attachment','Fixação VESA substituível do playfield',D,'13','PF_VESAEnvelope',material='adapter interface; exact construction TBD',note='CURRENT envelope is not a CNC wood part or selected bracket; no metal pivot introduced.')
add('F51','Playfield display-to-adapter fasteners','Fixadores do monitor ao adaptador do playfield',D,'13',cnc=False,note='Supplier-defined VESA screw depth/count; independent of eight saddle screws.')
add('H25','Optional removable toy shelf','Prateleira removível opcional de brinquedos',B,'13',qty=1,material='plywood accessory; not in current installed CAD',cnc=False,note='Study only; no mandatory toy shelf. No unvalidated production cut part generated.')
# Unoccupied geometric corridors: inventory coverage but never a buy quantity.
for id,en,pt,pattern in [
 ('R01','Cable / connector routing reserves','Reservas de passagem de cabos/conectores',r'(?:MX_(?:FixedConnector|MovingConnector|CableLoop|FixedCable)Reserve|FloorFanConnectorReserve[LR]|BB_FlexCorridor[LR])'),
 ('R02','Button service approach reserves','Reservas de acesso de serviço dos botões',r'Button(?:Wire|Tool|Body|Leaf)ServiceReserve_(?:primary|secondary)_[LR]'),
 ('R03','Future toy mounting volumes','Volumes livres para brinquedos',r'BB_ToyZone(?:Upper|Lower)[LR]'),
 ('R04','Unpopulated equipment/payload/plunger reserves','Reservas de equipamentos, carga e plunger',r'(?:SHELF_1_CandidatePayload|PLUNGER_RESERVED)')]:
    it=add(id,en,pt,E,'13',pattern,qty=0,cnc=False,material='nonphysical clearance',note='NOT A PURCHASE. CAD solids are clearance envelopes; retain in exploded metadata as hidden guides.');it['quantity_status']='NOT_PHYSICAL';it['service_removable']=False
# Every actual wood object receives a material class. Keep load-bearing adapters
# premium even though replaceable; secondary is never selected by price alone.
wood_rules=[
 (r'SIDE_[LR]','Cabinet side','Lateral da caixa','01',18,True),
 (r'FRONT|REAR','Cabinet end structure','Estrutura frontal/traseira','01',18,True),
 (r'FLOOR','Structural floor','Fundo estrutural','01',18,True),
 (r'FLOOR_CLEAT_\d+','Floor cleat','Sarrafo do fundo','01',18,True),
 (r'REAR_DOOR','Main rear door','Porta traseira principal','04',12,False),
 (r'SHELF_[123]','Removable equipment shelf','Prateleira removível de equipamentos','02',12,False),
 (r'SHELF_SUPPORT_\d[LR]','Fixed shelf support','Apoio fixo da prateleira','02',18,True),
 (r'CROSS_[123]','Removable crossmember','Travessa removível','02',18,True),
 (r'CROSS_GUIDE_\d[LR]','Crossmember guide','Guia da travessa','02',18,True),
 (r'PC_BASE','Floor-supported PCBase','PCBase apoiada no fundo','02',18,False),
 (r'BACKBOX_BASE','Rear bearing shelf','Prateleira traseira de apoio','06',18,True),
 (r'CandidateLegBlock(?:FL|FR|RL|RR)','Laminated leg block','Bloco laminado do pé','01',18,True),
 (r'SSF_BST_Carrier','Replaceable shaker carrier','Base substituível do transdutor','13',12,True),
 (r'PF_BasePlywood','Playfield load-carrying base','Base estrutural do playfield','03',18,True),
 (r'PF_OpenCradle[LR]','Floor-bearing open cradle','Apoio aberto apoiado no fundo','03',18,True),
 (r'RemovableIntakeFilter[LR]','Floor filter holder','Suporte do filtro do fundo','05',8,False),
 (r'MX_WoodSeat[LR]','Matrix seat','Apoio da matriz','12',18,True),
 (r'MatrixCarrier','Removable matrix carrier','Suporte removível da matriz','12',12,False),
 (r'BB_(?:Side[LR]|Floor|Top|RearFrame|TopFrontRail)','Backbox shell/frame','Estrutura da caixa superior','06',18,True),
 (r'BB_GlassLowerRail','Padded lower glass rail','Apoio inferior do vidro','10',18,True),
 (r'BB_GlassTopRetainer','Positive glass top retainer','Retentor superior positivo do vidro','10',12,True),
 (r'BB_Monitor(?:Rail[01]|RailCleat[LR][01]|Carrier[01]|DepthShoe[01][01])','Monitor structural carrier member','Elemento estrutural do suporte de monitor','10',18,True),
 (r'BB_ReplaceableVESAPlate','Replaceable load-carrying VESA plate','Placa VESA substituível estrutural','10',12,True),
 (r'BB_DisplayReplaceableBezel','Replaceable display bezel','Moldura substituível do monitor','10',6,False),
 (r'BB_MonitorStopBlock[01]','Monitor stop block','Bloco de batente do monitor','10',None,True),
 (r'BB_MonitorStopContact[01]','Monitor stop contact pad','Calço de contato do batente','10',4,True),
 (r'BB_LowerCassetteFrame','Lower cassette frame','Quadro do cassete inferior','11',18,True),
 (r'BB_SpeakerBaffle[LR]','Replaceable speaker baffle','Defletor substituível do alto-falante','11',12,False),
 (r'BB_DMDReplaceableBezel','Replaceable DMD bezel','Moldura substituível do DMD','11',12,False),
 (r'BB_DMDRearAdapter','Load-carrying DMD rear adapter','Adaptador traseiro estrutural do DMD','11',12,True),
 (r'BB_DMDDepthTie[01]','DMD depth tie','Travessa de profundidade do DMD','11',18,True),
 (r'BB_CassetteFixedCleat[LR][01]','Cassette fixed cleat','Apoio fixo do cassete','11',None,True),
 (r'BB_Door[LR]','Backbox rear door','Porta traseira superior','08',12,False),
 (r'BB_IntakeFilterFrame[LR]','Backbox intake filter frame','Quadro do filtro superior','09',6,False),
 (r'BB_IntakeDownBaffle[LR]','Downward intake baffle assembly','Conjunto defletor inferior de ar','09',6,False),
 (r'BB_HingeCleat[LR]','Continuous-hinge fixed cleat','Apoio fixo da dobradiça contínua','08',None,True),
 (r'BB_CenterAstragal','Center overlap strip','Régua de sobreposição central','08',12,False),
 (r'BB_UprightLock[LR]ParkingPad[01]','Lock parking lamination','Lâmina do bloco de estacionamento','07',18,True),
 (r'BB_FanBlank[LR]','Interchangeable fan blank','Tampa cega intercambiável da ventoinha','09',6,False)]
wi=0
for pat,en,pt,stage,thick,premium in wood_rules:
    for n,ob in objects.items():
        if re.fullmatch(pat,n):
            assert n not in assigned,n;wi+=1;id=f'P{wi:03}';assigned[n]=id
            lam=n.startswith('CandidateLegBlock');compound=n.startswith(('BB_IntakeDownBaffle','BB_GlassTopRetainer','BB_MonitorStopBlock','BB_CassetteFixedCleat','BB_HingeCleat'))
            cl=D if n=='SSF_BST_Carrier' else A
            wood.append({'id':id,'object':n,'description_en':en+' — '+n,'description_pt_BR':pt+' — '+n,'quantity':7 if lam else 1,'unit':'lamination' if lam else 'CAD component','material':'plywood','material_class':'STRUCTURAL_PREMIUM' if premium else 'MODULAR_SECONDARY','nominal_thickness_mm':thick,'nominal_dimensions':{'world_bounds_mm':ob['bounds_mm'],'world_size_mm':ob['size_world_mm'],'note':'Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction.'},'source':[ob['source'],n],'status':'CNC_COMPONENT_BREAKDOWN_HOLD' if compound else 'DESIGN_GEOMETRY_ONLY','measurement_required':True,'flatpack_classification':cl,'assembly_stage':stage,'parent_assembly':stages[stage]['assembly'],'notes':('Seven18 mm laminations per block;45-degree bores change each layer; do not nest7 identical outlines blindly.' if lam else 'Fused/stepped assembly needs explicit flatpack decomposition or CNC thickness plan; no new wood designed.' if compound else 'Secondary substitution only after nesting trigger and quality/load/joint qualification.' if not premium else 'Load path or positive retention: premium class cannot be automatically downgraded.'),'price_BRL':None,'installed_coordinate_xyz_mm':ob['center_xyz_mm'],'installation_direction':None,'service_removable':bool(not premium or n.startswith(('CROSS_','PF_','BB_GlassTop','BB_MonitorCarrier'))),'normal_assembly_removable':None})
unmapped=sorted(set(objects)-set(assigned));assert not unmapped,unmapped
# Deduplicate identical explicit washer dimensions while preserving usage roles.
alias=next(x for x in items if x['id']=='W05');canon=next(x for x in items if x['id']=='W02')
canon['additional_usages']=[{'flatpack_classification':B,'assembly_stage':'05','quantity':alias['quantity'],'instances':alias['instances'],'note':'Rear fan stack only; not mandatory when fans omitted.'}]
canon['additional_usages'] += [
 {'flatpack_classification':B,'assembly_stage':'05','quantity':16,'instances':[],'note':'Floor fan washer requirement in config, omitted from current CAD;2 per bolt. Stack fit HOLD.'},
 {'flatpack_classification':A,'assembly_stage':'09','quantity':16,'instances':[],'note':'Planning2 per backbox station for fan OR blank, counted once; bought with basic blank station. Washer stack HOLD.'}]
for x in alias['instances']:assigned[x['object']]='W02'
items.remove(alias)
handle_alias=next(x for x in items if x['id']=='W04')
canon['additional_usages'].append({'flatpack_classification':A,'assembly_stage':'04','quantity':2,'instances':handle_alias['instances'],'note':'Main rear handle washers have exact same CURRENT B-rep radii4.5/2.25 and1 mm thickness as W02.'})
for x in handle_alias['instances']:assigned[x['object']]='W02'
items.remove(handle_alias)
# Assign paths by kind, not manufacturer, and retain coordinate metadata separately.
for it in items:
    id=it['id'];kind=it['model']['kind'];stage=it['assembly_stage']
    folder='pinball/wpc-hinges' if id in ['H08','H09','H10','F14','F15','W06'] else 'pinball/legs' if id in ['H18','H19','B13','F37','F38'] else 'pinball/lockdown' if id in ['H20','H21','F36'] else 'standard/washers' if kind=='washer' else 'standard/inserts' if kind=='insert' else 'standard/nuts' if kind=='nut' else 'standard/screws' if kind=='screw' else 'doors/hinges' if id in ['H02','H14'] else 'doors/locks' if id in ['H03','H15','H16','H11'] else 'fans' if stage in ['05','09'] else 'provisional'
    it['model']['path']='library/hardware/'+folder+'/'+id+'.FCStd'
    it['installed_coordinate_status']='CURRENT_BREP_CENTERS' if it['instances'] else 'UNMODELED_INTERFACE; coordinates must be qualified before installation/CNC'
    it['measurement_fields']=it.get('measurement_fields',{'actual_dimensions_mm':None,'selected_manufacturer_part':None,'thread_standard_and_pitch':None,'drive_and_size':None,'mount_pattern_and_count':None,'installed_stack_and_engagement_mm':None,'material_grade':None,'physical_fit_approved':False})
    if id in ['H07','H17','F10','F11','F20','G08','G09']:
        it['controls_permanent_cnc']=True;it['freeze_status']='PURCHASE_BEFORE_CNC'
        it['notes']+=' Selected component must qualify the existing station/channel before CNC; optional classification does not waive the hold if fitted.'
    if id=='G01':it['unit']='ml; coverage unresolved'
    if id=='H01':it['material_class']='STRUCTURAL_PREMIUM'
    if id in ['H05','H23','H26']:it['unit']='set'
    if id in ['G04','G08','G09','G12']:it['unit']='cut set'
    if id in ['G01'] or id.startswith('R'):
        it['service_removable']=False;it['normal_assembly_removable']=False
    if id in ['H08','H09','H10','F14']:
        it['kinematic_axis_reference']={'y_mm':1066.8,'z_mm':508,'direction':[1,0,0],'not_drilling_authority':True}
    # Preserve handed directions; vectors describe approach, not object extrusion.
    for ins in it['instances']:
        n=ins['object'];v=None
        if id in ['F01','F04']:v=[-1,0,0] if re.search(r'L\d',n) else [1,0,0]
        elif id=='F02':
            import math
            angle=json.loads((R/'exports/generated/backbox-lock-integration-v32/mesh.json').read_text())['review']['closed_slope_deg'];v=[0,-math.sin(math.radians(angle)),math.cos(math.radians(angle))]
        elif id in ['F03','H11','F17','F24','F25','F27']:v=[0,0,-1]
        elif id in ['F10','F08','F30','F26']:v=[0,-1,0]
        elif id=='F12':v=[0,0,1]
        if v:ins['installation_direction']=v;ins['direction_status']='CURRENT_DESIGN_APPROACH; hardware physical check required'
catalog={'version':'V33','source_head':audit['source_head'],'authority':'CURRENT V32 unchanged; V33 inventory/library only','id_policy':'IDs permanent; never renumber/reuse. P wood; F fastener; W washer; I captive thread/nut; H mechanism; B fitting; G consumable/glass; E electronics; R nonphysical reference. Assemblies are counted once.','aliases':{'W05':'W02','W04':'W02'},'classification_codes':{'A':A,'B':B,'C':C,'D':D,'E':E},'units':'mm unless explicitly noted','manufacturing_ready':False,'hardware':items,'assembly_stages':stages,'object_to_id':assigned,'consolidation':{'actual_changes':[{'from':['W02','W04','W05'],'to':'W02','basis':'Identical measured CURRENT B-rep radii4.5/2.25,1 mm thickness for support/handle/rear fan washers; mandatory and optional quantities remain separate.'}],'geometry_changes':0,'opportunities':[{'families':['F02'],'proposal':'Ø3.4 envelope to commodity3.5×12 wood screw','status':'HOLD strap holes, head and pilot check'},{'families':['F10','F11','F20'],'proposal':'Common M4 diameter/head/washer/nut; preserve stack-specific length IDs','status':'Diameter architecture already M4; no length consolidation yet'},{'families':['F17','F35'],'proposal':'48 mm reserve versus4×50 stock wood screw','status':'HOLD tip penetration, head and pilot; no automatic substitution'},{'families':['I04','I13'],'proposal':'One M4 OD6×8 blind-insert family','status':'Same nominal envelope but floor bore6 / matrix6.1 differ; qualification at both hosts before purchase consolidation'},{'families':['I03','I07','I12'],'proposal':'Common M4 thread where suitable','status':'HOLD different host stock and captive form; do not equate insert OD'},{'families':['W01','W03'],'proposal':'Common M5 washer','status':'HOLD floor backing load area'},{'families':['F24','F25','F26','F27'],'proposal':'M6 drive family','status':'HOLD heads, lengths and captive stacks differ'},{'families':['H11','I05','I06'],'proposal':'M8 metric upright/parking architecture','status':'Retained; no replacement of WPC imperial threads'}]},'negative_controls':['A clearance cylinder is not a purchased screw or released drill','No automatic metric substitution on WPC or leg threads','Unknown count is null, never zero','CAD subcomponents of one purchased assembly do not multiply BOM count','Current viewer/wood/holes cannot change','No bearings, metal playfield axle, legacy props or PC slides in required BOM']}
(R/'config/hardware_catalog_v33.json').write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+'\n')
policy={'strategy':'PREMIUM_FIRST','first_pass':'Nest all plywood in premium material','secondary_trigger':{'type':'EXTRA_PREMIUM_SHEET_CAUSED_ONLY_BY_SMALL_MODULAR_SECONDARY_SUBSET','small_subset_max_parts':None,'requires_owner_or_supplier_review':True},'structural_premium_never_auto_downgrade':True,'secondary_allowed':'good-quality secondary plywood / virola only after thickness, bond, flatness, screw-holding and payload qualification','do_not_nest_world_aabb':True,'actual_sheet_sizes_mm':None,'kerf_mm':None,'grain_direction':None,'material_release':False}
(R/'config/wood_materials_v33.json').write_text(json.dumps({'policy':policy,'parts':wood,'solid_wood_stock':[{'id':'H01','object':'PF_WoodDowel','material_class':'STRUCTURAL_PREMIUM','material':'sound straight hardwood; species and moisture unselected','quantity':1,'diameter_mm':32,'length_mm':560,'include_in_plywood_nesting':False,'note':'Counted in required hardware BOM; do not double-count as plywood.'}]},indent=2,ensure_ascii=False)+'\n')
print('HARDWARE_V33_CATALOG_PASS',len(items),'families',len(wood),'wood objects',len(assigned),'mapped objects')
