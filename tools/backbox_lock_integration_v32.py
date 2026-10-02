"""Rear-operated positive backbox locks. Original CERN-OHL-S-2.0.
Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet
Hardware volumes are packaging reserves; permanent drilling remains provisional.
"""
from pathlib import Path
import sys,json,math
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
import backbox_service_v32 as service
from backbox_service_v32 import V,A,Part,box,shifted,mirror,hits,minimum,face,bounds,load,transform,actual,pf_names,mesh,WPC,PF
from backbox_structure_review_v32 import reserves,passage
C=json.loads((R/'config/backbox_lock_integration_v32.json').read_text());O=R/C['output_directory']
FLOOR=614.9;SHELF=596.9

def cyl(x,y,z,r,h):return Part.makeCylinder(r,h,V(x,y,z))
def knob(x,y,z):
    # z = underside of head. Full rotating head disk is the occupied envelope.
    return cyl(x,y,z,C['knob_radius_mm'],C['knob_height_mm']).fuse(cyl(x,y,z-C['under_head_length_mm'],C['shaft_diameter_mm']/2,C['under_head_length_mm'])).removeSplitter()
def ring(x,y,z,ro,ri,h):return cyl(x,y,z,ro,h).cut(cyl(x,y,z,ri,h))
def hand(x,y,dz=0):
    # Palm plus two bent-finger corridors reaching opposite knob sides. Includes
    # wrist entry behind the aperture; not a claim covering every hand/glove.
    w,d,h=C['hand_palm_size_mm'];fw,fd,fh=C['finger_size_mm']
    ss={'Palm':box(x-w/2,y-d/2,C['hand_palm_base_z_mm']+dz,w,d,h)}
    for side,xx in [('Left',x-30),('Right',x+16)]:ss['Finger'+side]=box(xx,y-fd/2,C['finger_base_z_mm']+dz,fw,fd,fh)
    return ss
def swept(ss,dx=0,dy=0,dz=0):
    out={}
    for n,s in ss.items():
        b=s.BoundBox;out[n]=box(b.XMin+min(0,dx),b.YMin+min(0,dy),b.ZMin+min(0,dz),b.XLength+abs(dx),b.YLength+abs(dy),b.ZLength+abs(dz))
    return out

def route(x,y):
    hi=C['entry_lift_mm'];yy=C['rear_entry_y_mm']
    return {**{'Entry'+n:s for n,s in swept(hand(x,y,hi),dy=yy-y).items()},**{'Lower'+n:s for n,s in swept(hand(x,y),dz=hi).items()}}

def build_locks(parked=False):
    fixed={};moving={};refs={}
    for i,((x,y),(px,py)) in enumerate(zip(C['lock_centers_xy_mm'],C['parking_centers_xy_mm'])):
        side='L' if i==0 else 'R';name='BB_UprightLock'+side
        # Load-spreading washer stays captive on the knob shank by a stock retainer.
        wx,wy=(px,py) if parked else (x,y)
        moving[name+'Washer']=ring(wx,wy,FLOOR+(36 if parked else 0),16,4.5,3)
        # Two CNC stock pads; generic blind parking thread. The two mounting
        # screws retain stowage pads, never carry upright backbox clamp loads.
        for j in range(2):
            s=box(px-25,py-16,FLOOR+j*18,50,32,18)
            bore=cyl(px,py,FLOOR-3,6,42);s=s.cut(bore)
            for xx in [px-17,px+17]:
                s=s.cut(cyl(xx,py,FLOOR-1,2.25,38))
                if j==1:s=s.cut(Part.makeCone(2.25,4.75,2.5,V(xx,py,FLOOR+33.5)))
            moving[name+'ParkingPad'+str(j)]=s.removeSplitter()
        moving[name+'ParkingThread']=ring(px,py,FLOOR+24,6,3.3,12)
        for j,xx in enumerate([px-17,px+17]):moving[name+'ParkingScrewReserve'+str(j)]=cyl(xx,py,FLOOR-12,2,48).fuse(Part.makeCone(2,4.5,2.5,V(xx,py,FLOOR+33.5))).removeSplitter()
        z=FLOOR+3
        if parked:x,y,z=px,py,FLOOR+39
        moving[name+'Knob']=knob(x,y,z)
        # Captive metal backing is below the shelf, never between bearing faces.
        ox,oy=C['lock_centers_xy_mm'][i]
        fixed['UprightLock'+side+'ShelfThread']=ring(ox,oy,578.9,6,3.3,12)
        fixed['UprightLock'+side+'ShelfBacking']=ring(ox,oy,575.9,16,4.5,3)
        refs[name+'WoodReserve']=cyl(ox,oy,578.9,26,36)
        refs[name+'BoreReference']=cyl(ox,oy,575,4.5,41)
    return moving,fixed,refs

def tether(side,center,head_z):
    i=0 if side=='L' else 1;px,py=C['parking_centers_xy_mm'][i]
    anchor=V(px,py-17.5,FLOOR+27);end=V(center[0],center[1]-22,head_z+13)
    def points(bow):return [anchor*(1-t)+end*t+V(0,0,bow*math.sin(math.pi*t)) for t in [j/24 for j in range(25)]]
    lo,hi=0,100
    for _ in range(36):
        mid=(lo+hi)/2;pp=points(mid);length=sum((b-a).Length for a,b in zip(pp,pp[1:]))
        if length<C['mechanical_tether_length_mm']:lo=mid
        else:hi=mid
    pp=points((lo+hi)/2);r=C['mechanical_tether_corridor_radius_mm'];ss=[]
    for a,b in zip(pp,pp[1:]):ss.append(Part.makeCylinder(r,(b-a).Length,a,b-a))
    for a in pp:ss.append(Part.makeSphere(r,a))
    return Part.makeCompound(ss),sum((b-a).Length for a,b in zip(pp,pp[1:]))

def stored_tether(side,center,head_z):
    """Conservative envelope of positively bundled slack, not a floating arch.
    A reusable cord keeper retains surplus around the knob; the short anchored
    lead has a small sag allowance. Exact keeper/cord requires physical trial.
    """
    i=0 if side=='L' else 1;px,py=C['parking_centers_xy_mm'][i]
    aa=V(px,py-17.5,FLOOR+27);bb=V(center[0],center[1]-22,head_z+13)
    pp=[aa*(1-t)+bb*t-V(0,0,3*math.sin(math.pi*t)) for t in [j/16 for j in range(17)]]
    ss=[]
    for a,b in zip(pp,pp[1:]):ss.append(Part.makeCylinder(1.5,(b-a).Length,a,b-a))
    for a in pp:ss.append(Part.makeSphere(1.5,a))
    # R22 / r3 includes a keeper and up to two 3 mm cord turns around the head.
    ss.append(Part.makeTorus(22,3,V(center[0],center[1],head_z+13)))
    return Part.makeCompound(ss)

def with_tethers(mm,parked):
    out=dict(mm)
    for side,i in [('L',0),('R',1)]:
        xy=C['parking_centers_xy_mm'][i] if parked else C['lock_centers_xy_mm'][i];z=FLOOR+(39 if parked else 3)
        out['BB_UprightLock'+side+'Tether']=stored_tether(side,xy,z)
    return out

def save(name,ss):
    d=A.newDocument('BackboxLocks');d.addProperty('App::PropertyString','Authority');d.Authority='CURRENT DESIGN CANDIDATE; hardware/material/CNC unmeasured; no manufacturing release'
    for n,s in ss.items():d.addObject('PartDesign::Feature',n).Shape=s
    d.recompute();assert not any('Invalid' in ob.State for ob in d.Objects)
    assert all(s.isValid() for s in ss.values());d.saveAs(str(O/(name+'.FCStd')));A.closeDocument(d.Name)

def bore_reference(p,shelf):
    """Design-only reference bores: hardware dimensions are NOT manufacturing frozen."""
    out=dict(p);f=out['BB_Floor'];s=shelf.copy()
    for x,y in C['lock_centers_xy_mm']:
        f=f.cut(cyl(x,y,596,4.5,20));s=s.cut(cyl(x,y,578,6,20))
    for x,y in C['parking_centers_xy_mm']:f=f.cut(cyl(x,y,FLOOR-3,4.5,4))
    out['BB_Floor']=f.removeSplitter();return out,s.removeSplitter()

def coarse_mesh(n,s):
    import MeshPart
    mm=MeshPart.meshFromShape(Shape=s,LinearDeflection=.35,AngularDeflection=.5,Relative=False)
    vv,ff=mm.Topology
    return {'name':n,'label':n,'vertices':[[round(v.x,6),round(v.y,6),round(v.z,6)] for v in vv],'faces':[list(t) for t in ff]}

def certify(mov,obs,start=0,end=90,axis=WPC,axis_direction='X',poser=None):
    """Continuous X-axis rotation, conservative pairwise arc displacement bound."""
    radii={}
    for n,s in mov.items():
        b=s.BoundBox
        radii[n]=max(math.hypot(y-axis.y,z-axis.z) for y in [b.YMin,b.YMax] for z in [b.ZMin,b.ZMax]) if axis_direction=='X' else max(math.hypot(x-axis.x,y-axis.y) for x in [b.XMin,b.XMax] for y in [b.YMin,b.YMax])
    todo=[(start,end)];rows=[]
    while todo:
        lo,hi=todo.pop();mid=(lo+hi)/2;ss=poser(mov,mid) if poser else transform(mov,angle=mid,axis=axis);ok=True
        for n,s in ss.items():
            limit=radii[n]*math.radians((hi-lo)/2)+1e-6;b=s.BoundBox
            for m,t in obs.items():
                c=t.BoundBox;lb=math.sqrt(sum(max(0,getattr(b,k+'Min')-getattr(c,k+'Max'),getattr(c,k+'Min')-getattr(b,k+'Max'))**2 for k in 'XYZ'))
                if lb>limit:continue
                if s.distToShape(t)[0]<=limit:ok=False;break
            if not ok:break
        if ok:rows.append([lo,hi])
        else:
            assert hi-lo>1e-6,('continuous collision',lo,hi,n,m)
            todo.extend([(lo,mid),(mid,hi)])
    return {'range_deg':[start,end],'intervals':sorted(rows),'method':'all pairs: OCC midpoint separation exceeds each moving part arc displacement bound; AABB only rejects distant pairs'}
