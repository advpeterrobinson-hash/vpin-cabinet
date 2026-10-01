"""Render actual tessellated study solids; no concept art. CERN-OHL-S-2.0."""
from pathlib import Path
import json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/matrix-hinge-study-v32';b=json.loads((O/'study-mesh.json').read_text());report=json.loads((O/'validation.json').read_text());cfg=json.loads((R/'config/matrix_hinge_study_v32.json').read_text());base={p['name']:p for p in b['baseline']['parts']};rows=b['candidates']
rearward=[p for p in rows if p['result'].get('rearward_limit_candidate')];best=next((p for p in rows if report['best'] and p['result']==report['best']),None)
if best is None and report.get('best_review'):best=next(p for p in rows if p['result']==report['best_review'])
if best is None:best=max(rearward,key=lambda p:(min(v['visible_row_sample_percent'] for v in p['result']['visibility']),p['result']['gap_mm']))
selected=[next(p for p in rows if p['result']['gap_mm']==g and p['result']['tilt_deg']==15) for g in (25.4,38.1,50.8)]+[best]
show=['SIDE_L','SIDE_R','FRONT','REAR','BACKBOX_BASE','PLAYFIELD_ENVELOPE','PF_BasePlywood','PF_WoodDowel','PF_OpenCradleL','PF_OpenCradleR','PF_BackboxCheckEnvelope','CandidateGlass']
def draw(ax,p,color,alpha=1):
 v=np.array(p['vertices']);ax.add_collection3d(Poly3DCollection([v[f] for f in p['faces']],facecolor=color,edgecolor='none',alpha=alpha,zorder=100 if p['name'].startswith('MatrixPanel') else 80 if p['name']=='MatrixCarrier' else 10))
def projected(ax,p,axes=(1,2),color='#7c8993',label=None):
 pts=sorted(set((q[axes[0]],q[axes[1]]) for q in p['vertices']))
 cross=lambda o,a,b:(a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
 lo=[];hi=[]
 for q in pts:
  while len(lo)>=2 and cross(lo[-2],lo[-1],q)<=0:lo.pop()
  lo.append(q)
 for q in reversed(pts):
  while len(hi)>=2 and cross(hi[-2],hi[-1],q)<=0:hi.pop()
  hi.append(q)
 hull=lo[:-1]+hi[:-1];ax.add_patch(plt.Polygon(hull,closed=True,facecolor=color,edgecolor=color,alpha=.35,label=label,lw=1.5))
def scene(ax,ps,state=None,remove=0,eye=False):
 for n in show:
  p=base[n]
  if state and n in b['baseline']['states'].get(state,{}):p=b['baseline']['states'][state][n]
  if p is None:continue
  draw(ax,p,'#777777' if n=='PLAYFIELD_ENVELOPE' else '#56B4E9' if n=='CandidateGlass' else '#baa37d',.12 if n.startswith(('SIDE','PF_Backbox','CandidateGlass')) else .75)
 for p in ps['parts']:
  q=dict(p);q['vertices']=[[x,y,z+remove] for x,y,z in p['vertices']];draw(ax,q,'#0072B2' if p['name']=='MatrixCarrier' else '#E69F00')
 ax.set(xlim=(-100,700),ylim=(0,1400),zlim=(250,1350));ax.set_box_aspect((800,1400,1100));ax.view_init(elev=28,azim=-62);ax.set_axis_off()
 if eye:
  e=cfg['eyes_xyz_mm'][1];ax.view_init(elev=math.degrees(math.atan2(e[2]-550,1100-e[1])),azim=-90)
def save(fig,name,title):
 fig.suptitle(title,fontsize=15);fig.text(.03,.025,'REAL CAD STUDY · candidates / dimensions provisional · manufacturing BLOCKED · accepted cabinet/viewer unchanged',fontsize=8);fig.savefig(O/name,dpi=150);plt.close(fig)
for i,p in enumerate(selected,1):
 fig=plt.figure(figsize=(12,9));ax=fig.add_subplot(projection='3d',computed_zorder=False);scene(ax,p);r=p['result'];ax.set_title(f"gap {r['gap_mm']:.4f} mm · tilt {r['tilt_deg']}° · feasible {r['feasible']}\nPLAY {r['PLAY_mm']:.2f} / SERVICE {r['SERVICE_mm']:.2f} / LIFT {r['LIFT_OUT_mm']:.2f} mm");save(fig,f'0{i}-candidate.png','V32 · MATRIX COMPARISON · IDENTICAL CAMERA')
fig,axs=plt.subplots(2,2,figsize=(14,10))
for ax,p in zip(axs.flat,selected):
 r=p['result'];eye=cfg['eyes_xyz_mm'][1]
 for n in ('PLAYFIELD_ENVELOPE','PF_BasePlywood','CandidateGlass','PF_BackboxCheckEnvelope'):
  projected(ax,base[n],color='#56B4E9' if n=='CandidateGlass' else '#888888',label=n)
 for q in p['parts']:
  projected(ax,q,color='#E69F00')
 for q in [p['parts'][1],p['parts'][-1]]:
  v=np.mean(q['vertices'],axis=0);ax.plot([eye[1],v[1]],[eye[2],v[2]],'--',color='#0072B2',lw=.7)
 ax.scatter([eye[1]],[eye[2]],c='black');ax.set(xlim=(-500,1320),ylim=(300,1100),xlabel='Y mm',ylabel='Z mm');ax.set_title(f"gap {r['gap_mm']:.3f} / tilt {r['tilt_deg']}°\nvisibility {min(v['visible_row_sample_percent'] for v in r['visibility']):.1f}% min; apparent gap {r['visibility'][1]['apparent_gap_deg']:.2f}°")
save(fig,'05-player-eye-comparison.png','V32 · PLAYER EYE ENVELOPE / REAL CAD SIGHTLINES')
fig,ax=plt.subplots(figsize=(12,7))
for n in ('PLAYFIELD_ENVELOPE','PF_BasePlywood','CandidateGlass','BACKBOX_BASE'):
 projected(ax,base[n],color='#56B4E9' if n=='CandidateGlass' else '#888888',label=n)
for q in best['parts']:
 projected(ax,q,color='#0072B2' if q['name']=='MatrixCarrier' else '#E69F00')
ax.set(xlim=(900,1320),ylim=(420,650),xlabel='Y mm',ylabel='Z mm');ax.legend();save(fig,'06-side-section.png','V32 · PLAYFIELD / GLASS / INDEPENDENT MATRIX')
for name,state,remove in [('07-service.png','SERVICE',0),('08-lift-out.png','LIFT-OUT',0),('09-matrix-removal.png',None,100)]:
 fig=plt.figure(figsize=(12,9));ax=fig.add_subplot(projection='3d',computed_zorder=False);scene(ax,best,state,remove);ax.set_title('INTERFERENCE STUDY — not a clearance approval' if state else '100 mm independent upward removal · glass removed first');save(fig,name,'V32 · '+name[3:-4].upper())
# Hinge datum drawing: actual accepted envelope, references only; no guessed bracket pattern.
fig,ax=plt.subplots(figsize=(12,6))
for n in ('SIDE_L','SIDE_R','PF_BackboxCheckEnvelope'):
 projected(ax,base[n],axes=(0,1),color='#bda67f',label=n)
for xouter,xref in [(-90,-90+59.8375),(690,690-59.8375)]:
 ax.annotate('',xy=(xref,1330),xytext=(xouter,1330),arrowprops={'arrowstyle':'<->'});ax.text((xouter+xref)/2,1340,'59.8375',ha='center');ax.scatter([xref],[1308.1-12.7],c='#0072B2');ax.text(xref,1270,'REFERENCE INSET\n3 × Ø6.35 / pitch44.45\npattern direction HOLD',ha='center',fontsize=8)
ax.set(xlim=(-120,720),ylim=(1020,1370),xlabel='X mm',ylabel='Y mm');ax.legend(loc='lower center');save(fig,'10-hinge-datums.png','V32 · 600 / 780 HINGE DATUM · NO PRODUCTION DRILLING')
# Full self-contained candidate report.
lines=['# CURRENT V32 — hinge datum cleanup and matrix positioning study','',f"HEAD BEFORE: `{cfg['source_head']}`",'', 'Accepted cabinet CAD and viewer are immutable inputs. This is an isolated comparison, not a replacement CURRENT model or manufacturing selection. Rebuild with `freecadcmd tools/matrix_hinge_study_v32_entry.py`, require MATRIX_STUDY_PASS, then run `freecadcmd tools/check_matrix_hinge_regressions_v32.py` (require MATRIX_REGRESSION_PASS), `freecadcmd tools/save_matrix_review_poses_v32.py` (require MATRIX_POSES_PASS), and `uv run --with matplotlib python tools/render_matrix_hinge_study_v32.py`.', '', '## Hinge reference', '', '600 mm cabinet / 780 mm backbox; `(780−600−60.325)/2 = 59.8375 mm` from each OUTER backbox-floor side. Cabinet pivot reference Ø12.7, rear offset38.1, bottom height508.0. Floor reference 3 × Ø6.35 per side, pitch44.45, row approximately12.7 from rear. These are reference datums only; no CNC hole pattern is frozen or new metal made. WPC 01-9011-L/R, 2 ×02-4352 and 2 ×4322-01139-12B remain HF-006 early procurement. Physical assembly measurement is mandatory before CNC; conflicting 02-4352 listings cannot define body length, bracket bends or holes. No intermediate cabinet prototype.', '', '## Matrix assumptions and measurements', '', 'Owner-provided Emil Jurica / Way of the Wrench feedback is experienced-builder guidance, not a mandatory inch dimension. Six unchanged 79.375 mm nominal panels sum476.25; vendor stated469.9 remains a6.35 discrepancy. 8 mm thickness is a provisional packaging reserve, not a vendor fact. One540 ×95.375 ×12 mm plywood carrier is independent of the playfield. Panel mounting slots/commodity attachment interface remain hardware-confirmation items; no permanent cabinet recuts. MX-DONNY electrical architecture is unchanged.', '', 'Gap means longitudinal Y separation from the actual TV envelope rear bound, not a misleading closest 3D distance. Tilt is absolute above horizontal; the historical extra15° render is not adopted. The playfield/glass slope is unchanged. Rearward limits use carrier rearY1125.125 (2 mm before the existing rear shelf front datum). Glass clearance is derived from actual CAD. No old render position or angle is adopted.', '', 'Provisional adult eyes: cabinet datum XYZ (220,−250,750), (300,−350,900), (380,−450,1050), corresponding to1,500–1,800 mm eyes above ground with a provisional750 mm cabinet-bottom elevation. Sampling checks all16 row centers in each of6 panels from each eye through actual opaque CAD, with transparent glass. Percentages are sampled row visibility, not an optical certification. Apparent gap is angular separation in the central sightline; a small angle can hide physical gap but is not proof of serviceability.', '', '## Every combination — mm except degrees/visibility', '', '|gap|tilt|visibility min %|apparent gap range °|PLAY|SERVICE|LIFT48|matrix removal100|fold envelope|wiring|feasible|','|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|']
for r in report['candidates']:
 vis=r['visibility'];lines.append('|'+ '|'.join([f"{r['gap_mm']:.4f}",str(r['tilt_deg']),f"{min(v['visible_row_sample_percent'] for v in vis):.1f}",f"{min(v['apparent_gap_deg'] for v in vis):.2f}–{max(v['apparent_gap_deg'] for v in vis):.2f}"]+[f"{r[k]:.3f}" for k in ('PLAY_mm','SERVICE_mm','LIFT_OUT_mm','removal_mm','fold_mm','wiring_mm')]+['YES' if r['feasible'] else 'NO'])+'|')
lines+=['', 'Zero distance with listed hits is a collision, not an acceptable tangent. Detailed per-candidate object hit lists are in validation.json. PLAY includes current shell/lockdown/side solids; glass plane checks include reserved panel thickness. SERVICE samples0–50° every2°; LIFT samples0–48 mm every2 mm; independent matrix removal samples0–100 mm every10 mm with glass removed. These are sampled motion screens, not continuous exact swept-volume certifications.', '', 'Backbox fold uses the real accepted PF_BackboxCheckEnvelope rotated0–90° every5° at the WPC reference pivot, not nonexistent detailed measured hardware. Cable opening/backglass interior and true bracket/bend offsets are absent from this accepted CAD, so their detailed clearances remain UNVERIFIED even if a packaging sample clears. Backbox must be upright and isolated during matrix removal. Full hardware fold verification remains blocked.', '', 'Wiring uses a provisional40 ×30 ×20 mm connector/bend reservation below the rear shelf, behind the moving playfield. Collision results must not be accepted as a valid harness route. The connector reservation is below the rear shelf and behind the moving playfield; each candidate also screens it against SERVICE/LIFT motion. A complete selected-harness bend/strain-relief route and removable keyed disconnect outside the lift-out corridor still require confirmation; no harness is cut or trapped by this study. Four Ø8 ×50 mm provisional top-driver probes check access on the carrier margins with glass removed. Mounting is not frozen before measured panels and lower-backbox interfaces. Rear airflow study is preserved without reopening thermal adequacy; no new duct or thermal claim.', '', 'Tool and unchanged-airflow-route clearance / hits for each combination are recorded in validation.json. Glass is removed for matrix access, but the accepted playfield remains installed. Candidate carrier attachment to the cabinet/lower backbox requires measured mating hardware; no permanent hinge or panel holes are generated.', '', '## Best review candidate', '']
r=best['result'];lines += [f"Gap {r['gap_mm']:.4f} mm; tilt {r['tilt_deg']}°; rearward offset relative to25.4-mm baseline {r['gap_mm']-25.4:.4f} mm. This is the most rearward of the PLAY-clear, independently removable comparison candidates with the best minimum sampled visibility across the eye envelope. Tool reserve is{r['tool_clearance_mm']:.3f} mm clear, connector reserve{r['wiring_mm']:.3f} mm clear, glass{r['glass_clearance_mm']:.3f} mm clear and the unchanged diagnostic airflow path{r['airflow_clearance_mm']:.3f} mm clear for this candidate. " + ('All screened constraints clear, with manufacturing holds retained.' if report['best'] else '**No fully feasible installed candidate was found.** This is only the most rearward comparison candidate, not a solved/approved assembly. Its installed service/lift/fold failures cannot be hidden by rendering or cleared by moving accepted parts.'), '', 'The independent upward removal comparison is included. Removing the matrix before playfield service/folding is a possible sequence to review, not an owner-approved substitute for the failed installed-clearance requirements. No rejected candidate is installed into the accepted viewer/current cabinet.', '', '## Regression / manufacturing', '', f"{len(report['checks'])} CAD checks passed; reopened-output and negative controls are in regression-validation.json: every accepted CAD solid unchanged, source exports and exact bilingual/palette/selection viewer bytes unchanged. Notches, buttons, floor fans/filters, rear fans, wood dowel/cradles/screws, shelves, PCBase, rear door and SSF exciter coordinates all retain accepted geometry. Historical engineering records stay historical; targeted current hinge texts and current entry-point supersession notices are corrected.", '', 'MANUFACTURING BLOCKED: physical hinge assembly measurement, actual matrix panel-set/thickness/connector confirmation, CNC shop stock/tool/clearance parameters and remaining freeze gates. No physical cabinet prototype or thermal re-analysis is added.', '', 'Actual combined review CAD poses are `service.FCStd`, `lift-out.FCStd` and `matrix-removal.FCStd` in the study directory; accepted pivot cylinder expressions remain live in these pose exports. pose-validation.json confirms them. Candidate snapshots and all views are review-only, not a manufacturing model.', '', '## Real CAD reviews', '']
for i in range(1,11):
 p=next(O.glob(f'{i:02d}-*.png'));lines.append(f'![{p.stem}](../exports/generated/matrix-hinge-study-v32/{p.name})')
(R/'docs/MATRIX_HINGE_STUDY_V32.md').write_text('\n'.join(lines)+'\n');print('MATRIX_RENDER_PASS',len(list(O.glob('*.png'))))
