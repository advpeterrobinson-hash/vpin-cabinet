"""Source-dimension schematic for a separate retention proposal. CERN-OHL-S-2.0."""
import hashlib,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,Patch
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'exports/generated/side-panel-v32'
p=json.loads((OUT/'retention-validation.json').read_text());c=p['config']
assert all(v['pass'] for v in p['checks'])
for name,h in p['source_hashes'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,name
assert hashlib.sha256((ROOT/p['saved_proposal']['path']).read_bytes()).hexdigest()==p['saved_proposal']['sha256']
m=json.loads((OUT/'motion-validation.json').read_text());b=m['scene_bounds_mm']['SHELF_1'];s=m['scene_bounds_mm']['SHELF_SUPPORT_1L']
wood='#dfbd8c';support='#bd8954';metal='#506b85';reserve='#159c92'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
fig=plt.figure(figsize=(13,11),facecolor='#f7f9fb')
gs=fig.add_gridspec(2,2,height_ratios=[1.1,1.25],left=.07,right=.96,top=.88,bottom=.07,hspace=.3,wspace=.2)
plan=fig.add_subplot(gs[0,:]);section=fig.add_subplot(gs[1,0]);notes=fig.add_subplot(gs[1,1])
fig.suptitle('V32 | Removable shelf retention',x=.07,y=.98,ha='left',fontsize=21,fontweight='bold',color='#20354b')
fig.text(.07,.937,'SEPARATE PROPOSAL — 4 top-release bolts per shelf; captured nuts in replaceable side supports.',fontsize=11)
fig.text(.07,.91,'Original cabinet unchanged. Candidate dimensions only; hardware, loads and CNC details remain unverified.',fontsize=10,color='#566574')
for i in (1,2,3):
    origin=(3-i)*195
    plan.add_patch(Rectangle((20,origin),560,150,facecolor=wood,edgecolor='#8c6944',alpha=.65))
    for xmin in (18,582-c['support_width_mm']):
        plan.add_patch(Rectangle((xmin,origin),c['support_width_mm'],150,facecolor=support,edgecolor='#845b32',alpha=.7))
    subset=[a for a in p['axes'] if a['shelf']==f'SHELF_{i}']
    by=m['scene_bounds_mm'][f'SHELF_{i}'][2]
    for a in subset:
        x,y,_=a['xyz_mm'];y=origin+y-by
        plan.add_patch(Circle((x,y),c['equipment_access_well_radius_mm'],facecolor='#e7faf6',edgecolor=reserve,lw=1.5))
        plan.add_patch(Circle((x,y),c['clearance_bore_diameter_mm']/2,facecolor=metal))
    plan.text(300,origin+83,f'S{i} | support width {c["support_width_mm"]:g} mm',ha='center',fontweight='bold')
    plan.text(300,origin+47,f'Y offsets {c["bolt_y_offsets_mm"][0]:g} / {c["bolt_y_offsets_mm"][1]:g} from shelf front',ha='center')
plan.set_xlim(0,600);plan.set_ylim(-15,555);plan.set_aspect(.48)
plan.set_xticks([0,48,300,552,600]);plan.set_yticks([])
plan.set_xlabel('Global X (mm) | shelves shown separately, front edge at bottom of each rectangle')
plan.set_title('Plan — bolt bores and equipment access wells',loc='left',fontweight='bold',pad=10)
for spine in plan.spines.values():spine.set_visible(False)
x,y,z=p['axes'][0]['xyz_mm'];zmin=s[4];ztop=b[5]
section.add_patch(Rectangle((20,b[4]),65,b[5]-b[4],facecolor=wood,edgecolor='#8c6944'))
section.add_patch(Rectangle((18,zmin),c['support_width_mm'],s[5]-s[4],facecolor=support,edgecolor='#845b32'))
pw=c['nut_pocket_width_mm']
section.add_patch(Rectangle((x-pw/2,zmin),pw,c['nut_pocket_depth_mm'],facecolor='white'))
section.add_patch(Rectangle((x-c['clearance_bore_diameter_mm']/2,zmin),c['clearance_bore_diameter_mm'],ztop-zmin,facecolor='white'))
section.add_patch(Rectangle((18,zmin-c['cover_thickness_mm']),c['support_width_mm'],c['cover_thickness_mm'],facecolor='#beccd8',edgecolor=metal))
section.add_patch(Rectangle((x-c['cover_bolt_passage_diameter_mm']/2,zmin-c['cover_thickness_mm']),c['cover_bolt_passage_diameter_mm'],c['cover_thickness_mm'],facecolor='white'))
section.add_patch(Rectangle((x-c['equipment_access_well_radius_mm'],ztop),2*c['equipment_access_well_radius_mm'],m['config']['candidate_shelf_payload_height_mm'],facecolor=reserve,alpha=.12,edgecolor=reserve,ls='--'))
section.add_patch(Rectangle((x-c['square_nut_width_mm']/2,zmin+c['nut_bottom_clearance_mm']),c['square_nut_width_mm'],c['square_nut_height_mm'],facecolor=metal))
section.add_patch(Rectangle((x-c['washer_diameter_mm']/2,ztop),c['washer_diameter_mm'],c['washer_thickness_mm'],facecolor=metal))
hz=ztop+c['washer_thickness_mm']
section.add_patch(Rectangle((x-c['shaft_diameter_mm']/2,hz-c['shaft_length_mm']),c['shaft_diameter_mm'],c['shaft_length_mm'],facecolor=metal))
section.add_patch(Rectangle((x-c['head_diameter_mm']/2,hz),c['head_diameter_mm'],c['head_height_mm'],facecolor=metal))
section.annotate('',xy=(x,hz+45),xytext=(x,hz+7),arrowprops={'arrowstyle':'->','color':metal,'lw':2})
section.text(x+13,hz+25,'40 mm\nwithdrawal',color=metal)
section.set_xlim(12,85);section.set_ylim(zmin-10,ztop+70);section.set_aspect('equal')
section.set_xlabel('X (mm)');section.set_ylabel('Z (mm)');section.set_title('Section at S1 left/front bolt',loc='left',fontweight='bold');section.grid(alpha=.1)
notes.axis('off')
lines=[
 'Candidate hardware envelope',
 '12 shafts: Ø5 × 35 mm; heads Ø9 × 4 mm',
 '12 washers: Ø12 × 1 mm',
 '12 square nuts: 10 × 10 × 5 mm',
 '6 bottom covers: 42 × 150 × 3 mm',
 '24 cover fixing locations; screws not modeled',
 '',
 'Access reserved in equipment layout',
 'Ø20 wells through the 60 mm equipment envelope',
 'Top driver probe: Ø16 × 100 mm',
 'Bottom cover driver probe: Ø10 × 80 mm',
 '',
 'After releasing all 4 bolts and washers:',
 'the existing horizontal-first shelf routes remain clear.',
 'Nut pockets stop rotation; covers intercept dropped nuts.',
 '',
 'Thread engagement, grip, vibration, strength, cutter',
 'relief and measured-stock tolerance remain pending.',
]
for index,text in enumerate(lines):
    notes.text(0,1-index*.051,text,va='top',fontweight='bold' if index in (0,7,12) else 'normal',fontsize=10,color='#20354b')
fig.text(.07,.025,'SCHEMATIC, NOT A FABRICATION DRAWING | CERN-OHL-S-2.0 | github.com/advpeterrobinson-hash/vpin-cabinet | CNC BLOCKED',fontsize=9,color='#566574')
fig.savefig(OUT/'05-shelf-retention.png',dpi=160,facecolor=fig.get_facecolor())
print('SHELF_RETENTION_RENDER_PASS')
