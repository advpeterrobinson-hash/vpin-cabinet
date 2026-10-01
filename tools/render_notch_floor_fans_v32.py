"""Ten new engineering review images from actual V32 CAD meshes. CERN-OHL-S-2.0."""
from pathlib import Path
import json,math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Rectangle,Circle
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/notch-floor-fans-v32';bundle=json.loads((O/'mesh.json').read_text());parts={p['name']:p for p in bundle['parts']};before={p['name']:p for p in json.loads((O/'before.json').read_text())['parts']};review=bundle['review'];n=review['notch'];f=review['floor_fans'];alpha=math.radians(review['closed_slope_deg']);bz=400.05+45*math.tan(alpha)-12-55*math.cos(alpha)
def local(v):x,y,z=v;y-=45;z-=bz;return [x,y*math.cos(alpha)+z*math.sin(alpha),-y*math.sin(alpha)+z*math.cos(alpha)]
def color(name):
 if 'Reserve' in name:return '#b5b5cd'
 if 'LeafButton' in name:return '#176eaa' if 'primary' in name else '#b75022'
 if name.startswith('SSF_'):return '#d98a48'
 if name.startswith('PC_'):return '#548c70'
 if 'Fan' in name or 'Filter' in name:return '#718797'
 if any(k in name for k in ['Strap','Screw','Bolt','Nut','LeafBracket','LeafContacts']):return '#83939d'
 return '#ddc79f'
def polys(p,transform=None):
 v=[transform(a) for a in p['vertices']] if transform else p['vertices'];return [[v[i] for i in face] for face in p['faces']]
def draw2(ax,p,c=None,alpha=1,transform=None):ax.add_collection(PolyCollection([[(v[0],v[1]) for v in poly] for poly in polys(p,transform)],facecolor=c or color(p['name']),edgecolor='none',alpha=alpha))
def crop(poly,axis,lo,hi):
 for bound,sign in [(lo,1),(hi,-1)]:
  out=[]
  for a,b in zip(poly,poly[1:]+poly[:1]):
   ai,bi=(a[axis]-bound)*sign>=0,(b[axis]-bound)*sign>=0
   if ai:out.append(a)
   if ai!=bi:
    t=(bound-a[axis])/(b[axis]-a[axis]);out.append([a[k]+t*(b[k]-a[k]) for k in range(3)])
  poly=out
  if not poly:break
 return poly

def draw3(ax,names,clips=None,opacity=None):
 for name in names:
  if name not in parts:continue
  ps=polys(parts[name]);clean=[]
  for p in ps:
   if clips:
    for axis,(lo,hi) in clips.items():p=crop(p,axis,lo,hi) if p else []
   if len(p)>2:clean.append(p)
  if clean:ax.add_collection3d(Poly3DCollection(clean,facecolor=color(name),edgecolor='none',alpha=(opacity or {}).get(name,1)))
def setup2(ax,x,y):ax.set(xlim=x,ylim=y,xlabel='X · mm',ylabel='Y · mm');ax.set_aspect('equal');ax.grid(alpha=.15)
def setup3(ax,x,y,z,elev,azim):ax.set(xlim=x,ylim=y,zlim=z);ax.set_box_aspect((x[1]-x[0],y[1]-y[0],z[1]-z[0]));ax.view_init(elev=elev,azim=azim);ax.set_axis_off()
def save(fig,name,title):
 fig.suptitle(title,fontsize=14);fig.text(.025,.025,'Actual FreeCAD meshes · provisional cutter / selected hardware pending · manufacturing BLOCKED\nCERN-OHL-S-2.0 · Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet',fontsize=8);fig.savefig(O/name,dpi=150);plt.close(fig);print('REVIEW_IMAGE',name,flush=True)
# 01: full top and enlarged button edge. All geometry is transformed to the existing board datum.
fig,(ax,z)=plt.subplots(1,2,figsize=(12,10));draw2(ax,parts['PF_BasePlywood'],transform=local);setup2(ax,(0,600),(0,1070));ax.set_title('TOP · one flat plywood base')
for name in ['PF_BasePlywood']+[name for name in parts if name.startswith('Leaf')]:draw2(z,parts[name],transform=local)
setup2(z,(0,110),(10,155));z.set_title('LEFT EDGE · right mirrored');z.annotate('22 mm relief · R8\n102.961 mm longitudinal',xy=(72,72),xytext=(5,140),arrowprops={'arrowstyle':'->'},fontsize=10);ax.text(130,520,'456 mm minimum central section\n18 mm plywood',fontsize=10)
save(fig,'01-playfield-notch-top.png','V32 · PLAYFIELD BUTTON CLEARANCE · TOP')
# 02: underside of the full accepted playfield unit; only its base outline changes.
fig=plt.figure(figsize=(12,9));ax=fig.add_axes([.04,.09,.92,.82],projection='3d');names=['PF_BasePlywood','PF_WoodDowel','PF_VESAEnvelope']+[k for k in parts if k.startswith(('PF_CommercialStrap','PF_StrapScrew'))];draw3(ax,names);setup3(ax,(0,600),(20,1100),(300,600),-35,-55);fig.text(.06,.86,'Symmetric rounded side reliefs\nVESA / four straps / dowel unchanged',fontsize=11);save(fig,'02-playfield-notch-underside.png','V32 · PLAYFIELD PLYWOOD · UNDERSIDE')
# 03/04: body, leaf contacts, wiring and a 20 mm driver/finger approach allowance.
for side,num in [('L',3),('R',4)]:
 fig=plt.figure(figsize=(12,8));ax=fig.add_axes([.03,.15,.62,.66],projection='3d');names=['PF_BasePlywood']+[k for k in parts if k.startswith('Leaf') and k.endswith('_'+side)]+[k for k in parts if k.startswith(('ButtonWireService','ButtonToolService')) and k.endswith('_'+side)];opacity={k:.2 for k in names if 'Reserve' in k};draw3(ax,names,{1:(55,175)},opacity);setup3(ax,(-8,145) if side=='L' else (455,608),(55,175),(300,390),-24,-60 if side=='L' else -120)
 inset=fig.add_axes([.70,.27,.27,.50]);
 for name in ['PF_BasePlywood']+[name for name in parts if name.startswith('Leaf') and name.endswith('_'+side)]:draw2(inset,parts[name],transform=local)
 for name in names:
  if 'Wire' in name:draw2(inset,parts[name],alpha=.25,transform=local)
 setup2(inset,(0,100) if side=='L' else (500,600),(20,135));inset.set_title('LOCAL TOP / WIRE ALLOWANCE',fontsize=10)
 rows=[r for r in n['clearances'] if r['side']==side];fig.text(.03,.86,'Primary body: 20 → 24.950 mm   ·   secondary: 20 → 34.533 mm\nWire allowance: overlap → 6.009 / 10 mm   ·   tool probe: overlap → 1.894 / 2 mm',fontsize=11);fig.text(.04,.09,'Translucent volumes are provisional service allowances, not unselected hardware machining dimensions.',fontsize=9);save(fig,f'{num:02d}-{ "left" if side=="L" else "right"}-button-clearance.png',f'V32 · {"LEFT" if side=="L" else "RIGHT"} BUTTON / LEAF / WIRE / TOOL CLEARANCE')
# 05: before and after profiles, same scale, both mirrored notches visible.
fig,axes=plt.subplots(1,3,figsize=(14,8))
for ax,p,title in [(axes[0],before['PF_BasePlywood'],'BEFORE · straight edge'),(axes[1],parts['PF_BasePlywood'],'AFTER · rounded clearance')]:draw2(ax,p,transform=local);setup2(ax,(30,100),(10,145));ax.set_title(title)
draw2(axes[2],before['PF_BasePlywood'],'#e69f00',transform=local);draw2(axes[2],parts['PF_BasePlywood'],transform=local);setup2(axes[2],(30,100),(10,145));axes[2].set_title('REMOVED AREA · orange');save(fig,'05-notch-before-after.png','V32 · NOTCH BEFORE / AFTER · LEFT SHOWN, RIGHT EXACTLY MIRRORED')
# 06: top of floor stations without overhead parts hiding them.
fig,ax=plt.subplots(figsize=(10,10));draw2(ax,parts['FLOOR']);
for side in ['L','R']:draw2(ax,parts['FloorIntakeFan'+side]);cx,cy,_=f['stations'][0 if side=='L' else 1]['center_xyz_mm'];ax.text(cx,cy+80,'120 mm INTAKE '+side,ha='center',fontsize=10)
setup2(ax,(0,600),(18,1295));ax.set_title('Centers remain X150 / X450, Y710\nØ116 openings · 105 mm mounting pitch');save(fig,'06-floor-fan-top.png','V32 · TWO ACTIVE FLOOR FAN STATIONS · TOP')
# 07: actual floor/frame fasteners, commercial media/guard envelopes drawn as dashed allowances.
fig,ax=plt.subplots(figsize=(12,7))
for side in ['L','R']:
 draw2(ax,parts['FloorIntakeFan'+side]);draw2(ax,parts['RemovableIntakeFilter'+side])
 for name in parts:
  if name.startswith(('FloorFilterScrew'+side,'FloorFanBolt'+side,'FloorFanNut'+side)):draw2(ax,parts[name],'#4a4a4a')
 row=f['stations'][0 if side=='L' else 1];cx,cy,_=row['center_xyz_mm'];ax.text(cx,cy,'Ø116\nMEDIA / GUARD\nALLOWANCE',ha='center',va='center',fontsize=10)
 ax.annotate('Separate filter screws',xy=(cx+70,cy+70),xytext=(cx-55,cy+100),arrowprops={'arrowstyle':'->'},fontsize=9)
 ax.add_patch(Rectangle((cx-85,cy-85),170,170,fill=False,ec='#20313c',lw=1.5))
setup2(ax,(50,550),(595,830));fig.text(.03,.88,'170 × 170 × 8 mm removable frames · separate M4 fixings · fan stays installed',fontsize=11);fig.text(.03,.10,'Actual underside frame projection · 80 mm downward withdrawal; Ø12 passages clear stationary fan nuts.\nReplaceable media and independent ordinary commercial guard attach to the removable frame; purchased hardware pending.',fontsize=10);save(fig,'07-floor-fan-underside-filters.png','V32 · FLOOR UNDERSIDE / INDEPENDENT FILTERS')
# 08: plan clearances, shelf overhead shown by dashed line rather than obscuring components.
fig,ax=plt.subplots(figsize=(11,10));draw2(ax,parts['FLOOR']);
for name in ['SSF_Subwoofer_DCS165_Reference','SSF_BST_Carrier','SSF_BST1_Reference','PC_BASE','PC_ENVELOPE','FloorIntakeFanL','FloorIntakeFanR']:draw2(ax,parts[name])
for name in ['SHELF_1','SHELF_2','SHELF_3']:
 v=parts[name]['vertices'];x0,x1=min(vv[0] for vv in v),max(vv[0] for vv in v);y0,y1=min(vv[1] for vv in v),max(vv[1] for vv in v);ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,fill=False,ls='--',ec='#20313c'));ax.text(x0+5,y0+10,name+' overhead',fontsize=8)
setup2(ax,(0,600),(18,1300));fig.text(.69,.54,'Fan envelope clearances\nSubwoofer: 144.973 mm\nBST carrier: 300 mm\nPCBase: 60 mm\nS2 above: 119 mm\nImmediate outlet blockage: 0%\nS2 projected overlap: 55.48%',fontsize=10);save(fig,'08-floor-fan-equipment-clearance.png','V32 · FANS / SUBWOOFER / BST / LOW PCBASE')
# 09: geometric flow corridors. They are diagnostic lines, not ducts or a thermal adequacy certificate.
fig=plt.figure(figsize=(12,10));ax=fig.add_axes([.03,.08,.94,.82],projection='3d',computed_zorder=False);names=['FLOOR','SIDE_R','REAR','FRONT','SHELF_1','SHELF_2','SHELF_3','PC_BASE','PC_ENVELOPE','SSF_Subwoofer_DCS165_Reference','SSF_BST_Carrier','SSF_BST1_Reference','FloorIntakeFanL','FloorIntakeFanR','FAN_230','FAN_370','PF_OpenCradleL','PF_OpenCradleR'];draw3(ax,names,opacity={'SIDE_R':.10,'FRONT':.10,'FLOOR':.35,'REAR':.25,'SHELF_1':.25,'SHELF_2':.25,'SHELF_3':.25})
for row in f['thermal']:
 route=row['airflow_approach_route_xyz_mm'];xs,ys,zs=zip(*route);ax.plot(xs,ys,zs,color='#0072b2',lw=3,zorder=100);cx,cy,_=f['stations'][0 if row['side']=='L' else 1]['center_xyz_mm'];ax.quiver(cx,cy,-20,0,0,100,color='#0072b2',arrow_length_ratio=.2,zorder=100);ex=230 if row['side']=='L' else 370;ax.quiver(ex,1250,500,0,110,0,color='#20313c',arrow_length_ratio=.2,zorder=100)
setup3(ax,(0,600),(0,1380),(-40,650),27,-135);fig.text(.04,.85,'2 × 120 mm floor INTAKE + 2 × 120 mm rear EXHAUST\nIntake / exhaust gross aperture area: 21,136.635 mm² each',fontsize=11);fig.text(.04,.09,'Geometric corridors only · no duct added · thermal adequacy NOT certified\nLater analytical gate: fan curves, filter pressure drop, PC / PSU / amplifier heat and warm ambient.',fontsize=9);save(fig,'09-full-cabinet-airflow-path.png','V32 · ANALYTICAL AIRFLOW PACKAGING SCREEN')
# 10: same XY window and scale. Only the floor stations and obsolete filter mounts change.
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(13,7))
for ax,p,title in [(ax1,before['FLOOR'],'BEFORE · 2 × 100 × 160 R3 passive slots'),(ax2,parts['FLOOR'],'AFTER · 2 × Ø116 + 8 mounting holes')]:draw2(ax,p);setup2(ax,(60,540),(605,815));ax.set_title(title,fontsize=11)
for row in f['stations']:
 cx,cy,_=row['center_xyz_mm']
 for dx in [-70,70]:
  for dy in [-70,70]:ax2.add_patch(Circle((cx+dx,cy+dy),3,fill=False,ec='#20313c',ls='--'))
fig.text(.05,.17,'Dashed Ø6 marks: 8 mm blind filter-insert pockets from UNDERSIDE only; 10 mm floor skin retained.\nAll subwoofer / BST / PC anchor cuts retained. Minimum opening-to-fan-hole web: 13.996 mm.',fontsize=10);save(fig,'10-floor-before-after.png','V32 · FLOOR MACHINING BEFORE / AFTER')
