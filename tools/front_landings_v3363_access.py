"""Native front-door hand/tool corridor screen. Original CERN-OHL-S-2.0.
Swept envelopes are explicit packaging assumptions, not universal ergonomics.
"""
from pathlib import Path
import sys,json,hashlib,math
import FreeCAD as A, Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,PF
from coin_door_v32 import definitions,turn
V=A.Vector; O=R/'exports/generated/front-landings-v3363';O.mkdir(parents=True,exist_ok=True)
source=O/'play.FCStd'
if not source.exists():source=R/'exports/generated/playfield-rest-v3362/play.FCStd'
p=load(source);cfg=json.loads((R/'config/front_panel_v32.json').read_text())
obs=actual(p)
# Ordinary front keyed door opens with its attached coin mechanisms. Retain
# frame, tray and fixed supports; use the existing documented hinge trajectory.
moving_coin=[]
for n,(s,k,moves) in definitions(cfg,True).items():
 key='CoinStudy_'+n
 if key in p:
  obs[key]=turn(p[key],cfg['coin_door'],110) if moves else p[key]
  if moves:moving_coin.append(key)
for n,s in p.items():
 if n=='PLUNGER_RESERVED' or n.endswith('CandidatePayload') or (n.startswith('Button') and 'ServiceReserve' in n):obs[n]=s
def box(x,y,z,w,d,h):return Part.makeBox(w,d,h,V(x,y,z))
def shift(s,dx=0,dy=0,dz=0):s=s.copy();s.translate(V(dx,dy,dz));return s
def mirror(s):
 m=A.Matrix();m.A11=-1;m.A14=600;s=s.copy();s.transformShape(m,True);return s
def sweep(s,dx=0,dy=0,dz=0):
 b=s.BoundBox
 return box(b.XMin+min(0,dx),b.YMin+min(0,dy),b.ZMin+min(0,dz),b.XLength+abs(dx),b.YLength+abs(dy),b.ZLength+abs(dz))
def hits(s,ignored=()):
 return [{'part':n,'volume_mm3':s.common(t).Volume} for n,t in obs.items() if n not in ignored and s.BoundBox.intersect(t.BoundBox) and s.common(t).Volume>1e-4]
def nearest(s,ignored=()):
 best=(1e9,'')
 a=s.BoundBox
 rows=[]
 for n,t in obs.items():
  if n in ignored:continue
  b=t.BoundBox;lb=math.sqrt(sum(max(0,getattr(a,k+'Min')-getattr(b,k+'Max'),getattr(b,k+'Min')-getattr(a,k+'Max'))**2 for k in 'XYZ'))
  rows.append((lb,n,t))
 for lb,n,t in sorted(rows,key=lambda q:q[0]):
  if lb>best[0]:break
  d=s.distToShape(t)[0]
  if d<best[0]:best=(d,n)
 return best
def hull2(points):
 points=sorted(set(points))
 def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
 lo=[];hi=[]
 for p in points:
  while len(lo)>=2 and cross(lo[-2],lo[-1],p)<=0:lo.pop()
  lo.append(p)
 for p in reversed(points):
  while len(hi)>=2 and cross(hi[-2],hi[-1],p)<=0:hi.pop()
  hi.append(p)
 return lo[:-1]+hi[:-1]
report={'source':str(source.relative_to(R)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scope':'OCC swept hand/tool envelopes with existing coin door at110 degrees; not a human-factors certification. No electronics removal.','coin_door_open_deg':110,'coin_members_opened':moving_coin,'checks':[],'operations':{},'manufacturing_release':False}
shapes={}
# Axis atY245 andY275 is supplied by exact native landing search. The two
# workflows use the same front aperture and are evaluated independently.
geo=json.loads((O/'geometry-validation.json').read_text())
retz=sum(geo['retention']['nominal_hex_head_z_range_mm'])/2
adjustz=geo['selected']['body_bounds_mm'][5]+5.5
for kind,y,z,palm_z,headr in [('retention',275,retz,249,12),('adjuster',245,adjustz,318,13)]:
 # Ring/open-spanner reserve: head24/26dia x6, handle92x12x6. Palm60x70x28
 # below handle with a short finger bridge. Position assumes an ordinary
 # short flat spanner; purchased shape is a fit gate.
 shapes0={'tool_head':Part.makeCylinder(headr,6,V(72,y,z-3)),
          'tool_handle':box(72,y-6,z-3,92,12,6),
          'palm':box(142,y-35,palm_z,60,70,28),
          'fingers':box(142,y-12,palm_z+20,30,24,max(1,z+2-(palm_z+20)))}
 for side in ['L','R']:
  ignored=[n for n in obs if n.startswith('FrontLanding'+side) and any(w in n for w in (['Retention','Captive'] if kind=='retention' else ['Adjust','Pad','Locknut','Insert']))]
  # If invoked before the final native assembly this is explicitly preliminary.
  final={k:(s if side=='L' else mirror(s)) for k,s in shapes0.items()}
  entrydx=138 if side=='L' else -138
  stages={}
  for n,s in final.items():
   dz=-50 if kind=='adjuster' else 0
   stages['Entry_'+n]=sweep(shift(s,dx=entrydx,dy=-y-100,dz=dz),dy=y+100)
   if dz:stages['Raise_'+n]=sweep(shift(s,dx=entrydx,dz=dz),dz=-dz)
   stages['Lateral_'+n]=sweep(s,dx=entrydx)
   if kind=='retention':stages['Release_'+n]=sweep(s,dz=-10.5)
  # A limited±15-degree tool stroke plus repositioning; do not suggest an
  # unrestricted360-degree sweep through the side wall.
  stroke={}
  for angle in range(-15,16):
   for n,s in final.items():
    if n.startswith('tool_'):
     q=s.copy();q.rotate(V(72 if side=='L' else 528,y,z),V(0,0,1),angle);stroke.setdefault(n,[]).append(q)
  for n,ss in stroke.items():
   b=Part.makeCompound(ss).BoundBox
   if n=='tool_head':stages['ContinuousStroke_'+n]=final[n]
   else:
    # Convex XY hull of rotated rectangular handle, expanded1mm, encloses
    # every between-sample pose (<110mm radius,1degree spacing). A full AABB
    # incorrectly fills a large triangle beside the bolt and is not used.
    points=[(v.Point.x+dx,v.Point.y+dy) for s in ss for v in s.Vertexes for dx in [-1,1] for dy in [-1,1]]
    vv=[V(x,y,b.ZMin) for x,y in hull2(points)]
    stages['ContinuousStroke_'+n]=Part.Face(Part.makePolygon(vv+[vv[0]])).extrude(V(0,0,b.ZLength))
  bad=[];mind=(1e9,'')
  for n,s in stages.items():
   for h in hits(s,ignored):bad.append({'stage':n,**h})
   d=nearest(s,ignored)
   if d[0]<mind[0]:mind=d
   shapes[f'{kind}_{side}_{n}']=s
  report['operations'][kind+'_'+side]={'hand':'60x70x28 palm plus finger bridge','tool':'24/26dia head x6,92mm handle; limited stroke15deg','route':'Open coin door110deg; enter centrally above S1 at lowered height; raise only beyond front relief when adjusting; translate laterally behind plunger; operate below playfield.','ignored_intentional_tool_host':ignored,'hits':bad,'minimum_clearance_mm':mind[0],'nearest_part':mind[1],'pass':not bad}
report['side_attachment_access']={}
saved_obs=obs
# Initial assembly / rare body replacement: playfield module, main glass and
# matrix removed. This is not required to release the routine closed clamps.
obs={n:s for n,s in saved_obs.items() if n!='CandidateGlass' and not n.startswith(('PF_','PLAYFIELD_','Matrix','MX_Retainer'))}
for side in ['L','R']:
 for index in range(1,5):
  name=f'FrontLanding{side}_SideScrew{index}';b=p[name].BoundBox
  x=86 if side=='L' else 514;axis=V(1 if side=='L' else -1,0,0);point=V(x,b.Center.y,b.Center.z)
  shaft=Part.makeCylinder(4,124,point,axis)
  handle=Part.makeCylinder(22,80,point+axis*104,axis)
  q=Part.makeCompound([shaft,handle]);bad=hits(q,[name])
  report['side_attachment_access'][name]={'pass':not bad,'hits':bad,'driver':'8mm shaft x124mm;44mm grip envelope x80mm','prerequisites':'PF module/main glass/matrix removed for installation or rare body replacement'}
  shapes[name+'_Driver']=q
obs=saved_obs
report['pass']=all(x['pass'] for x in report['operations'].values()) and all(x['pass'] for x in report['side_attachment_access'].values())
report['preliminary_without_new_supports']=source.name=='play.FCStd' and 'playfield-rest-v3362' in str(source)
(O/'tool-access.json').write_text(json.dumps(report,indent=2)+'\n')
doc=A.newDocument('FrontLandingToolAccess')
for n,s in {**{n:p[n] for n in ['FRONT','SHELF_1','PLUNGER_RESERVED','PF_BasePlywood']},**shapes}.items():
 ob=doc.addObject('PartDesign::Feature',n.replace('-','m'));ob.Shape=s
doc.recompute();doc.saveAs(str(O/'tool-access.FCStd'))
print('V3363_ACCESS_RESULT',report['pass'], {n:len(v['hits']) for n,v in report['operations'].items()},flush=True)
