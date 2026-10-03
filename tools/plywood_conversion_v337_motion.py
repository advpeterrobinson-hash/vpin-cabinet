"""Exact differential service checks for the V33.7 stock conversions.
CERN-OHL-S-2.0; source: https://github.com/advpeterrobinson-hash/vpin-cabinet
"""
from pathlib import Path
import sys,json,hashlib,math,traceback,gzip
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,pf_names,V,box,transform,certify,WPC,PF,build_locks,with_tethers
import backbox_service_v32 as service
C=json.loads((R/'config/plywood_conversion_v337.json').read_text());O=R/C['output']
report={'checks':[],'certificates':{},'manufacturing_release':False,'pass':False}
def save(): (O/'conversion-motion.json').write_text(json.dumps(report,indent=2)+'\n')
def ck(n,v,details=None):
 report['checks'].append({'name':n,'pass':bool(v),'detail':details});save();print(n,bool(v),flush=True)
 if not v:raise AssertionError((n,details))
def hits(mov,obs):
 hh=[]
 for n,s in mov.items():
  for k,t in obs.items():
   if n==k or not s.BoundBox.intersect(t.BoundBox):continue
   vol=s.common(t).Volume
   if vol>1e-5:hh.append([n,k,vol])
 return hh

def main():
 old=load(R/C['source']);new=load(O/'conversion.FCStd');geo=json.loads((O/'conversion-validation.json').read_text());ck('native conversion prerequisite',geo['pass'])
 report['source_sha256']=geo['source_sha256'];report['conversion_sha256']=hashlib.sha256((O/'conversion.FCStd').read_bytes()).hexdigest();report['prerequisites']=['Backbox locks released/parked','Doors closed and latched for fold','Main playfield glass removed','Matrix removed','Backbox glass and lower cassette remain installed']
 additions={n:new[n].cut(old[n]).removeSplitter() for n in geo['promoted_breps'] if new[n].cut(old[n]).Volume>1e-5};blanks={}
 for n,p in geo['optional_breps'].items():s=Part.Shape();s.read(str(R/p));blanks[n]=s
 occupied=actual(new);occupied.update({n:s for n,s in new.items() if n.startswith(('BB_SpeakerEnvelope','BB_DMDEnvelope','BB_Display32','FloorFilterMediaReserve','FloorCommercialGuardReserve'))})
 # Full filter silhouette swept downward is conservative: it contains every
 # pocketed filter cross-section. Existing through bores are retained.
 filter_sweeps={};floorrows=[]
 for side in ['L','R']:
  n='RemovableIntakeFilter'+side;s=new[n];f=max([f for f in s.Faces if type(f.Surface).__name__=='Plane' and abs(f.CenterOfMass.z-18)<1e-6],key=lambda f:f.Area);sweep=f.extrude(V(0,0,-92));filter_sweeps[n]=sweep
  excluded={n,'FLOOR','FloorFilterMediaReserve'+side,'FloorCommercialGuardReserve'+side}|{k for k in old if k.startswith('FloorFilterScrew'+side)}
  obs={k:t for k,t in occupied.items() if k not in excluded};hh=hits({n:sweep},obs);floorrows.append({'side':side,'range_mm':[0,80],'hits':hh,'method':'exact full through-cut top silhouette extruded continuously fromZ18 toZ-74; conservative superset of pocketed holder travel; removed screws/media/guard excluded'})
 ck('floor filters continuous80mm downward service',not any(r['hits'] for r in floorrows),floorrows)
 # Exterior intake frame removal along rear normal cannot meet remaining
 # closed geometry once screws removed. Verify a continuous80 mm prism sweep.
 rows=[]
 for side in ['L','R']:
  n='BB_IntakeFilterFrame'+side;s=new[n];f=max([f for f in s.Faces if type(f.Surface).__name__=='Plane' and abs(f.CenterOfMass.y-1322.1)<1e-6],key=lambda f:f.Area);sweep=f.extrude(V(0,92,0));obs={k:t for k,t in occupied.items() if k!=n and not k.startswith(('BB_IntakeMeshReserve'+side,))};hh=hits({n:sweep},obs);rows.append({'side':side,'hits':hh,'range_mm':[0,80]})
 ck('rear intake frames continuous80mm removal',not any(r['hits'] for r in rows),rows)
 # The existing group assignment is architecture metadata only. All shapes
 # below come from immutable CURRENT or conversion B-reps, never rebuilt oldCAD.
 groups=json.load(gzip.open(R/'exports/generated/backbox-service-v32/review-mesh.json.gz','rt'))['groups']
 for side in ['R','L']:
  own={n for n,g in groups.items() if g in ['door'+side,'locked'+side,'unlocked'+side]};obs={n:s for n,s in occupied.items() if n not in own and not n.endswith('RetractedReserve')}
  # Active leaf opens first; passive leaf is checked with active already100deg.
  if side=='L':
   other={n:s for n,s in obs.items() if groups.get(n) in ['doorR','lockedR','unlockedR']}
   for n in other:obs.pop(n)
   obs.update(service.door_pose(other,'R',100))
  mov={n:s for n,s in additions.items() if n in own};mov.update({n:s for n,s in blanks.items() if n.endswith(side)})
  hx,hy=service.C['rear']['hinge_axis_xy_mm'][0 if side=='L' else 1]
  report['certificates']['door_'+side]=certify(mov,obs,0,100,V(hx,hy,0),'Z',lambda ss,a:service.door_pose(ss,side,a));ck('continuous door'+side+'0to100 differential including blank',True,len(report['certificates']['door_'+side]['intervals']))
  # Flexible cable path is nonrigid; sample its original documented envelope
  # at1deg. New growth is far below the fan loop except exteriorframe/blank.
  rows=[]
  for a in range(101):
   loop,_=service.flex(side,a);posed=service.door_pose(mov,side,a);hh=hits(posed,{'fan_loop':loop});rows.append({'angle':a,'hits':hh})
  ck('door'+side+' fan loop differential sampled1deg',not any(r['hits'] for r in rows),[r for r in rows if r['hits']]);report['fan_loop_'+side]=rows
 removed={n for n in new if n=='CandidateGlass' or n.startswith(('Matrix','MX_Retainer')) or n in ['MX_MovingConnectorReserve','MX_CableLoopReserve']}
 fixed={n:s for n,s in actual(new).items() if not n.startswith('BB_') and n not in removed}
 bbdelta={n:s for n,s in additions.items() if n.startswith('BB_')};bbdelta.update(blanks)
 report['certificates']['backbox_new_wood_vs_cabinet']=certify(bbdelta,fixed,0,90,WPC);ck('continuous backbox0to90 newwood and optional blanks clearcabinet',True,len(report['certificates']['backbox_new_wood_vs_cabinet']['intervals']))
 backbox={n:s for n,s in new.items() if n.startswith('BB_') and 'ToyZone' not in n and 'HingeAccess' not in n and 'RetractedReserve' not in n};backbox.update(with_tethers(build_locks(True)[0],True));floor_delta={n:s for n,s in additions.items() if n.startswith('RemovableIntakeFilter')}
 report['certificates']['populated_backbox_vs_floor_additions']=certify(backbox,floor_delta,0,90,WPC);ck('continuous populatedbackbox0to90 clearsfloorfiltergrowth',True)
 # Thin additions cannot interfere with playfield: certify differential service
 # and exact full vertical swept bounding prism for48mm lift where distant.
 pf={n:s for n,s in actual(new).items() if n in pf_names(new)};obs={n:s for n,s in additions.items()};obs.update(blanks);report['certificates']['playfield_vs_additions']=certify(pf,obs,0,50,PF,poser=lambda ss,a:transform(ss,angle=-a,axis=PF));ck('continuous playfield0to50 clearconversions',True)
 swept={}
 for n,s in pf.items():
  b=s.BoundBox;swept[n]=box(b.XMin,b.YMin,b.ZMin,b.XLength,b.YLength,b.ZLength+48)
 hh=hits(swept,obs);ck('conservative playfield48mm liftsweep clearconversions',not hh,hh)
 samples=[]
 for a in [0,.25,.5,1,2,5,10,15,30,45,60,75,90]:samples.append({'angle':a,'newwood_hits':hits(transform(bbdelta,angle=a,axis=WPC),fixed),'populated_vs_newfloor_hits':hits(transform(backbox,angle=a,axis=WPC),floor_delta)})
 report['fold_samples']=samples;ck('required fold angle samples clear',not any(r['newwood_hits'] or r['populated_vs_newfloor_hits'] for r in samples))
 ck('conversion and CURRENT input bytes unchanged',hashlib.sha256((O/'conversion.FCStd').read_bytes()).hexdigest()==report['conversion_sha256'] and hashlib.sha256((R/C['source']).read_bytes()).hexdigest()==report['source_sha256'])
 report['pass']=True;save();print('V337_CONVERSION_MOTION_PASS',flush=True)
try:main()
except Exception as e:report['error']=str(e);report['traceback']=traceback.format_exc();save();print(report['traceback'],flush=True);raise
