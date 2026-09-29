"""Schematic blind-anchor layout. Original material: CERN-OHL-S-2.0."""
import hashlib,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'exports/generated/side-panel-v32'
r=json.loads((OUT/'anchorage-validation.json').read_text());c=r['config']
assert all(x['pass'] for x in r['checks'])
for n,h in r['source_hashes'].items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,n
assert hashlib.sha256((ROOT/r['saved_proposal']['path']).read_bytes()).hexdigest()==r['saved_proposal']['sha256']
m=json.loads((OUT/'motion-validation.json').read_text());b=m['scene_bounds_mm']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
fig=plt.figure(figsize=(13,10),facecolor='#f7f9fb');gs=fig.add_gridspec(2,1,height_ratios=[1.4,1],left=.08,right=.96,top=.85,bottom=.12,hspace=.38)
side=fig.add_subplot(gs[0]);section=fig.add_subplot(gs[1])
fig.suptitle('V32 | Replaceable support anchorage',x=.08,y=.975,ha='left',fontsize=21,fontweight='bold',color='#20354b')
fig.text(.08,.928,'SEPARATE PROPOSAL — two inward-facing anchors per support; blind inserts in each side.',fontsize=11)
fig.text(.08,.902,'Original V32 is unchanged. Nominal envelopes only; threads, plywood strength and machining remain unverified.',fontsize=10,color='#566574')
side.plot([0,1308.1,1308.1,1127.125,0,0],[0,0,596.9,596.9,400.05,0],color='#7e8c9b')
colors=['#176a9a','#167553','#a35d13']
for i,color in enumerate(colors,1):
 bb=b[f'SHELF_SUPPORT_{i}L'];side.add_patch(Rectangle((bb[2],bb[4]),bb[3]-bb[2],bb[5]-bb[4],facecolor=color,alpha=.3,edgecolor=color))
 for a in r['axes']:
  if a['support']==f'SHELF_SUPPORT_{i}L':
   _,y,z=a['xyz_mm'];side.add_patch(Circle((y,z),c['side_blind_bore_diameter_mm']/2,facecolor=color))
 side.text((bb[2]+bb[3])/2,bb[4]-14,f'S{i}: Y{bb[2]+55:g}/{bb[2]+125:g}\nZ{(bb[4]+bb[5])/2:g}',ha='center',va='top',color=color)
for y in (255,310):side.add_patch(Circle((y,270),14.2875,facecolor='none',edgecolor='#a5afb9'))
side.set_xlim(-20,1330);side.set_ylim(-10,630);side.set_aspect('equal');side.set_xlabel('Y (mm), front → rear');side.set_ylabel('Z (mm)');side.grid(alpha=.12)
side.set_title('Side elevation — 6 blind bores per side, mirrored about X300',loc='left',fontweight='bold')
a=r['axes'][0];_,y,z=a['xyz_mm'];bb=b['SHELF_SUPPORT_1L'];sb=b['SHELF_1'];support_width=a['support_inner_face_mm']-a['xyz_mm'][0]
wood='#dfbd8c';metal='#506b85';insert='#8771a8'
section.add_patch(Rectangle((0,z-24),18,60,facecolor=wood,edgecolor='#8c6944'))
section.add_patch(Rectangle((18,bb[4]),support_width,bb[5]-bb[4],facecolor='#bd8954',edgecolor='#845b32'))
section.add_patch(Rectangle((20,sb[4]),155,sb[5]-sb[4],facecolor=wood,edgecolor='#8c6944',alpha=.5))
section.add_patch(Rectangle((18-c['side_blind_depth_mm'],z-c['side_blind_bore_diameter_mm']/2),c['side_blind_depth_mm'],c['side_blind_bore_diameter_mm'],facecolor='white'))
section.add_patch(Rectangle((18,z-c['support_bore_diameter_mm']/2),support_width,c['support_bore_diameter_mm'],facecolor='white'))
section.add_patch(Rectangle((18-c['insert_length_mm'],z-c['insert_diameter_mm']/2),c['insert_length_mm'],c['insert_diameter_mm'],facecolor=insert))
section.add_patch(Rectangle((18-c['insert_length_mm'],z-c['shaft_diameter_mm']/2),c['insert_length_mm'],c['shaft_diameter_mm'],facecolor='white'))
section.add_patch(Rectangle((a['tip_x_mm'],z-c['shaft_diameter_mm']/2),c['shaft_length_mm'],c['shaft_diameter_mm'],facecolor=metal))
section.add_patch(Rectangle((a['support_inner_face_mm'],z-c['washer_diameter_mm']/2),c['washer_thickness_mm'],c['washer_diameter_mm'],facecolor=metal))
section.add_patch(Rectangle((a['head_start_x_mm'],z-c['head_diameter_mm']/2),c['head_length_mm'],c['head_diameter_mm'],facecolor=metal))
start=a['head_start_x_mm']+c['head_length_mm']
section.add_patch(Rectangle((start,z-c['driver_radius_mm']),c['driver_length_mm'],2*c['driver_radius_mm'],facecolor='#14998e',alpha=.1,edgecolor='#14998e',ls='--'))
section.annotate('',xy=(start+55,z),xytext=(start+2,z),arrowprops={'arrowstyle':'->','color':metal,'lw':2})
section.text(106,z-14,'55 mm screw withdrawal',ha='center',color=metal)
section.annotate('7.5 mm nominal\nouter skin',xy=(3.75,z),xytext=(25,z-30),arrowprops={'arrowstyle':'->','color':'#566574'},ha='center',fontsize=9)
section.text(125,z+26,'Shelf shown in installed position.\nRemove/unload it before releasing supports.',ha='center',fontsize=9)
section.set_xlim(-5,180);section.set_ylim(z-36,z+39);section.set_aspect('equal');section.set_xlabel('X (mm), outside at left → cabinet interior');section.set_ylabel('Z (mm)');section.grid(alpha=.1)
section.set_title('S1 left section — candidate shaft Ø5 ×50; insert Ø8 ×10; blind bore Ø8.5 ×10.5',loc='left',fontweight='bold',fontsize=10)
fig.text(.08,.059,'12 anchor withdrawals + 6 support replacement routes clear in the modeled teardown scene. Existing shelf release paths preserved.',fontsize=10,color='#20354b')
fig.text(.08,.031,'SCHEMATIC, NOT A FABRICATION DRAWING | CERN-OHL-S-2.0 | github.com/advpeterrobinson-hash/vpin-cabinet | CNC BLOCKED',fontsize=9,color='#566574')
fig.savefig(OUT/'06-shelf-anchorage.png',dpi=160,facecolor=fig.get_facecolor());print('SHELF_ANCHORAGE_RENDER_PASS')
