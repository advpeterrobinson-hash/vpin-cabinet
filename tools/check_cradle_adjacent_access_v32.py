"""Retained screw drivers and matrix removal route vs newly promoted parts. CERN-OHL-S-2.0."""
from pathlib import Path
import sys,json,math
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from pivot_cradle_integration_v32 import *
O=R/C['output_directory'];s=load(O/'play.FCStd');drivers={}
for row in BASE['support_mounting']['positions']:
 x,y,z=row['head_xyz_mm'];drivers[row['id']]=Part.makeCylinder(8,150,V(x,y,z),V(-row['axis'][0],0,0))
assert not hits(drivers,hardware())
mc=json.loads((R/'config/matrix_cassette_v32.json').read_text());prior=json.loads((R/'exports/generated/matrix-hinge-study-v32/validation.json').read_text())['best_review'];angle=math.radians(mc['tilt_deg']);y0=prior['front_xyz_mm'][1];z0=prior['front_xyz_mm'][2]+mc['installed_z_adjustment_mm'];axis=V(300,y0+95.375*math.cos(angle),z0+95.375*math.sin(angle));mov={n:t for n,t in s.items() if n.startswith('Matrix')};newobs={n:t for n,t in s.items() if n.startswith('BB_') or n.startswith('PF_OpenCradle')};samples=[]
for phase,values in [('rock',[i*.25 for i in range(105)]),('forward',range(69)),('lift',range(101))]:
 for val in values:
  mm=transform(mov,angle=-(val if phase=='rock' else 26),axis=axis)
  for sh in mm.values():sh.translate(V(0,-(0 if phase=='rock' else val if phase=='forward' else 68),val if phase=='lift' else 0))
  hh=hits(mm,newobs);assert not hh,(phase,val,hh);samples.append({'phase':phase,'value':val,'hits':hh})
(O/'adjacent-access-validation.json').write_text(json.dumps({'pass':True,'support_driver_hardware_hits':[],'matrix_route_against_promoted_wood':samples,'scope':'existing matrix route unchanged; extra checks only against promoted backbox/cradle wood, no connector redesign','manufacturing_ready':False},indent=2)+'\n');print('CRADLE_ADJACENT_ACCESS_PASS',len(samples))
