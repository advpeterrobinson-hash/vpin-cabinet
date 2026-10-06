"""Deterministic non-production rectangle MaxRects search with long-axis grain alignment."""
from pathlib import Path
import json
O=Path(__file__).resolve().parents[1]/'exports/generated/widebody-v351';rows=json.loads((O/'manufacturing-register.json').read_text())['parts'];old=json.loads((O/'nesting.json').read_text());out={}
def contains(a,b):return b[0]>=a[0] and b[1]>=a[1] and b[0]+b[2]<=a[0]+a[2]+1e-6 and b[1]+b[3]<=a[1]+a[3]+1e-6
def split(f,p):
 x,y,w,h=f;px,py,pw,ph=p
 if px>=x+w or py>=y+h or px+pw<=x or py+ph<=y:return [f]
 q=[]
 if px>x:q.append((x,y,px-x,h))
 if px+pw<x+w:q.append((px+pw,y,x+w-px-pw,h))
 if py>y:q.append((x,y,w,py-y))
 if py+ph<y+h:q.append((x,py+ph,w,y+h-py-ph))
 return q
for t in [18,12]:
 items=[]
 for a in rows:
  if a['nominal_stock_thickness_mm']!=t:continue
  b=a['finished_xy_bounds_mm'];w,h=b[2]-b[0],b[3]-b[1];items.append((a['instance_id'],max(w,h),min(w,h),w<h))
 trials=[]
 for strategy in ['area','length','width','perimeter']:
  key={'area':lambda a:a[1]*a[2],'length':lambda a:a[1],'width':lambda a:a[2],'perimeter':lambda a:a[1]+a[2]}[strategy];sheets=[]
  for name,w,h,rot in sorted(items,key=key,reverse=True):
   cand=[]
   for si,sh in enumerate(sheets):
    for f in sh['free']:
     if w+15<=f[2]+1e-6 and h+15<=f[3]+1e-6:cand.append((min(f[2]-w-15,f[3]-h-15),max(f[2]-w-15,f[3]-h-15),si,f))
   if not cand:sheets.append({'free':[(0,0,2475,1575)],'parts':[]});si=len(sheets)-1;f=sheets[si]['free'][0]
   else:_,_,si,f=min(cand)
   sh=sheets[si];pp=(f[0],f[1],w+15,h+15);free=[q for r in sh['free'] for q in split(r,pp)];sh['free']=[q for i,q in enumerate(free) if not any(i!=j and contains(r,q) and (r!=q or j<i) for j,r in enumerate(free))];sh['parts'].append({'instance':name,'x':20+f[0],'y':20+f[1],'w':w,'h':h,'rotated':rot})
  trials.append((len(sheets),strategy,sheets))
 count,st,sheets=min(trials,key=lambda x:(x[0],x[1]));checks=[]
 for sh in sheets:
  for i,a in enumerate(sh['parts']):
   checks.append(a['x']>=20 and a['y']>=20 and a['x']+a['w']<=2480.0001 and a['y']+a['h']<=1580.0001)
   for b in sh['parts'][i+1:]:checks.append(a['x']+a['w']+15<=b['x']+.0001 or b['x']+b['w']+15<=a['x']+.0001 or a['y']+a['h']+15<=b['y']+.0001 or b['y']+b['h']+15<=a['y']+.0001)
  sh['largest_free_reference_rectangles_mm']=sorted(sh.pop('free'),key=lambda r:r[2]*r[3],reverse=True)[:5]
 assert all(checks)
 d=old[str(t)];d.update(sheets=sheets,sheet_count=count,method='MaxRects best-short-side; four deterministic sorting trials; long part axis aligned to sheet long grain; no arbitrary structural90deg change',trials=[{'order':a,'sheets':n} for n,a,_ in trials],sheet_area_m2=count*4,usable_area_m2=count*2460*1560/1e6,unused_full_sheet_outer_m2=count*4-d['outer_contour_area_m2'],utilization_outer_percent=100*d['outer_contour_area_m2']/(count*4),grain='Long part axis aligned to2500mm sheet axis; supplier face-grain confirmation required. No production authorization.',checks=len(checks),**{"pass":True});out[str(t)]=d
(O/'nesting.json').write_text(json.dumps(out,indent=2)+'\n');print('V351 PRELIMINARY',[(t,d['sheet_count']) for t,d in out.items()])
