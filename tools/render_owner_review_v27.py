"""Sixteen owner-review states and a five-face penetration map from saved geometry."""
import csv,json,html,math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.patches import Rectangle,Circle,FancyBboxPatch,Polygon
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import proj3d
import numpy as np
from owner_review_scenes_v27 import scenes
from owner_features_v27 import config
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'exports/generated/review'
NOTICE='CERN-OHL-S-2.0 • Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet'
COLORS={'STRUCTURAL_WOOD':'#bb965f','LOCAL_METAL':'#698398','REMOVABLE_CARRIER':'#4c99ad','REMOVABLE_ADAPTER':'#4c99ad','ELECTRONICS_ZONE':'#729d8f','SSF_ZONE':'#b25c91','CONTROL_ZONE':'#df8643','ACCESS_ZONE':'#80a5c5','AIRFLOW_ROUTE':'#e0a620','REVIEW_STATE':'#5f849e'}

def main():
 OUT.mkdir(parents=True,exist_ok=True);report=json.loads((ROOT/'exports/generated/active-geometry-report.json').read_text());parts={p['name']:p for p in report['inventory']};c=config()
 indexes={n:str(i+1) for i,n in enumerate(parts)}
 listings=scenes(parts)
 # Only superseded files owned by the former active renderer are removed.
 for stem in ('01-exterior','02-rear-elevation','03-door-closed','04-door-open','05-pc-stowed','06-pc-extended','07-interior','09-rear-load-path','10-rear-utility-selected','11-utility-A','13-underside','14-material-roles'):
  (OUT/(stem+'.png')).unlink(missing_ok=True)
 for key,title,names,elev,azim,note in listings:
  if not names:continue
  fig=plt.figure(figsize=(15,10));ax=fig.add_subplot(111,projection='3d');points=[];labels=[];faces=[];facecolors=[]
  for n in dict.fromkeys(names):
   p=parts[n];v=np.asarray(p['mesh_vertices']);tri=np.asarray(p['mesh_triangles'],dtype=int)
   if len(tri)==0:continue
   role=p.get('role','LOCAL_METAL');color=COLORS.get(role,'#aab2ba');alpha=.9
   if n in ['CabinetLeftSide','CabinetRightSide','RearPanelWithCPUHatchV24'] or role in ['ACCESS_ZONE','ELECTRONICS_ZONE']:alpha=.20
   if n=='CapturedFrontPanelV20':alpha=.27
   if n=='CapturedBottomV20':alpha=.35
   if 'Display' in n:color='#477b99';alpha=.28
   if 'DoorOpen' in n or n=='BackboxServiceDoorV14':color='#dfad59';alpha=.65
   if 'Prop' in n or 'SafetyStayOpen' in n:color='#426785';alpha=.95
   if role=='SSF_ZONE':alpha=.65
   if key=='16-structural-exploded':
    cen=v.mean(0);v=v+np.array([(cen[0]-300)*.75,(cen[1]-650)*.3,(cen[2]-500)*.22])
   faces.extend(v[tri]);facecolors.extend([to_rgba(color,alpha)]*len(tri));points.extend(v.tolist())
   # Compact numbered keys avoid text overprinting; full names in HTML legends.
   if key not in ('01-full-exterior','09-airflow-path') and not n.startswith('Airflow'):labels.append((v.mean(0),indexes[n]))
  # Sort all triangles together: whole-object depth sorting can hide small
  # controls/trays behind a large perforated panel despite correct geometry.
  ax.add_collection3d(Poly3DCollection(faces,facecolors=facecolors,edgecolors=(.22,.29,.35,.2),linewidth=.12))
  v=np.asarray(points);lo=v.min(0);hi=v.max(0)
  ax.set_xlim(lo[0]-25,hi[0]+25);ax.set_ylim(lo[1]-25,hi[1]+25);ax.set_zlim(lo[2]-25,hi[2]+25);ax.set_box_aspect(hi-lo+50);ax.view_init(elev,azim)
  if key=='09-airflow-path':
   for route in c['airflow_review_routes_mm']:
    for p,q in zip(route,route[1:]):
     d=np.asarray(q)-np.asarray(p);ax.quiver(*p,*d,color='#d78b00',linewidth=3,arrow_length_ratio=.18)
  ax.set_xlabel('X / mm');ax.set_ylabel('Y → rear / mm');ax.set_zlabel('Z / mm');ax.set_title(title+'\nENGINEERING REVIEW — NOT MANUFACTURING RELEASE',fontsize=15)
  fig.canvas.draw();used=[]
  for pt,label in labels:
   xx,yy,_=proj3d.proj_transform(*pt,ax.get_proj());px,py=ax.transAxes.inverted().transform(ax.transData.transform((xx,yy)));py=max(.06,min(.94,py))
   tries=0
   while any(abs(px-x)<.03 and abs(py-y)<.027 for x,y in used) and tries<6:py+=.029;tries+=1
   used.append((px,py));ax.text2D(px,py,label,transform=ax.transAxes,fontsize=7,zorder=100,bbox=dict(facecolor='white',edgecolor='#777',alpha=.9,pad=.6))
  import textwrap
  fig.text(.045,.055,'\n'.join(textwrap.wrap(note,160)),fontsize=10);fig.text(.045,.015,NOTICE,fontsize=8)
  fig.savefig(OUT/(key+'.png'),dpi=150);plt.close(fig)
 # Bottom map is drawn from exact feature parameters with reserved hardware kept blank.
 def bottom(ax):
  ax.add_patch(Rectangle((12,12),576,1284.1,facecolor='#e8dac2',edgecolor='#555'))
  v=c['bottom_intake']
  for x in v['bank_center_x_mm']:
   for y in v['row_center_y_mm']:ax.add_patch(FancyBboxPatch((x-40,y-6),80,12,boxstyle='round,pad=0,rounding_size=6',facecolor='white',edgecolor='#225c6c'))
  for x,y in v['filter_mount_xy_mm']:ax.add_patch(Circle((x,y),2.25,color='#225c6c'))
  x,y,w,h=v['filter_outer_xy_mm'];ax.add_patch(Rectangle((x,y),w,h,fill=False,linestyle='--',edgecolor='#197d94',linewidth=2))
  for y in (260,650,1040):ax.add_patch(Rectangle((12,y),576,18,facecolor='#8d9caf',alpha=.5))
  for n,p in parts.items():
   if n.startswith(('ClassicLegBracket','CPURailBacking','RearCPUSupportRail')):
    x0,x1,y0,y1,z0,z1=p['bounds'];ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,facecolor='#d88473',alpha=.5,edgecolor='#934c3c',hatch='//'))
  ax.text(300,445,'18 × 80 × 12 slots\n18 mm row webs\n20 mm center spine',ha='center',fontsize=8,bbox=dict(facecolor='white',alpha=.9))
  ax.text(300,760,'Central service / future toys\nNo subwoofer opening\nNo SSF hole',ha='center',fontsize=8)
  ax.text(300,1150,'CPU rail/backing zone\nHF-026 holes BLOCKED',ha='center',fontsize=8)
  ax.set_xlim(-20,620);ax.set_ylim(-20,1330);ax.set_aspect('equal');ax.set_xlabel('X mm');ax.set_ylabel('Y → rear / mm');ax.set_title('BOTTOM — actual generic cuts, reserved hardware')
 fig,ax=plt.subplots(figsize=(8,13));bottom(ax);fig.text(.08,.025,'Mains entry remains on rear panel; no bottom mains penetration.\nFilter cassette removes from outside below the bottom. SSF couples into solid sidewalls.\n'+NOTICE,fontsize=8);fig.tight_layout(rect=(0,.07,1,1));fig.savefig(OUT/'05-bottom-penetration-map.png',dpi=160);plt.close(fig)
 # Dedicated five-face review: no guessed hardware pattern dots.
 fig,axs=plt.subplots(2,3,figsize=(19,13));bottom(axs[0,0]);cab=json.loads((ROOT/'config/cabinet_structure_v20.json').read_text())
 for ax,side in [(axs[0,1],'LEFT'),(axs[0,2],'RIGHT')]:
  ax.add_patch(Polygon([(0,0),(1308.1,0),(1308.1,596.9),(1127.125,596.9),(0,400.05)],facecolor='#e8dac2',edgecolor='#555'))
  for y,z in c['controls']['side_positions_yz_mm']:
   ax.add_patch(Circle((y,z),18,fill=False,edgecolor='#ce7031',linestyle='--'));ax.plot(y,z,'+',color='#b45c24')
  for q in cab['ssf_keepouts']['sidewall_exciter_zones_each_side']:
   y0,y1=q['y_mm'];z0,z1=q['z_mm'];ax.add_patch(Rectangle((y0,z0),y1-y0,z1-z0,facecolor='#c783af',alpha=.65));ax.text((y0+y1)/2,(z0+z1)/2,'SSF\nSOLID',ha='center',va='center',fontsize=8)
  for y in (18,1195.1):ax.add_patch(Rectangle((y,18),95,150,fill=False,edgecolor='#ad4834',hatch='//'))
  ax.add_patch(Rectangle((982,438),120,75,fill=False,edgecolor='#3376a2',hatch='..'))
  ax.plot([80,976.8],[330,330],color='#466f93',lw=2);ax.text(550,350,'Prop stow / HF-010 anchors blocked',ha='center',fontsize=8)
  ax.text(1035,530,'Pivot HF-008',ha='center',fontsize=8);ax.annotate('HF-020 centers\nbores BLOCKED',xy=(280,270),xytext=(250,115),ha='center',fontsize=8,arrowprops=dict(arrowstyle='-',color='#cc7335'))
  if side=='RIGHT':
   ax.add_patch(Rectangle((18,195),202,40,fill=False,edgecolor='#cf6c22'));ax.text(130,180,'Plunger body reserve',ha='center',fontsize=8)
  ax.set_xlim(-20,1330);ax.set_ylim(-20,650);ax.set_aspect('equal');ax.set_xlabel('Y mm');ax.set_ylabel('Z mm');ax.set_title(side+' SIDE — solid SSF skin / no final bores')
 ax=axs[1,0];ax.add_patch(Rectangle((0,0),600,400.05,facecolor='#e8dac2',edgecolor='#555'))
 ax.add_patch(Rectangle((175,90),250,210,facecolor='#8eb0bd',alpha=.7));ax.text(300,190,'COIN DOOR\nHF-019 BLOCKED',ha='center',fontsize=9)
 for b in c['controls']['front_buttons']:
  ax.add_patch(Circle((b['x'],b['z']),18,fill=False,edgecolor='#cc7335'));ax.text(b['x'],b['z']+23,b['name'],ha='center',fontsize=7)
 ax.add_patch(Rectangle((500,195),40,40,fill=False,edgecolor='#cc7335'));ax.text(520,180,'Plunger\nHF-030',ha='center',fontsize=8)
 ax.add_patch(Rectangle((50,315),500,65,fill=False,hatch='//'));ax.text(300,342,'Lockdown receiver / HF-022',ha='center',fontsize=8)
 ax.set_xlim(-20,620);ax.set_ylim(-20,430);ax.set_aspect('equal');ax.set_title('FRONT — human controls / lockdown');ax.set_xlabel('X mm');ax.set_ylabel('Z mm')
 ax=axs[1,1];ax.add_patch(Rectangle((12,0),576,596.9,facecolor='#e8dac2',edgecolor='#555'))
 for x,z,w,h,label in [(130,110,340,240,'CPU HATCH'),(60,405,70,50,'MAINS'),(518,413,24,24,'RJ45')]:ax.add_patch(Rectangle((x,z),w,h,facecolor='white',edgecolor='#476b7b'));ax.text(x+w/2,z+h/2,label,ha='center',fontsize=8)
 ax.add_patch(Rectangle((12,578.9),576,18,facecolor='#8297ac'));ax.text(300,545,'Rear shelf / backbox support\nHF-007 lock patterns blocked',ha='center',fontsize=8);ax.set_xlim(620,-20);ax.set_ylim(-20,630);ax.set_aspect('equal');ax.set_title('REAR — small utilities / CPU / support');ax.set_xlabel('X mm (rear view)');ax.set_ylabel('Z mm')
 axs[1,2].axis('off');axs[1,2].text(.02,.93,'FEATURE MAP KEY\n\nWhite openings: modeled generic wood cuts.\nOrange: ergonomic/control reserve, NOT bore.\nPink SSF: intact full-thickness plywood.\nRed hatch: leg/rail hardware reservation.\nBlue: pivot/support/airflow interfaces.\n\n18 bottom slots + externally serviced filter.\nNo bottom mains entry or subwoofer opening.\nNo electronics-specific permanent wood holes.\n\nActual buttons, plunger, props, legs and bearings\ncontrol their final hardware patterns.\n\nNOT FOR CNC PRODUCTION',va='top',fontsize=12)
 fig.suptitle('17 — Bottom / both sides / front / rear penetration and reservation review',fontsize=18);fig.tight_layout(rect=(0,.05,1,.95));fig.text(.02,.015,NOTICE,fontsize=9);fig.savefig(OUT/'17-five-face-feature-map.png',dpi=160);plt.close(fig)
 data=json.loads((ROOT/'exports/generated/owner-services-analysis.json').read_text());feat=list(csv.DictReader((ROOT/'bom/CNC_FEATURES_V25.csv').open()));counts={k:sum(f['status']==k for f in feat) for k in ('DEFINED_PARAMETRIC','BLOCKED_MEASURE_HARDWARE','BLOCKED_DESIGN')}
 page=['<!doctype html><meta charset="utf-8"><title>Owner engineering review v27</title><style>body{font:16px sans-serif;max-width:1450px;margin:30px;background:#f1eee6}img{width:100%}section{background:white;margin:24px 0;padding:18px}table{border-collapse:collapse}td{padding:5px;border-bottom:1px solid #ccc}nav{columns:2}</style><h1>Manual props / modular electronics / airflow / playable controls</h1><p>Owner-directed engineering review. No baseline gas assistance. 29 permanent structural wood records; 32 total wood records including two doors and CPU board. 11 replaceable carriers (including existing adapters), counted separately.</p>',f'<p>Feature groups: {counts}. Manufacturing ready: false. Estimated peak manual lift {data["lift"]["vertical_hand_force_peak_n"]:.1f} N; actual effort and independent prop proof still required.</p><nav>']
 for key,title,*_ in listings:page.append(f'<p><a href="#{key}">{key}: {html.escape(title)}</a></p>')
 page.append('<p><a href="#17-five-face-feature-map">17: Five-face penetration map</a></p></nav>')
 for key,title,names,elev,azim,note in listings:
  page.append(f'<section id="{key}"><h2>{key}: {html.escape(title)}</h2><p>{html.escape(note)}</p><img src="{key}.png" alt="{html.escape(title)}"><details><summary>Numbered object/part legend</summary><table>')
  for n in dict.fromkeys(names):page.append(f'<tr><td>{indexes[n]}</td><td>{html.escape(parts[n].get("part_id", ""))}</td><td>{html.escape(parts[n]["label"])}</td></tr>')
  page.append('</table></details></section>')
 page.append('<section id="17-five-face-feature-map"><h2>17: All five faces</h2><img src="17-five-face-feature-map.png" alt="Five-face penetration map"></section><p>'+NOTICE+'</p>')
 (OUT/'index.html').write_text('\n'.join(page));print('OWNER_REVIEW_PASS',OUT/'index.html')
if __name__=='__main__':main()
