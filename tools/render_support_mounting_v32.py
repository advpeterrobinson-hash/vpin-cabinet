"""Nominal CNC/assembly SVG from validated V32 support dimensions. CERN-OHL-S-2.0."""
from pathlib import Path
import json, math
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/wood-dowel-pivot-v32';r=json.loads((O/'validation.json').read_text());v=r['review'];m=v['support_mounting'];c=json.loads((R/'config/wood_dowel_pivot_v32.json').read_text());py,pz=v['pivot_xyz_mm'][1:];rr=16.5;cz=pz+.5;top=pz+30;front=m['foot_y_min_mm'];rear=m['foot_y_max_mm'];shoulder=m['shoulder_z_mm']
X=lambda y:110+(y-(py-40))*1.15
Z=lambda z:680-(z-36)*1.15
pt=lambda y,z:f'{X(y):.3f},{Z(z):.3f}'
path=f'M {pt(front,36)} L {pt(rear,36)} L {pt(rear,268)} L {pt(1068,268)} L {pt(1068,332)} L {pt(rear,332)} L {pt(rear,top)} L {pt(py+rr,top)} L {pt(py+rr,cz)} A {rr*1.15},{rr*1.15} 0 0 1 {pt(py-rr,cz)} L {pt(py-rr,top)} L {pt(py-40,top)} L {pt(py-40,shoulder)} L {pt(front,shoulder)} Z'
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="900" viewBox="0 0 1200 900"><rect width="1200" height="900" fill="white"/><style>text{font-family:sans-serif;fill:#20313c;font-size:16px}.small{font-size:13px}</style>']
def text(x,y,s,cl=''):svg.append(f'<text x="{x}" y="{y}" class="{cl}">{s}</text>')
text(35,35,'V32 · SUPPORT MOUNTING · NOMINAL ASSEMBLY DRAWING', '')
text(35,60,'CNC/assembly reference · geometry not manufacturing-approved · measure both plywood pieces and purchased screw', 'small')
svg.append(f'<path d="{path}" fill="#dec498" stroke="#5c4530" stroke-width="1.5"/>')
svg.append(f'<circle cx="{X(py)}" cy="{Z(pz)}" r="{16*1.15}" fill="#8c623c" fill-opacity=".4" stroke="#5c4530"/>')
for row in m['positions']:
 if 'ScrewL' not in row['id']:continue
 x,y,z=row['head_xyz_mm'];svg.append(f'<circle cx="{X(y)}" cy="{Z(z)}" r="{2.5*1.15}" fill="white" stroke="#20313c"/><circle cx="{X(y)}" cy="{Z(z)}" r="{4.5*1.15}" fill="none" stroke="#20313c" stroke-dasharray="3 2"/>');text(88,Z(z)+5,row['id'][-1])
text(35,100,'Identical 18 mm profiles; countersinks face cabinet interior')
text(230,135,'80 mm upper profile; open U depth 46 mm')
text(230,160,'Mouth 33 mm; dowel Ø32; minimum unseating lift 46 mm')
text(230,185,'Demonstrated lift 48 mm: 2 mm over the upper edges')
text(230,220,'Front shoulder clears retained crossmember guide by 1 mm')
text(230,245,'Rear relief clears unchanged SSF exciter by 2 mm')
text(35,715,'DIRECT BEARING ON CABINET FLOOR · Z36')
text(230,285,'HEADS: left X36 / right X564')
for i,row in enumerate([row for row in m['positions'] if 'ScrewL' in row['id']]):
    _,y,z=row['head_xyz_mm'];text(230,310+i*25,f'{i+1}: Y {y:.3f} / Z {z:.3f}')
svg.append('<rect x="550" y="315" width="108" height="150" fill="#dec498" stroke="#20313c"/><rect x="658" y="315" width="108" height="150" fill="#c9ad81" stroke="#20313c"/><line x1="550" y1="385" x2="730" y2="385" stroke="#7899ad" stroke-width="9"/><circle cx="550" cy="385" r="12" fill="#7899ad"/>')
text(545,290,'SCREW STACK · head inside → outer face')
text(550,490,'SUPPORT 18 mm');text(658,515,'SIDE 18 mm')
text(550,550,'4.5 × 30 mm countersunk wood screw; Torx candidate')
text(550,575,'Length includes head; flush seat: 12 mm side engagement')
text(550,600,'6 mm wood remains beyond tip; no exterior breakthrough')
text(550,625,'Clearance Ø5 through support; countersink Ø9 × 90°, depth 2')
text(550,650,'Side CNC: Ø3 × 1 mm shallow pilot mark from inside ONLY')
text(550,675,'Manual pilot: Ø3, total depth 13 mm from SIDE INNER FACE')
text(550,700,'Maximum total pilot depth: 15 mm (including drill tip)')
text(550,725,'Measure drill projection; use depth stop; never drill through')
text(35,755,'XYZ HEAD DATUMS: left X36 (drive −X); right X564 (drive +X). Side pilots: left X18; right X582.')
text(35,780,'SCREWS = REQUIRED · WOOD GLUE = OPTIONAL AFTER FINAL VALIDATION · NAILS = NOT USED')
text(35,805,'Dry fit → confirm floor/side contact → test pivot/lift → validate geometry → optional PVA on side/floor interfaces')
text(35,830,'Vertical load: PLAYFIELD / DOWEL → WOOD CRADLE → WOOD SUPPORT → DIRECT BEARING ON CABINET FLOOR')
text(35,850,'Side screws retain against tipping, separation and longitudinal/service displacement. No glue-dependent load path.', 'small')
text(35,880,'CERN-OHL-S-2.0 · Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet', 'small')
svg.append('</svg>');(O/'support-mounting-assembly.svg').write_text('\n'.join(svg)+'\n')
(O/'support-mounting-schedule.json').write_text(json.dumps(m,indent=2)+'\n')
