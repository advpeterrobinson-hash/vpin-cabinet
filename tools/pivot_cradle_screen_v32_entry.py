"""Study all requested radii before any promotion. CERN-OHL-S-2.0."""
from pathlib import Path
import sys,json,math
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from pivot_cradle_integration_v32 import *
O=R/C['output_directory'];O.mkdir(parents=True,exist_ok=True);s=load(R/C['source_directory']/'play.FCStd');orig=s['PF_OpenCradleL'];area0=seat_area(orig);rows=[];shapes={}
for r in C['radii_mm']:
 pair,cut=relief(orig,r);left=pair['PF_OpenCradleL'];top=WPC.z-r-C['radial_allowance_mm'];guide=top-C['external_corner_radius_mm']-SEAT.z;wrap=seat_area(left)/(SR*18)*180/math.pi;hw=keepout(r);gap=minimum(pair,hw)['mm'];seat_arc=Part.makeCompound([f for f in orig.Faces if isinstance(f.Surface,Part.Cylinder) and abs(f.Surface.Radius-SR)<1e-7]);ear=PF.y+40-(PF.y+SR)
 reasons=[];g=C['geometry_screen'];web=BASE['support_mounting']['minimum_upper_ligament_mm']
 if len(left.Solids)!=1 or not left.isValid():reasons.append('not one valid CNC solid')
 if wrap<g['minimum_seat_wrap_deg']:reasons.append('loaded semicircular seat shortened')
 if guide<g['minimum_straight_rear_guide_above_seat_axis_mm']:reasons.append('insufficient rear straight guidance height')
 if top-SEAT.z<g['minimum_rear_top_above_seat_axis_mm']:reasons.append('insufficient rear top margin above seat axis')
 if web<g['minimum_existing_seat_web_mm']:reasons.append('existing seat web below screen')
 if hits(pair,hw) or gap<C['radial_allowance_mm']-1e-6:reasons.append('hardware reserve lacks radial allowance')
 row={'radius_mm':r,'profile':C['profile'],'pass':not reasons,'fail_reasons':reasons,'solid_count':len(left.Solids),'valid':left.isValid(),'seat_wrap_before_deg':area0/(SR*18)*180/math.pi,'seat_wrap_after_deg':wrap,'minimum_existing_seat_web_mm':web,'rear_ear_nominal_width_before_relief_mm':ear,'rear_top_z_mm':top,'rear_top_above_seat_axis_mm':top-SEAT.z,'rear_straight_guide_height_mm':guide,'coaxial_reserve_gap_mm':gap,'reserve_to_original_loaded_seat_mm':seat_arc.distToShape(hw['L'])[0],'removed_volume_each_mm3':orig.Volume-left.Volume,'support_volume_retained_percent':100*left.Volume/orig.Volume}
 rows.append(row);shapes[r]=pair
 d=A.newDocument('Relief'+str(r))
 for n,sh in pair.items():o=d.addObject('PartDesign::Feature',n);o.Shape=sh
 d.addProperty('App::PropertyString','StudyStatus');d.StudyStatus=('GEOMETRY SCREEN PASS' if not reasons else 'REJECTED')+'; NO MANUFACTURING RELEASE';d.recompute();d.saveAs(str(O/f'R{r}.FCStd'));A.closeDocument(d.Name)
 print('RADIUS',row,flush=True)
# Meaningful fixed-integration and moving-assembly probes before selecting anything.
for row in rows:
 if not row['pass']:continue
 r=row['radius_mm'];fixed=actual(load(R/C['source_directory']/'matrix-removed.FCStd'));fixed.update(shapes[r]);names=pf_names(fixed);moving={n:fixed.pop(n) for n in names};back={n:fixed.pop(n) for n in list(fixed) if n.startswith('BB_')};hw=hardware();installed={n:t for n,t in hw.items() if n.startswith('WPC_')};moving_arms={n:t for n,t in hw.items() if n.startswith('BB_')};fixed.update(back)
 cross={}
 for kind,values in [('service',range(51)),('lift',range(49))]:
  bad=[]
  for v in values:
   ps=transform(moving,angle=-v if kind=='service' else 0,lift=v if kind=='lift' else 0)
   hh=hits(ps,{**fixed,**hw})
   if hh:bad.append({'value':v,'hits':hh})
  cross[kind]=bad
 cross['hardware_closed']=hits(installed,{n:t for n,t in {**fixed,**moving}.items() if n not in ['SIDE_L','SIDE_R']})
 cross['tool_closed']=hits(tools_for_pivot(),{n:t for n,t in {**fixed,**moving}.items() if n not in ['SIDE_L','SIDE_R']})
 cross['tool_service']=hits(tools_for_pivot(),{**{n:t for n,t in fixed.items() if n not in ['SIDE_L','SIDE_R']},**transform(moving,angle=-50)})
 cross['tool_lift']=hits(tools_for_pivot(),{**{n:t for n,t in fixed.items() if n not in ['SIDE_L','SIDE_R']},**transform(moving,lift=48)})
 row['cross_screen']=cross;print('CROSS',r,cross,flush=True)
report={'source_head':C['source_head'],'dowel_axis_xyz_mm':list(PF),'seat_circle_axis_xyz_mm':list(SEAT),'wpc_axis_xyz_mm':list(WPC),'axis_separation_mm':math.hypot(PF.y-WPC.y,PF.z-WPC.z),'wpc_to_seat_circle_axis_mm':math.hypot(SEAT.y-WPC.y,SEAT.z-WPC.z),'wpc_to_rear_edge_mm':orig.BoundBox.YMax-WPC.y,'wpc_to_top_edge_mm':orig.BoundBox.ZMax-WPC.z,'wpc_to_seat_opening_rear_wall_mm':WPC.y-(PF.y+SR),'wpc_to_loaded_semicircle_mm':seat_arc.distToShape(Part.Vertex(V(27,WPC.y,WPC.z)))[0],'candidates':rows,'manufacturing_ready':False}
(O/'radius-study.json').write_text(json.dumps(report,indent=2)+'\n');print('CRADLE_RADIUS_SCREEN_DONE',flush=True)
