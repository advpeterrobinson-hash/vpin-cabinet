"""Compact current mesh bundle from the exact native-derived viewer dictionary.
Reuses unchanged approved triangles; no re-tessellation of unrelated surfaces.
CERN-OHL-S-2.0. Native FCStd/B-rep geometry remains engineering authority.
"""
from pathlib import Path
import json,gzip,io
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/structural-v335'
D=json.loads(gzip.decompress((O/'viewer-data.json.gz').read_bytes()));base={p['key']:p for p in D['installed']}
def part(n,g):return {'name':n,'label':base[n]['meta']['names']['en'],**D['geometry'][g]}
parts=[part(n,p['geometry']) for n,p in base.items()];states={}
for state,entries in D['states'].items():
 states[state]={n:(part(n,g) if g else None) for n,g in entries.items() if n in base and g!=base[n]['geometry']}
review=json.loads((R/'exports/generated/backbox-lock-integration-v32/mesh.json').read_text())['review'];review['V335']={'authority':'config/current_v32.json','manufacturing_register':'config/manufacturing/flatpack_v335.json','release':False,'sparse_state_rule':'Apply base parts, then replace/hide named variants. Native named FCStd files remain exact.'}
with (O/'mesh.json.gz').open('wb') as f:
 with gzip.GzipFile(fileobj=f,mode='wb',mtime=0) as gz:
  with io.TextIOWrapper(gz,encoding='utf-8') as text:json.dump({'parts':parts,'states':states,'review':review},text,separators=(',',':'))
print('V335_COMPACT_MESH_PASS',len(parts),len(states),(O/'mesh.json.gz').stat().st_size)
