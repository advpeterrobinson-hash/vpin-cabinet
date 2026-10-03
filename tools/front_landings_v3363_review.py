"""Eighteen native CAD reviews for side landings. CERN-OHL-S-2.0."""
from pathlib import Path
import gzip,json,sys,math
import FreeCAD as A,Part,MeshPart
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,transform,pf_names,PF,V
C=json.loads((R/'config/front_landings_v3363.json').read_text());O=R/C['output']
new=load(O/'play.FCStd');released=load(O/'released.FCStd');old=load(R/C['source']);study=load(O/'study.FCStd')
G=json.loads((O/'geometry-validation.json').read_text());M=json.loads((O/'metrology.json').read_text());scenes=[]
def sub(d,names):return {n:d[n] for n in names if n in d}
def select(d,*starts):return {n:s for n,s in d.items() if n.startswith(starts)}
def clip(s,x0,x1,y0,y1,z0,z1):return s.common(Part.makeBox(x1-x0,y1-y0,z1-z0,V(x0,y0,z0)))
def colors(n):
 if n.startswith('HELD'):return '#a97158'
 if 'Layer' in n:return '#cc9b5c'
 if 'ContactPad' in n:return '#1c625e'
 if 'Retention' in n:return '#527593'
 if 'Adjuster' in n or 'Swivel' in n or 'Screw' in n:return '#65757d'
 if 'Button' in n or 'Leaf' in n:return '#a55736'
 if 'PLUNGER' in n:return '#b79bb6'
 if n=='PLAYFIELD_ENVELOPE':return '#3e5964'
 if 'Dowel' in n:return '#978161'
 if 'CROSS' in n or 'Cradle' in n:return '#587f88'
 return '#c6b596'
def edges(s):return [[list(v) for v in e.discretize(Deflection=.2)] for e in s.Edges]
def panel(label,objects,view=(1,-2,1.2),alpha=None,annotations=None,lines=None):
 meshes=[]
 for name,s in objects.items():
  if s.isNull():continue
  m=MeshPart.meshFromShape(Shape=s,LinearDeflection=.5,AngularDeflection=.5,Relative=False);vv,ff=m.Topology
  meshes.append({'name':name,'vertices':[list(v) for v in vv],'faces':ff,'color':colors(name),'alpha':(alpha or {}).get(name,1)})
 return {'label':label,'meshes':meshes,'view':view,'annotations':annotations or [],'edges':lines or []}
def add(id,title,panels,note,legend=None):scenes.append({'id':id,'title':title,'panels':panels,'note':note,'legend':legend or []})
def ann(point,text,offset=(15,20)):return {'point':point,'text':text,'offset':offset}
wood=sub(new,G['new_wood_names']);hw=sub(new,G['new_hardware_names']);left={n:s for n,s in (wood|hw).items() if n.startswith('FrontLandingL')}
left_fixed={n:s for n,s in left.items() if 'Receiver' not in n};support=wood|hw
base=new['PF_BasePlywood'];basefront=clip(base,45,555,30,335,250,500);leftbase=clip(base,45,110,205,310,300,440)
basebottom=max([f for f in base.Faces if type(f.Surface).__name__=='Plane' and f.normalAt(0,0).z<-.5],key=lambda f:f.Area)
Y=245;Z=G['contacts'][0]['center_xyz_mm'][2]
add('01','Previous closed pose — front support absent',[panel('V33.6.2: rear dowel only',sub(old,['PF_BasePlywood','PF_WoodDowel','PF_OpenCradleL','PF_OpenCradleR','CROSS_1','CROSS_2','CROSS_3']),(1,-2,-.6),annotations=[ann([72,245,Z],'No front landing\nin previous geometry',(-50,-45))])],'The previous CAD PLAY placement did not mechanically establish pitch. The rear dowel has seat contact but permits rotation; this view is an audit of the superseded unsupported configuration.')
gap_panels=[]
for i in [1,2,3]:
 t=old['CROSS_'+str(i)];b=t.BoundBox;yc=(b.YMin+b.YMax)/2
 gap_panels.append(panel('T'+str(i)+' ·22 mm normal gap',{'Base':clip(base,110,145,yc-45,yc+45,0,650),'CROSS_'+str(i):clip(t,110,145,yc-45,yc+45,0,650)},(-1,0,0)))
add('02','Crossmember clearance is intentional after front support',[*gap_panels],'Actual same-Y vertical gap is22.333 mm at each crossmember. T1/T2/T3 remain cabinet structural crossmembers; they do not carry playfield gravity load in the selected architecture.')
shoes={}
for side in ['L','R']:
 q=Part.Shape();q.read(str(R/'exports/generated/playfield-rest-v3362/t1-rest-study/brep'/('HELD_captured_shoe_'+side+'.brep')));shoes['HELD_T1_Shoe'+side]=q
add('03','T1 shoes — comparison only',[panel('Rejected in favor of earlier side landings',{'Base':clip(base,70,530,290,445,250,450),'CROSS_1':new['CROSS_1'],**shoes},(1,-1,-.7),alpha={'Base':.2})],'The held shoe pair supports aroundY380 and leaves315.986 mm centerline front overhang. It makes the playfield dependent on removable T1. No T1 shoe is promoted; new side contacts are atY245.')
searchparts={'Base':basefront,**select(new,'Leaf','Button'), 'PLUNGER_RESERVED':new['PLUNGER_RESERVED'],**wood,**{n:s for n,s in hw.items() if 'ContactPad' in n}}
add('04','Front-side search — earliest simple body',[panel('Search 150–250 · right plunger corridor controls',searchparts,(0,0,1),alpha={'Base':.16,'PLUNGER_RESERVED':.3},annotations=[ann([528,225,300],'Body frontY225\n5 mm behind plunger reserve',(-160,-45)),ann([72,245,Z],'Selected padY245',(15,20))])],'202 candidates compare36 and54 mm body heights in1 mm Y increments. The54 mm body first passes atY245 with5 mm obstacle reserve and a complete contact footprint. Buttons and their conservative hand/tool paths are also screened.')
add('05','Selected landing — three 18 mm layers',[panel('Left support · direct structural side attachment',left|{'Base':leftbase},(1,-1,.55),alpha={'Base':.18},annotations=[ann([18,245,310],'68 ×70 ×54 mm body\n3×18 mm offcuts',(-90,-50)),ann([72,245,Z],'M8 articulated contact',(20,35))])],'Symmetric body pair; six actual18 mm plywood pieces. All purchased inserts, screws and adjusters remain provisional. No side-wall or M025 machining is frozen.')
buttonparts={n:s for n,s in new.items() if n.startswith(('Leaf','Button')) and n.endswith('_R')}
add('06','Button and plunger service clearance',[panel('Right front interior',buttonparts|{'Base':clip(base,485,555,50,320,250,420),'PLUNGER_RESERVED':new['PLUNGER_RESERVED']}|{n:s for n,s in support.items() if n.startswith('FrontLandingR')},(-1,-1,.45),alpha={'Base':.16,'PLUNGER_RESERVED':.3},annotations=[ann([528,225,286],'5 mm plunger margin',(-115,-40)),ann([558,149,347],'Button wire/service preserved',(-60,40))])],'Body-to-secondary wire reserve76 mm; body-to-occupied button87.303 mm. The original button hand/tool corridors remain clear. The right plunger reserve, not the buttons, determines the symmetric support location.')
sidepiece=clip(new['SIDE_L'],0,22,205,315,265,355)
add('07','Positive body-to-side attachment',[panel('Four provisional screws per landing',left|{'SIDE_L_Section':sidepiece},(1,-1,.2),alpha={n:.20 for n in wood if n.startswith('FrontLandingL')},annotations=[ann([18,234,331.4469],'12 mm side embedment\n6 mm exterior skin',(-100,55)),ann([86,286,295.4469],'36 mm vertical row pitch\n52 mm Y pitch',(-95,-55))])],'Four4.5×80-class screws per side are a packaging reference. Minimum body screw-center edge distance9 mm; side-panel outer-boundary distance≥107.838 mm. Final pilot, head seat and actual plywood load qualification remain HOLD. No exterior breakthrough is permitted.')
adjust={n:s for n,s in left.items() if any(t in n for t in ['Adjuster','Swivel','ContactPad','Layer'])}
add('08','Adjuster stack — pad thickness included',[panel('M8 insert / locknut / swivel / replaceable pad',adjust|{'Base':leftbase},(1,-1,.65),alpha={**{n:.18 for n in wood if n.startswith('FrontLandingL')},'Base':.16},annotations=[ann([72,245,Z],'Ø24 contact;3 mm pad\nArticulation follows9.906669°',(15,45)),ann([72,245,340.4469],'22 mm nominal complete stack',(-105,-50))])],'±3 mm is tolerance-compensation travel to reproduce the accepted pose. It is not permission to lower the whole display or twist the board. ±5 mm is rejected by the100 mm retention stack; jamnut stops are reset after leveling.')
pad=hw['FrontLandingL_ContactPad'];padtop=max([f for f in pad.Faces if type(f.Surface).__name__=='Plane' and f.normalAt(0,0).z>.5],key=lambda f:f.Area)
add('09','M025 contact footprint — useful continuous wood',[panel('Underside at left pad',{'Base':clip(base,45,140,135,300,250,450),'ContactPad':pad},(0,0,-1),alpha={'Base':.55},lines=[{'lines':edges(padtop),'color':'#152e34','width':2}],annotations=[ann([72,245,Z],'452.389 mm² per pad\n10 mm to outer base edge',(15,-45))])],f'Contact is behind the front relief, on continuous18 mm M025. Pad-to-VESA reserve is{M["rows"][0]["pad_to_VESA_mm"]:.3f} mm. Rear service window and strain slots remain unchanged; actual receiver bore is a separate purchased-hardware hold.')
add('10','Left/right leveling — preserve current playing slope',[panel('Two contacts at the same nominal height',support|{'Base':clip(base,45,555,215,295,250,420)},(0,-1,.15),alpha={'Base':.25},annotations=[ann([72,245,Z],'L contactZ362.446911',(15,45)),ann([528,245,Z],'R contactZ362.446911',(-150,45))])],'Level means level across X while retaining9.906669° front/rear slope. The rear dowel is a fixed line: opposing adjuster heights are not an authorized rigid-board twist. An actual common−3 mm pose collides the display envelope with button hardware; compensate build tolerances to the nominal pose.')
add('11','Front overhang — 245 mm versus 380 mm support',[panel('Same base; front at right',{'Base':clip(base,110,145,30,430,250,500),**{n:s for n,s in support.items() if n.startswith('FrontLandingL')},'CROSS_1':clip(new['CROSS_1'],110,145,365,395,250,450)},(-1,0,0),annotations=[ann([72,245,Z],'Side contact centerY245\nOverhang180.986 mm',(-150,-65)),ann([125,380,386],'T1 centerY380\nOverhang315.986 mm',(-50,65))])],'Using the same base front bound, side landings shorten centerline front overhang by135 mm. The first pad edge begins169.165 mm behind the base front bound. Root load report compares bending tendency; contact area alone is not strength certification.')
context=sub(new,['FLOOR','PF_OpenCradleL','PF_OpenCradleR','PF_WoodDowel','CROSS_1','CROSS_2','CROSS_3'])
add('12','Explicit closed load path',[panel('Front into sides; rear into cradles/floor',context|support|{'Base':base},(1,-2,.4),alpha={'Base':.13},annotations=[ann([72,245,310],'FRONT: pad → body\n→ structural side',(-65,-55)),ann([30,1035.25,440],'REAR: dowel → cradle\n→ cabinet floor',(10,50))])],'Normal weight is carried by two front pads and the rear dowel line. The side screws are positive load-transfer connections. Glass, lockdown, buttons, electronics, cables and T1/T2/T3 are not gravity supports. Separate M6 retainers resist uplift.')
opening=[]
for a in [0,.25,1]:
 moved=transform({'Base':leftbase},angle=-a,axis=PF)
 opening.append(panel(f'{a:g}° from PLAY',moved|{n:s for n,s in released.items() if n.startswith('FrontLandingL') and 'Receiver' not in n},(-1,0,0)))
add('13','Early opening — pads release cleanly',opening,'Both M6 retainers are backed out and captive/parked. Exact continuous separating-plane proof covers first release; OCC interval bounds cover the remaining0–50° motion. The support blocks and M8 adjusters stay installed.')
pf={n:new[n] for n in json.loads((O/'viewer-motion.json').read_text())['playfield_moving_names'] if n in new};fixed=sub(new,['SIDE_R','FLOOR','FRONT','SHELF_1','SHELF_2','SHELF_3','PF_OpenCradleL','PF_OpenCradleR'])|{n:s for n,s in released.items() if n in support and n not in pf}
add('14','50° playfield service',[panel('Retainers released; supports remain installed',fixed|transform(pf,angle=-50,axis=PF),(1,-2,1),alpha={'PLAYFIELD_ENVELOPE':.22})],'Main playfield glass and matrix are removed. Both front retainers are parked; service support procedure remains mandatory. Native validation includes all new support hardware and the unchanged cabinet systems.')
add('15','48 mm lift-out — clear vertical extraction',[panel('Rear dowel leaves its open cradles',fixed|transform(pf,lift=48),(1,-2,.7),alpha={'PLAYFIELD_ENVELOPE':.16})],'Continuous differential clearance proves the48 mm vertical extraction with all new landings fixed. The seated2° /48→0 mm lowering sequence is also checked before final2→0° closure. Full module removal is preserved.')
ret_panels=[]
for label,d in [('ENGAGED ·7 mm nominal thread engagement',new),('RELEASED ·10.5 mm captive withdrawal',released)]:
 parts={n:s for n,s in d.items() if n.startswith('FrontLandingL') and ('Layer' in n or 'Retention' in n)}
 ret_panels.append(panel(label,parts|{'Base':leftbase},(-1,0,0),alpha={**{n:.22 for n in wood if n.startswith('FrontLandingL')},'Base':.16},annotations=[ann([72,275,367.6863],'Metal blind receiver\nUncut reference / hardware HOLD',(-180,50))]))
add('16','Uplift retention is separate from gravity support',ret_panels,'Two independent M6×100-class hex bolts with two thin jamnuts each set6–8 mm receiver engagement. A grooveless push-on ring keeps each bolt captive after withdrawal. Root access study checks a compact10 mm wrench. Glass/lockdown carry no normal playfield weight; no support hardware is removed for routine service.')
full=actual(new);full.update({n:s for n,s in support.items()})
add('17','Complete cabinet — closed supported playfield',[panel('Accepted pose and owner front relief preserved',full,(1.5,-2,1),alpha={'CandidateGlass':.12,'PLAYFIELD_ENVELOPE':.20})],'Both support pads touch M025 in the original PLAY pose. Both positive retainers are engaged. Y89/Y127 side buttons,52 mm side reliefs,396 mm front width, rear window, WPC, shelves and backbox remain unchanged. Manufacturing and physical qualification remain blocked.')
exploded={}
for name,s in left.items():
 q=s.copy()
 if 'Layer' in name:
  j=int(name[-1]);q.translate(V(0,0,(j-1)*30-60))
 elif 'SideScrew' in name:q.translate(V(85,0,0))
 elif 'LaminationScrew' in name:q.translate(V(0,0,55))
 elif 'Retention' in name:q.translate(V(0,30,-25 if 'Receiver' not in name else 35))
 elif any(a in name for a in ['Adjuster','Swivel','ContactPad']):q.translate(V(0,-35,40))
 exploded[name]=q
add('18','Landing hardware — semantic exploded review',[panel('One side shown; mirrored pair in cabinet',exploded,(1,-1.6,.75),annotations=[ann([72,210,Z+40],'One commodity articulated\nM8 foot assembly',(15,30)),ann([72,305,274],'Captive M6 retention stack',(-115,-40))])],'Three real18 mm layers per side; four side screws and two lamination screws per body. Exploded offsets explain assembly and are not insertion-path validation. Swivel, disc and resilient tip are visualization subparts of one purchased foot assembly, not custom metal or duplicate BOM items.')
for s in scenes:
 for a,b in [('22.333','22.333'),('aroundY','around Y'),('atY','at Y'),('Search150','Search 150'),('compare36','compare 36'),('and54','and 54'),('in1','in 1'),('The54','The 54'),('with5','with 5'),('three18','three 18'),('68 ×70 ×54','68 × 70 × 54'),('3×18','3 × 18'),('Six actual18','Six actual 18'),('reserve76','reserve 76'),('button87','button 87'),('Four4','Four 4'),('side9','side 9'),('distance9','distance 9'),('follows9','follows 9'),('the100','the 100'),('continuous18','continuous 18'),('is193','is 193'),('retaining9','retaining 9'),('common−3','common −3'),('by135','by 135'),('begins169','begins 169'),('remaining0','remaining 0'),('the48','the 48'),('seated2','seated 2'),('final2','final 2'),('set6','set 6'),('compact10','compact 10'),('buttons,52','buttons, 52'),('width,396','width, 396'),('real18','real 18')]:s['note']=s['note'].replace(a,b)
(O/'review-scenes.json.gz').write_bytes(gzip.compress(json.dumps(scenes,separators=(',',':')).encode(),mtime=0))
assert len(scenes)==18
print('V3363_REVIEW_SCENES_PASS',len(scenes),flush=True)
