"""Orthographic review renderings from CAD tessellation, plus unlocated control schematic.
CERN-OHL-S-2.0. Rendering is not manufacturing authority.
"""
from pathlib import Path
import json,gzip,math,textwrap
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import to_rgb
from matplotlib.patches import Rectangle,Circle
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/structural-v335';scenes=json.loads(gzip.decompress((O/'review-scenes.json.gz').read_bytes()));gallery=[]
for scene in scenes:
 fig=plt.figure(figsize=(14,9),facecolor='#f7f8f9');ax=fig.add_axes([.035,.16,.93,.72]);ax.set_aspect('equal');ax.axis('off')
 fig.text(.035,.95,'V33.5 / '+scene['id'],fontsize=12,color='#425464');fig.text(.035,.91,scene['title'],fontsize=20,color='#23323d')
 if scene.get('schematic'):
  ax.add_patch(Rectangle((0,0),220,55,facecolor='#dac5a8',edgecolor='#263743'))
  for x,label,r in [(30,'MASTER\nVOLUME',9),(85,'OFF / AUDIO /\nPINBALL',9),(140,'BLUETOOTH\nPAIR',6)]:
   ax.add_patch(Circle((x,34),r,facecolor='#e8eef1',edgecolor='#263743'));ax.text(x,12,label,ha='center',va='center',fontsize=10)
  ax.add_patch(Rectangle((186,31),12,6,facecolor='#e8eef1',edgecolor='#263743'));ax.text(192,12,'USB-C\nOPTIONAL',ha='center',va='center',fontsize=10)
  ax.set_xlim(-10,230);ax.set_ylim(-15,70);ax.text(110,-10,'SYMBOL POSITIONS ONLY — NO INSTALLED COORDINATES',ha='center',fontsize=11)
 else:
  normal=np.array(scene['view'],dtype=float);normal/=np.linalg.norm(normal);up=np.array([0,0,1.])
  if abs(normal@up)>.99:up=np.array([0,1.,0])
  right=np.cross(up,normal);right/=np.linalg.norm(right);up=np.cross(normal,right);rot=np.array([right,up,normal]).T
  polys=[];cols=[];depth=[];allpts=[]
  for m in scene['meshes']:
   pts=np.array(m['vertices'])@rot;faces=np.array(m['faces']);poly=pts[faces];allpts.extend(pts[:,:2]);color=np.array(to_rgb(m['color']))
   e1=poly[:,1]-poly[:,0];e2=poly[:,2]-poly[:,0];norm=np.cross(e1,e2);ln=np.linalg.norm(norm,axis=1);shade=.62+.36*np.abs(norm[:,2]/np.maximum(ln,1e-10))
   polys.extend(poly[:,:,:2]);depth.extend(poly[:,:,2].mean(axis=1));cols.extend(np.clip(color[None,:]*shade[:,None],0,1))
  ix=np.argsort(depth);pc=PolyCollection([polys[i] for i in ix],facecolors=[cols[i] for i in ix],edgecolors='none',linewidths=0);ax.add_collection(pc)
  points=np.array(allpts);lo=points.min(axis=0);hi=points.max(axis=0);pad=max(hi-lo)*.045;ax.set_xlim(lo[0]-pad,hi[0]+pad);ax.set_ylim(lo[1]-pad,hi[1]+pad)
 if scene['id']=='04':
  ax.set_xlim(-5,100);ax.set_ylim(-5,65)
 fig.text(.035,.085,'\n'.join(textwrap.wrap(scene['note'],138)),fontsize=11,color='#273f50');fig.text(.035,.025,'NOMINAL ENGINEERING REVIEW · NOT FOR CNC · physical hardware/material/coupon pending',fontsize=10,color='#81472b')
 file=scene['id']+'-review.png';fig.savefig(O/file,dpi=140);plt.close(fig);gallery.append({'image':file,'title':scene['title'],'note':scene['note']})
(O/'review-index.json').write_text(json.dumps(gallery,indent=2)+'\n')
html='<!doctype html><meta charset="utf-8"><title>V33.5 CAD review</title><style>body{font:16px system-ui;margin:25px;background:#eef1f3}img{width:100%;max-width:1300px}article{background:white;padding:18px;margin:24px 0}</style><h1>V33.5 — CAD review</h1><p>Nominal preparation only. CNC release blocked. <a href="README.md">Report</a></p>'
for g in gallery:html+=f'<article><h2>{g["title"]}</h2><img src="{g["image"]}"><p>{g["note"]}</p></article>'
(O/'review.html').write_text(html);print('V335_RENDER_PASS',len(gallery))
