"""Actual CAD mesh review of straight support and moved exciters. CERN-OHL-S-2.0."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/wood-dowel-pivot-v32'
b=json.loads((O/'mesh.json').read_text());parts={p['name']:p for p in b['parts']};old={p['name']:p for p in json.loads((O/'cradle-profile-before-cleanup.json').read_text())['parts']};m=b['review']['support_mounting'];py,pz=b['review']['pivot_xyz_mm'][1:]
def draw(ax,p,color,alpha=1):
 vs=p['vertices'];ax.add_collection(PolyCollection([[(vs[i][1],vs[i][2]) for i in f] for f in p['faces']],facecolor=color,edgecolor='none',alpha=alpha))
def setup(ax,x,y):ax.set(xlim=x,ylim=y,xlabel='Y · mm',ylabel='Z · mm');ax.set_aspect('equal');ax.grid(alpha=.15)
def save(fig,name):
 fig.text(.03,.025,'Actual FreeCAD meshes · left / right mirrored · no manufacturing approval\nCERN-OHL-S-2.0 · Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet',fontsize=8);fig.savefig(O/name,dpi=160);plt.close(fig)
fig,(ax,zoom)=plt.subplots(1,2,figsize=(12,9));draw(ax,parts['PF_OpenCradleL'],'#dec498');setup(ax,(990,1090),(20,530));ax.set_title('FINAL · one straight rear edge\nOne CNC plywood solid')
draw(zoom,parts['PF_OpenCradleL'],'#dec498');draw(zoom,parts['PF_WoodDowel'],'#997046');setup(zoom,(990,1082),(450,530));zoom.set_title('UNCHANGED OPEN U / Ø32 DOWEL')
zoom.annotate('Minimum ligament 8.25 mm',xy=(1014.5,pz+.5),xytext=(1017,456),arrowprops={'arrowstyle':'->'},fontsize=10)
fig.suptitle('V32 · FINAL CRADLE · EXCITER NOTCH REMOVED');save(fig,'04-final-cradle-close.png')
fig,ax=plt.subplots(figsize=(11,7));draw(ax,parts['PF_OpenCradleL'],'#dec498');draw(ax,parts['SSF_Exciter2L'],'#d98a48');setup(ax,(1000,1145),(245,350));rear=m['foot_y_max_mm'];newmin=m['exciter_moves'][0]['after_y_min_mm'];z=300
ax.annotate('',xy=(rear,z),xytext=(newmin,z),arrowprops={'arrowstyle':'<->','color':'#20313c','lw':2});ax.annotate('2.00 mm clearance',xy=((rear+newmin)/2,z),xytext=(1014,344),arrowprops={'arrowstyle':'->'},fontsize=12)
ax.text(1005,260,'STRAIGHT SUPPORT',fontsize=11);ax.text(1090,275,'EXCITER\n+7.251 mm in Y\nX / Z / orientation unchanged',fontsize=10);fig.suptitle('V32 · EXCITER / CRADLE CLEARANCE · REAR SSF ZONE');save(fig,'05-exciter-cradle-clearance.png')
fig,axes=plt.subplots(1,3,figsize=(13,9))
for ax,source,title in [(axes[0],old,'BEFORE · rejected exciter notch'),(axes[1],parts,'AFTER · straight rear edge')]:
 draw(ax,source['PF_OpenCradleL'],'#dec498');setup(ax,(995,1085),(20,530));ax.set_title(title,fontsize=11)
ax=axes[2];draw(ax,parts['PF_OpenCradleL'],'#0072b2');draw(ax,old['PF_OpenCradleL'],'#dec498');setup(ax,(1057,1080),(255,345));ax.set_title('LOCAL COMPARISON\nBlue = restored plywood',fontsize=11)
fig.suptitle('V32 · BEFORE / AFTER SUPPORT PROFILE · ALL MOUNTING HOLES UNCHANGED');save(fig,'06-cradle-before-after.png')
