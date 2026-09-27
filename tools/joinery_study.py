"""Isolated nominal captured-shell study. No adoption or manufacturing release."""
import json
from pathlib import Path
import FreeCAD as App
import Part
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'exports/generated/joinery-study-v32'
BASE=ROOT/'.work/joinery-study/v32-baseline.FCStd'
CFG=ROOT/'config/joinery_study_v32.json'

def box(x,y,z,dx,dy,dz):
    return Part.makeBox(dx,dy,dz,App.Vector(x,y,z))

def build():
    c=json.loads(CFG.read_text())
    assert not c['manufacturing_ready'] and c['status']=='PROPOSAL_NOT_ADOPTED'
    assert c['nominal_stock_mm']==18, 'Different stock requires a complete baseline regeneration'
    assert c['capture_depth_mm']>0 and c['total_fit_clearance_mm']>=0
    assert c['nominal_stock_mm']-c['capture_depth_mm']>=c['minimum_residual_skin_mm']
    OUT.mkdir(parents=True,exist_ok=True)
    base=App.openDocument(str(BASE));doc=App.newDocument('V32CapturedShellStudy')
    for old in base.Objects:
        if not hasattr(old,'Shape'): continue
        o=doc.addObject('PartDesign::Feature',old.Name);o.Shape=old.Shape.copy();o.Label=old.Label
        for prop in ['PartCode','LegacyId','PartStatus','NameEN','NamePTBR','Purpose','Category']:
            o.addProperty('App::PropertyString',prop);setattr(o,prop,getattr(old,prop))
        o.addProperty('App::PropertyString','StudyStatus');o.StudyStatus='PROPOSAL / CNC BLOCKED'
        if old.Name in c['changed_parts']:
            o.addProperty('App::PropertyString','ProposedRevision');o.ProposedRevision='R2-PROPOSAL'
            o.Label=old.PartCode+'-R2-PROPOSAL - '+old.NameEN
    d=c['capture_depth_mm'];gap=c['total_fit_clearance_mm']/2
    # Extend only mating edges; existing cutouts remain untouched.
    for name,y,z,length,height in [('FLOOR',18,18,1272.1,18),('FRONT',0,0,18,400.05),('REAR',1290.1,0,18,596.9)]:
        o=doc.getObject(name)
        o.Shape=o.Shape.fuse(box(18-d,y,z,d,length,height)).fuse(box(582,y,z,d,length,height)).removeSplitter()
    for name,x in [('SIDE_L',18-d),('SIDE_R',582)]:
        o=doc.getObject(name)
        floor=box(x,18,18-gap,d,1272.1,18+2*gap)
        front=box(x,0,0,d,18+gap,596.9)  # open edge/top: no fragile stopped lip above Front
        rear=box(x,1290.1-gap,0,d,18+gap,596.9)
        o.Shape=o.Shape.cut(floor.fuse(front).fuse(rear)).removeSplitter()
    doc.recompute()
    doc.saveAs(str(OUT/'captured-shell-proposal.FCStd'))
    App.closeDocument(doc.Name);App.closeDocument(base.Name)
    print('JOINERY_STUDY_BUILT')

def verify(path=None,write=True):
    c=json.loads(CFG.read_text());doc=App.openDocument(str(path or OUT/'captured-shell-proposal.FCStd'))
    base=App.openDocument(str(BASE));obs={o.Name:o for o in doc.Objects if hasattr(o,'Shape')}
    old={o.Name:o for o in base.Objects if hasattr(o,'Shape')};checks=[]
    def check(name,passed,detail=None): checks.append(dict(check=name,passed=bool(passed),detail=detail))
    try:
        check('same 45 objects',set(obs)==set(old) and len(obs)==45)
        check('all valid single solids',all(o.Shape.isValid() and len(o.Shape.Solids)==1 and 'Invalid' not in str(o.State) for o in obs.values()))
        changes=[]
        for n,o in obs.items():
            a=o.Shape;b=old[n].Shape;removed=b.cut(a).Volume;added=a.cut(b).Volume
            if added+removed>1e-5:changes.append(dict(id=n,part_code=o.PartCode,removed_mm3=removed,added_mm3=added,before_bounds=bounds(b),after_bounds=bounds(a)))
        check('only five approved study interfaces changed',{p['id'] for p in changes}==set(c['changed_parts']),changes)
        check('identity and bilingual names retained',all(all(getattr(o,p)==getattr(old[n],p) for p in ['PartCode','LegacyId','NameEN','NamePTBR','Category','PartStatus']) for n,o in obs.items()))
        check('candidate revisions explicit',all(getattr(obs[n],'ProposedRevision','')=='R2-PROPOSAL' for n in c['changed_parts']))
        check('remaining forty objects unchanged',all(obs[n].Shape.cut(o.Shape).Volume+o.Shape.cut(obs[n].Shape).Volume<1e-5 for n,o in old.items() if n not in c['changed_parts']))
        check('side outer dimensions unchanged',all(all(abs(a-b)<1e-6 for a,b in zip(bounds(obs[n].Shape),bounds(old[n].Shape))) for n in ['SIDE_L','SIDE_R']))
        reflection=App.Matrix();reflection.A11=-1;reflection.A14=600
        mirrored=obs['SIDE_L'].Shape.transformGeometry(reflection);right=obs['SIDE_R'].Shape
        check('left and right sides are mirror symmetric',mirrored.cut(right).Volume+right.cut(mirrored).Volume<1e-5)
        pairs=[];items=list(obs.items())
        for i,(n,o) in enumerate(items):
            for m,p in items[i+1:]:
                v=o.Shape.common(p.Shape).Volume
                if v>.01:pairs.append(dict(a=n,b=m,mm3=v))
        check('no positive-volume intersections above 0.01 mm3',not pairs,pairs)
        depth=c['capture_depth_mm'];gap=c['total_fit_clearance_mm']/2
        residuals={}
        for name,x,skin_x in [('SIDE_L',18-depth,0),('SIDE_R',582,582+depth)]:
            side=obs[name].Shape
            # Exact retained outer skin in all three machined regions, compared with baseline.
            skin=box(skin_x,0,0,18-depth,1308.1,596.9)
            check(name+' retains full outer skin',old[name].Shape.common(skin).cut(side).Volume<1e-5)
            for joint,witness in [('Floor',box(x,600,18-gap,depth,1,18+2*gap)),('Front',box(x,5,100,depth,1,1)),('Rear',box(x,1295,100,depth,1,1))]:
                check(name+' actual '+joint+' capture void exists',side.common(witness).Volume<1e-5)
            section=side.common(box(0,600,20,600,1,14))
            residuals[name]=section.BoundBox.XLength
        check('minimum nominal residual is 12 mm',all(v>=c['minimum_residual_skin_mm']-1e-6 for v in residuals.values()),residuals)
        for n in ['FLOOR','FRONT','REAR']:
            s=obs[n].Shape;b=s.BoundBox
            check(n+' mating width 576 mm and original holes retained',abs(b.XMin-12)<1e-6 and abs(b.XMax-588)<1e-6 and old[n].Shape.cut(s).Volume<1e-5 and s.common(box(18,-1,-1,564,1310,700)).cut(old[n].Shape).Volume<1e-5)
        # Local capture only: no whole-cabinet insertion-path claim is made.
        for side in ['SIDE_L','SIDE_R']:
            s=obs[side].Shape
            for mate in ['FLOOR','FRONT','REAR']:
                b=old[mate].Shape.BoundBox
                y=(b.YMin+b.YMax)/2;z=(b.ZMin+b.ZMax)/2
                check(side+' '+mate+' has 6 mm edge engagement',obs[mate].Shape.common(box(12 if side=='SIDE_L' else 582,y-.5,z-.5,6,1,1)).Volume>5.999)
        check('manufacturing and hardware gates remain blocked',not c['manufacturing_ready'] and c['hardware_keepout_status']=='BLOCKED_UNMEASURED')
        result=dict(status='PROPOSAL_NOT_ADOPTED',manufacturing_ready=False,object_count=len(obs),checks=checks,changes=changes,collisions=pairs,residual_skin_mm=residuals,
                    unresolved=['Measured leg/bracket and backbox hinge load zones: NOT VERIFIED','Actual stock thickness and coupon fit','Cutter-radius/entry/end relief at rabbet-groove junctions','Fastener pattern, glue and structural proof','Physical dry-fit sequence'],
                    baseline='Committed V32; copied into .work/joinery-study/v32-baseline.FCStd')
        if write:
            records=[]
            for n,o in obs.items():
                vertices,faces=o.Shape.tessellate(1.5)
                edges=[[[v.x,v.y,v.z] for v in e.discretize(Deflection=.5)] for e in o.Shape.Edges] if n in c['changed_parts'] else []
                records.append(dict(id=n,code=o.PartCode,category=o.Category,vertices=[[v.x,v.y,v.z] for v in vertices],faces=faces,edges=edges))
            (OUT/'geometry.json').write_text(json.dumps(dict(parts=records),indent=2)+'\n')
            (OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
            # Saved-solid XY/XZ sections, exported as face meshes rather than schematic rectangles.
            sections={}
            for label,region in [('floor',box(0,599.5,0,65,1,55)),('front',box(0,-1,99.5,65,55,1)),('baseline_floor',box(0,599.5,0,65,1,55)),('baseline_front',box(0,-1,99.5,65,55,1))]:
                sections[label]=[]
                for n in ['SIDE_L','FLOOR' if label.endswith('floor') else 'FRONT']:
                    source=old if label.startswith('baseline') else obs
                    s=source[n].Shape.common(region);v,f=s.tessellate(.1)
                    sections[label].append(dict(id=n,vertices=[[p.x,p.y,p.z] for p in v],faces=f))
            (OUT/'sections.json').write_text(json.dumps(sections)+'\n')
        failed=[p['check'] for p in checks if not p['passed']]
        if failed:raise AssertionError('; '.join(failed))
        return result
    finally:
        App.closeDocument(doc.Name);App.closeDocument(base.Name)

def bounds(s):
    b=s.BoundBox;return [b.XMin,b.XMax,b.YMin,b.YMax,b.ZMin,b.ZMax]
