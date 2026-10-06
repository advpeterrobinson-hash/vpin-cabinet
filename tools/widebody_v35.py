"""V35 independently dimensioned widebody candidate; never scales solids."""
from widebody_v35_common import *
from pivot_cradle_integration_v32 import pf_names,PF
import re
s={};audit={};checks=[]
def ck(n,p,d=None):checks.append({'name':n,'pass':bool(p),'detail':d});print(n,bool(p),flush=True)
widened={'FRONT','REAR','FLOOR','BACKBOX_BASE','PF_BasePlywood','PF_WoodDowel',*[f'SHELF_{i}' for i in [1,2,3]],*[f'CROSS_{i}' for i in [1,2,3]]}
# Explicit parent policy first; all other source objects are centered rigidly.
sideprefix=('Leaf','Button','CandidateFixedSupportScrew','SimpleShelfBolt','CROSS_GUIDE','CROSS_BRACKET','SHELF_SUPPORT','SSF_Exciter','PF_OpenCradle','PF_SupportMountScrew','FrontLanding')
def move(n):
 if n.startswith('CandidateFrontButton'):return (DELTA if n.endswith('4') else 0),'REPOSITIONED'
 if n=='CandidateMainsEnclosure':return 0,'UNCHANGED'
 if n.startswith('BB_') or n.startswith('UprightLock') or n.startswith(('MX_','Matrix','Underfront')):return DX,'RECENTERED'
 if n=='SIDE_L' or n=='FLOOR_CLEAT_18':return 0,'UNCHANGED'
 if n=='SIDE_R' or n=='FLOOR_CLEAT_552':return DELTA,'REPOSITIONED'
 if n.startswith(sideprefix):
  side='R' if re.search(r'R(?:\d|_|$)',n) else 'L'
  return (DELTA if side=='R' else 0),'REPOSITIONED' if side=='R' else 'UNCHANGED'
 if n.startswith(('CandidateLeg','Plunger','PLUNGER')):return (DELTA if ('FR' in n or 'RR' in n or 'Plunger' in n or 'PLUNGER' in n) else 0),'REPOSITIONED'
 if n.startswith(('PF_Strap','PF_CommercialStrap')):return (DELTA if re.search(r'(?:Strap|Screw)[34]',n) else 0),'REPOSITIONED'
 return DX,'RECENTERED'
for n,q in p0.items():
 dx,kind=move(n)
 holecuts=[]
 if n=='BACKBOX_BASE':
  for xx in [45,555]:
   for yy in [1140,1180]:
    region=box(xx-4,yy-4,578.9,8,8,18);void=region.cut(q)
    if void.Volume>1e-6:q=q.fuse(void).removeSplitter();holecuts.append(shift(void,x=DX))
 if n=='FRONT':
  # Retire two outer provisional receiver bores; actual A-16773-1 drilling stays NULL.
  for xx in [68.225,477.8]:
   region=box(xx-5,0,360,10,18,10);void=region.cut(q)
   if void.Volume>1e-6:q=q.fuse(void).removeSplitter()
 if n in widened:
  cuts={'FRONT':(120,480),'REAR':(160,440),'FLOOR':(60,540),'BACKBOX_BASE':(60,540),'PF_BasePlywood':(120,480)}.get(n,(100,500))
  s[n]=extend_at(extend_at(q,cuts[0],DX),cuts[1]+DX,DX)
  for h in holecuts:s[n]=s[n].cut(h).removeSplitter()
  kind='WIDENED'
 else:s[n]=shift(q,x=dx)
 audit[n]={'classification':kind,'translation_x_mm':None if kind=='WIDENED' else dx,'method':('constant-section insertion at X'+str(cuts)+'; no scaling') if kind=='WIDENED' else 'rigid parent placement','source_bounds':bb(q),'new_bounds':bb(s[n])}
# Restore unchanged BB local floor, including its historical local rebate; no unnecessary machining added.
# Retire moving glass channel; shorter standard rear stop becomes a main-body interface.
s.pop('BB_PFRearChannel');audit['BB_PFRearChannel']['classification']='REPLACED BY COMMERCIAL INTERFACE'
L=C['glass']['commercial_reference_mm'][1];th=C['glass']['commercial_reference_mm'][2];gb=C['glass']['reference_bottom_normal_mm'];gap=C['playfield']['selected_planning_gap_mm'];top=gb-gap;gf=C['glass']['front_local_offset_mm']
s['CandidateGlass']=tf(box((W-603.25)/2,gf,gb,603.25,L,th))
# Original abstract commercial packaging U, not reproduction of an unmeasured extrusion.
# Interior-face groove; plastic lip rises only6.7625mm normal, metal trim wraps the whole edge.
rail=box(11.2,gf,-5,1,1076.325,gb+th+6.5).fuse(box(12.2,gf,gb-1.5,7.8,1076.325,1)).fuse(box(12.2,gf,gb+th+.5,7.8,1076.325,1)).removeSplitter()
s['CandidateGlassChannelL']=tf(rail);s['CandidateGlassChannelR']=mirror(s['CandidateGlassChannelL'])
for side,x in [('L',10.95),('R',W-18)]:
 cut=tf(box(x,gf,-5.25,7.05,1076.325,14));s['SIDE_'+side]=s['SIDE_'+side].cut(cut).removeSplitter();audit['SIDE_'+side]['classification']='REPOSITIONED + REFERENCE ROUTING'
# Conventional siderail reference shell. Cross-section unmeasured: compatibility reserve, not selected SKU CAD.
trim=box(-1,-20,-30,1,1116.325,gb+th+32.5).fuse(box(0,-20,gb+th+1.5,20,1116.325,1)).removeSplitter()
s['CommercialSiderailL']=tf(trim);s['CommercialSiderailR']=mirror(s['CommercialSiderailL'])
rearW=582.6125;rx=(W-rearW)/2
u=box(rx,gf+L-9,gb-1.5,rearW,13,1).fuse(box(rx,gf+L-9,gb+th+.5,rearW,13,1)).fuse(box(rx,gf+L+.5,gb-.5,rearW,3.5,th+1)).removeSplitter()
s['PF_RearGlassChannel']=tf(u)
# Existing rear shelf front edge supports commercial rear U; local TOP reference rebate.
seatcut=tf(box(rx-1,gf+L-9,gb-1.5,rearW+2,14,25))
s['BACKBOX_BASE']=s['BACKBOX_BASE'].cut(seatcut).removeSplitter()
audit['BACKBOX_BASE']['method']+='; local one-face TOP angled rear-channel seat'
s['PF_LockdownGlassRetainer']=tf(box(-3.175,-35,gb+th+1.5,635,69,1.5).fuse(box((W-603.25)/2,gf-2,gb,603.25,1.5,th+2)))
s['LockdownReceiverReference']=box(CENTER-260,18,365,520,42,25)
# Keep mechanical PF base/axis/supports YZ. Thin TVs on ordinary selected VESA spacers fit new high screen plane.
pfb=local(p0['PLAYFIELD_ENVELOPE']).BoundBox
s['PLAYFIELD_ENVELOPE']=tf(box(CENTER-280,(pfb.YMin+pfb.YMax-961)/2+20,top-41.1,560,961,41.1))
s['PF_VESAEnvelope']=tf(box(CENTER-100,358.7655225809816,-61.19312351915857,200,250,12.59312351915857))
variants={}
TVS=[('LG42C5',540,932,41.1),('Samsung43QN93D',558.9,960.8,26.9),('TCL40S5K',507,892,77)]
tvcases=[]
for n,w,l,d in TVS:
 q=tf(box(CENTER-w/2,(pfb.YMin+pfb.YMax-l)/2+20,top-d,w,l,d));variants[n]=q
 tvcases.append({'reference':n,'portrait_transverse_width_mm':w,'longitudinal_mm':l,'depth_mm':d,'left_gap_mm':(W-36-w)/2,'right_gap_mm':(W-36-w)/2,'available_depth_mm':top-pfb.ZMin,'depth_packaging_pass':d<=top-pfb.ZMin,'optional_LED_geometric_width_possible':(W-36-w)/2>=15,'selected':False})
variants['SunkenNegativeControl']=shift(s['PLAYFIELD_ENVELOPE'],y=sa*50,z=-ca*50)
for side,x in [('L',22),('R',W-32)]:variants['OptionalLEDEnvelope'+side]=tf(box(x,40,top-8,10,910,8))
for n in s:ck('valid solid '+n,s[n].isValid() and len(s[n].Solids)>0)
ck('body nominal 628.65',abs(W-628.65)<1e-9 and abs(DELTA-28.65)<1e-9,{'datum':'source exterior planes X0/X600 translated to X0/X628.65; OCC spline bounding boxes not width authority'})
ck('backbox local shapes unchanged',all(abs(s[n].Volume-q.Volume)<1e-3 and audit[n]['translation_x_mm']==DX for n,q in p0.items() if n.startswith('BB_') and n!='BB_PFRearChannel'),'Rigid whole-assembly translation only; independent inverse-transform comparison in regression')
ck('glass commercial reference',abs(s['CandidateGlass'].Volume-603.25*L*th)<.001)
ck('high parallel target',gap<=10 and abs(local(s['PLAYFIELD_ENVELOPE']).BoundBox.ZMax-(gb-gap))<1e-6)
ck('M025 no horn / original front relief retained',abs(local(s['PF_BasePlywood']).BoundBox.XLength-528.65)<.001)
# Explicit rear support obstruction to promotion unless a simple existing-panel interface is found.
rear_support=s['PF_RearGlassChannel'].distToShape(s['BACKBOX_BASE'])[0]
ck('rear commercial channel supported by existing shelf',rear_support<.01,{'separation_mm':rear_support,'note':'No floating rear-channel attachment permitted'})
ck('landings move with side',abs(s['FrontLandingR_ContactPad'].BoundBox.Center.x-(W-72))<.001)
ck('plywood two families',C['plywood_mm']==[12,18])
# Pair checks for new glass package against physically occupied source geometry.
obs={n:q for n,q in s.items() if n in actual(s) and not any(t in n for t in ['Screw','Bolt','Washer','Reserve','Envelope','Liner','Cushion','Tether'])}
newnames=['CandidateGlass','CandidateGlassChannelL','CandidateGlassChannelR','CommercialSiderailL','CommercialSiderailR','PF_RearGlassChannel','PF_LockdownGlassRetainer','LockdownReceiverReference']
clashes=hits({n:s[n] for n in newnames},{n:q for n,q in obs.items() if n not in newnames})
ck('commercial stack no occupied collision',not clashes,clashes)
for a in tvcases:
 q=variants[a['reference']];h=hits({'TV':q},{n:t for n,t in obs.items() if n!='PLAYFIELD_ENVELOPE'});a['collision_hits']=h;a['geometry_pass']=not h
ck('42-inch envelope screen',tvcases[0]['geometry_pass'],tvcases[0])
ck('43-inch envelope screen',tvcases[1]['geometry_pass'],tvcases[1])
# R22 axis reserve comparison; X follows cabinet sides, floor arm attachments remain physically held.
for side,x,dr in [('L',0,1),('R',W,-1)]:
 q=Part.makeCylinder(22,40,V(x,1066.8,508),V(dr,0,0));variants['WPC_AccessReserve'+side]=q
# Native reference states; validation is separate and required before promotion.
for n in audit:
 if n in s:audit[n]['new_bounds']=bb(s[n])
save('candidate',s);save('variants',variants)
dump('width-audit',audit);dump('geometry',{'checks':checks,'pass':all(a['pass'] for a in checks),'angle_deg':ANG,'glass_bottom_normal_mm':gb,'display_top_normal_mm':top,'gap_front_center_rear_mm':[gap]*3,'gap_trials_mm':[5,7.5,10],'TV_cases':tvcases,'rear_support_gap_mm':rear_support,'commercial_shape_status':'PACKAGING_ONLY_PURCHASE_REQUIRED','source_head':C['head_before'],'base_decision':'500mm centered would leave only7.675mm from landing center to edge, with12mm pad radius.528.65mm retains22mm original edge distance and existing attachment holes. No scale.','dowel_length_mm':s['PF_WoodDowel'].BoundBox.XLength,'counts':len(s)})

assert all(a["pass"] for a in checks), "V35 construction gate failed"
