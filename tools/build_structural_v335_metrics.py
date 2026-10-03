"""Reuse established V33.4 accounting algorithm with explicit V33.5 authorities.
CERN-OHL-S-2.0. This does not run or modify any V33.4 artifact builder.
"""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'tools/build_solid_leg_metrics_v334.py').read_text()
s=s.replace("O=R/'exports/generated/solid-leg-v334'","O=R/'exports/generated/structural-v335'")
s=s.replace("reg=read('exports/generated/solid-leg-v334/manufacturing-register.json')","reg=read('exports/generated/structural-v335/manufacturing-register.json')")
s=s.replace("SC=read('config/solid_leg_blocks_v334.json')","metrics.update({p['instance_id']:p for p in read('exports/generated/structural-v335/changed-piece-metrics.json')})\nSC=read('config/solid_leg_blocks_v334.json')")
s=s.replace("cat=read('config/hardware_catalog_v33.json')","cat=read('config/hardware_catalog_v335.json')")
s=s.replace("manual=read('exports/generated/solid-leg-v334/assembly-manual.json')","manual=read('exports/generated/structural-v335/assembly-manual.json')")
s=s.replace("read('exports/generated/flatpack-v331/hardware-quantity-closure.json')","read('exports/generated/structural-v335/hardware-quantity-closure.json')")
s=s.replace("v=vols.get(h['id']);q=h['quantity']","v=vols.get(h['id']) if h['id'] not in ['F27','F57','F58','I10','I11'] else None;q=h['quantity']")
exec(compile(s,str(R/'tools/build_solid_leg_metrics_v334.py'),'exec'),{'__file__':str(__file__)})
