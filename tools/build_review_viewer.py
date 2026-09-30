"""Build an offline, single-file CAD review viewer. Original CERN-OHL-S-2.0."""
from pathlib import Path
import argparse
import hashlib
import html
import json
import math

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mesh', type=Path, default=ROOT/'exports/generated/consolidated-v32/mesh.json')
    parser.add_argument('--output', type=Path, default=ROOT/'exports/generated/viewer-v32/index.html')
    args = parser.parse_args()
    raw = args.mesh.read_bytes()
    parts = json.loads(raw)
    names = set()
    for part in parts:
        assert part['name'] not in names, 'Duplicate part ID'
        names.add(part['name'])
        assert part['vertices'] and part['faces'], 'Empty mesh'
        for vertex in part['vertices']:
            assert len(vertex) == 3 and all(math.isfinite(v) for v in vertex)
        for face in part['faces']:
            assert len(face) == 3 and all(isinstance(i, int) and 0 <= i < len(part['vertices']) for i in face)
        part['vertices'] = [[round(v, 3) for v in vertex] for vertex in part['vertices']]
    template = (ROOT/'tools/viewer/template.html').read_text()
    replacements = {
        '__THREE__': (ROOT/'tools/viewer/vendor/three.min.js').read_text(),
        '__ORBIT__': (ROOT/'tools/viewer/vendor/OrbitControls.js').read_text(),
        '__MESH__': json.dumps(parts, separators=(',', ':')).replace('</', '<\\/'),
        '__PROVENANCE__': json.dumps({'source': str(args.mesh.relative_to(ROOT)) if args.mesh.is_relative_to(ROOT) else args.mesh.name,
                                    'sha256': hashlib.sha256(raw).hexdigest(), 'parts': len(parts)}, ensure_ascii=False),
        '__LICENSE__': html.escape((ROOT/'LICENSE').read_text()),
        '__NOTICE__': html.escape((ROOT/'NOTICE.md').read_text()),
        '__MIT__': html.escape((ROOT/'tools/viewer/vendor/LICENSE.three').read_text()),
    }
    for key, value in replacements.items():
        template = template.replace(key, value)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(template)
    print(f'{args.output}: {len(parts)} parts, {args.output.stat().st_size / 1e6:.1f} MB; offline')

if __name__ == '__main__':
    main()
