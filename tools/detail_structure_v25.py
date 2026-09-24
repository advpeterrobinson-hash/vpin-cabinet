"""Derive zero-clearance joint review geometry from fresh active source.
Owns a separate detail document; never converts previews into production toolpaths.
"""
import csv,json
from pathlib import Path
import FreeCAD as A
import Part
ROOT=Path(__file__).resolve().parents[1]

def main():
 cfg=json.loads((ROOT/'config/cnc_detail_v25.json').read_text())
 t=cfg['stock']['preview_main_mm']; d=t*cfg['fit']['capture_depth_fraction']
 if cfg['stock']['measured_main_mm'] is not None:
  raise RuntimeError('Measured stock requires coordinated source migration before detail generation; preview cannot silently use nominal stock')
 doc=A.openDocument(str(ROOT/'cad/active/vpin-active.FCStd'))
 rows=list(csv.DictReader((ROOT/'bom/ACTIVE_PARTS.csv').open()))
 wood={r['object_name']:doc.getObject(r['object_name']) for r in rows}
 contacts=[]
 for i,(n,o) in enumerate(wood.items()):
  for m,p in list(wood.items())[i+1:]:
   if o.Shape.distToShape(p.Shape)[0]<1e-6:
    contacts.append(dict(a=n,b=m,overlap_mm3=o.Shape.common(p.Shape).Volume))
 ops=[]
 def remove(n,cut,kind,m):
  before=wood[n].Shape
  actual=before.common(cut)
  if actual.Volume<1e-5:return
  result=before.cut(cut).removeSplitter()
  if not result.isValid() or len(result.Solids)!=1:raise RuntimeError('Joint breaks solid '+n+' / '+m)
  wood[n].Shape=result
  b=actual.BoundBox
  ops.append(dict(part=n,mate=m,type=kind,bounds=[b.XMin,b.XMax,b.YMin,b.YMax,b.ZMin,b.ZMax],removed_mm3=actual.Volume))
 def overlap(a,b):return wood[a].Shape.common(wood[b].Shape)
 def box(x,y,z,dx,dy,dz):return Part.makeBox(dx,dy,dz,A.Vector(x,y,z))
 # Main shell: existing six-mm captures become real receiving cuts.
 for side in ('Left','Right'):
  n='Cabinet'+side+'Side'
  for m in ['CapturedFrontPanelV20','RearPanelWithCPUHatchV24','CapturedBottomV20']+['LowCrossmember%dV20'%i for i in (1,2,3)]:
   remove(n,wood[m].Shape,'RABBET' if 'Panel' in m else 'DADO',m)
 for n in ('CapturedFrontPanelV20','RearPanelWithCPUHatchV24'):
  remove(n,wood['CapturedBottomV20'].Shape,'DADO','CapturedBottomV20')
 # Rear shelf: full-strength side bearing via t/3 capture, rear edge t/3 rabbet.
 n='RearShelfV14';b=wood[n].Shape.BoundBox
 wood[n].Shape=box(t-d,b.YMin,b.ZMin,600-2*(t-d),b.YLength,b.ZLength)
 rear='RearPanelWithCPUHatchV24';rb=wood[rear].Shape.BoundBox
 remove(n,box(-100,rb.YMin+d,-100,1000,100,2000),'PROFILE',rear)
 for m in ('CabinetLeftSide','CabinetRightSide',rear):remove(m,wood[n].Shape,'RABBET',n)
 # Backbox sides stay full-height; top/floor enter t/3 rebates.
 for n in ('BackboxFloorV14','BackboxTopV14'):
  b=wood[n].Shape.BoundBox
  remove(n,box(b.XMin-1,b.YMin-1,b.ZMin-1,t-d+1,b.YLength+2,b.ZLength+2),'PROFILE','BackboxLeftSideV14')
  remove(n,box(b.XMax-(t-d),b.YMin-1,b.ZMin-1,t-d+1,b.YLength+2,b.ZLength+2),'PROFILE','BackboxRightSideV14')
  for side in ('Left','Right'):remove('Backbox'+side+'SideV14',wood[n].Shape,'RABBET',n)
 # Four frame strips remain: capture rear t/3 in perimeter; half-lap strip corners.
 frames=[n for n in wood if n.startswith('BackboxRearFrame')]
 for n in frames:
  for m in ('BackboxFloorV14','BackboxTopV14','BackboxLeftSideV14','BackboxRightSideV14'):
   ov=overlap(n,m)
   if ov.Volume<1e-5:continue
   b=ov.BoundBox
   # Rear rebate has t/3 depth into perimeter measured along Y.
   limit=b.YMax-d
   remove(n,box(b.XMin-1,b.YMin-1,b.ZMin-1,b.XLength+2,max(0.001,limit-b.YMin+1),b.ZLength+2),'PROFILE',m)
   remove(m,wood[n].Shape,'RABBET',n)
 # Cradle overlaps: split shared X material into outer 2t/3 rail and inner t/3 capture.
 for side in ('Left','Right'):
  rail='CradleSideRail'+side+'V18';b=wood[rail].Shape.BoundBox
  cut_x=b.XMax-d if side=='Left' else b.XMin+d
  for m in ['CradleCrossmember%dV18'%i for i in (1,2,3)]+['CradlePivotDoubler'+side+'V18']:
   ov=overlap(rail,m)
   if ov.Volume<1e-5:continue
   # X is unaffected by playfield rotation.
   if side=='Left':outer=box(-100,-100,-100,cut_x+100,2000,2000)
   else:outer=box(cut_x,-100,-100,1000-cut_x,2000,2000)
   remove(m,ov.common(outer),'PROFILE',rail)
   remove(rail,wood[m].Shape,'DADO',m)
 # Rear tie overlaps pivot block: tie is top member, block receives shallow local lap.
 for side in ('Left','Right'):
  remove('CradlePivotDoubler'+side+'V18',wood['CradleCrossmember3V18'].Shape,'POCKET','CradleCrossmember3V18')
 # Preserve new generic cuts when shelf capture extends its nominal blank.
 from owner_features_v27 import features
 from build_owner_services_v27 import cut_shape
 for f in features():wood[f['part']].Shape=wood[f['part']].Shape.cut(cut_shape(f)).removeSplitter()
 # Verify ALL wood pairs, not merely the pairs explicitly edited.
 clashes=[]
 for i,(n,o) in enumerate(wood.items()):
  for m,p in list(wood.items())[i+1:]:
   v=o.Shape.common(p.Shape).Volume
   if v>1e-4:clashes.append([n,m,v])
 if clashes:raise RuntimeError('Unresolved wood overlaps '+str(clashes))
 for n,o in wood.items():
  if not o.Shape.isValid() or len(o.Shape.Solids)!=1:raise RuntimeError('Invalid detail '+n)
  o.MachiningStatus='PARAMETRIC JOINT PREVIEW; STOCK/TOOL/HARDWARE BLOCKED'
 doc.recompute()
 out=ROOT/'exports/generated/cnc-detail';out.mkdir(parents=True,exist_ok=True)
 inventory=[]
 for n,o in wood.items():
  v,tr=o.Shape.tessellate(2)
  inventory.append(dict(name=n,part_id=o.PartID,vertices=[[p.x,p.y,p.z] for p in v],triangles=tr))
 (out/'geometry.json').write_text(json.dumps(dict(contacts=contacts,operations=ops,inventory=inventory,wood_overlap_pairs=clashes),indent=2)+'\n')
 doc.saveAs(str(out/'vpin-cnc-detail-preview.FCStd'));A.closeDocument(doc.Name)
 print('\nCNC_DETAIL_GEOMETRY_PASS',len(wood),'wood parts;',len(ops),'receiving/profile operations; zero wood overlaps')
if __name__=='__main__':main()
