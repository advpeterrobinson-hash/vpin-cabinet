"""Saved B-rep sections and review meshes. CERN-OHL-S-2.0."""
from backbox_lock_integration_v32 import *
import gzip
q=json.loads((O/'validation.json').read_text());assert all(c['pass'] for c in q['checks'])
d=json.loads((O/'review-mesh.json').read_text())
for state in ['option-a','search-map']:
    ss=load(O/(state+'.FCStd'));d['scenes'][state]=[coarse_mesh(n,s) for n,s in ss.items()]
old=load(R/C['service_source']/'rear-closed.FCStd');obs={n:s for n,s in old.items() if n in ['BB_Floor','BB_LowerCassetteFrame','BB_DMDEnvelope','BB_DMDRearAdapter']}
for x in [120,480]:
    obs['OldCompactSocket'+str(x)]=cyl(x,1188,FLOOR+3,10,24)
    obs['OldWingHead'+str(x)]=cyl(x,1188,FLOOR+3,22,18)
    obs['OldReleasedHead'+str(x)]=cyl(x,1188,FLOOR+3+13.1,8,8)
save('option-a-compact',obs);d['scenes']['option-a-compact']=[coarse_mesh(n,s) for n,s in obs.items()]
# Actual cross section of the two-piece wood/metal engagement at the left lock.
ss=load(O/'locks-engaged.FCStd');plane=box(129.95,1218,568,.1,90,140)
section={n:s.common(plane) for n,s in ss.items() if n in ['BB_Floor','BACKBOX_BASE'] or n.startswith(('BB_UprightLockL','UprightLockL'))}
section={n:s for n,s in section.items() if s.Volume>1e-6};save('lock-section',section);d['scenes']['lock-section']=[coarse_mesh(n,s) for n,s in section.items()]
both=load(O/'access-L.FCStd');right=load(O/'access-R.FCStd');both.update({n:s for n,s in right.items() if n.startswith('BB_UprightLockR') and any(k in n for k in ['Entry','Lower','Lift','Transfer'])});save('both-access',both)
# Actual cropped B-reps for readable close-ups; do not rely on Matplotlib's
# non-clipping 3-D axes to hide geometry outside a close-up camera.
clips={
 'lock-close-L':('locks-engaged',(60,1215,570,165,110,240)),
 'lock-close-R':('locks-engaged',(375,1215,570,165,110,240)),
 'lower-open':('doors-open',(-95,1125,568,790,230,257)),
 'hand-close-L':('access-L',(60,1215,590,165,320,215)),
 'hand-close-R':('access-R',(375,1215,590,165,320,215)),
 'both-access-section':('both-access',(-80,1170,590,760,460,260))}
for state,(source,bb) in clips.items():
    ss=load(O/(source+'.FCStd'));clip=box(*bb);cut={n:s.common(clip) for n,s in ss.items() if s.BoundBox.intersect(clip.BoundBox)};cut={n:s for n,s in cut.items() if s.Volume>1e-6};save(state,cut);d['scenes'][state]=[coarse_mesh(n,s) for n,s in cut.items()]
# Deduplicate all per-state shapes to keep committed review data compact.
bank={}
def intern(m):
    import hashlib
    raw=json.dumps(m,separators=(',',':'));k=hashlib.sha256(raw.encode()).hexdigest()[:24];bank[k]=m;return k
packed={'scenes':{n:[intern(m) for m in mm] for n,mm in d['scenes'].items()},'details':{n:[intern(m) for m in mm] for n,mm in d['details'].items()},'meshes':bank}
(O/'review-mesh.json.gz').write_bytes(gzip.compress(json.dumps(packed,separators=(',',':')).encode(),compresslevel=6,mtime=0))
print('BACKBOX_LOCK_DETAILS_PASS',flush=True)
