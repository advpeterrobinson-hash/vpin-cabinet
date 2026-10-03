"""Build an offline, single-file CAD review viewer. Original CERN-OHL-S-2.0."""
from pathlib import Path
import argparse
import hashlib
import html
import json
import math
import re

ROOT = Path(__file__).resolve().parents[1]
from validate_wood_dowel_pivot_v32 import validate_visible_mechanism

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    current = json.loads((ROOT/'config/current_v32.json').read_text())
    parser.add_argument('--mesh', type=Path, default=ROOT/current.get('geometry_mesh',current['geometry_directory']+'/mesh.json'))
    parser.add_argument('--output', type=Path, default=ROOT/'exports/generated/viewer-v32/index.html')
    parser.add_argument('--legacy', action='store_true', help='Build historical V32 controls for an isolated study')
    args = parser.parse_args()
    if not args.legacy and args.mesh == ROOT/current.get('geometry_mesh',current['geometry_directory']+'/mesh.json') and args.output == ROOT/'exports/generated/viewer-v32/index.html':
        import runpy
        runpy.run_path(str(ROOT/('tools/build_viewer_v3363.py' if (ROOT/'config/viewer_v3363.json').exists() else 'tools/build_viewer_v3362.py' if (ROOT/'config/viewer_v3362.json').exists() else 'tools/build_viewer_v3361.py' if (ROOT/'config/viewer_v3361.json').exists() else 'tools/build_viewer_v336.py' if (ROOT/'config/viewer_v336.json').exists() else 'tools/build_viewer_v335.py' if (ROOT/'config/viewer_v335.json').exists() else 'tools/build_viewer_v334.py' if (ROOT/'config/viewer_v334.json').exists() else 'tools/build_viewer_v333.py' if (ROOT/'config/viewer_v333.json').exists() else 'tools/build_assembly_viewer_v332.py')), run_name='__main__')
        return
    raw = args.mesh.read_bytes()
    import gzip
    bundle = json.loads(gzip.decompress(raw) if args.mesh.suffix=='.gz' else raw)
    validate_visible_mechanism(bundle)
    report_path = args.mesh.with_name('validation.json')
    report = json.loads(report_path.read_text())
    assert report['mesh_sha256'] == hashlib.sha256(raw).hexdigest(), 'Stale CAD/viewer mesh'
    assert all(check['pass'] for check in report['checks']), 'Failed CAD checks; viewer generation blocked'
    parts = bundle['parts']
    variants = [part for state in bundle['states'].values() for part in state.values() if part]
    names = set()
    for part in parts:
        assert part['name'] not in names, 'Duplicate part ID'
        names.add(part['name'])
    for part in parts + variants:
        assert part['vertices'] and part['faces'], 'Empty mesh'
        for vertex in part['vertices']:
            assert len(vertex) == 3 and all(math.isfinite(v) for v in vertex)
        for face in part['faces']:
            assert len(face) == 3 and all(isinstance(i, int) and 0 <= i < len(part['vertices']) for i in face)
        part['vertices'] = [[round(v, 3) for v in vertex] for vertex in part['vertices']]
    template = (ROOT/'tools/viewer/template.html').read_text()
    translations=json.loads((ROOT/'tools/viewer/translations.json').read_text())
    assert all(v.get('en')==k and v.get('pt-BR') for k,v in translations.items()), 'Canonical English / PT-BR translation missing'
    ui_keys={html.unescape(k) for k in re.findall(r'data-i18n(?:-placeholder|-aria-label)?="([^"]+)"',template)}
    ui_keys.update(re.findall(r"\bt\('([^']+)'",template))
    assert ui_keys<=translations.keys(), 'Viewer text missing from translation source: '+str(ui_keys-translations.keys())
    replacements = {
        '__I18N__': json.dumps(translations,ensure_ascii=False,separators=(',', ':')).replace('</','<\\/'),
        '__THREE__': (ROOT/'tools/viewer/vendor/three.min.js').read_text(),
        '__ORBIT__': (ROOT/'tools/viewer/vendor/OrbitControls.js').read_text(),
        '__MESH__': json.dumps(parts, separators=(',', ':')).replace('</', '<\\/'),
        '__STATES__': json.dumps(bundle['states'], separators=(',', ':')).replace('</', '<\\/'),
        '__REVIEW__': json.dumps(bundle['review'], separators=(',', ':')),
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
