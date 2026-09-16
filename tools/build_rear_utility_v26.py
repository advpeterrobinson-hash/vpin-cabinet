"""Two unselected utility studies, grounded in actual active solid geometry.
All candidate cut volumes are review-only. Neither permanent panel is modified.
"""
import json
from pathlib import Path
import FreeCAD as App
import Part
ROOT=Path(__file__).resolve().parents[1]

def box(spec):
    x,y,z,dx,dy,dz=spec
    return Part.makeBox(dx,dy,dz,App.Vector(x,y,z))

def add(doc,group,name,shape,role,label):
    o=doc.addObject('PartDesign::Feature',name);o.Shape=shape;o.Label=label
    group.addObject(o)
    o.addProperty('App::PropertyString','EngineeringRole');o.EngineeringRole=role
    o.addProperty('App::PropertyString','ReleaseStatus');o.ReleaseStatus='REVIEW ONLY / PLACEMENT NOT SELECTED / HOLES BLOCKED'
    return o

def main(doc):
    c=json.loads((ROOT/'config/rear_utility_v26.json').read_text())
    protection=doc.addObject('App::Part','RearLoadPathKeepoutsV26')
    # Solid rectangular leg-corner reserves conservatively protect more than the L steel itself.
    for side in ['RL','RR']:
        b=doc.getObject('ClassicLegBracket'+side+'V21').Shape.BoundBox
        m=c['leg_keepout_margin_mm']
        add(doc,protection,'RearLegKeepout'+side+'V26',box([b.XMin-m,b.YMin-m,b.ZMin-m,b.XLength+2*m,b.YLength+2*m,b.ZLength+2*m]),'PROTECTED_LOAD_PATH','LEG LOAD PATH + 15 mm engineering margin / hardware unmeasured')
    bottom=doc.getObject('CapturedBottomV20').Shape.BoundBox
    # Four boundary strips protect captured bottom edges, including the rear-panel dado.
    margin=c['joint_margin_mm'];inner=box([18+margin,18+margin,bottom.ZMin-1,564-2*margin,1272.1-2*margin,bottom.ZLength+2])
    protect=box([0,0,bottom.ZMin-1,600,1308.1,bottom.ZLength+2]).cut(inner)
    add(doc,protection,'BottomJointKeepoutV26',protect,'PROTECTED_LOAD_PATH','BOTTOM CAPTURE / edge material + 20 mm no-cut margin')
    for option in ['A','B']:
        group=doc.addObject('App::Part','UtilityCandidate'+option+'V26');group.Label='REVIEW OPTION '+option+' / NOT SELECTED'
        for function in ['mains','ethernet']:
            for kind,spec in c[option][function].items():
                role={'carrier':'REMOVABLE_ADAPTER','opening':'CANDIDATE_CUT','enclosure':'ELECTRONICS_ZONE','internal_access':'ELECTRONICS_ZONE','plug_access':'ACCESS_ZONE'}[kind]
                name='Utility'+option+function.title()+''.join(s.title() for s in kind.split('_'))+'V26'
                add(doc,group,name,box(spec),role,option+' '+function.upper()+' '+kind+' / dimensions provisional')
        target='RearPanelWithCPUHatchV24' if option=='A' else 'CapturedBottomV20'
        original=doc.getObject(target).Shape
        cut=original
        for function in ['Mains','Ethernet']:cut=cut.cut(doc.getObject('Utility'+option+function+'OpeningV26').Shape)
        add(doc,group,'Utility'+option+'PanelPreviewV26',cut,'REVIEW_PANEL','OPTION '+option+' PANEL WITH CANDIDATE CUTS / NOT ACTIVE WOOD')
