"""Offline orthographic rendering of V33.6 native CAD triangles. CERN-OHL-S-2.0."""
from pathlib import Path
import json,gzip,textwrap,html
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import to_rgb
from matplotlib.patches import FancyBboxPatch
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/monitor-support-v336';scenes=json.loads(gzip.decompress((O/'review-scenes.json.gz').read_bytes()));gallery=[]
def draw(ax,p):
 normal=np.array(p['view'],float);normal/=np.linalg.norm(normal);up=np.array([0,0,1.])
 if abs(normal@up)>.99:up=np.array([0,1.,0])
 right=np.cross(up,normal);right/=np.linalg.norm(right);up=np.cross(normal,right);rot=np.array([right,up,normal]).T
 polys=[];colors=[];depths=[];allpoints=[]
 for m in p['meshes']:
  pts=np.array(m['vertices'])@rot;f=np.array(m['faces']);poly=pts[f];allpoints.extend(pts[:,:2]);color=np.array(to_rgb(m['color']))
  norms=np.cross(poly[:,1]-poly[:,0],poly[:,2]-poly[:,0]);ln=np.linalg.norm(norms,axis=1);shade=.65+.33*np.abs(norms[:,2]/np.maximum(ln,1e-10))
  polys.extend(poly[:,:,:2]);depths.extend(poly[:,:,2].mean(axis=1));colors.extend(np.column_stack((np.clip(color[None,:]*shade[:,None],0,1),np.full(len(poly),m.get('alpha',1)))))
 points=np.array(allpoints);lo=points.min(axis=0);hi=points.max(axis=0);pad=max(hi-lo)*.075
 if p.get('limits'):
  x0,x1,y0,y1=p['limits']
 else:x0,x1,y0,y1=lo[0]-pad,hi[0]+pad,lo[1]-pad,hi[1]+pad
 ax.set_xlim(x0,x1);ax.set_ylim(y0,y1)
 # Per-pixel depth buffer: triangle-centroid painters fail for a large display
 # behind small carriers. These are the same native CAD triangles, unchanged.
 aspect=(x1-x0)/(y1-y0);height=1000;width=max(100,min(1800,round(height*aspect)))
 rgb=np.ones((height,width,3))*np.array(to_rgb('#f4f6f7'));zbuf=np.full((height,width),-np.inf)
 triangles=[]
 for m in p['meshes']:
  pts=np.array(m['vertices'])@rot;f=np.array(m['faces']);poly=pts[f];color=np.array(to_rgb(m['color']))
  norms=np.cross(poly[:,1]-poly[:,0],poly[:,2]-poly[:,0]);ln=np.linalg.norm(norms,axis=1);shade=.65+.33*np.abs(norms[:,2]/np.maximum(ln,1e-10))
  for j,q in enumerate(poly):triangles.append((q,np.clip(color*shade[j],0,1),m.get('alpha',1)))
 opaque=[t for t in triangles if t[2]>=.999];transparent=sorted([t for t in triangles if t[2]<.999],key=lambda t:t[0][:,2].mean())
 for q,color,alpha in opaque+transparent:
  xx=(q[:,0]-x0)/(x1-x0)*width;yy=(q[:,1]-y0)/(y1-y0)*height
  lx=max(0,int(np.floor(xx.min())));hx=min(width-1,int(np.ceil(xx.max())))
  ly=max(0,int(np.floor(yy.min())));hy=min(height-1,int(np.ceil(yy.max())))
  if lx>hx or ly>hy:continue
  den=(yy[1]-yy[2])*(xx[0]-xx[2])+(xx[2]-xx[1])*(yy[0]-yy[2])
  if abs(den)<1e-9:continue
  X,Y=np.meshgrid(np.arange(lx,hx+1)+.5,np.arange(ly,hy+1)+.5)
  b0=((yy[1]-yy[2])*(X-xx[2])+(xx[2]-xx[1])*(Y-yy[2]))/den
  b1=((yy[2]-yy[0])*(X-xx[2])+(xx[0]-xx[2])*(Y-yy[2]))/den;b2=1-b0-b1
  zz=b0*q[0,2]+b1*q[1,2]+b2*q[2,2];z=zbuf[ly:hy+1,lx:hx+1]
  mask=(b0>=-1e-8)&(b1>=-1e-8)&(b2>=-1e-8)&(zz>z+1e-7)
  if not mask.any():continue
  tile=rgb[ly:hy+1,lx:hx+1]
  tile[mask]=tile[mask]*(1-alpha)+color*alpha
  if alpha>=.999:z[mask]=zz[mask]
 ax.imshow(rgb,extent=(x0,x1,y0,y1),origin='lower',interpolation='bilinear')
 for e in p.get('edges',[]):
  for line in e['lines']:
   pp=np.array(line)@rot;ax.plot(pp[:,0],pp[:,1],color=e['color'],lw=e.get('width',1),linestyle=e.get('style','-'),zorder=5)
 for ann in p.get('annotations',[]):
  xy=np.array(ann['point'])@rot;ax.annotate(ann['text'],xy[:2],xytext=ann.get('offset',[20,20]),textcoords='offset points',fontsize=10,color='#173948',bbox={'boxstyle':'round,pad=.35','fc':'#ffffff','ec':'#778b93','alpha':.92},arrowprops={'arrowstyle':'-','color':'#355964'},zorder=8)
 ax.set_aspect('equal');ax.axis('off')
def diagram(ax):
 ax.set_xlim(0,100);ax.set_ylim(0,100);ax.axis('off')
 blocks=[(3,70,28,22,'HISTORICAL NOTCH\nY89 / Y127 + horned M025\nnotch-floor-fans-v32','#f2d5c5'),(36,70,28,22,'INHERITED B-REP\nBackbox integration → V33.5\nPF geometry protected unchanged','#f2d5c5'),(69,70,28,22,'INHERITED DISPLAY\nViewer meshes / saved states\nAnimation reused old silhouette','#f2d5c5'),(3,23,28,28,'V33.6 AUTHORITY\nOwner Y255 / Y310, Z270\nClean prior base recovered\nFunctional support openings','#d7e9e5'),(36,23,28,28,'CANONICAL NATIVE CAD\nNew play / service B-reps\nGeometry + motion gates\nHardware bores stay HOLD','#d7e9e5'),(69,23,28,28,'REGENERATED OUTPUTS\nManufacturing pieces / BOM\nViewer / animation meshes\nPer-object geometry authority','#d7e9e5')]
 for x,y,w,h,t,c in blocks:
  ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.4,rounding_size=1',facecolor=c,edgecolor='#536b76',linewidth=1.2));ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=10.5,color='#203c49',linespacing=1.7)
 for a,b in [((31,81),(36,81)),((64,81),(69,81)),((31,37),(36,37)),((64,37),(69,37)),((17,70),(17,51))]:ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','lw':2,'color':'#536b76'})
 ax.text(50,9,'CANONICAL CORRECTION FIRST  →  GENERATED ARTIFACTS SECOND',ha='center',fontsize=12,color='#203c49')
for s in scenes:
 fig=plt.figure(figsize=(15,10),facecolor='#f4f6f7');fig.text(.035,.953,'V33.6 / '+s['id']+'  ·  NATIVE CAD REVIEW',fontsize=11,color='#55717b');fig.text(.035,.910,s['title'],fontsize=20,color='#223d49')
 if s.get('diagram'):diagram(fig.add_axes([.035,.19,.93,.67]))
 else:
  n=len(s['panels']);gap=.04;width=(.93-gap*(n-1))/n
  for i,p in enumerate(s['panels']):
   ax=fig.add_axes([.035+i*(width+gap),.20,width,.64]);draw(ax,p);ax.set_title(p['label'],fontsize=12,color='#294450',pad=12)
 if s.get('legend'):fig.text(.035,.157,'   |   '.join(s['legend']),fontsize=10,color='#365865')
 fig.text(.035,.105,'\n'.join(textwrap.wrap(s['note'],145)),fontsize=11,color='#314c58',linespacing=1.4)
 fig.text(.035,.025,'NOT FOR CNC · actual plywood / coupon / purchased hardware remain pending · dimensions in mm',fontsize=10,color='#884d35')
 file=s['id']+'-review.png';fig.savefig(O/file,dpi=145);plt.close(fig);gallery.append({'image':file,'title':s['title'],'note':s['note'],'native_cad':not s.get('diagram',False)})
(O/'review-index.json').write_text(json.dumps(gallery,indent=2)+'\n')
h='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V33.6 CAD review</title><style>body{font:16px system-ui;margin:24px;background:#edf1f3;color:#253d48}article{background:white;padding:18px;margin:24px 0;max-width:1450px}img{width:100%;height:auto}p{max-width:1100px;line-height:1.6}</style><h1>V33.6 — Native CAD review</h1><p>20 CAD views and one source-authority diagram. Full-sheet release remains blocked. Central backbox service-window candidate is held, not promoted. <a href="README.md">Report</a></p>'
for g in gallery:h+=f'<article><h2>{html.escape(g["title"])}</h2><img loading="lazy" src="{g["image"]}" alt="{html.escape(g["title"])}"><p>{html.escape(g["note"])}</p></article>'
(O/'review.html').write_text(h+'</html>');print('V336_REVIEW_RENDER_PASS',len(gallery))
