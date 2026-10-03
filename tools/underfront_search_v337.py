"""Native underfloor location/layout search; no manufacturing hole authority.
Original CERN-OHL-S-2.0. X left/right, Y rearwards, Z up.
"""
from pathlib import Path
import FreeCAD as A, Part, sys,json,math
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,V
O=R/'exports/generated/two-stock-user-module-v337';O.mkdir(exist_ok=True,parents=True)
ss=load(R/'exports/generated/front-landings-v3363/play.FCStd')
obs=actual(ss);obs.pop('FLOOR',None)
obs.update({n:s for n,s in ss.items() if n.startswith(('Leaf','Button','FrontLanding','CoinStudy')) or n=='PLUNGER_RESERVED'})
def box(x,y,z,w,d,h):return Part.makeBox(w,d,h,V(x,y,z))
def lower(a,b):
 a,b=a.BoundBox,b.BoundBox
 return math.sqrt(sum(max(0,getattr(a,k+'Min')-getattr(b,k+'Max'),getattr(b,k+'Min')-getattr(a,k+'Max'))**2 for k in 'XYZ'))
def hits(s,margin=3):
 out=[]
 for n,t in obs.items():
  if lower(s,t)>=margin:continue
  d=s.distToShape(t)[0]
  if d<margin:out.append({'part':n,'distance_mm':d,'intersection_mm3':s.common(t).Volume if d<1e-5 else 0})
 return out
# Rounded nuts/terminals +strain allowance fit an intentionally conservative
# 40x40 footprint and85mm behind panel face; USB42x42x70.
layouts=[{'id':'SIX_SINGLE','count':6,'usb':False,'size':[276,76],'cells':[(i*42-105,0) for i in range(6)]},
 {'id':'FIVE_USB_SINGLE','count':5,'usb':True,'size':[276,76],'cells':[(i*42-105,0) for i in range(6)]},
 {'id':'FOUR_USB_SINGLE','count':4,'usb':True,'size':[234,76],'cells':[(i*42-84,0) for i in range(5)]},
 {'id':'SIX_DOUBLE','count':6,'usb':False,'size':[160,116],'cells':[(x,y) for y in [-21,21] for x in [-42,0,42]]},
 {'id':'FIVE_USB_DOUBLE','count':5,'usb':True,'size':[160,116],'cells':[(x,y) for y in [-21,21] for x in [-42,0,42]]},
 {'id':'FOUR_USB_DOUBLE','count':4,'usb':True,'size':[160,116],'cells':[(-42,-21),(0,-21),(-42,21),(0,21),(42,0)]}]
allrows=[]
for layout in layouts:
 w,h=layout['size'];rows=[]
 for yc in range(math.ceil(52+h/2),151,4):
  for xc in range(math.ceil(90+w/2),math.floor(510-w/2)+1,4):
   # structural exteriorbay margin≥30mm beyond rear of4mmfront capture.
   plate=box(xc-w/2,yc-h/2,8,w,h,12)
   solids=[plate]
   for i,(x,y) in enumerate(layout['cells']):
    usb=layout['usb'] and i==len(layout['cells'])-1
    size=42 if usb else 40;depth=70 if usb else 85
    solids.append(box(xc+x-size/2,yc+y-size/2,8,size,size,depth))
   blocked=hits(Part.makeCompound(solids));rows.append({'center_xy_mm':[xc,yc],'pass':not blocked,'blocked_by':blocked})
  if any(r['pass'] for r in rows):break
 allrows.append({**layout,'positions':rows,'passes':sum(r['pass'] for r in rows),'first_pass':next((r for r in rows if r['pass']),None)})
(O/'module-location-search.json').write_text(json.dumps({'planning':True,'obstacle_count':len(obs),'margin_mm':3,'minimum_recess_front_y_mm':52,'layouts':allrows},indent=2)+'\n')
print('V337_MODULE_SEARCH',[(r['id'],r['first_pass']) for r in allrows],flush=True)
