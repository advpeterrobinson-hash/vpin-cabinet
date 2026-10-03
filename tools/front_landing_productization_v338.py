"""SW02 exact-union simplification and captive hand-retention packaging study.
Original CERN-OHL-S-2.0. No selected hardware or manufacturing release.
"""
from pathlib import Path
import json,math,sys,hashlib
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,V,transform,PF,WPC,certify
from coin_door_v32 import definitions,turn
C=json.loads((R/'config/service_productization_v338.json').read_text());O=R/C['output'];O.mkdir(exist_ok=True,parents=True);B=O/'landing-brep';B.mkdir(exist_ok=True)
p=load(R/C['source']);prior=json.loads((R/'exports/generated/front-landings-v3363/geometry-validation.json').read_text())
def box(x,y,z,w,d,h):return Part.makeBox(w,d,h,V(x,y,z))
def cyl(x,y,z,r,h,axis=V(0,0,1)):return Part.makeCylinder(r,h,V(x,y,z),axis)
def mirror(s):
 m=A.Matrix();m.A11=-1;m.A14=600;q=s.copy();q.transformShape(m,True);return q
def shift(s,dx=0,dy=0,dz=0):q=s.copy();q.translate(V(dx,dy,dz));return q
def bounds(s):b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def diff(s,t):return s.cut(t).Volume+t.cut(s).Volume
def union(ss):
 q=ss[0]
 for s in ss[1:]:q=q.fuse(s)
 return q.removeSplitter()
def hits(ss,obs,ignore=()):
 out=[]
 for n,s in ss.items():
  for k,t in obs.items():
   if k in ignore or n==k or not s.BoundBox.intersect(t.BoundBox):continue
   v=s.common(t).Volume
   if v>1e-5:out.append({'moving':n,'fixed':k,'volume_mm3':v})
 return out
def sweep(s,dx=0,dy=0,dz=0):
 b=s.BoundBox;return box(b.XMin+min(0,dx),b.YMin+min(0,dy),b.ZMin+min(0,dz),b.XLength+abs(dx),b.YLength+abs(dy),b.ZLength+abs(dz))
def gap(s,t):
 a,b=s.BoundBox,t.BoundBox
 return math.sqrt(sum(max(0,getattr(a,k+'Min')-getattr(b,k+'Max'),getattr(b,k+'Min')-getattr(a,k+'Max'))**2 for k in 'XYZ'))
def nearest(ss,obs,ignore=()):
 best=(1e9,'','')
 for n,s in ss.items():
  for k,t in sorted(obs.items(),key=lambda q:gap(s,q[1])):
   if k in ignore or n==k:continue
   if gap(s,t)>best[0]:continue
   d=s.distToShape(t)[0]
   if d<best[0]:best=(d,n,k)
 return {'gap_mm':best[0],'moving':best[1],'fixed':best[2]}
def save(name,ss):
 d=A.newDocument('V338_'+name.replace('-','_'))
 for n,s in ss.items():d.addObject('PartDesign::Feature',n).Shape=s
 d.recompute();d.saveAs(str(O/(name+'.FCStd')));A.closeDocument(d.Name)
checks=[]
def ck(n,v,d=None):checks.append({'name':n,'pass':bool(v),'detail':d});print(n,bool(v),flush=True)
wood={};blank={};oldunion={};interfaces={};rows=[]
z0=p['FrontLandingL_Layer1'].BoundBox.ZMin;zt=z0+54
cuts=[cyl(72,245,z0-1,4.5,56),cyl(72,275,z0-1,3.5,56),cyl(72,245,zt-16,6,17)]
for y in [234,286]:
 for z in [z0+9,z0+45]:
  cuts += [cyl(17,y,z,2.5,70,V(1,0,0)),Part.makeCone(4.5,2.25,2,V(86,y,z),V(-1,0,0))]
for side in ['L','R']:
 tf=(lambda s:s) if side=='L' else mirror
 ss=[p[f'FrontLanding{side}_Layer{i}'] for i in [1,2,3]];u=union(ss);oldunion['FrontLanding'+side+'_OldUnion']=u
 b=tf(box(18,225,z0,68,70,54));s=box(18,225,z0,68,70,54)
 for c in cuts:s=s.cut(c)
 s=tf(s.removeSplitter());wood['FrontLanding'+side+'_Block']=s;blank['SW02_'+side+'_Blank']=b
 oldmissing=b.cut(u);newmissing=b.cut(s);filling=s.cut(u)
 # Bound differences by the two obsolete binder bores including head cones.
 obsolete=[]
 for x,y in [(38,260),(70,260)]:obsolete += [tf(cyl(x,y,zt-50,2.25,51)),tf(Part.makeCone(2.25,4.5,2,V(x,y,zt-2)))]
 binder=union(obsolete).common(b)
 ck(side+' external block/mating datums remain exact68x70x54',all(abs(a-c)<1e-7 for a,c in zip(bounds(u),bounds(s))))
 ck(side+' fills only obsolete binder drillings',u.cut(s).Volume<1e-5 and diff(filling,binder)<1e-4,{'removed_old_wood_mm3':u.cut(s).Volume,'filled_binder_mm3':filling.Volume,'binder_proof_difference_mm3':diff(filling,binder)})
 ck(side+' valid single solid and all functional bore volumes retained',s.isValid() and len(s.Solids)==1 and newmissing.cut(oldmissing).Volume<1e-5)
 rows.append({'side':side,'bounds_mm':bounds(s),'old_volume_mm3':u.Volume,'new_volume_mm3':s.Volume,'blank_volume_mm3':b.Volume,'symmetric_difference_mm3':diff(u,s),'difference_reason':'Only redundant binder bores filled; no external or functional bore movement','filled_binder_mm3':filling.Volume,'minimum_side_center_to_Y_end_mm':9,'reference_head_edge_ligament_mm':4.5})
for n,s in (wood|blank|oldunion).items():s.exportBrep(str(B/(n+'.brep')))
removed=[n for n in p if n.startswith('FrontLanding') and ('_Layer' in n or '_LaminationScrew' in n)]
new={n:s for n,s in p.items() if n not in removed};new.update(wood)
fixed=actual(new);coin=json.loads((R/'config/front_panel_v32.json').read_text())
for n,(s,k,m) in definitions(coin,True).items():
 key='CoinStudy_'+n
 if key in fixed and m:fixed[key]=turn(p[key],coin['coin_door'],110)
fixed.update({n:s for n,s in new.items() if n=='PLUNGER_RESERVED' or n.endswith('CandidatePayload') or n.startswith(('Button','Leaf','Underfront'))})
underhead=prior['retention']['nominal_underhead_z_mm'];candidates=[];candidate_shapes={};access_shapes={}
for diam in C['retention']['head_diameter_candidates_mm']:
 h=C['retention']['head_height_reference_mm'];s0=cyl(72,275,underhead-h,diam/2,h)
 this={'diameter_mm':diam,'height_mm':h,'variants':[],'commodity_source':'GN7336 / MDA / MCT family examples only; overall envelope not selected SKU'}
 for side in ['L','R']:
  tf=(lambda s:s) if side=='L' else mirror
  knob=tf(s0);candidate_shapes[f'HandKnob_D{diam}_{side}']=knob
  # Generous cylindrical finger motion reserve, with palm/wrist toward centre.
  # Each stage is a full translation upper bound, not only endpoints.
  hand={'FingerSweep':cyl(72,275,underhead-h-4,diam/2+12,h+8),
        'Palm':box(95,240,249,70,70,28),
        'Bridge':box(78,260,249,30,30,28)}
  final={n:tf(s) for n,s in hand.items()};entrydx=138 if side=='L' else -138;stages={}
  for n,s in final.items():
   stages['Entry_'+n]=sweep(shift(s,dx=entrydx,dy=-375),dy=375)
   stages['Lateral_'+n]=sweep(s,dx=entrydx)
   stages['Release_'+n]=sweep(s,dz=-10.5)
  ignore=[n for n in fixed if n.startswith('FrontLanding'+side+'_Retention')]
  pathhits=hits(stages,fixed,ignore);bodyhits=hits({'knob':sweep(knob,dz=-10.5)},fixed,ignore)
  near=nearest(stages,fixed,ignore)
  this['variants'].append({'side':side,'path_hits':pathhits,'knob_sweep_hits':bodyhits,'nearest':near,'pass':not pathhits and not bodyhits})
  access_shapes.update({f'Hand_D{diam}_{side}_{n}':s for n,s in stages.items()})
 this['pass']=all(a['pass'] for a in this['variants']);candidates.append(this);print('KNOB',diam,this['pass'],[a['nearest'] for a in this['variants']],flush=True)
# Unmodified tool is a positive control against new filled binder wood.
accessold=load(R/'exports/generated/front-landings-v3363/tool-access.FCStd')
toolss={n:s for n,s in accessold.items() if n.startswith(('retention_','adjuster_'))}
newwoodhits=hits(toolss,wood);ck('existing adjustment/retention tool corridors clear SW02',not newwoodhits,newwoodhits)
ck('all protected objects retained byte-shape except retired layers/binders',all(new[n] is s for n,s in p.items() if n not in removed))
# No selection of a hand grip solely because an unpurchased shape fits.
# Procurement/retention/access decision made explicitly after study review.
save('landing-candidate',new);save('landing-study',wood|blank|oldunion|candidate_shapes|access_shapes)
report={'pass':all(c['pass'] for c in checks),'checks':checks,'SW02':rows,'removed_names':removed,'added_names':list(wood),'hand_knob_candidates':candidates,'source_sha256':hashlib.sha256((R/C['source']).read_bytes()).hexdigest(),'native_sha256':hashlib.sha256((O/'landing-candidate.FCStd').read_bytes()).hexdigest(),'manufacturing_release':False,'selected_retention':'PENDING_EXPLICIT_STUDY_DECISION'}
(O/'landing-study.json').write_text(json.dumps(report,indent=2)+'\n')
assert report['pass'],checks
print('V338_LANDING_STUDY_PASS',len(checks),flush=True)
