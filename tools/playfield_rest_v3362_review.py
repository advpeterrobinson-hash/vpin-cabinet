"""V33.6.2 review scenes from exact native B-reps. CERN-OHL-S-2.0.
No scene grants CNC release. Held adapter window is never shown as current.
"""
from pathlib import Path
import gzip,json,sys,math
import FreeCAD as A,Part,MeshPart
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,transform,pf_names,PF,V
O=R/'exports/generated/playfield-rest-v3362';old=load(R/'exports/generated/button-relief-v3361/play.FCStd');new=load(O/'play.FCStd');st=load(O/'study.FCStd');historical=load(R/'exports/generated/structural-v335/play.FCStd')
C=json.loads((R/'config/playfield_rest_v3362.json').read_text());a=json.loads((R/'exports/generated/notch-floor-fans-v32/validation.json').read_text())['review']['closed_slope_deg'];bz=400.05+45*math.tan(math.radians(a))-12-55*math.cos(math.radians(a))
scenes=[];cache={}
def inv(s):q=s.copy();q.translate(V(0,-45,-bz));q.rotate(V(),V(1,0,0),-a);return q
def sub(d,names):return {n:d[n] for n in names if n in d}
def select(d,*starts):return {n:s for n,s in d.items() if n.startswith(starts)}
def slice(s,axis,low,high):
 b=s.BoundBox;pos=[b.XMin-1,b.YMin-1,b.ZMin-1];size=[b.XLength+2,b.YLength+2,b.ZLength+2];pos[axis]=low;size[axis]=high-low;return s.common(Part.makeBox(*size,V(*pos)))
def col(n):
 if 'HELD' in n or 'Held_' in n:return '#bb6352'
 if 'Cable' in n or 'Connector' in n:return '#15717e'
 if n.startswith(('LeafButton','LeafNut')):return '#984524'
 if n.startswith(('Leaf','ButtonAccess','Button')):return '#446e80'
 if 'VESA' in n or 'Clamp' in n:return '#6a879c'
 if 'Stop' in n:return '#b27b28'
 if 'Slot' in n or 'Thread' in n:return '#267568'
 if 'Display' in n or n in ['TV_ENVELOPE','PLAYFIELD_ENVELOPE']:return '#354858'
 if 'Glass' in n:return '#a9c0c9'
 if 'Screw' in n or 'Bolt' in n:return '#555b61'
 return '#c8ae8c'
def panel(label,parts,view=(1,-2,1.5),colors=None,alpha=None,limits=None,annotations=None,edges=None):
 meshes=[]
 for n,s in parts.items():
  if s.isNull():continue
  mm=MeshPart.meshFromShape(Shape=s,LinearDeflection=.45,AngularDeflection=.5,Relative=False);vv,ff=mm.Topology;meshes.append({'name':n,'vertices':[list(p) for p in vv],'faces':ff,'color':(colors or {}).get(n,col(n)),'alpha':(alpha or {}).get(n,1)})
 return {'label':label,'meshes':meshes,'view':view,'limits':limits,'annotations':annotations or [],'edges':edges or []}
def line_wire(s,y=None):
 # True native edges, projected by renderer; no traced/invented silhouette.
 out=[]
 for e in s.Edges:
  pts=e.discretize(Deflection=.12)
  if len(pts)>1:out.append([list(p) for p in pts])
 return out
def add(id,title,panels,note,legend=None):scenes.append({'id':id,'title':title,'panels':panels,'note':note,'legend':legend or []})
def lp(d):return {n:inv(s) for n,s in d.items()}
def buttonset(d):return {n:s for n,s in d.items() if n.startswith(('Leaf','Button')) and n.endswith('_L')}
before=inv(old['PF_BasePlywood']);after=inv(new['PF_BasePlywood'])
add('01','Front relief: another30 mm inward on each side',[panel('Before22 mm / now52 mm per side',{'M025':after},(0,0,1),limits=[35,160,0,180],colors={'M025':'#e8e1d5'},edges=[{'lines':line_wire(before),'color':'#b44428','width':2,'style':'--'},{'lines':line_wire(after),'color':'#213e49','width':1.4}]),panel('Full one-piece base',{'M025':after},(0,0,1),edges=[{'lines':line_wire(after),'color':'#213e49','width':.7}])],'Owner-confirmed transverse trim only. Total inset52 mm each side; front width396 mm. Length87 mm andR8 unchanged. Rear service window and strain slots preserved.',['Dashed: previous22 mm inset','Solid: current52 mm inset'])
ann=[]
for i in [1,2,3]:
 q=new['CROSS_'+str(i)];y=q.BoundBox.Center.y;line=Part.makeLine(V(300,y,0),V(300,y,1000));z=q.common(line).BoundBox.ZMax;ann.append({'point':[300,y,z],'text':'T'+str(i)+' · 22 mm gap','offset':[-30,-55]})
add('02','Current closed pose has no front landing',[panel('Left-side section · REAR left / FRONT right',sub(new,['PF_BasePlywood','PF_WoodDowel','PF_OpenCradleL','CROSS_1','CROSS_2','CROSS_3']),(-1,0,0),annotations=ann)],'Each T top is22 mm normal below the base. Rear dowel/cradles support the rear but do not stop rotation. This is an unsupported CAD pose, NOT a qualified closed assembly. See separate HELD T1 landing-shoe study.')
add('03','Wider front relief with unchanged VESA/dowel',[panel('Base underside; supports intentionally separated',sub(new,['PF_BasePlywood','PF_WoodDowel','PF_VESAEnvelope'])|select(new,'PF_CommercialStrap','PF_StrapScrew'),(1,-1,-1))],'VESA load reserve, wooden dowel, four commercial saddle straps and eight screws remain exact. Front section396 x18 =7128 mm2. Structural qualification requires the missing closed-position support and actual materials.')
for sc in scenes:
 for a,b in [('another30','another 30'),('Before22','Before 22'),('now52','now 52'),('inset52','inset 52'),('width396','width 396'),('Length87','Length 87'),('andR8','and R8'),('is22','is 22'),('section396','section 396'),('x18','x 18'),('previous22','previous 22'),('current52','current 52')]:
  sc['note']=sc['note'].replace(a,b);sc['title']=sc['title'].replace(a,b)
  sc['legend']=[x.replace(a,b) for x in sc['legend']]
  for panelrow in sc['panels']:panelrow['label']=panelrow['label'].replace(a,b)
(O/'review-scenes.json.gz').write_bytes(gzip.compress(json.dumps(scenes,separators=(',',':')).encode(),mtime=0))
print('V3362_REVIEW_SCENES_PASS',len(scenes),flush=True)
