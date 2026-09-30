"""Measure supplied STL cross-section; STL units assumed mm. CERN-OHL-S-2.0."""
import hashlib,json,struct
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1]
p=R/'library/references/3d-print/piant/Pinball_Leg_Hole_Guide.stl'
b=p.read_bytes();count=struct.unpack_from('<I',b,80)[0];assert len(b)==84+50*count
triangles=np.array([struct.unpack_from('<12fH',b,84+i*50)[3:12] for i in range(count)]).reshape(-1,3,3)
points=[]
for triangle in triangles:
 for a,b in zip(triangle,np.roll(triangle,-1,axis=0)):
  if (a[2]-22)*(b[2]-22)<0:points.append((a+(b-a)*(22-a[2])/(b[2]-a[2]))[:2])
points=np.array(points);circles=[]
for low,high in [(-8,5),(-65,-52)]:
 xy=points[(points[:,0]>-16)&(points[:,0]<-4)&(points[:,1]>low)&(points[:,1]<high)]
 a=np.column_stack([2*xy[:,0],2*xy[:,1],np.ones(len(xy))]);rhs=(xy*xy).sum(axis=1)
 x,y,k=np.linalg.lstsq(a,rhs,rcond=None)[0];radius=float((k+x*x+y*y)**.5)
 error=float(np.abs(np.linalg.norm(xy-[x,y],axis=1)-radius).max());assert error<.01
 circles.append({'center_xy':[float(x),float(y)],'diameter_mm_assumed':2*radius,'max_fit_error_mm_assumed':error})
pitch=abs(circles[0]['center_xy'][1]-circles[1]['center_xy'][1]);assert abs(pitch-57)<.01;assert abs(pitch-58)>.9
vs=triangles.reshape(-1,3)
report={'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'triangles':count,'bounds_stl_units':[vs.min(axis=0).tolist(),vs.max(axis=0).tolist()],'units':'STL unitless; mm assumed, not manufacturing evidence','section_z':22,'circles':circles,'pitch_mm_assumed':pitch,'license':'CC-BY-4.0, PiAnt; see adjacent ATTRIBUTION.txt','scope':'Fits two circular sections; not print tolerance, mesh manifoldness or physical hardware qualification'}
p.with_name('measurement.json').write_text(json.dumps(report,indent=2)+'\n')
print('LEG_JIG_MEASUREMENT_PASS',round(pitch,6),'mm assumed; distinct from 58mm linked jig')
