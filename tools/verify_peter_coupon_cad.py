"""Independent OpenCascade coupon solid / corner-fit verification.
Run with freecadcmd. Original CERN-OHL-S-2.0 source.
"""
from pathlib import Path
import json
import math
import FreeCAD as A
import Part

R=Path(__file__).resolve().parents[1]
O=R/'exports/generated/manufacturing-peter-v1'
manifest=json.loads((O/'coupon-manifest.json').read_text())
t=manifest['stock_thickness_mm'];V=A.Vector
checks=[]
def check(name,ok):
    if not ok:raise ValueError(name)
    checks.append(name)

def footprint(row):
    x,y,w,h=row['bounds_xywh_mm'];kind=row['shape'];r=row.get('radius_mm',2)
    if kind=='circle':return Part.Face(Part.Wire([Part.makeCircle(w/2,V(x+w/2,y+h/2,0))]))
    if kind=='tbone':
        # Independently construct the footprint as rectangle union four full disks;
        # exactly the outward semicircles used in the SVG contour remain exposed.
        s=Part.makeBox(w,h,1,V(x,y,0))
        for cx,cy in [(x+2,y),(x+w-2,y),(x+2,y+h),(x+w-2,y+h)]:
            s=s.fuse(Part.makeCylinder(2,1,V(cx,cy,0)))
        s=s.removeSplitter()
        check(row['id']+' T-bone area matches four semicircles',abs(s.Volume-(w*h+8*math.pi))<1e-6)
    elif r:
        s=Part.makeBox(w-2*r,h,1,V(x+r,y,0)).fuse(Part.makeBox(w,h-2*r,1,V(x,y+r,0)))
        for cx,cy in [(x+r,y+r),(x+w-r,y+r),(x+r,y+h-r),(x+w-r,y+h-r)]:
            s=s.fuse(Part.makeCylinder(r,1,V(cx,cy,0)))
        s=s.removeSplitter()
    else:s=Part.makeBox(w,h,1,V(x,y,0))
    return next(f for f in s.Faces if f.BoundBox.ZLength<1e-7 and abs(f.BoundBox.ZMin)<1e-7)

features={f['id']:f for f in manifest['features']}
shapes={id:footprint(row) for id,row in features.items()}
board=shapes['BOARD'].extrude(V(0,0,t))
for id,row in features.items():
    if id in ('BOARD','FIT_KEY'):continue
    depth=t if row['operation']=='THROUGH' else row['depth_mm']
    cut=shapes[id].extrude(V(0,0,depth));cut.translate(V(0,0,t-depth))
    board=board.cut(cut)
board=board.removeSplitter()
key=shapes['FIT_KEY'].extrude(V(0,0,t))
check('Coupon board remains one valid solid',board.isValid() and len(board.Solids)==1)
check('Fit key remains one valid solid',key.isValid() and len(key.Solids)==1)
check('15 mm separate part spacing',abs(board.distToShape(key)[0]-15)<1e-6)
for id in ('TBONE_POCKET','R2_POCKET'):
    x,y,_,_=features[id]['bounds_xywh_mm']
    test=Part.makeBox(25,25,6,V(x,y,t-6))
    vol=test.common(board).Volume
    check('Square key corner '+id,vol<1e-6 if id=='TBONE_POCKET' else vol>1)
for i in range(6):
    row=features[f'SLOT_{i+1}'];x,y,w,h=row['bounds_xywh_mm']
    # Stand the key on its 25 mm edge: mating width is actual sheet thickness.
    test=Part.makeBox(t,25,t,V(x+(w-t)/2,y+(h-25)/2,0))
    overlap=test.common(board).Volume
    check(row['id']+' geometric clearance sign',overlap<1e-6 if row['total_clearance_mm']>=0 else overlap>1)
check('Blind pockets retain measured stock minus6 floor',t>6)
doc=A.newDocument('PeterCouponReview')
for name,shape in [('CouponBoard',board),('FitKey',key)]:
    obj=doc.addObject('PartDesign::Feature',name);obj.Shape=shape
    obj.addProperty('App::PropertyString','Authority');obj.Authority=manifest['thickness_authority']+' — REVIEW ONLY'
doc.recompute()
check('Document recomputes',all('Invalid' not in o.State for o in doc.Objects))
doc.saveAs(str(O/'coupon-review.FCStd'));A.closeDocument(doc.Name)
(O/'cad-validation.json').write_text(json.dumps({'pass':True,'checks':checks,
    'package_sha256':manifest['package_sha256'],'physical_fit_validated':False,
    'thickness_authority':manifest['thickness_authority'],'manufacturing_release':False},indent=2)+'\n')
print('PETER_COUPON_CAD_PASS',len(checks),flush=True)
