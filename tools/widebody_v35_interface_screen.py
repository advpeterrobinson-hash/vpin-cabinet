"""V35 supplemental native interface screens; no commercial-profile certification."""
from widebody_v35_common import *
p=load(O/'candidate.FCStd');v=load(O/'variants.FCStd');out={}
# Unmodified commercial overall length applied to the SAME original abstract section.
full=box(-1,-20,-30,1,1198.5625,37.2625).fuse(box(0,-20,6.2625,20,1198.5625,1)).removeSplitter()
out['uncut_rail_reference_hits']=hits({'uncut_L':tf(full),'uncut_R':mirror(tf(full))},{n:q for n,q in p.items() if n.startswith('BB_') and n in actual(p)})
q=p['PF_RearGlassChannel'];seat=p['BACKBOX_BASE'];contact=q.common(seat)
out['rear_channel']={'contact_area_mm2':sum(f.common(g).Area for f in q.Faces for g in seat.Faces if f.distToShape(g)[0]<1e-6),'intersection_volume_mm3':contact.Volume,'distance_mm':q.distToShape(seat)[0],'note':'Coincident contact only; actual extrusion retention/attachment is unresolved. Contact is not fastening proof.'}
out['gap_trials']=[]
obs={n:q for n,q in p.items() if n in actual(p) and n not in ['PLAYFIELD_ENVELOPE','PF_VESAEnvelope'] and not any(t in n for t in ['Reserve','Envelope','Tether','Cushion'])}
for gap in [5,7.5,10]:
 q=shift(p['PLAYFIELD_ENVELOPE'],y=-(7.5-gap)*sa,z=(7.5-gap)*ca)
 out['gap_trials'].append({'gap_mm':gap,'static_occupied_hits':hits({'TV':q},obs),'meaning':'Only7.5 has complete motion validation; chassis flex/tolerance not physically qualified.'})
out['clearances']={}
for label,names in [('buttons',[n for n in p if n.startswith(('Leaf','Button'))]),('front_landings',[n for n in p if n.startswith('FrontLanding')]),('legs',[n for n in p if n.startswith('CandidateLeg')])]:
 out['clearances'][label]=min(p[n].distToShape(p[k])[0] for n in names for k in ['CandidateGlassChannelL','CandidateGlassChannelR']) if names else None
out['LED_width_reserve']={n:{'L_mm':v[n].distToShape(v['OptionalLEDEnvelopeL'])[0],'R_mm':v[n].distToShape(v['OptionalLEDEnvelopeR'])[0]} for n in ['LG42C5','Samsung43QN93D','TCL40S5K']}
r=592.65/564
out['relative_span_screen']={'span_ratio':r,'same_total_load_bending_ratio':r,'same_total_load_deflection_ratio':r**3,'same_line_load_bending_ratio':r**2,'same_line_load_deflection_ratio':r**4,'scope':'Conservative simple-span comparison only; not strength/load certification. Shelves/T/Floor maintained thickness and load paths.'}
out['commercial_fit_authority']='ABSTRACT_ENVELOPES_ONLY; uncut commercial siderail profile and rear-stop attachment unresolved; do not infer purchased fit from collision-free candidate.'
dump('interface-screen',out);print(json.dumps(out,indent=2))
