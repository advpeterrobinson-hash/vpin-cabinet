"""Exact seat/relief and contact metrology from saved B-reps. CERN-OHL-S-2.0."""
from pathlib import Path
import sys,json,math
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from pivot_cradle_integration_v32 import *
O=R/C['output_directory'];old=load(R/C['source_directory']/'play.FCStd')['PF_OpenCradleL'];seat=Part.makeCompound([f for f in old.Faces if isinstance(f.Surface,Part.Cylinder) and abs(f.Surface.Radius-SR)<1e-7]);rows=[]
def sidearea(s):return sum(f.Area for f in s.Faces if abs(f.normalAt(0,0).x)>.99 and abs(f.CenterOfMass.x-18)<1e-7)
for r in C['radii_mm']:
 s=load(O/f'R{r}.FCStd')['PF_OpenCradleL'];removed=old.cut(s);gap=seat.distToShape(removed)[0]
 # A narrow horizontal slice at the seat-circle center distinguishes the narrow
 # front load web from the wider upper front ear. Do not use top width for the seat.
 widths=[]
 for y0,y1 in [(990,PF.y-SR),(PF.y+SR,1080)]:
  sec=s.common(box(17,y0,SEAT.z-.00001,20,y1-y0,.00002));widths.append(sec.Volume/(18*.00002))
 rows.append({'radius_mm':r,'loaded_seat_to_actual_removed_wood_mm':gap,'minimum_local_ligament_mm':min(BASE['support_mounting']['minimum_upper_ligament_mm'],gap),'front_seat_wall_mm':widths[0],'rear_seat_wall_mm':widths[1],'side_contact_area_mm2':sidearea(s),'side_contact_retained_percent':100*sidearea(s)/sidearea(old),'floor_contact_mm2':face(s,36).Area})
q={'radii':rows,'original_side_contact_mm2':sidearea(old),'definition':'minimum local ligament = smaller of unchanged front seat web and exact distance from original loaded semicircular seat surface to removed relief material. Separate from rear ear width and guide height. R22=0 indicates removed seat material.','geometry_only':True,'manufacturing_ready':False}
(O/'cradle-metrology.json').write_text(json.dumps(q,indent=2)+'\n');print('CRADLE_METROLOGY_PASS',rows,flush=True)
