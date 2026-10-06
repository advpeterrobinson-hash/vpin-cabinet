"""Native V35 motion, reconstructed solids and negative-control checks."""
from widebody_v35_common import *
from pivot_cradle_integration_v32 import PF
from backbox_service_v32 import C as BC
p=load(O/'candidate.FCStd');variants=load(O/'variants.FCStd');audit=json.loads((O/'width-audit.json').read_text());reg=json.loads((O/'manufacturing-register.json').read_text());checks=[];detail={}
def ck(n,b,d=None):checks.append({'name':n,'pass':bool(b),'detail':d});print(n,bool(b),flush=True);dump('validation',{'checks':checks,'details':detail,'pass':all(a['pass'] for a in checks),'manufacturing_release':False})
wood={a['source_component']:p[a['source_component']] for a in reg['parts'] if a['source_component'] in p}
for a in reg['parts']:
 q=Part.Shape();q.read(str(R/a['finished_member_brep']));ck('manufacturing valid '+a['instance_id'],q.isValid() and len(q.Solids)==1 and a['reconstruction_difference_mm3']<.001)
ck('exact stock families',sorted({a['nominal_stock_thickness_mm'] for a in reg['parts'] if a['nominal_stock_thickness_mm']})==[12,18])
# Backbox proof: equal corresponding native vertices/surface volume after inverse rigid placement; no topology changes allowed.
errs={}
for n,q in p0.items():
 if n.startswith('BB_') and n!='BB_PFRearChannel':
  t=shift(p[n],x=-DX);err=max((a.Point-b.Point).Length for a,b in zip(t.Vertexes,q.Vertexes));errs[n]=err
  assert len(t.Vertexes)==len(q.Vertexes) and len(t.Faces)==len(q.Faces)
ck('all backbox local topology vertices preserved',max(errs.values())<1e-6,{'max_vertex_error_mm':max(errs.values()),'components':len(errs)})
# Main-body construction datum, not loose spline bounding-box extrapolation.
for side,x in [('L',0),('R',W)]:
 faces=[f for f in p['SIDE_'+side].Faces if isinstance(f.Surface,Part.Plane) and abs(abs(f.normalAt(0,0).x)-1)<1e-6 and abs(f.CenterOfMass.x-x)<1e-6]
 ck('outside side plane '+side,bool(faces),x)
ck('negative width controls',all(abs(W-b)>1 for b in [600,630,635]))
ck('no retired mechanisms',not any(n.startswith(('BB_MonitorRail','BB_MonitorCarrier','BB_MonitorDepthShoe','BB_LowerCassette')) for n in p))
# Pairwise wood interferences: report inherited intentional joints separately, all new intersections fail.
newhits=[];inherited=[]
for i,n in enumerate(wood):
 for m in list(wood)[i+1:]:
  a,b=wood[n],wood[m]
  if not a.BoundBox.intersect(b.BoundBox):continue
  v=a.common(b).Volume
  if v>.01:
   old=p0[n].common(p0[m]).Volume
   (inherited if old>.01 and abs(v-old)<.02 else newhits).append({'a':n,'b':m,'mm3':v,'before_mm3':old})
ck('no new wood penetration',not newhits,{'new':newhits,'inherited':inherited})
# Glass prism translated towards front, bounded analytically by union swept extrusion in glass coordinates.
gf=C['glass']['front_local_offset_mm'];L=1092.2;gb=C['glass']['reference_bottom_normal_mm'];th=4.7625
path=tf(box((W-603.25)/2,gf-1150,gb,603.25,L+1150,th))
obs=wood|{n:p[n] for n in ['CandidateGlassChannelL','CandidateGlassChannelR','CommercialSiderailL','CommercialSiderailR','PF_RearGlassChannel']}
h=hits({'glass_forward_path':path},obs);ck('glass forward insertion removal',not h,h)
bar={n:p[n] for n in ['CandidateGlassChannelL','CandidateGlassChannelR','PF_RearGlassChannel','PF_LockdownGlassRetainer']}
contain=[]
for axis in [V(1,0,0),V(0,ca,sa),V(0,-sa,ca)]:
 for sign in [-1,1]:
  q=p['CandidateGlass'].copy();q.translate(axis*sign*2);contain.append(bool(hits({'g':q},bar)))
ck('glass six direction containment reference',all(contain),contain)
# WPC closed locked parts replaced by parked source geometry and same centerline placement.
park=load(R/'exports/generated/backbox-v342/locks-parked.FCStd')
movebb={n:q for n,q in p.items() if n.startswith('BB_') and not any(t in n for t in ['Reserve','Liner','Tether','Mask'])}
for n in movebb:
 if 'UprightLock' in n and n in park:movebb[n]=shift(park[n],x=DX)
fixed={n:q for n,q in wood.items() if not n.startswith('BB_') and not n.startswith(('Matrix','MX_Wood'))}
# Fixed MX seats remain; matrix itself removed.
fixed.update({n:q for n,q in wood.items() if n.startswith('MX_Wood')})
fixed.update({n:p[n] for n in ['PLAYFIELD_ENVELOPE','CandidateGlassChannelL','CandidateGlassChannelR','CommercialSiderailL','CommercialSiderailR','PF_RearGlassChannel','PF_LockdownGlassRetainer']})
angles=[0,.25,.5,1,2,5,10,15,30,45,60,75,90];fold=[]
for a in angles:
 h=hits(transform(movebb,angle=a,axis=WPC),fixed);fold.append({'angle':a,'hits':h})
ck('WPC required sample angles',not any(a['hits'] for a in fold),fold)
# Continuous changed interface with backbox wood; exclude intentional shelf bearing at exactly0 and prove release via fine samples.
newfixed={n:p[n] for n in ['CandidateGlassChannelL','CandidateGlassChannelR','CommercialSiderailL','CommercialSiderailR','PF_RearGlassChannel','PF_LockdownGlassRetainer']}
try:detail['fold_continuous']=certify({n:q for n,q in wood.items() if n.startswith('BB_')},newfixed,0,90);ck('continuous fold vs new commercial stack',True)
except AssertionError as e:ck('continuous fold vs new commercial stack',False,str(e))
# PF geometric motion, no prop/load certification. Released front clamps and main glass/matrix/lockdown removed.
pfn=[n for n in p if n.startswith(('PF_Base','PF_Wood','PF_VESA','PF_CommercialStrap','PF_StrapScrew')) or n=='PLAYFIELD_ENVELOPE']
pm={n:p[n] for n in pfn};po={n:q for n,q in wood.items() if n not in pm and n!='MatrixCarrier'}
po.update({n:p[n] for n in ['CandidateGlassChannelL','CandidateGlassChannelR','CommercialSiderailL','CommercialSiderailR','PF_RearGlassChannel']})
po.update({n:q for n,q in p.items() if n.startswith(('Leaf','Button'))})
sv=[]
for a in [0,.25,.5,1,2,5,10,15,25,35,45,50]:sv.append({'angle':a,'hits':hits(transform(pm,angle=-a,axis=PF),po)})
ck('PF 0 to50 samples',not any(a['hits'] for a in sv),sv)
lift=[]
for z in [0,.25,.5,1,2,5,10,20,30,40,48]:lift.append({'lift':z,'hits':hits(transform(pm,lift=z),po)})
ck('PF48mm lift samples',not any(a['hits'] for a in lift),lift)
# Single assembly rigid transformation preserves all backbox door clearances; independent sample against widened MAIN geometry.
for side in ['L','R']:
 mov={n:q for n,q in p.items() if n.endswith(side) and n.startswith(('BB_Door','BB_Fan','BB_Lower','BB_PianoLeafDoor'))}
 x,y=BC['rear']['hinge_axis_xy_mm'][0 if side=='L' else 1];out=[]
 for a in [0,10,25,50,75,100]:
  posed={n:q.copy() for n,q in mov.items()}
  for q in posed.values():q.rotate(V(x+DX,y,0),V(0,0,1),a if side=='L' else -a)
  out+=hits(posed,{n:q for n,q in fixed.items() if not n.startswith('BB_')})
 ck('rear door '+side+' main-body clearance',not out,out)
# States exported from candidate, never from differently dimensioned old assemblies.
for fn,a,z in [('play',0,0),('service',-50,0),('lift-out',0,48)]:
 state=dict(p)
 if a or z:
  state.pop('CandidateGlass',None);state.pop('PF_LockdownGlassRetainer',None)
  for n in list(state):
   if n.startswith('Matrix') or n.startswith('MX_Retainer'):state.pop(n)
  state.update(transform(pm,angle=a,lift=z,axis=PF))
 save(fn,state)
for a in [1,45,90]:
 state={n:q for n,q in p.items() if not n.startswith('BB_') and n!='CandidateGlass' and not n.startswith(('Matrix','MX_Retainer'))};state.update(transform(movebb,angle=a,axis=WPC));save('fold-'+str(a),state)
ck('no production release',C['manufacturing_release'] is False)

assert all(a["pass"] for a in checks), "V35 native gate failed; do not export success views or promote"
