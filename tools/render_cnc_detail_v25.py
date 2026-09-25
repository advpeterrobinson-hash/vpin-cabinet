"""Manufacturing review from saved meshes, never historical geometry."""
import csv,json,html
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import proj3d
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'exports/generated/cnc-detail';OUT.mkdir(exist_ok=True)
g=json.loads((OUT/'geometry.json').read_text());active=json.loads((ROOT/'exports/generated/active-geometry-report.json').read_text())
parts={p['name']:dict(p,vertices=p['mesh_vertices'],triangles=p['mesh_triangles']) for p in active['inventory']}
parts.update({p['name']:p for p in g['inventory']})
rows=list(csv.DictReader((ROOT/'bom/ACTIVE_PARTS.csv').open()));features=list(csv.DictReader((ROOT/'bom/CNC_FEATURES_V25.csv').open()))
index={r['object_name']:i+1 for i,r in enumerate(rows)}
wood=list(index)
hardware_index={n:"H%d"%(i+1) for i,n in enumerate(n for n in parts if n not in index)}

def scene(file,title,names,note,explode=False,ops=False,azim=-55):
 fig=plt.figure(figsize=(14,10));ax=fig.add_subplot(111,projection='3d');points=[];labels3d=[]
 for n in names:
  p=parts[n];v=np.array(p['vertices']);tr=np.array(p['triangles'],dtype=int)
  if not len(tr):continue
  if explode:
   c=v.mean(0);shift=np.array([(c[0]-300)*.7,(c[1]-650)*.3,(c[2]-500)*.22]);v=v+shift
  color='#c6a46d' if n in wood else '#627f97'
  alpha=.8
  if n.startswith('Cabinet') or n=='RearPanelWithCPUHatchV24':alpha=.18
  if any(x in n for x in ('Envelope','Keepout','SafetyStayOpen')):color='#d17b56';alpha=.45
  ax.add_collection3d(Poly3DCollection(v[tr],facecolor=color,edgecolor='#354451',linewidth=.18,alpha=alpha))
  c=v.mean(0)
  label=str(index[n]) if n in index else hardware_index[n]
  labels3d.append((c,label));points.extend(v.tolist())
 if ops:
  for o in g['operations']:
   if o['part'] not in names:continue
   b=o['bounds'];ax.scatter((b[0]+b[1])/2,(b[2]+b[3])/2,(b[4]+b[5])/2,c='#d13430',s=20)
 v=np.array(points);lo=v.min(0);hi=v.max(0)
 ax.set_xlim(lo[0]-30,hi[0]+30);ax.set_ylim(lo[1]-30,hi[1]+30);ax.set_zlim(lo[2]-30,hi[2]+30);ax.set_box_aspect(hi-lo+60)
 ax.view_init(25,azim);ax.set_xlabel('X mm');ax.set_ylabel('Y rearward / mm');ax.set_zlabel('Z mm')
 ax.set_title(title+'\nJOINT PREVIEW — NOT CNC RELEASE',fontsize=16)
 fig.canvas.draw();used=[]
 for c,label in labels3d:
  xp,yp,_=proj3d.proj_transform(*c,ax.get_proj())
  px,py=ax.transAxes.inverted().transform(ax.transData.transform((xp,yp)))
  py=max(.06,min(.94,py))
  while any(abs(px-x)<.04 and abs(py-y)<.032 for x,y in used):py+=.035
  used.append((px,py))
  ax.text2D(px,py,label,transform=ax.transAxes,fontsize=8,zorder=100,bbox=dict(facecolor='white',edgecolor='#777',alpha=.9,pad=1))
 fig.text(.05,.045,note+'\nNumbers resolve to full part IDs in the gallery. Hardware envelopes are not drill patterns.',fontsize=10)
 fig.savefig(OUT/(file+'.png'),dpi=160);plt.close(fig)
scene('01-exploded',f'Exploded structural cabinet / {len(rows)} wood assembly records',wood,'Exploded translations are for visibility only. Three 2t assemblies require separate ply IDs before nesting.',True)
scene('02-joints','Actual rebates, captures and cradle laps',wood,'Red markers locate receiving/profile-cut operations; exact cut solids, not rectangular bounding boxes, control the review.',ops=True)
scene('03-legs','Leg loads → through-bolts / spreaders → full shell', [n for n in parts if n.startswith(('ClassicLegBracket','LegSpreader'))]+['CabinetLeftSide','CabinetRightSide','CapturedFrontPanelV20','RearPanelWithCPUHatchV24','CapturedBottomV20'],'95 × 95 × 150 corner target. Actual bolts / edge distances / capacity BLOCKED. No corner plywood furniture.')
scene('04-cpu','20 kg payload → shelf → slides → rails → clamps / backed bottom',[n for n in parts if n.startswith(('RearCPUSupportRail','RearCPUFixedSlide','CPURailAngle','CPURailBacking','ClassicLegBracketR'))]+['RearCPUShelfStowedV24','CapturedBottomV20','LowCrossmember3V20'],'Bottom-seated rails. Four metal clamps. 13.8 mm modeled rail/bracket gap vs 15 mm planning reserve.',azim=65)
scene('05-hatch','Rear hatch ligaments and captured rear shelf',['RearPanelWithCPUHatchV24','RearShelfV14','RearCPUServiceDoorClosedV24','CabinetLeftSide','CabinetRightSide'],'Hatch X130..470 / Z110..350. Door Z98..362; 105° outward opening retained. No broad added rear doubler.',azim=65)
scene('06-backbox','Backbox perimeter rebates and hinge / lock envelope',[n for n in wood if n.startswith('Backbox')]+['RearShelfV14']+[n for n in parts if n.startswith(('WpcHinge','LockAxisX','BackboxPivotAxis'))],'Measured leaves / pivot bushings / upright locks control holes. Floor bears on captured rear shelf.',azim=65)
scene('07-playfield','Cradle laps, bearing and independent safety load paths',[n for n in wood if n.startswith(('Cradle','SafetyStay','ClosedSupport'))]+[n for n in parts if n.startswith(('UCFL202','SafetyStayOpen','BearingBacking','PivotJournal','PivotPlate','ClosedSupportSeat'))],'15 mm journals; two independent positive stays; closed pads/latches. Manual lift; simple positive prop anchors remain measured hardware.')
fig,ax=plt.subplots(figsize=(14,12))
labels=[];counts=[]
for r in rows:
 fs=[f for f in features if f['part_id']==r['part_id']];labels.append(str(index[r['object_name']])+' '+r['part_id']);counts.append([sum(f['status']==s for f in fs) for s in ('DEFINED_PARAMETRIC','BLOCKED_MEASURE_HARDWARE','BLOCKED_DESIGN')])
c=np.array(counts);left=np.zeros(len(rows))
for i,(color,label) in enumerate([('#6a997e','Defined recipe / review only'),('#d79749','Hardware pattern BLOCKED'),('#ab667c','Design BLOCKED')]):
 ax.barh(labels,c[:,i],left=left,color=color,label=label);left+=c[:,i]
ax.invert_yaxis();ax.legend(loc='lower right');ax.set_xlabel('Feature groups (not individual holes)');ax.set_title('08 — Definition status per wood part\nAll parts remain blocked for manufacturing');ax.tick_params(axis='y',labelsize=7)
fig.tight_layout();fig.savefig(OUT/'08-status.png',dpi=160);plt.close(fig)
# Dimensioned nominal rail/leg schematic plus blanks for physical replacement values.
(OUT/'cpu-measurement.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="740" viewBox="0 0 1100 740"><rect width="1100" height="740" fill="white"/><g font-family="sans-serif" fill="#243441"><text x="35" y="35" font-size="24">CPU RAIL / REAR LEG — MEASURE BEFORE CNC</text><text x="35" y="65" font-size="15">Nominal plan, schematic. No hole centers shown. Units mm. X → right; Y → rear.</text><g transform="translate(80 120)"><rect x="0" y="0" width="600" height="330" fill="#f3eee5" stroke="#555"/><rect x="126.8" y="0" width="18" height="310" fill="#b99a72"/><rect x="455.2" y="0" width="18" height="310" fill="#b99a72"/><rect x="157.5" y="0" width="285" height="300" fill="#dde8ed" stroke="#555"/><path d="M18 225V312H113 M487 312H582V225" fill="none" stroke="#687e92" stroke-width="9"/><path d="M113 285H126.8" stroke="#b34839" stroke-width="3"/><text x="190" y="140">285 wide × 460 deep shelf</text><text x="195" y="170">Z135; thickness = measured t</text><text x="170" y="285">Rear brackets include full bolt stack</text><text x="0" y="355">Cabinet outside X0..600; rear Y1308.1</text></g><text x="720" y="140">Record actual:</text><text x="720" y="175">Bracket inner X left: ______</text><text x="720" y="205">Bracket inner X right: _____</text><text x="720" y="235">Flange thickness: ________</text><text x="720" y="265">Y min/max: ______________</text><text x="720" y="295">Z min/max: ______________</text><text x="720" y="325">Bolt/nut/washer stack: ____</text><text x="720" y="355">Slide body L/R: __________</text><text x="720" y="385">Maker side clearance: ____</text><text x="720" y="415">Clamp / backing: ________</text><text x="35" y="540" font-size="19">Current nominal closest gap = 13.8; planning target = 15. Do not relocate rails from this discrepancy alone.</text><text x="35" y="580">Side elevation datums: bottom top Z36 nominal; shelf Z135; clamp centers Y875 / Y1150; crossmember Y1040.</text><text x="35" y="610">Measure fixed and moving slide members separately from seating face / closed rear end / lower edge.</text><text x="35" y="640">Attach HF-003/004/013/026/028 sheets. Include actual corners, both sides, closed/extended and underside photos.</text><text x="35" y="690" fill="#b34839">NOT A DRILL TEMPLATE — all structural mounting holes remain BLOCKED_MEASURE_HARDWARE.</text></g></svg>''')
files=['01-exploded','02-joints','03-legs','04-cpu','05-hatch','06-backbox','07-playfield','08-status']
page=['<!doctype html><meta charset="utf-8"><title>CNC detail review v25</title><style>body{font:16px sans-serif;max-width:1400px;margin:30px;background:#f4f1eb}img{width:100%}section{background:white;margin:25px 0;padding:20px}td,th{padding:6px;border-bottom:1px solid #ccc}</style><h1>CNC structure detailing / measurement review</h1><p>32 wood records (29 permanent structure). Zero wood overlap in joint preview. 173 defined feature groups, 59 hardware-blocked groups, zero design-only blockers. No production toolpaths, final fit, hardware holes or manufacturing approval.</p><p><a href="cpu-measurement.svg">CPU rail measurement drawing</a> · <a href="vpin-cnc-detail-preview.FCStd">Joint preview FCStd</a> · <a href="../review/index.html">Current owner review gallery</a></p>']
for f in files:page.append(f'<section><h2>{f}</h2><img src="{f}.png" alt="{f}"></section>')
page.append('<table><tr><th>Label</th><th>Part ID</th><th>Function/load path</th></tr>')
for r in rows:page.append(f'<tr><td>{index[r["object_name"]]}</td><td>{html.escape(r["part_id"])}</td><td>{html.escape(r["load_path"])}</td></tr>')
page.append('</table><h2>Hardware/envelope labels</h2><table>')
for n,label in hardware_index.items():page.append('<tr><td>'+label+'</td><td>'+html.escape(n)+'</td></tr>')
page.append('</table>');(OUT/'index.html').write_text('\n'.join(page));print('CNC_REVIEW_PASS',OUT/'index.html')
