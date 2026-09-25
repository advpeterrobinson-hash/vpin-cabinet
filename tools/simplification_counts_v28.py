"""Planning counts with explicit physical-object and operation scope; not a purchase BOM."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 r=json.loads((ROOT/'exports/generated/simplification-v28/geometry.json').read_text());names={o['name'] for o in r['inventory']}
 def pref(*p):return sorted(n for n in names if n.startswith(p))
 # Count one represented assembly/blank, never geometry ghosts or individual screws.
 custom=pref('SideRail','LockdownBar','LockdownReceiver','PivotPlate','PivotJournal','BearingBacking','ClosedSupportSeat','SafetyStayNutPlate','LegSpreader','CPURailBacking','CarrierAngle','PropRod','BackboxSpeakerLeftArm','BackboxSpeakerRightArm','VesaAdapter')
 remaining=pref('SideRail','LockdownBar','LockdownReceiver')
 commodity_before=pref('ClassicLegBracket','WpcHinge','CPURailAngle')
 commodity_after=pref('ClassicLegBracket','WpcHinge','SBracket','SBridgeAngle','SShaftClamp')+['speaker_arm_L_as_commodity','speaker_arm_R_as_commodity']
 operations={
 'PC':{'before':['seat rails','fit four angles','fit four backing plates','fit fixed slide members','fit moving slide members to board','align slide pair','bolt case','fit retainer'], 'proposed':['remove CM3 only after structural acceptance','bolt case to base','place base on bottom','secure base with common fasteners']},
 'holder':{'before':['assemble rail/tie frame','laminate pivot doublers','laminate rear beam','fit VESA plate','fit cheek plates','fit journals','fit bearings/backing','align pivot','fit fixed clevises','fit prop receivers','fit rods/pins/keepers','fit stow clips','fit closed pads/latches'], 'proposed':['bolt bridge to two beams','fit plain bushes','fit cross-axis/supports','fit landing pads/latches','fit two captive restraints','fit/verify positive opening stops','adjust and secure display interface']},
 'boards':{'before':['fit four custom angle stations','fit left carrier','fit right carrier','secure cable loops'],'proposed':['fit six matching brackets','fit board A','fit board B','fit board C','secure disconnectable cable loops']},
 'rear_door':{'before':['fit hinge','hang door','fit latch/catch','check sweep'],'proposed':['fit hinge','hang door','fit latch/catch','check sweep']}}
 moving_before=['playfield assembly','left prop','right prop','left upper locking pin','right upper locking pin','left stow keeper','right stow keeper','left drawer carriage','right drawer carriage','rear door','backbox door']
 moving_after=['playfield assembly','left flexible restraint','right flexible restraint','rear door','backbox door']
 data=dict(status='PROPOSED_NOT_ACCEPTED',custom_metal_before=custom,custom_metal_proposed=remaining,
 custom_scope='Conservative make-to-project planning classification, including cut/drilled rods and VESA metal adapter; stock backglass channels and bought hardware excluded. Future commodity substitutions require fit proof; no purchasing authority.',
 commodity_bracket_assemblies_before=commodity_before,commodity_bracket_assemblies_proposed=commodity_after,
 commodity_other_before=['slide pair','UCFL202 pair','door hinges/latches','closed latches','prop pins/clevises/receivers/stow hardware'],
 commodity_other_proposed=['cross stock axis','plain bush pair','two rated captive straps with ordinary anchor hardware','four commodity leg backing plates','door hinges/latches','closed latches'],
 moving_assemblies_before=moving_before,moving_assemblies_proposed=moving_after,
 fastener_families_before_known=['wood screw','M4','M6','M8 pivot-plate bolt','3/8-16 backbox lock'],fastener_families_proposed_target=['wood screw','M4','M6','3/8-16 backbox lock'],
 fastener_limit='Lower bound / target only: leg threads, bought hardware screws, pins, length/grade variants not frozen. Exact full-cabinet fastener count and family count UNKNOWN; no invented savings.',
 assembly_macro_operations=operations,assembly_macro_count_before=sum(len(o['before']) for o in operations.values()),assembly_macro_count_proposed=sum(len(o['proposed']) for o in operations.values()),
 assembly_scope='Changed systems only, one listed task per operation; unchanged shell/backbox, preparation and individual fastener turns excluded. Not a time estimate or complete assembly instruction.')
 (ROOT/'bom/SIMPLIFICATION_COUNTS_V28.json').write_text(json.dumps(data,indent=2)+'\n')
 print('custom',len(custom),'->',len(remaining),'commodity bracket assemblies',len(commodity_before),'->',len(commodity_after),'moving',len(moving_before),'->',len(moving_after),'macro',data['assembly_macro_count_before'],'->',data['assembly_macro_count_proposed'])
if __name__=='__main__':main()
