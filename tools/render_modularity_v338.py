"""Render isolated V33.8 review12–20 with shared native-triangle renderer. CERN-OHL-S-2.0."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'tools/render_two_stock_v337.py').read_text().replace('two-stock-user-module-v337','service-productization-v338').replace('review-scenes.json.gz','modularity-review-scenes.json.gz').replace('review-index.json','modularity-review-index.json').replace('review.html','modularity-review.html').replace('V33.7','V33.8').replace('24 native CAD reviews. Two nominal plywood stocks and removable under-front user module; purchased hardware remains provisional.','9 native CAD reviews. Optional modules and cable planning; no permanent hardpoint holes.').replace('V337_REVIEW_RENDER_PASS','V338_MODULARITY_RENDER_PASS')
exec(compile(s,str(Path(__file__)),'exec'))
