"""Exact line/arc/ellipse DXF + SVG REVIEW export infrastructure, not production.
CERN-OHL-S-2.0. Native B-reps retain authority; no toolpath/G-code output.
"""
from pathlib import Path
import json,math,html
import FreeCAD as A
import Part
V=A.Vector
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/flatpack-v331';D=json.loads((O/'manufacturing-register.json').read_text())
by={r['instance_id']:r for r in D['parts']};P=O/'part-reviews';P.mkdir(exist_ok=True)
def load(path):s=Part.Shape();s.read(str(R/path));return s
def xy(p):return [p.x,p.y]
def curves(shape):
 edges=shape.Edges;out=[]
 for e in edges:
  c=e.Curve;t=type(c).__name__;a=e.valueAt(e.FirstParameter);b=e.valueAt(e.LastParameter)
  if t=='Line':out.append({'type':'LINE','a':xy(a),'b':xy(b)})
  elif t=='Circle':
   full=abs(e.LastParameter-e.FirstParameter-2*math.pi)<1e-6
   out.append({'type':'CIRCLE' if full else 'ARC','c':xy(c.Center),'r':c.Radius,'a':xy(a),'b':xy(b),
       'start':math.degrees(math.atan2(a.y-c.Center.y,a.x-c.Center.x))%360,
       'end':math.degrees(math.atan2(b.y-c.Center.y,b.x-c.Center.x))%360,
       'ccw':c.Axis.z>0,'span':e.LastParameter-e.FirstParameter})
  elif t=='Ellipse':
   out.append({'type':'ELLIPSE','c':xy(c.Center),'major':xy(c.MajorAxis*c.MajorRadius),'ratio':c.MinorRadius/c.MajorRadius,
       'start_param':e.FirstParameter,'end_param':e.LastParameter,'note':'DXF exact ellipse; SVG review samples only'})
  else:
   raise RuntimeError('Unimplemented exact vector curve: '+t)
 return out

def svg_curve(c):
 t=c['type']
 if t=='LINE':return f'<path d="M {c["a"][0]} {c["a"][1]} L {c["b"][0]} {c["b"][1]}"/>'
 if t=='CIRCLE':return f'<circle cx="{c["c"][0]}" cy="{c["c"][1]}" r="{c["r"]}"/>'
 if t=='ARC':return f'<path d="M {c["a"][0]} {c["a"][1]} A {c["r"]} {c["r"]} 0 {int(c["span"]>math.pi)} {int(c["ccw"])} {c["b"][0]} {c["b"][1]}"/>'
 if t=='ELLIPSE':
  x,y=c['major'];rr=math.hypot(x,y);angle=math.degrees(math.atan2(y,x));cx,cy=c['c']
  if abs(c['end_param']-c['start_param']-2*math.pi)<1e-6:return f'<ellipse cx="{cx}" cy="{cy}" rx="{rr}" ry="{rr*c["ratio"]}" transform="rotate({angle} {cx} {cy})"/>'
  raise RuntimeError('Partial ellipse SVG not implemented; retain native B-rep')

def dxf_curves(items):
 lines=['0','SECTION','2','HEADER','9','$ACADVER','1','AC1015','9','$INSUNITS','70','4','0','ENDSEC','0','SECTION','2','TABLES','0','TABLE','2','LAYER','70','5']
 for layer in ('CUT','POCKET','LOCATOR','ENGRAVE','REFERENCE'):lines+=['0','LAYER','2',layer,'70','0','62','7','6','CONTINUOUS']
 lines+=['0','ENDTAB','0','ENDSEC','0','SECTION','2','ENTITIES']
 for layer,cs in items.items():
  for c in cs:
   t=c['type'];lines+=['0',t,'8',layer]
   if t=='LINE':lines+=['10',str(c['a'][0]),'20',str(c['a'][1]),'30','0','11',str(c['b'][0]),'21',str(c['b'][1]),'31','0']
   elif t in ('CIRCLE','ARC'):
    lines+=['10',str(c['c'][0]),'20',str(c['c'][1]),'30','0','40',str(c['r'])]
    if t=='ARC':lines+=['50',str(c['start'] if c['ccw'] else c['end']),'51',str(c['end'] if c['ccw'] else c['start'])]
   elif t=='ELLIPSE':lines+=['10',str(c['c'][0]),'20',str(c['c'][1]),'30','0','11',str(c['major'][0]),'21',str(c['major'][1]),'31','0','40',str(c['ratio']),'41',str(c['start_param']),'42',str(c['end_param'])]
 lines+=['0','TEXT','8','REFERENCE','10','0','20','-12','30','0','40','4','1','PRELIMINARY - NOT FOR CNC - FACE A ONLY','0','ENDSEC','0','EOF']
 return '\n'.join(lines)+'\n'
manifest=[]
for family in D['families']:
 p=by[family['instances'][0]];id=family['id'];items={n:[] for n in ['CUT','POCKET','LOCATOR','ENGRAVE','REFERENCE']}
 # Only cutter-access contours go in CUT/POCKET; finished boundaries remain reference.
 items['CUT']+=curves(load(p['cnc_outer_access_brep']))
 items['REFERENCE']+=curves(load(p['outer_contour_brep']))
 for op in p['through_cuts']+p['pockets']:
  if op.get('whole_face'):continue
  path=op.get('tool_access_boundary_brep') or op.get('reference_geometry_brep')
  if not path:continue
  s=load(path)
  if s.Solids:
   faces=[f for f in s.Faces if type(f.Surface).__name__=='Plane' and abs(abs(f.normalAt(0,0).z)-1)<1e-6]
   if not faces:continue
   s=max(faces,key=lambda f:f.CenterOfMass.z)
  items[op['group']]+=[dict(c,operation_id=op['id'],depth_mm=op.get('depth_mm')) for c in curves(s)]
 # Reference-only center marks: no enlargement of a <Ø4 accepted pilot hole.
 for m in p['manual_finish']:
  for b in m.get('bores',[]):
   if b.get('entry_local_xyz_mm'):
    x,y,z=b['entry_local_xyz_mm'];items['REFERENCE']+=[{'type':'LINE','a':[x-1,y],'b':[x+1,y]},{'type':'LINE','a':[x,y-1],'b':[x,y+1]}]
 width,height=p['finished_xy_size_mm'];x0,y0,_,_=p['finished_xy_bounds_mm']
 svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width+20}mm" height="{height+35}mm" viewBox="{x0-10} {y0-20} {width+20} {height+35}">',
      '<title>'+id+' PRELIMINARY — NOT FOR CNC</title>', '<metadata>CERN-OHL-S-2.0; Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet</metadata>']
 for layer,cs in items.items():
  svg+=[f'<g id="{layer}" fill="none" stroke="black" stroke-width="0.15"'+(' stroke-dasharray="1 1"' if layer=='REFERENCE' else '')+'>']+[('<g data-operation="'+html.escape(c.get('operation_id','OUTLINE_OR_REFERENCE'))+'">'+svg_curve(c)+'</g>') for c in cs]+['</g>']
 svg += [f'<g id="REVIEW_LABELS"><text x="{x0}" y="{y0-8}" font-family="sans-serif" font-size="{min(5,max(1.2,width/90))}">{id} — PRELIMINARY — NOT FOR CNC</text></g></svg>']
 (P/(id+'-review.svg')).write_text('\n'.join(svg)+'\n');(P/(id+'-review.dxf')).write_text(dxf_curves(items))
 manifest.append({'id':id,'svg':str((P/(id+'-review.svg')).relative_to(O)),'dxf':str((P/(id+'-review.dxf')).relative_to(O)),
                  'semantic_groups':list(items),'entity_operations':{k:[{'operation':c.get('operation_id','OUTLINE_OR_REFERENCE'),'depth_mm':c.get('depth_mm')} for c in cs] for k,cs in items.items()},'exact_vector_curves':True,'operation_depth_authority':'manufacturing-register.json',
                  'engraving_geometry_enabled':False,'pilot_locators':'REFERENCE crosses only where no safe Ø4 recess can fit inside accepted removal',
                  'full_sheet_release':False})
(O/'review-export-index.json').write_text(json.dumps(manifest,indent=2)+'\n')
# Wood-only exploded native assembly; translation only, no scaling of members.
doc=A.newDocument('V331ExplodedWood');exploded_offsets={}
for p in D['parts']:
 s=load(p['finished_member_brep']);mat=A.Matrix(*p['local_to_installed_matrix']);s.transformShape(mat,True)
 com=s.Solids[0].CenterOfMass
 offset=V((com.x-300)*.35,(com.y-650)*.3,(com.z-600)*.2)
 if p['source_component'].startswith('CandidateLegBlock'):offset.z+=int(p['instance_id'][-1])*25
 if '-Ply' in p['instance_id']:offset.z+=int(p['instance_id'][-1])*20
 exploded_offsets[p['instance_id']]=list(offset)
 s.translate(offset);o=doc.addObject('PartDesign::Feature',p['instance_id'].replace('-','_'));o.Shape=s;o.Label=p['manufacturing_part_id']+' '+p['instance_id']
doc.recompute();doc.saveAs(str(O/'exploded-wood-review.FCStd'));A.closeDocument(doc.Name)
(O/'exploded-transforms.json').write_text(json.dumps(exploded_offsets,indent=2)+'\n')
print('FLATPACK_V331_EXACT_REVIEW_EXPORT_PASS',len(manifest),flush=True)
