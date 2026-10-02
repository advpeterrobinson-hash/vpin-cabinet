"""Actual B-rep section and access review geometry. CERN-OHL-S-2.0."""
from pathlib import Path
import sys,json
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_service_v32 import *
src=load(R/C['source_directory']/'play.FCStd');p,g,m,b=build(src);closed=occupied(p,g)
sections={}
for name,slab in [('airflow_x155',box(154.8,900,590,.4,600,800)),('center_lock_z960',box(270,1260,959.8,100,100,.4)),('glass_edge_z1000',box(-95,1070,999.8,50,130,.4))]:
    ss={}
    for n,s in closed.items():
        if s.BoundBox.intersect(slab.BoundBox):
            sh=s.common(slab)
            if sh.Volume>1e-6:ss[n]=sh
    sections[name]=[mesh(n,s) for n,s in ss.items()]
detail={'sections':sections,'parts':[{'name':n,'group':g[n],'material':m[n]['material'],'authority':m[n]['authority'],'bounds_mm':bounds(s),'volume_mm3':s.Volume,'valid':s.isValid(),'solids':len(s.Solids)} for n,s in p.items()]}
from backbox_structure_review_v32 import reserves
access={n:s for n,s in reserves().items() if 'LockTool' in n or 'HingeAccess' in n}
detail['lock_hinge_access']=[mesh(n,s) for n,s in access.items()]
detail['installed_access_hits']=hits(access,{n:s for n,s in closed.items() if g[n]=='cassette'})
# A removable-adapter upgrade scenario, not a smaller canonical display envelope.
# A 55 mm chassis plus a central 45 mm adapter reservation fits entirely inside
# the already tested maximum-depth display box. Thus side toys can gain depth
# without new permanent wall holes or a shell/depth change.
thin=closed.copy();b=list(C['display']['envelope_box_mm']);b[1]+=C['front_layout_insets_mm']['display_carrier'];b[4]=55
thin['BB_Display32']=box(*b)
adapter=box(120,b[1]+55,949,360,45,230)
thin['BB_ShallowAdapterReserve']=adapter
expanded={}
for n,s in p.items():
    if not n.startswith('BB_ToyZoneUpper'):continue
    bb=s.BoundBox;expanded[n]=box(bb.XMin,1202,bb.ZMin,bb.XLength,84,bb.ZLength)
clear=hits(expanded,thin);subset=thin['BB_Display32'].cut(closed['BB_Display32']).Volume+adapter.cut(closed['BB_Display32']).Volume
assert not clear and subset<1e-6
thin.update(expanded)
detail['shallow_display']=[mesh(n,s) for n,s in thin.items()]
detail['shallow_display_validation']={'pass':True,'chassis_depth_mm':55,'central_adapter_depth_mm':45,'upper_side_zones_each_mm':[96,84,326],'clearance_hits':clear,'outside_validated_maximum_display_volume_mm3':subset,'note':'conditional future scenario with removable central adapter; no particular chime or mount load rating qualified'}
doc=A.newDocument('ShallowDisplayToyStudy')
for n,s in thin.items():doc.addObject('PartDesign::Feature',n).Shape=s
doc.recompute();assert all('Invalid' not in o.State for o in doc.Objects);doc.saveAs(str(O/'thin-display-toys.FCStd'));A.closeDocument(doc.Name)
(O/'details.json').write_text(json.dumps(detail,separators=(',',':'))+'\n')
print('BACKBOX_SERVICE_SECTIONS_PASS',flush=True)
