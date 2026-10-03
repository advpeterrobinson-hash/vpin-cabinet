"""Solid corner blocks and original parametric drill tooling. CERN-OHL-S-2.0.
Run with FreeCADCmd. Config reference values do NOT release drilling or printing
for use. Exports are virtual-fit demonstrators until hardware/print qualification.
"""
from pathlib import Path
import json,math,gzip,zipfile
import FreeCAD as A, Part, MeshPart
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/solid-leg-v334';O.mkdir(parents=True,exist_ok=True)
C=json.loads((R/'config/solid_leg_blocks_v334.json').read_text());P=C['jig'];V=A.Vector
source=A.openDocument(str(R/'exports/generated/backbox-lock-integration-v32/play.FCStd'))
reg=json.loads((R/'exports/generated/flatpack-v331/manufacturing-register.json').read_text())
def fuse(ss):
 s=ss[0]
 for q in ss[1:]:s=s.fuse(q)
 return s.removeSplitter()
def difference(a,b):return a.cut(b).Volume+b.cut(a).Volume
def mesh(s):
 m=MeshPart.meshFromShape(Shape=s,LinearDeflection=.15,AngularDeflection=.25,Relative=False);v,f=m.Topology
 return {'vertices':[list(x) for x in v],'faces':[list(x) for x in f]}
def block(w,d,h):return Part.Face(Part.makePolygon([V(0,0,0),V(w,0,0),V(0,d,0),V(0,0,0)])).extrude(V(0,0,h))
W,D,H=[P[k] for k in ['block_width_mm','block_depth_mm','block_height_mm']]
blank=block(W,D,H);rows=[];shapes={};meshdata={};newparts=[];packing_mesh={}
for side,pid,sx,sy,ox,oy,z0 in [('FL','P029',1,1,18,18,54),('FR','P030',-1,1,582,18,54),('RL','P031',1,-1,18,1290.1,36),('RR','P032',-1,-1,582,1290.1,36)]:
 original=source.getObject('CandidateLegBlock'+side).Shape.copy()
 # Mirror placement preserves the exact triangular structural blank, not its
 # loose cylindrical OCCT bounding box. Finite planar top vertices are datums.
 m=A.Matrix(sx,0,0,ox,0,sy,0,oy,0,0,1,z0,0,0,0,1)
 proposed=blank.copy();proposed.transformShape(m,True);packing_mesh[pid+'-Solid']=mesh(proposed)
 axes=[];drilled=proposed.copy()
 for f in original.Faces:
  if type(f.Surface).__name__!='Cylinder':continue
  surf=f.Surface;ax=surf.Axis;c=surf.Center
  bore=Part.makeCylinder(surf.Radius,250,c-ax*30,ax);drilled=drilled.cut(bore)
  a=V(sx/math.sqrt(2),sy/math.sqrt(2),0);entry=V(ox+sx*W/2,oy+sy*D/2,c.z);exit=V(ox,oy,c.z)
  axes.append({'axis_world':list(ax),'point_world':list(c),'entry_on_diagonal_world':list(entry),'block_exit_corner_world':list(exit),'nominal_block_travel_mm':entry.distanceToPoint(exit),'diameter_mm':2*surf.Radius,'height_from_bottom_mm':c.z-z0,'depth_from_top_mm':z0+H-c.z})
 rebuilt=[]
 for p in reg['parts']:
  if p['assembly_id']!=pid:continue
  s=Part.read(str(R/p['finished_member_brep']));s.transformShape(A.Matrix(*p['local_to_installed_matrix']));rebuilt.append(s)
 union=fuse(rebuilt);delta=difference(union,drilled)
 assert delta<1e-3,(side,delta)
 top=max((f for f in original.Faces if type(f.Surface).__name__=='Plane' and f.normalAt(0,0).z>.99),key=lambda f:f.CenterOfMass.z)
 ext=[max(getattr(v.Point,k) for v in top.Vertexes)-min(getattr(v.Point,k) for v in top.Vertexes) for k in ['x','y']]
 assert max(abs(ext[i]-[W,D][i]) for i in range(2))<1e-6 and abs(original.BoundBox.ZLength-H)<1e-6
 axes.sort(key=lambda a:a['height_from_bottom_mm']);assert abs(axes[1]['height_from_bottom_mm']-axes[0]['height_from_bottom_mm']-58)<1e-6
 row={'assembly_id':pid,'side':side,'source_component':'CandidateLegBlock'+side,'family':'SW01','raw_square_stock_mm':[W,D,H],
 'finished_section':'RIGHT_ISOSCELES_TRIANGLE_45_DEG_SHOP_RIP','triangular_blank_volume_mm3':blank.Volume,'finished_reference_volume_mm3':drilled.Volume,
 'square_stock_excess_over_blank_mm3':W*D*H-blank.Volume,'old_lamination_union_difference_mm3':delta,'original_difference_mm3':difference(original,drilled),'axes':axes,'local_to_installed_matrix':list(m.A)}
 rows.append(row);shapes[side]=drilled;meshdata[pid+'-Solid']=mesh(drilled)
 local=blank.copy()
 for ax in axes:local=local.cut(Part.makeCylinder(ax['diameter_mm']/2,130,V(-20,-20,ax['height_from_bottom_mm']),V(1,1,0)))
 local.exportBrep(str(O/(pid+'-solid-reference.brep')))
 # Finished stock is shop-made, never a member of the plywood nesting set.
 old=next(p for p in reg['parts'] if p['assembly_id']==pid)
 q={**old,'instance_id':pid+'-Solid','manufacturing_part_id':'SW01','description_en':'Solid-wood leg corner block '+side,'description_pt_BR':'Bloco maciço do pé '+side,
 'manufacturing_class':'SHOP_MADE_SOLID_WOOD_PART','material_class':'STRUCTURAL_SOLID_WOOD','nominal_stock_thickness_mm':None,'finished_reference_thickness_mm':H,
 'finished_xy_bounds_mm':[0,0,W,D],'finished_xy_size_mm':[W,D],'volume_mm3':drilled.Volume,'projected_area_mm2':W*D/2,
 'local_to_installed_matrix':list(m.A),'finished_member_brep':str((O/(pid+'-solid-reference.brep')).relative_to(R)),
 'through_cuts':[],'pockets':[],'reference_features':axes,'manual_finish':[{'operation':'SHOP_CUT_SQUARE_STOCK_AND_45_DEG_RIP','instruction':'Shop supplies triangular prism; ordinary builder tools do not make the long rip.'},{'operation':'JIG_GUIDED_DRILLING_HOLD','instruction':'Measure real leg/backing/bolt hardware; qualify print/bushings and hand drill before drilling. Use selected parameters, not reference58mm by default.'}],
 'manufacturing_status':'SHOP_MADE_SOLID_WOOD_PART','machining_face':'SHOP_DATUM_A_DIAGONAL','opposite_face':'NO CNC','face_A_outward_world':[sx/math.sqrt(2),sy/math.sqrt(2),0],
 'facing_reduction_mm':0,'fit_dependent':True,'coupon_dependent':False,'joinery':'One solid triangular prism; no plywood lamination glue-up. Cabinet attachment qualification unchanged.',
 'review_outline':[[0,0],[W,0],[0,D],[0,0]],'quantity':1}
 newparts.append(q)
# Jig local system: U across the diagonal; V away from the wood; Z up. Printed
# guide bores are parallel to V. Rotation into world reproduces the45°CAD axis.
span=math.hypot(W,D);t=P['plate_thickness_mm'];L=P['guide_length_mm'];OD=P['bushing_outer_diameter_mm'];ID=P['bushing_inner_diameter_mm'];fit=P['print_fit_clearance_mm']
assert OD>ID>=P['bore_diameter_mm'] and t>=6 and L>0, 'Invalid sleeve/guide packaging parameters'
delta=math.radians(P['bore_angle_deg']-math.degrees(math.atan2(D,W)))
guide_axis=V(math.sin(delta),math.cos(delta),0)
assert abs(delta)<math.radians(25),'Large angle change requires a new guide-body packaging review'
zhi=H-P['edge_offset_mm'];zlo=zhi-P['bore_spacing_mm'];assert zlo>OD/2+5 and zhi<H-OD/2-5
plate=Part.makeBox(span-.4,t,H,V(-(span-.4)/2,0,0))
body=plate
for z in [zlo,zhi]:
 origin=V(0,0,z);boss=Part.makeCylinder(OD/2+P['boss_wall_mm'],L,origin+guide_axis*(t/math.cos(delta)),guide_axis);body=body.fuse(boss).cut(Part.makeCylinder((P['bore_diameter_mm']+fit)/2,L+t/math.cos(delta)+2,origin-guide_axis,guide_axis)).cut(Part.makeCylinder((OD+fit)/2,L+1,origin+guide_axis*(t/math.cos(delta)),guide_axis))
# Clamp flats are broad uninterrupted lands away from guide axes.
for u in [-span/2+4,span/2-16]:body=body.fuse(Part.makeBox(12,5,24,V(u,t,50)))
body=body.removeSplitter()
# Separate top saddle clips over the body top, with a hard depth shoulder and
#20mm bearing shelf on the block top. Prints on its U end face; localized tongue support may be needed.
body=body.cut(Part.makeBox(20,t-4,10,V(-10,2,H-10))).removeSplitter()
cap=Part.makeBox(30,26+t,6,V(-15,-20,H))
cap=cap.fuse(Part.makeBox(20-fit,t-4-fit,10,V(-10+fit/2,2+fit/2,H-10))).removeSplitter()
# Front stop raises the universal rear-index body14mm. A tongue captured by the
# saddle throat locates it; the assembly clamp supplies positive retention.
shimH=P['edge_offset_mm']-P['front_edge_offset_mm'];assert shimH>0
shim=Part.makeBox(30,18,shimH,V(-15,-20,H-shimH))
bushings={};sacrificial={}
for i,z in enumerate([zlo,zhi]):
 bushings['Bushing'+str(i+1)]=Part.makeCylinder(OD/2,L,V(0,0,z)+guide_axis*(t/math.cos(delta)),guide_axis).cut(Part.makeCylinder(ID/2,L,V(0,0,z)+guide_axis*(t/math.cos(delta)),guide_axis))
 sacrificial['Sacrificial'+str(i+1)]=Part.makeCylinder(OD/2,L,V(0,0,z)+guide_axis*(t/math.cos(delta)),guide_axis).cut(Part.makeCylinder((P['bore_diameter_mm']+fit)/2,L,V(0,0,z)+guide_axis*(t/math.cos(delta)),guide_axis))
# Raised UP triangle, visible without color and without text-font dependency.
arrow=Part.Face(Part.makePolygon([V(22,t,108),V(30,t,108),V(26,t,117),V(22,t,108)])).extrude(V(0,1,0))
body=body.fuse(arrow).removeSplitter()
toolparts={'GuideBody':body,'TopSaddle':cap,'FrontStop14':shim,**bushings,**sacrificial};toolmesh={k:mesh(s) for k,s in toolparts.items()}
doc=A.newDocument('LegDrillJigReference');params=doc.addObject('Spreadsheet::Sheet','Parameters')
for i,(k,value) in enumerate(P.items(),1):
 params.set('A'+str(i),k);params.set('B'+str(i),str(value));
 if isinstance(value,(int,float)) and not isinstance(value,bool):params.setAlias('B'+str(i),k)
params.set('D1','REFERENCE ONLY — PHYSICAL HARDWARE AND PRINT QUALIFICATION REQUIRED')
for name,s in toolparts.items():
 obj=doc.addObject('PartDesign::Feature',name);obj.Shape=s;obj.addProperty('App::PropertyString','Authority');obj.Authority='Generated parametric source tools/solid_leg_v334.py + config/solid_leg_blocks_v334.json; regenerate after any parameter change.'
 obj.Label='JIG TOOLING / '+name
 if name.startswith('Sacrificial'):obj.Visibility=False
 doc.recompute()
doc.saveAs(str(O/'leg-drill-jig-REFERENCE.FCStd'))
Part.export([doc.getObject(n) for n in ['GuideBody','TopSaddle','FrontStop14','Bushing1','Bushing2']],str(O/'leg-drill-jig-REFERENCE.step'))
for n in ['GuideBody','TopSaddle','FrontStop14','Sacrificial1']:
 s=toolparts[n].copy()
 # Each member is separately oriented for FDM; no misleading assembled print.
 if n in ['GuideBody','Sacrificial1']:s.rotate(V(),V(1,0,0),90)
 elif n=='TopSaddle':s.rotate(V(),V(0,1,0),90)
 bb=s.BoundBox;s.translate(V(-bb.XMin,-bb.YMin,-bb.ZMin));mt=MeshPart.meshFromShape(Shape=s,LinearDeflection=.1,AngularDeflection=.2,Relative=False);mt.write(str(O/(n+'-REFERENCE.stl')))
 # Minimal standard3MF, one object per file, millimeters, no slicer settings.
 vs,fs=mt.Topology
 xml='<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"><metadata name="Title">REFERENCE ONLY — '+n+'</metadata><resources><object id="1" type="model"><mesh><vertices>'+''.join(f'<vertex x="{v.x}" y="{v.y}" z="{v.z}"/>' for v in vs)+'</vertices><triangles>'+''.join(f'<triangle v1="{f[0]}" v2="{f[1]}" v3="{f[2]}"/>' for f in fs)+'</triangles></mesh></object></resources><build><item objectid="1"/></build></model>'
 with zipfile.ZipFile(O/(n+'-REFERENCE.3mf'),'w',zipfile.ZIP_DEFLATED) as z:
  z.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>');z.writestr('_rels/.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>');z.writestr('3D/3dmodel.model',xml)
print_checks={n:{'valid_solid':s.isValid(),'solids':len(s.Solids),'volume_mm3':s.Volume} for n,s in toolparts.items()}
assert all(v['valid_solid'] and v['solids']==1 for v in print_checks.values()),print_checks
(O/'print-solid-checks.json').write_text(json.dumps(print_checks,indent=2)+'\n')
# Virtual installed jig/tool corridors. Contact surfaces are allowed; penetration
# beyond1e-3mm³ is recorded. Drill body is a conservative example, not chosen tool.
validation=[];scenes={}
for row in rows:
 side=row['side'];m=A.Matrix(*row['local_to_installed_matrix']);sx=m.A11;sy=m.A22;ox=m.A14;oy=m.A24;z0=m.A34
 # Front spacer raises universal body; rear uses bare saddle. Orientation is a
 # rigid right-handed frame for mirrored corners (U sign chosen accordingly).
 normal=V(sx/math.sqrt(2),sy/math.sqrt(2),0);u=V(sy/math.sqrt(2),-sx/math.sqrt(2),0)
 tf=A.Matrix(u.x,normal.x,0,ox+sx*W/2,u.y,normal.y,0,oy+sy*D/2,0,0,1,z0+(shimH if side[0]=='F' else 0),0,0,0,1)
 jig={n:s.copy() for n,s in toolparts.items() if not n.startswith('Sacrificial') and (n!='FrontStop14' or side[0]=='F')}
 for s in jig.values():s.transformShape(tf)
 # The spacer top touches raised saddle, bottom touches block top.
 if side[0]=='F':jig['FrontStop14'].translate(V(0,0,0))
 axes_ok=[];corridors={};hits=[]
 for i,ax in enumerate(row['axes']):
  entry=V(*ax['entry_on_diagonal_world']);zc=zlo if i==0 else zhi;q=tf.multVec(V(0,0,zc));axes_ok.append(q.distanceToPoint(entry))
  world_guide=tf.multVec(guide_axis)-tf.multVec(V())
  corridors['Bit'+str(i)]=Part.makeCylinder(P['bore_diameter_mm']/2,110,q+world_guide*50,-world_guide)
  corridors['DrillBody'+str(i)]=Part.makeCylinder(30,180,q+world_guide*(t/math.cos(delta)+L+15),world_guide)
 # Screen against every CURRENT wood solid (not only shell), separately report
 # intended bore stock/cabinet drill path vs unintended tool body interference.
 for obj in source.Objects:
  if not hasattr(obj,'Shape') or obj.Shape.isNull():continue
  if obj.Name not in {p['source_component'] for p in reg['parts']}:continue
  for n,s in {**jig,**{n:s for n,s in corridors.items() if n.startswith('DrillBody')}}.items():
   if s.BoundBox.intersect(obj.Shape.BoundBox):
    v=s.common(obj.Shape).Volume
    if v>1e-3:hits.append({'tool':n,'obstacle':obj.Name,'penetration_mm3':v})
 if P['bore_spacing_mm']==58 and P['edge_offset_mm']==40 and P['front_edge_offset_mm']==26:assert max(axes_ok)<1e-6,(side,axes_ok)
 # Reference clamp jaw pads on broad lands; actual clamp bars/handles remain
 # selected-tool HOLD. These are installation tooling, never cabinet BOM parts.
 for j,u0 in enumerate([-span/2+10,span/2-10]):
  jaw=Part.makeBox(10,6,18,V(u0-5,t+5,53));jaw.transformShape(tf);corridors['ClampJaw'+str(j)]=jaw
 excluded={'SHELF_1','FLOOR','PC_BASE'}
 setup_hits=[h for h in hits if h['obstacle'] not in excluded]
 assert not setup_hits,setup_hits
 pair_hits=[]
 for i,(an,aa) in enumerate(jig.items()):
  for bn,bb in list(jig.items())[i+1:]:
   volume=aa.common(bb).Volume
   if volume>1e-3:pair_hits.append({'a':an,'b':bn,'volume_mm3':volume})
 assert not pair_hits,pair_hits
 plate=source.getObject('CandidateLegPlate'+side).Shape
 plate_bores=[{'center':list(f.Surface.Center),'axis':list(f.Surface.Axis),'diameter':2*f.Surface.Radius} for f in plate.Faces if type(f.Surface).__name__=='Cylinder']
 registration={'guide_to_block_mm':jig['GuideBody'].distToShape(shapes[side])[0],'top_stop_to_block_mm':jig['FrontStop14' if side[0]=='F' else 'TopSaddle'].distToShape(shapes[side])[0]}
 validation.append({'side':side,'registration_distances':registration,'tooling_pair_penetrations':pair_hits,'backing_plate_reference_bores':plate_bores,'axis_error_mm':axes_ok,'wood_interferences':hits,'early_assembly_obstacles_absent':sorted(excluded),'early_assembly_interferences':setup_hits,'hand_drill_clearance':'HOLD_SELECTED_TOOL_AND_PHYSICAL_TRIAL','clamp_status':'JAW_LANDS_SHOWN_FULL_CLAMP_AND_FIXTURE_HOLD','angle_reference_error_deg':P['bore_angle_deg']-45,'reference_body_radius_mm':30,'reference_body_length_mm':180,'registration':'Diagonal face +top saddle; full-width plate end lands center against adjoining corner planes; clamp required; print tolerance qualification HOLD','mode':'F +14mm stop' if side[0]=='F' else 'R bare stop'})
 scenes[side]={'PlateReference':mesh(source.getObject('CandidateLegPlate'+side).Shape),**{row['assembly_id']+'-Solid':mesh(shapes[side])},**{n:mesh(s) for n,s in jig.items()},**{n:mesh(s) for n,s in corridors.items()}}
(O/'metrology.json').write_text(json.dumps(rows,indent=2)+'\n');(O/'jig-validation.json').write_text(json.dumps({'rows':validation,'physical_accuracy_validated':False,'drilling_released':False,'jig_body_variants':1,'mode_spacer_count':1,'bushing_interface_provisional':True},indent=2)+'\n')
(O/'solid-members.json').write_text(json.dumps(newparts,indent=2)+'\n');(O/'review-mesh.json.gz').write_bytes(gzip.compress(json.dumps({'blocks':meshdata,'packing_blocks':packing_mesh,'tooling':toolmesh,'scenes':scenes}).encode(),mtime=0))
A.closeDocument(doc.Name);A.closeDocument(source.Name)
print('SOLID_LEG_V334_PASS',[(r['side'],r['old_lamination_union_difference_mm3']) for r in rows],flush=True)
