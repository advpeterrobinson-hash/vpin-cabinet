"""Original lightweight CAD library, isolated from CURRENT V32. CERN-OHL-S-2.0.
No helical threads, vendor CAD, fit certification or permanent-wood mutations.
"""
from pathlib import Path
import json,math,gzip,hashlib
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[1];C=json.loads((R/'config/hardware_catalog_v33.json').read_text());V=A.Vector
O=R/'exports/generated/hardware-v33';O.mkdir(parents=True,exist_ok=True)
audit=json.loads((R/'library/hardware/current-object-audit.json').read_text());current=R/'exports/generated/backbox-lock-integration-v32/play.FCStd'
d=A.openDocument(str(current));parts={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')};A.closeDocument(d.Name)
refpath=R/'exports/generated/wpc-fold-v32/reference-0.FCStd'
d=A.openDocument(str(refpath));wpc={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')};A.closeDocument(d.Name)
def shift(s,v):t=s.copy();t.translate(V(*v));return t
def cyl(r,h,z=0):return Part.makeCylinder(r,h,V(0,0,z))
def washer(di,do,t):return cyl(do/2,t).cut(cyl(di/2,t)).removeSplitter()
def screw(p):
    dia=p['diameter_mm'];length=p['length_mm'];hd=p['head_diameter_mm'];head=p.get('head','pan')
    if head=='countersunk':
        hh=(hd-dia)/2;shape=cyl(dia/2,length-hh,-length).fuse(Part.makeCone(dia/2,hd/2,hh,V(0,0,-hh)))
    else:
        hh=p['head_height_mm'];shape=cyl(dia/2,length,-length).fuse(cyl(hd/2,hh))
    return shape.removeSplitter()
def marker():
    # Cross marker has no implied hardware dimension. Used only for unmeasured
    # interfaces; never passed to fit/collision or CNC tools.
    return Part.makeBox(20,4,4,V(-10,-2,-2)).fuse(Part.makeBox(4,20,4,V(-2,-10,-2))).fuse(Part.makeBox(4,4,20,V(-2,-2,-10))).removeSplitter()
def compound(names):return Part.makeCompound([parts[n] for n in names])
def representative(it):
    names=[v['object'] for v in it['instances']];id=it['id']
    if id=='H02':names=[n for n in names if n.endswith('1')]
    elif id=='H14':names=[n for n in names if n.endswith('L')]
    elif id=='H16':names=[n for n in names if n.endswith('0')]
    elif id=='I05':names=[n for n in names if n.startswith('UprightLockL')]
    elif id not in ['H03','H15','H22','H23','H24'] and names:names=names[:1]
    return names
def shape(it):
    p=it['model']['parameters'];k=it['model']['kind'];id=it['id'];names=representative(it)
    if k in ['screw','knob'] and all(p.get(x) for x in ['diameter_mm','length_mm','head_diameter_mm']) and (p.get('head')=='countersunk' or p.get('head_height_mm')):
        return screw(p),'ORIGINAL_PARAMETRIC_NOMINAL_NO_THREADS'
    if k=='washer' and all(p.get(x) for x in ['inner_diameter_mm','outer_diameter_mm','thickness_mm']):
        return washer(p['inner_diameter_mm'],p['outer_diameter_mm'],p['thickness_mm']),'ORIGINAL_PARAMETRIC_NOMINAL_NO_THREADS'
    if names:return compound(names),'CURRENT_SIMPLIFIED_ENVELOPE'
    if id in ['H08','H09']:
        from backbox_structure_review_v32 import reserves
        rr=reserves();side='L' if id=='H08' else 'R'
        return Part.makeCompound([rr['BB_HingeArmReserve'+side],rr['BB_HingeFlangeReserve'+side]]),'CURRENT_GROSS_HINGE_RESERVE_NOT_PART_OUTLINE'
    if id in ['H10','F14']:
        name='ConcentricBushingSchematic_L' if id=='H10' else 'PivotBoltSchematic_L'
        return wpc['MovingHardwareSchematic_'+name].copy(),'ORIGINAL_WPC_TOPOLOGY_SCHEMATIC_NOT_PURCHASED_DIMENSIONS'
    return marker(),'UNRESOLVED_MARKER_NOT_HARDWARE_SHAPE'
def save(path,shapes,labels=None):
    doc=A.newDocument('HardwareV33');doc.Comment='CERN-OHL-S-2.0; Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet; VISUALIZATION ONLY; manufacturing BLOCKED'
    for n,s in shapes.items():
        o=doc.addObject('PartDesign::Feature',n);o.Shape=s;o.Label=(labels or {}).get(n,n)
    doc.recompute();assert all(o.Shape.isValid() and len(o.Shape.Solids)>0 for o in doc.Objects)
    path.parent.mkdir(parents=True,exist_ok=True);doc.saveAs(str(path));A.closeDocument(doc.Name)
def mesh(n,s):
    vv,ff=s.tessellate(1.0);return {'name':n,'vertices':[list(v) for v in vv],'faces':ff}
library={};validation=[];modelmesh={}
for it in C['hardware']:
    s,strategy=shape(it);b=s.BoundBox;s=shift(s,[-b.Center.x,-b.Center.y,-b.Center.z]);id=it['id'];library[id]=s
    path=R/it['model']['path'];save(path,{id:s},{id:id+' | '+it['description_en']+' | '+strategy})
    # JSON sidecar is the nominal/provisional parametric source and uncertainty.
    sidecar={'id':id,'model_status':strategy,'coordinate_origin':'representative model bounding-box center; installed coordinates separately cataloged','parameters':it['model']['parameters'],'manufacturing_ready':False,'detailed_threads':False,'source':it['source'],'license':'CERN-OHL-S-2.0','measured':False}
    path.with_suffix('.json').write_text(json.dumps(sidecar,indent=2)+'\n')
    modelmesh[id]=mesh(id,s);validation.append({'id':id,'valid':s.isValid(),'solid_count':len(s.Solids),'model_status':strategy,'file':str(path.relative_to(R)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
for oldid in C['aliases']:
    for p in (R/'library/hardware').rglob(oldid+'.*'):
        if p.suffix in ['.FCStd','.json','.FCBak']:p.unlink() # own generated aliases only
views=[
 ('01','Cabinet mechanical hardware overview',['01','02','03','04','05','12']),
 ('02','Wooden playfield pivot hardware',['03']),('03','Shelf and support hardware',['02']),
 ('04','Main rear service door hardware',['04']),('05','Main fan and filter hardware',['05']),
 ('06','WPC hinge family — physical measurement hold',['06']),('07','Backbox upright locks',['07']),
 ('08','Twin backbox door hardware',['08']),('09','Backbox fan / blank hardware',['09']),
 ('10','Display carrier hardware',['10']),('11','DMD / speaker cassette hardware',['11']),
 ('12','Glass retention hardware',[]),('13','Leg / lockdown unresolved interfaces',[]),
 ('14','All required hardware — separated families',[]),('15','Optional mechanical accessories',[])]
scenes={};review=[]
for num,title,stages in views:
    selected=[it for it in C['hardware'] if it['assembly_stage'] in stages and it['flatpack_classification'] not in ['REFERENCE_ONLY_NOT_FROZEN','FUTURE_ELECTRONICS_HARDWARE','USER_ADAPTER_HARDWARE']]
    if num=='06':selected=[it for it in C['hardware'] if it['id'] in ['H08','H09','H10','F14','F15','W06','B16']]
    if num=='12':selected=[it for it in C['hardware'] if it['id'] in ['F24','I08','G08','G09','G10','B12','G11','G12','F36']]
    if num=='13':selected=[it for it in C['hardware'] if it['id'] in ['H18','H19','B13','F37','F38','H20','H21','F36']]
    if num=='14':selected=[it for it in C['hardware'] if it['flatpack_classification']=='REQUIRED_FLATPACK_HARDWARE']
    if num=='15':selected=[it for it in C['hardware'] if it['flatpack_classification']=='OPTIONAL_FLATPACK_HARDWARE']
    # Native family board stays 1:1; 900 mm cell pitch fits long hinge/glass.
    # Raster atlas renders each cell at its own clearly stated visual scale.
    scene={};labels={}
    for i,it in enumerate(selected):
        id=it['id'];scene[id]=shift(library[id],[i%5*900,i//5*900,0]);labels[id]=id+' x '+str(it['quantity'])+' | '+it['description_en']
    save(O/(num+'-families.FCStd'),scene,labels)
    # Installed review: exact CURRENT objects for selected families plus wood
    # host context in separate native geometry, never merged into CURRENT.
    installed={n:s for n,s in parts.items() if C['object_to_id'].get(n) in {i['id'] for i in selected}}
    if installed:save(O/(num+'-installed.FCStd'),installed)
    review.append({'number':num,'title':title,'family_ids':[it['id'] for it in selected],'cad':num+'-families.FCStd','installed_cad':num+'-installed.FCStd' if installed else None,'quantity_note':'One representative per family. Exact quantity and unresolved counts in catalog. Native family board1:1; raster cell scales independent.'})
with gzip.open(O/'review-mesh.json.gz','wt') as f:json.dump(modelmesh,f,separators=(',',':'))
with gzip.open(O/'installed-mesh.json.gz','wt') as f:json.dump({n:mesh(n,s) for n,s in parts.items()},f,separators=(',',':'))
(O/'cad-library-validation.json').write_text(json.dumps({'pass':all(x['valid'] for x in validation),'models':validation,'detailed_threads':False,'current_modified':False},indent=2)+'\n')
(O/'review-views.json').write_text(json.dumps(review,indent=2)+'\n')
for path,digest in audit['input_sha256'].items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
print('HARDWARE_V33_CAD_LIBRARY_PASS',len(validation),len(review),flush=True)
