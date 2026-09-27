"""Conservative tracked-file classification and reference evidence; never deletes files."""
import collections
import hashlib
import json
import re
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
files = subprocess.check_output(['git','ls-files'], cwd=root, text=True).splitlines()
# Include the new review/audit route before its first commit.
files = sorted(set(files) | {str(p.relative_to(root)) for p in [Path(__file__).resolve(), root/'tools/run_v32_review.sh', root/'tools/verify_v32_entry.py']})
text = {}
for name in files:
    try: text[name] = (root/name).read_text()
    except (UnicodeError, OSError): pass
refs = {}
for name in files:
    path = Path(name)
    tokens = {name, path.name}
    if path.suffix == '.py': tokens.add(path.stem)
    pattern = re.compile(r'(?<![\w.-])(?:'+ '|'.join(re.escape(t) for t in tokens) + r')(?![\w.-])')
    refs[name] = sorted(n for n,s in text.items() if n != name and pattern.search(s))
roots = {'tools/audit_repository.py','tools/test_v32_entry.py','Makefile','exports/generated/cabinet-v32/build_v32.py','exports/generated/cabinet-v32/render_v32.py'} | {n for n in files if n.startswith('.github/workflows/')}
reachable = set(roots)
while True:
    added = {n for n in files if set(refs[n]) & reachable} - reachable
    if not added: break
    reachable.update(added)
rows = []
for name in files:
    if '__pycache__' in name or name.endswith(('.pyc','.pyo')):
        category,why = 'REMOVE','Reproducible tracked Python cache'
    elif name.startswith('reference/'):
        category,why = 'REFERENCE','Preserve provenance and licensing; no edits'
    elif name.startswith('exports/generated/') and not name.endswith(('.py','.md')):
        category,why = 'GENERATED-REVIEW','Retained review evidence; not temporary solely because generated'
    elif '/history/' in name or '/archive/' in name:
        category,why = 'HISTORY','Explicit historical location; preserve engineering evidence'
    elif name in reachable:
        category,why = 'CURRENT','Referenced from retained Make/CI or V32 route; may be PRE-V32 dependency'
    elif name.startswith(('tools/','config/')) and 'cabinet-v32' not in name:
        category,why = 'HISTORY','Outside computed build closure; preserve until dynamic imports and engineering value are reviewed'
    else:
        category,why = 'CURRENT','Retained contributor/documentation/engineering record; no deletion justified'
    rows.append(dict(path=name,classification=category,rationale=why,referenced_by=refs[name],build_reachable=name in reachable))
hashes = collections.defaultdict(list)
for name in files:
    if (root/name).is_file(): hashes[hashlib.sha256((root/name).read_bytes()).hexdigest()].append(name)
result = dict(method='Literal path/basename/Python-stem references and transitive closure from Make, CI and V32. Conservative candidates, not deletion authorization; dynamic references need manual review.',
              counts=dict(collections.Counter(x['classification'] for x in rows)),files=rows,
              exact_duplicate_groups=[v for v in hashes.values() if len(v)>1])
out = root/'.work/v32-audit';out.mkdir(parents=True,exist_ok=True)
(out/'repository-inventory.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(tracked=len(files),counts=result['counts'],duplicates=result['exact_duplicate_groups']),indent=2))
