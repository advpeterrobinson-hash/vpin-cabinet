#!/usr/bin/env python3
"""Active v26 utility policy; obsolete v08 fascia dimensions are not active inputs."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    c=json.loads((ROOT/'config/rear_utility_v26.json').read_text())
    p=json.loads((ROOT/'config/cabinet_rear_cpu_shelf_v24.json').read_text())
    assert c['selected_architecture'] is None, 'Placement must remain unselected until owner visual review'
    assert not c['manufacturing_ready']
    assert c['permanent_functions']==['AC_MAINS_MASTER_DISCONNECT','OPTIONAL_ETHERNET']
    assert set(c['removed_rear_functions'])=={'SERVICE_HDMI','USB_A_SERVICE','USB_C_SERVICE','RESERVE','PC_POWER','PC_RESET','DOF_SERVICE'}
    assert c['interface_policy']['mount_to_cpu_door'] is False
    assert c['minimum_mains_signal_gap_mm']>=75
    for option in ('A','B'):
        for role in ('mains','ethernet'):
            for spec in c[option][role].values():
                assert len(spec)==6 and all(v>0 for v in spec[3:])
        assert 'enclosure' in c[option]['mains']
    assert p['rear_service_door']['aperture_bottom_z_mm']==110
    assert p['rear_service_door']['door_panel_bottom_z_mm']==98
    assert p['pc_shelf']['shelf_z_mm']==135
    assert p['pc_shelf']['fixed_support_rail_width_x_mm']==18
    print('PASS utility policy: mains + optional Ethernet only; two unselected layouts; independent enclosure; CPU datum unchanged')
    return 0

if __name__=='__main__':raise SystemExit(main())
