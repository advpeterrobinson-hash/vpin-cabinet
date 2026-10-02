"""Actual B-rep-derived review views. CERN-OHL-S-2.0. Not CNC geometry."""
from pathlib import Path
import json,gzip,math,textwrap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parents[2];O=R/'exports/generated/flatpack-v331';D=json.loads((O/'manufacturing-register.json').read_text());L=json.loads((O/'preliminary-layout.json').read_text())
parts=D['parts'];by={p['instance_id']:p for p in parts};representatives=[by[f['instances'][0]] for f in D['families']]
with gzip.open(O/'review-mesh.json.gz','rt') as f:meshes=json.load(f)
views=[]
def color(p):return '#46788b' if p['material_class']=='STRUCTURAL_PREMIUM' else '#b97844'
def profile(ax,p):
 poly=np.array(p['review_outline']);ax.add_patch(Polygon(poly,closed=True,facecolor=color(p),edgecolor='#24434c',alpha=.32,lw=.6))
 for op in p['through_cuts']+p['pockets']:
  for wire in op.get('review_wires',[]):
   v=np.array(wire);ax.plot(v[:,0],v[:,1],color='#174e62' if op['group']=='CUT' else '#b75d16',lw=.6)
 for op in p['reference_features']:
  for b in op.get('bores',[]):
   if 'entry_local_xyz_mm' in b:ax.plot(*b['entry_local_xyz_mm'][:2],marker='+',markersize=3,color='#9b3e47')
 x0,y0,x1,y1=p['finished_xy_bounds_mm'];pad=max(x1-x0,y1-y0)*.08+2
 ax.set_xlim(x0-pad,x1+pad);ax.set_ylim(y1+pad,y0-pad);ax.set_aspect('equal');ax.axis('off')
 caption=p['instance_id']+' / '+p['manufacturing_part_id']+'\n'+p['source_component']+'\n'+f"{x1-x0:.2f} × {y1-y0:.2f}; stock {p['nominal_stock_thickness_mm']:g} / finished {p['finished_reference_thickness_mm']:.2f} mm"
 ax.set_title('\n'.join(textwrap.wrap(caption.split('\n')[1],33)).join([caption.split('\n')[0]+'\n','\n'+caption.split('\n')[2]]),fontsize=7.5,pad=2)
 if p['facing_reduction_mm']>.001:ax.set_title(ax.get_title()+f"\nFACE A reduction {p['facing_reduction_mm']:.2f} mm",fontsize=7.5,pad=2)
def atlas(n,title,items,cols=4):
 nr=math.ceil(len(items)/cols);fig=plt.figure(figsize=(cols*3.8,nr*3.5+1.1),facecolor='#f8fafb')
 for i,p in enumerate(items):ax=fig.add_subplot(nr,cols,i+1);profile(ax,p)
 fig.suptitle(n+'  '+title,x=.025,y=1-.15/(nr*3.5+1.1),ha='left',fontsize=16,fontweight='bold')
 fig.subplots_adjust(top=1-.9/(nr*3.5+1.1),bottom=.04,wspace=.3,hspace=.4)
 fig.text(.025,.008,'PRELIMINARY — NOT FOR CNC • FACE A • exact B-rep views, independent scales\nBlue: structural • ochre: secondary • CERN-OHL-S-2.0',fontsize=8)
 fig.savefig(O/(n+'-review.png'),dpi=145);plt.close(fig);views.append({'number':n,'title':title,'image':n+'-review.png','instances':[p['instance_id'] for p in items]})
def atlas3d(n,title,items,cols=7):
 nr=math.ceil(len(items)/cols);fig=plt.figure(figsize=(cols*3.15,nr*3.9+1.1),facecolor='#f8fafb')
 for i,p in enumerate(items):
  ax=fig.add_subplot(nr,cols,i+1,projection='3d');m=meshes[p['instance_id']];v=np.array(m['vertices']);faces=np.array(m['faces'])
  ax.add_collection3d(Poly3DCollection(v[faces],facecolor=color(p),edgecolor='none',alpha=.9))
  lo=v.min(0);hi=v.max(0);c=(hi+lo)/2;lim=(hi-lo).max()*.6
  ax.set_xlim(c[0]-lim,c[0]+lim);ax.set_ylim(c[1]-lim,c[1]+lim);ax.set_zlim(c[2]-lim,c[2]+lim);ax.set_box_aspect((1,1,1));ax.view_init(32,-55);ax.axis('off')
  ax.set_title(p['instance_id']+' / '+p['manufacturing_part_id']+'\n'+('Bore / partial bore present' if p['manual_finish'] else 'Unbored layer'),fontsize=9)
 fig.suptitle(n+'  '+title,fontsize=19,fontweight='bold',y=.98)
 fig.text(.025,.02,'ACTUAL CAD LAYERS — finished geometry shown; diagonal bores completed with guided manual drilling after lamination. PRELIMINARY — NOT FOR CNC.',fontsize=10)
 fig.subplots_adjust(top=.84,bottom=.1,wspace=.02);fig.savefig(O/(n+'-review.png'),dpi=145);plt.close(fig)
 views.append({'number':n,'title':title,'image':n+'-review.png','instances':[p['instance_id'] for p in items]})
select=lambda text:[p for p in parts if text in p['source_component']]
atlas('01','Complete flatpack inventory — canonical families',representatives,5)
atlas('02','18 mm structural stock members',[p for p in representatives if p['nominal_stock_thickness_mm']==18 and p['material_class']=='STRUCTURAL_PREMIUM'],5)
atlas('03','Modular / secondary-eligible members',[p for p in representatives if p['material_class']=='MODULAR_SECONDARY'])
atlas('04','Glass-retainer cap + reduced strip',select('GlassTopRetainer'),2)
atlas('05','Monitor stops — 18 + 12 mm planar lamination',select('MonitorStopBlock'),4)
atlas('06','Four cassette cleats — eight identical 12 mm layers',select('CassetteFixedCleat'),4)
atlas('07','Intake baffles — face, top and two returns',select('IntakeDownBaffle'),4)
atlas('08','Hinge cleats — 18 mm stock faced to 14 mm',select('HingeCleat'),2)
atlas3d('09','Front leg blocks — real seven-layer geometry',[p for p in parts if p['source_component'].startswith('CandidateLegBlockF')],7)
atlas3d('10','Rear leg blocks — split bore across L5 / L6',[p for p in parts if p['source_component'].startswith('CandidateLegBlockR')],7)
atlas('11','One-face pocket and reduction examples',[by[i] for i in ['P005-Main','P057-Main','P048-Main','P085-Reduced18']],4)
atlas('12','Manual drilling / countersink / bevel examples',[by[i] for i in ['P035-Main','P012-Main','P018-Main','P001-Main']],4)
atlas('13','R2 decisions — open radii, mating captures, hand-finished roots',[by[i] for i in ['P035-Main','P021-Main','P048-Main','P064-Base18']],4)
atlas('14','Largest manufacturing pieces',[by[x['instance']] for x in L['largest_parts'][:8]],4)
fig,axs=plt.subplots(3,2,figsize=(17,17));axs=np.ravel(axs)
for ax,sh in zip(axs,L['sheets']):
 ax.add_patch(Rectangle((0,0),2500,1600,fill=False,edgecolor='#243e4d'))
 ax.add_patch(Rectangle((20,20),2460,1560,fill=False,edgecolor='#b23c3c',linestyle='--',lw=.6))
 for p in sh['placements']:
  arr=np.array(p['finished_outline']);x0,y0,_,_=p['outline_local_bounds'];arr-=np.array([x0,y0])
  if p['rotation_deg']==90:arr=np.column_stack([arr[:,1],p['height_mm']-arr[:,0]])
  arr+=np.array([p['x_mm'],p['y_mm']]);ax.add_patch(Polygon(arr,closed=True,facecolor='#86a6b3' if p['material_class']=='STRUCTURAL_PREMIUM' else '#d2ae81',edgecolor='#24434c',lw=.3))
  if min(p['width_mm'],p['height_mm'])>24:ax.text(p['x_mm']+p['width_mm']/2,p['y_mm']+p['height_mm']/2,p['manufacturing_part_id'],ha='center',va='center',fontsize=5)
 ax.set_xlim(-20,2520);ax.set_ylim(1620,-20);ax.set_aspect('equal');ax.axis('off');ax.set_title(sh['sheet_id']+f" — {len(sh['placements'])} pieces; premium-first",fontsize=12)
for ax in axs[len(L['sheets']):]:ax.axis('off')
fig.suptitle('15  Preliminary sheet layout — NOT FOR CNC',fontsize=20,fontweight='bold');fig.text(.04,.02,'2500 × 1600 sheets • 20 mm border • >=15 mm boundary gap • row heuristic, NOT optimized • no final clearance / CAM / G-code',fontsize=11)
fig.tight_layout(rect=[0,.04,1,.95]);fig.savefig(O/'15-review.png',dpi=150);plt.close(fig);views.append({'number':'15','title':'Preliminary sheet feasibility','image':'15-review.png'})
offsets=json.loads((O/'exploded-transforms.json').read_text())
fig=plt.figure(figsize=(15,13));ax=fig.add_subplot(111,projection='3d');allv=[]
for p in parts:
 m=meshes[p['instance_id']];v=np.array(m['vertices']);mat=np.array(p['local_to_installed_matrix']).reshape(4,4)
 v=(np.column_stack([v,np.ones(len(v))])@mat.T)[:,:3];offset=np.array(offsets[p['instance_id']])
 v+=offset;allv.append(v);ax.add_collection3d(Poly3DCollection(v[np.array(m['faces'])],facecolor=color(p),edgecolor='none',alpha=.68))
v=np.concatenate(allv);lo=v.min(0);hi=v.max(0);center=(hi+lo)/2;d=(hi-lo).max()/2
ax.set_xlim(center[0]-d,center[0]+d);ax.set_ylim(center[1]-d,center[1]+d);ax.set_zlim(center[2]-d,center[2]+d);ax.set_box_aspect((1,1,1));ax.view_init(25,-58);ax.axis('off')
fig.suptitle('16  Manufacturing exploded wood only — review offsets',fontsize=20,fontweight='bold');fig.text(.05,.04,'Actual member B-reps; translations expose laminations. Installed equivalents remain in installed-members.FCStd. PRELIMINARY — NOT FOR CNC.',fontsize=10)
fig.savefig(O/'16-review.png',dpi=150);plt.close(fig);views.append({'number':'16','title':'Exploded wood-only members','image':'16-review.png'})
(O/'review-views.json').write_text(json.dumps(views,indent=2)+'\n')
print('FLATPACK_V331_REVIEW_VIEWS_PASS',len(views))
