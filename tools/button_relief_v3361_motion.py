"""V33.6.1 differential rigid-motion validation from exact CURRENT B-reps.
CERN-OHL-S-2.0. No manufacturing release and no invented flexible cable proof.
"""
from pathlib import Path
import hashlib,json,math,sys,traceback
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import certify,load,transform,actual,pf_names,WPC,PF,V,build_locks,with_tethers

cp=R/'config/button_relief_v3361.json'
C=json.loads(cp.read_text()) if cp.exists() else {}
O=R/C.get('output','exports/generated/button-relief-v3361');O.mkdir(parents=True,exist_ok=True)
oldpath=R/'exports/generated/monitor-support-v336/play.FCStd';newpath=O/'play.FCStd'
report={'checks':[],'certificates':{},'samples':{},'pass':False,'manufacturing_release':False,
        'source_before':str(oldpath.relative_to(R)),'source_after':str(newpath.relative_to(R)),
        'prerequisites':{'playfield':'MAIN PLAYFIELD GLASS + MATRIX REMOVED; fixed matrix supports retained; accepted 50-degree manually supported service and 48mm lift-out',
                         'backbox':'MAIN PLAYFIELD GLASS + MATRIX REMOVED; rear doors closed/latched; upright locks released and parked; backbox glass/cassette retained'},
        'scope':'Continuous differential certificate for every newly occupied volume plus explicit whole-assembly samples; unchanged interfaces inherit the cited previous certificates.'}

def save():
 (O/'motion-validation.json').write_text(json.dumps(report,indent=2)+'\n')
def check(n,v,d=None):
 report['checks'].append({'name':n,'pass':bool(v),'detail':d});print('V3361_MOTION_CHECK',n,bool(v),flush=True);save()
 if not v:raise AssertionError((n,d))
def difference(a,b):
 if a.exportBrepToString()==b.exportBrepToString():return 0.0
 if not a.BoundBox.intersect(b.BoundBox):return a.Volume+b.Volume
 # Overlapping primitive compounds (e.g. tether tubes/spheres) are not fused
 # solids: union-Boolean subtraction can create false slivers on reload.
 # Compare the corresponding individual solids before treating material as new.
 if len(a.Solids)>1 and len(a.Solids)==len(b.Solids):
  return sum(difference(x,y) for x,y in zip(a.Solids,b.Solids))
 return a.cut(b).Volume+b.cut(a).Volume
def hits(mov,obs):
 out=[]
 for n,s in mov.items():
  for m,t in obs.items():
   if n==m or not s.BoundBox.intersect(t.BoundBox):continue
   v=s.common(t).Volume
   if v>1e-4:out.append({'moving':n,'fixed':m,'volume_mm3':v})
 return out

def additions(new,old):
 result={}
 for n,s in new.items():
  if n in old:
   if s.exportBrepToString()==old[n].exportBrepToString():continue
   if len(s.Solids)>1 and len(s.Solids)==len(old[n].Solids) and difference(s,old[n])<1e-5:continue
   q=(s.cut(old[n]).removeSplitter() if s.BoundBox.intersect(old[n].BoundBox) else s.copy())
  else:q=s.copy()
  if q.Volume>1e-5:result[n]=q
 return result

def certify_translation(mov,obs,start=0,end=48):
 """Midpoint OCC separation exceeds translation half interval for all pairs."""
 if not mov or not obs:return {'range_mm':[start,end],'intervals':[[start,end]],'proof':'empty changed moving/obstacle set'}
 todo=[(start,end)];rows=[];calls=0
 while todo:
  lo,hi=todo.pop();mid=(lo+hi)/2;posed=transform(mov,lift=mid);limit=(hi-lo)/2+1e-6;ok=True
  for n,s in posed.items():
   b=s.BoundBox
   for m,t in obs.items():
    c=t.BoundBox;lb=math.sqrt(sum(max(0,getattr(b,k+'Min')-getattr(c,k+'Max'),getattr(c,k+'Min')-getattr(b,k+'Max'))**2 for k in 'XYZ'))
    if lb>limit:continue
    gap=s.distToShape(t)[0];calls+=1
    if gap<=limit:ok=False;break
   if not ok:break
  if ok:rows.append([lo,hi])
  else:
   if hi-lo<1e-6:raise AssertionError(('continuous lift collision or unproven contact',lo,hi,n,m,gap))
   todo.extend([(lo,mid),(mid,hi)])
 return {'range_mm':[start,end],'intervals':sorted(rows),'distance_calls':calls,'method':'OCC midpoint separation > translation half interval, all non-AABB-separated pairs'}

def rotation(name,mov,obs,start,end,axis,sign=1):
 if not mov or not obs:r={'range_deg':[start,end],'intervals':[[start,end]],'proof':'no newly occupied volume'}
 else:r=certify(mov,obs,start,end,axis,poser=lambda ss,a:transform(ss,angle=sign*a,axis=axis))
 report['certificates'][name]=r;check(name,True,{'intervals':len(r['intervals']),'moving_ids':list(mov),'obstacle_ids':list(obs)})

def whole_samples(label,newmov,newobs,oldmov,oldobs,values,poser):
 rows=[];regressions=[];inherited=[]
 for value in values:
  nh=hits(poser(newmov,value),newobs)
  # Existing intended contacts/screw hosts remain inherited evidence, not a
  # reason to silently suppress a new conflict. Compare exact pair volumes.
  if nh:
   oh={(h['moving'],h['fixed']):h['volume_mm3'] for h in hits(poser(oldmov,value),oldobs)}
  else:oh={}
  bad=[]
  for h in nh:
   before=oh.get((h['moving'],h['fixed']),0)
   if h['volume_mm3']>before+1e-3:bad.append({**h,'before_mm3':before})
   else:inherited.append({'value':value,**h,'before_mm3':before})
  rows.append({'value':value,'new_collisions':bad,'inherited_positive_volume_pairs':len(nh)-len(bad)})
  regressions.extend([{'value':value,**h} for h in bad])
 report['samples'][label]={'rows':rows,'inherited_contacts':inherited}
 check(label+' no added penetration',not regressions,regressions)
 check(label+' no inherited unintended penetration after prerequisites',not inherited,inherited)

def main():
 old=load(oldpath);new=load(newpath)
 report['source_sha256']={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [oldpath,newpath]}
 report['inherited_certificates']={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in [
  'exports/generated/monitor-support-v336/motion-validation.json','exports/generated/monitor-support-v336/geometry-validation.json','exports/generated/monitor-support-v336/backbox-study/validation.json',
  'exports/generated/pivot-cradle-integration-v32/validation.json','exports/generated/backbox-lock-integration-v32/validation.json',
  'exports/generated/backbox-service-v32/motion-validation.json']}
 protected=['BB_MonitorCarrier0','BB_MonitorCarrier1','PF_WoodDowel','PF_OpenCradleL','PF_OpenCradleR','PF_VESAEnvelope','PLAYFIELD_ENVELOPE','BB_MonitorStopRail','BACKBOX_BASE','CandidateGlass','CandidateGlassChannelL','CandidateGlassChannelR']
 check('validated axes and retained core parts unchanged',all(n in old and n in new and difference(old[n],new[n])<1e-5 for n in protected),{'WPC':list(WPC),'PF':list(PF),'protected':protected})
 removed_for_service={n for n in new if n=='CandidateGlass' or n.startswith('Matrix') or n.startswith('MX_Retainer') or n in ['MX_MovingConnectorReserve','MX_CableLoopReserve']}
 report['removed_for_service']=sorted(removed_for_service)
 report['retained_matrix_fixed_parts']=[n for n in new if n.startswith('MX_') and n not in removed_for_service]
 pf_ids=pf_names(new);npf={n:s for n,s in actual(new).items() if n in pf_ids};opf={n:s for n,s in actual(old).items() if n in pf_names(old)}
 nf={n:s for n,s in actual(new).items() if n not in npf and n not in removed_for_service};of={n:s for n,s in actual(old).items() if n not in opf and n not in removed_for_service}
 addpf=additions(npf,opf);addfixed=additions(nf,of)
 report['added_volume_mm3']={'playfield':{n:s.Volume for n,s in addpf.items()},'fixed_for_playfield':{n:s.Volume for n,s in addfixed.items()}}
 # Changed parts retain old positive contacts only when there is no new material.
 rotation('PF_restored_material_vs_current_fixed',addpf,nf,0,50,PF,-1)
 rotation('PF_complete_vs_new_fixed_material',npf,addfixed,0,50,PF,-1)
 for name,mov,obs in [('PF_restored_material_lift',addpf,nf),('PF_complete_vs_new_fixed_lift',npf,addfixed)]:
  report['certificates'][name]=certify_translation(mov,obs);check(name,True,{'intervals':len(report['certificates'][name]['intervals'])})
 # Operational reserve is separate from occupied hardware. This tests existing
 # conservative body/leaf/wire/tool shapes as geometry, not actual ergonomics.
 service={n:s for n,s in new.items() if n.startswith('Button') and 'ServiceReserve_' in n}
 if service:
  rotation('PF_complete_vs_button_service_reserves',npf,service,0,50,PF,-1)
  report['certificates']['PF_lift_vs_button_service_reserves']=certify_translation(npf,service);check('PF lift vs button service reserves',True)
 whole_samples('playfield_service',npf,nf,opf,of,sorted(set([i*.5 for i in range(101)]+[.01,.05,.1,.25])),lambda ss,a:transform(ss,angle=-a,axis=PF))
 whole_samples('playfield_lift',npf,nf,opf,of,sorted(set(list(range(49))+[.01,.05,.1,.25,.5])),lambda ss,a:transform(ss,lift=a))
 # Parked locks and tethers are co-moving. Closed installed door state is retained.
 park=with_tethers(build_locks(True)[0],True)
 def backbox(ss):
  p={n:s for n,s in ss.items() if n.startswith('BB_') and 'ToyZone' not in n and 'HingeAccess' not in n and 'RetractedReserve' not in n}
  p.update(park);return p
 nb,ob=backbox(new),backbox(old)
 def foldfixed(ss):return {n:s for n,s in actual(ss).items() if not n.startswith('BB_') and n not in removed_for_service}
 nff,off=foldfixed(new),foldfixed(old);addb=additions(nb,ob);addff=additions(nff,off)
 report['added_volume_mm3']['backbox']={n:s.Volume for n,s in addb.items()};report['added_volume_mm3']['fold_fixed']={n:s.Volume for n,s in addff.items()}
 rotation('populated_fold_vs_new_fixed_material',nb,addff,0,90,WPC)
 rotation('new_backbox_material_vs_current_fixed',addb,nff,0,90,WPC)
 whole_samples('backbox_fold',nb,nff,ob,off,sorted(set(list(range(91))+[.001,.01,.05,.1,.25,.5,2,5,10,15,30,45,60,75,90])),lambda ss,a:transform(ss,angle=a,axis=WPC))
 # Subtractive monitor openings cannot create new occupied interference during
 # door/display/glass/cassette motions. Prove actual subset before inheriting.
 bb_changed={n:s for n,s in new.items() if n.startswith('BB_') and n in old and difference(s,old[n])>1e-5}
 check('changed backbox wood is subtractive only; accepted service paths preserved',all(s.cut(old[n]).Volume<1e-5 for n,s in bb_changed.items()),list(bb_changed))
 report['service_inheritance']={'backbox_changed_parts':list(bb_changed),'proof':'New BB shapes subset old shapes; M067 and all positive retention/hinge/door/glass/cassette mechanisms unchanged. Original exact swept service certificates remain valid for removed material.','flexible_wiring':'Independent parametric corridor study, not certified by this rigid-motion script.'}
 check('native input bytes unchanged during motion validation',all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in report['source_sha256'].items()))
 report['pass']=all(r['pass'] for r in report['checks']);save();print('V3361_MOTION_PASS',len(report['checks']),flush=True)
try:main()
except Exception as exc:
 report['error']=str(exc);report['traceback']=traceback.format_exc();save();print(report['traceback'],flush=True);raise
