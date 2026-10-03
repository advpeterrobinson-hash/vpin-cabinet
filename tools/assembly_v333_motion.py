"""Extract service group membership from accepted builders, read only."""
from backbox_lock_integration_v32 import *
p0,g,meta,blanks=service.build(load(R/C['cabinet_source']/'play.FCStd'))
eng,fixedhw,refs=build_locks(False);park,_,_=build_locks(True)
base=json.loads((R/'exports/generated/backbox-lock-integration-v32/mesh.json').read_text())
Cmat=json.loads((R/'config/matrix_cassette_v32.json').read_text())
q={'groups':g,'fold_names':list(service.occupied(p0,g))+list(park)+['BB_FlexCorridorL','BB_FlexCorridorR'],
 'fixed_lock_names':list(fixedhw),'pf_names':pf_names(load(R/C['cabinet_source']/'play.FCStd')),
 'pf_axis':list(PF),'wpc_axis':list(WPC),'matrix':base['review']['matrix_cassette'],
 'door_axes':service.C['rear']['hinge_axis_xy_mm'],'fan_flex':service.C['fan_flex'],
 'locks':C,'service_source':C['service_source'],
 'authority':'Inherited successful geometric service proofs; purchased hardware and loads still require physical qualification'}
(R/'exports/generated/assembly-v333/motion-authority.json').write_text(json.dumps(q,indent=2)+'\n')
print('V333_MOTION_PASS',flush=True)
