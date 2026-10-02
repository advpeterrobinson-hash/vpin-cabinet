"""Active WPC kinematic datum. No CNC drilling authority. CERN-OHL-S-2.0."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def reference_axis(reference=None):
 c=reference or json.loads((ROOT/'config/wpc_kinematics_v32.json').read_text())
 axis=[300,c['cabinet_rear_y_mm']-c['pivot_from_rear_mm'],c['pivot_z_mm']]
 if axis!=[300,1066.8,508] or c['axis_xyz_mm']!=axis or c['motion']!='PURE_ROTATION':
  raise ValueError('Invalid active WPC datum; use validated 241.3 mm rear offset, Y1066.8/Z508')
 if c['final_hinge_hole_pattern'] is not None or c['manufacturing_ready']:
  raise ValueError('Kinematic reference does not release hardware drilling')
 return axis
