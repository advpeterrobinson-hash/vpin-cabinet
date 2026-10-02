# V33 — Flatpack bill of materials

One cabinet inventory. Manufacturing BLOCKED. TBD means unresolved, never zero. The mechanical kit needs no electronics. Do not sum alternative fan and blank configurations. No prices.

Wood dimensions are installed bounding boxes, not nesting rectangles. The93 wood lines include assemblies awaiting decomposition. Full source and technical notes are retained in JSON.

## BOM 1 — Flatpack wood

### Stage 01 — Cabinet shell and legs

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| P001 | Cabinet side — SIDE_L | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P002 | Cabinet side — SIDE_R | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P003 | Cabinet end structure — FRONT | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P004 | Cabinet end structure — REAR | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P005 | Structural floor — FLOOR | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P006 | Floor cleat — FLOOR_CLEAT_18 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P007 | Floor cleat — FLOOR_CLEAT_552 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P029 | Laminated leg block — CandidateLegBlockFL | 7 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P030 | Laminated leg block — CandidateLegBlockFR | 7 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P031 | Laminated leg block — CandidateLegBlockRL | 7 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P032 | Laminated leg block — CandidateLegBlockRR | 7 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |

- **P001** — Nominal dimensions: {"world_bounds_mm":[-3.88908730122752,-3.88908730122752,0.0,25.939277162768004,1311.9890873012264,596.9],"world_size_mm":[29.828364463995523,1315.878174602454,596.9],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; SIDE_L. Load path or positive retention: premium class cannot be automatically downgraded.
- **P002** — Nominal dimensions: {"world_bounds_mm":[574.0607228372319,-3.88908730122752,0.0,603.8890873012274,1311.9890873012264,596.9],"world_size_mm":[29.828364463995513,1315.878174602454,596.9],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; SIDE_R. Load path or positive retention: premium class cannot be automatically downgraded.
- **P003** — Nominal dimensions: {"world_bounds_mm":[14.110912703472618,0.0,0.0,585.8890872965293,22.05018986624017,400.05],"world_size_mm":[571.7781745930566,22.05018986624017,400.05],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; FRONT. Load path or positive retention: premium class cannot be automatically downgraded.
- **P004** — Nominal dimensions: {"world_bounds_mm":[14.110912703472106,1286.0498101337764,0.0,585.8890956835587,1308.1,596.9],"world_size_mm":[571.7781829800866,22.05018986622349,596.9],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; REAR. Load path or positive retention: premium class cannot be automatically downgraded.
- **P005** — Nominal dimensions: {"world_bounds_mm":[18.0,18.0,18.0,582.0,1290.1,36.0],"world_size_mm":[564.0,1272.1,18.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; FLOOR. Load path or positive retention: premium class cannot be automatically downgraded.
- **P006** — Nominal dimensions: {"world_bounds_mm":[18.0,120.0,0.0,48.0,1272.1,18.0],"world_size_mm":[30.0,1152.1,18.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; FLOOR_CLEAT_18. Load path or positive retention: premium class cannot be automatically downgraded.
- **P007** — Nominal dimensions: {"world_bounds_mm":[552.0,120.0,0.0,582.0,1272.1,18.0],"world_size_mm":[30.0,1152.1,18.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; FLOOR_CLEAT_552. Load path or positive retention: premium class cannot be automatically downgraded.
- **P029** — Nominal dimensions: {"world_bounds_mm":[14.110912699983817,14.110912699983817,54.0,72.0,72.0,180.0],"world_size_mm":[57.889087300016186,57.889087300016186,126.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; CandidateLegBlockFL. Seven18 mm laminations per block;45-degree bores change each layer; do not nest7 identical outlines blindly.
- **P030** — Nominal dimensions: {"world_bounds_mm":[528.0,14.11091269998229,54.0,585.8890873000176,72.0,180.0],"world_size_mm":[57.88908730001765,57.88908730001771,126.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; CandidateLegBlockFR. Seven18 mm laminations per block;45-degree bores change each layer; do not nest7 identical outlines blindly.
- **P031** — Nominal dimensions: {"world_bounds_mm":[14.110912699982261,1236.1,36.0,72.0,1293.9890873000177,162.0],"world_size_mm":[57.889087300017735,57.88908730001776,126.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; CandidateLegBlockRL. Seven18 mm laminations per block;45-degree bores change each layer; do not nest7 identical outlines blindly.
- **P032** — Nominal dimensions: {"world_bounds_mm":[528.0,1236.1,36.0,585.8890873000154,1293.9890873000154,162.0],"world_size_mm":[57.889087300015376,57.88908730001549,126.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; CandidateLegBlockRR. Seven18 mm laminations per block;45-degree bores change each layer; do not nest7 identical outlines blindly.

### Stage 02 — Shelf supports and crossmembers

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| P009 | Removable equipment shelf — SHELF_1 | 1 | MODULAR_SECONDARY | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P010 | Removable equipment shelf — SHELF_2 | 1 | MODULAR_SECONDARY | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P011 | Removable equipment shelf — SHELF_3 | 1 | MODULAR_SECONDARY | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P012 | Fixed shelf support — SHELF_SUPPORT_1L | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P013 | Fixed shelf support — SHELF_SUPPORT_1R | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P014 | Fixed shelf support — SHELF_SUPPORT_2L | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P015 | Fixed shelf support — SHELF_SUPPORT_2R | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P016 | Fixed shelf support — SHELF_SUPPORT_3L | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P017 | Fixed shelf support — SHELF_SUPPORT_3R | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P018 | Removable crossmember — CROSS_1 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P019 | Removable crossmember — CROSS_2 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P020 | Removable crossmember — CROSS_3 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P021 | Crossmember guide — CROSS_GUIDE_1L | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P022 | Crossmember guide — CROSS_GUIDE_1R | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P023 | Crossmember guide — CROSS_GUIDE_2L | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P024 | Crossmember guide — CROSS_GUIDE_2R | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P025 | Crossmember guide — CROSS_GUIDE_3L | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P026 | Crossmember guide — CROSS_GUIDE_3R | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P027 | Floor-supported PCBase — PC_BASE | 1 | MODULAR_SECONDARY | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |

- **P009** — Nominal dimensions: {"world_bounds_mm":[20.0,120.0,160.0,580.0,270.0,172.0],"world_size_mm":[560.0,150.0,12.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; SHELF_1. Secondary substitution only after nesting trigger and quality/load/joint qualification.
- **P010** — Nominal dimensions: {"world_bounds_mm":[20.0,565.0,180.0,580.0,715.0,192.0],"world_size_mm":[560.0,150.0,12.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; SHELF_2. Secondary substitution only after nesting trigger and quality/load/joint qualification.
- **P011** — Nominal dimensions: {"world_bounds_mm":[20.0,865.0,240.0,580.0,1015.0,252.0],"world_size_mm":[560.0,150.0,12.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; SHELF_3. Secondary substitution only after nesting trigger and quality/load/joint qualification.
- **P012** — Nominal dimensions: {"world_bounds_mm":[18.0,120.0,142.0,60.0,270.0,160.0],"world_size_mm":[42.0,150.0,18.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; SHELF_SUPPORT_1L. Load path or positive retention: premium class cannot be automatically downgraded.
- **P013** — Nominal dimensions: {"world_bounds_mm":[540.0,120.0,142.0,582.0,270.0,160.0],"world_size_mm":[42.0,150.0,18.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; SHELF_SUPPORT_1R. Load path or positive retention: premium class cannot be automatically downgraded.
- **P014** — Nominal dimensions: {"world_bounds_mm":[18.0,565.0,162.0,60.0,715.0,180.0],"world_size_mm":[42.0,150.0,18.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; SHELF_SUPPORT_2L. Load path or positive retention: premium class cannot be automatically downgraded.
- **P015** — Nominal dimensions: {"world_bounds_mm":[540.0,565.0,162.0,582.0,715.0,180.0],"world_size_mm":[42.0,150.0,18.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; SHELF_SUPPORT_2R. Load path or positive retention: premium class cannot be automatically downgraded.
- **P016** — Nominal dimensions: {"world_bounds_mm":[18.0,865.0,222.0,60.0,1015.0,240.0],"world_size_mm":[42.0,150.0,18.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; SHELF_SUPPORT_3L. Load path or positive retention: premium class cannot be automatically downgraded.
- **P017** — Nominal dimensions: {"world_bounds_mm":[540.0,865.0,222.0,582.0,1015.0,240.0],"world_size_mm":[42.0,150.0,18.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; SHELF_SUPPORT_3R. Load path or positive retention: premium class cannot be automatically downgraded.
- **P018** — Nominal dimensions: {"world_bounds_mm":[30.2,371.0,283.691375367901,569.8000000000001,389.0,365.2632063538165],"world_size_mm":[539.6,18.0,81.57183098591548],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; CROSS_1. Load path or positive retention: premium class cannot be automatically downgraded.
- **P019** — Nominal dimensions: {"world_bounds_mm":[30.2,691.0,339.578699311563,569.8000000000001,709.0,421.1505302974785],"world_size_mm":[539.6,18.0,81.57183098591548],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; CROSS_2. Load path or positive retention: premium class cannot be automatically downgraded.
- **P020** — Nominal dimensions: {"world_bounds_mm":[30.2,971.0,388.4801077622672,569.8000000000001,989.0,470.0519387481827],"world_size_mm":[539.6,18.0,81.57183098591548],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; CROSS_3. Load path or positive retention: premium class cannot be automatically downgraded.
- **P021** — Nominal dimensions: {"world_bounds_mm":[18.0,350.0,238.691375367901,36.0,410.0,383.691375367901],"world_size_mm":[18.0,60.0,145.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; CROSS_GUIDE_1L. Load path or positive retention: premium class cannot be automatically downgraded.
- **P022** — Nominal dimensions: {"world_bounds_mm":[564.0,350.0,238.691375367901,582.0,410.0,383.691375367901],"world_size_mm":[18.0,60.0,145.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; CROSS_GUIDE_1R. Load path or positive retention: premium class cannot be automatically downgraded.
- **P023** — Nominal dimensions: {"world_bounds_mm":[18.0,670.0,294.578699311563,36.0,730.0,439.578699311563],"world_size_mm":[18.0,60.0,145.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; CROSS_GUIDE_2L. Load path or positive retention: premium class cannot be automatically downgraded.
- **P024** — Nominal dimensions: {"world_bounds_mm":[564.0,670.0,294.578699311563,582.0,730.0,439.578699311563],"world_size_mm":[18.0,60.0,145.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; CROSS_GUIDE_2R. Load path or positive retention: premium class cannot be automatically downgraded.
- **P025** — Nominal dimensions: {"world_bounds_mm":[18.0,950.0,343.4801077622672,36.0,1010.0,488.4801077622672],"world_size_mm":[18.0,60.0,145.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; CROSS_GUIDE_3L. Load path or positive retention: premium class cannot be automatically downgraded.
- **P026** — Nominal dimensions: {"world_bounds_mm":[564.0,950.0,343.4801077622672,582.0,1010.0,488.4801077622672],"world_size_mm":[18.0,60.0,145.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; CROSS_GUIDE_3R. Load path or positive retention: premium class cannot be automatically downgraded.
- **P027** — Nominal dimensions: {"world_bounds_mm":[157.5,830.0,36.0,442.5,1290.0,54.0],"world_size_mm":[285.0,460.0,18.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; PC_BASE. Secondary substitution only after nesting trigger and quality/load/joint qualification.

### Stage 03 — Wooden playfield pivot

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| P034 | Playfield load-carrying base — PF_BasePlywood | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P035 | Floor-bearing open cradle — PF_OpenCradleL | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P036 | Floor-bearing open cradle — PF_OpenCradleR | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |

- **P034** — Nominal dimensions: {"world_bounds_mm":[49.999999999999986,64.01361107210916,331.3788680816646,550.0,1071.9014918612513,524.5951171988511],"world_size_mm":[500.0,1007.8878807891422,193.21624911718646],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; PF_BasePlywood. Load path or positive retention: premium class cannot be automatically downgraded.
- **P035** — Nominal dimensions: {"world_bounds_mm":[17.999999999999993,995.2506198471799,36.0,36.0,1075.25061984718,514.2203301149066],"world_size_mm":[18.000000000000007,80.0,478.2203301149066],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; PF_OpenCradleL. Load path or positive retention: premium class cannot be automatically downgraded.
- **P036** — Nominal dimensions: {"world_bounds_mm":[564.0,995.2506198471799,36.0,582.0,1075.25061984718,514.2203301149066],"world_size_mm":[18.0,80.0,478.2203301149066],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; PF_OpenCradleR. Load path or positive retention: premium class cannot be automatically downgraded.

### Stage 04 — Main rear service door

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| P008 | Main rear door — REAR_DOOR | 1 | MODULAR_SECONDARY | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |

- **P008** — Nominal dimensions: {"world_bounds_mm":[102.0,1296.1,54.0,498.0,1308.1,383.0],"world_size_mm":[396.0,12.0,329.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; REAR_DOOR. Secondary substitution only after nesting trigger and quality/load/joint qualification.

### Stage 05 — Main ventilation and filter interfaces

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| P037 | Floor filter holder — RemovableIntakeFilterL | 1 | MODULAR_SECONDARY | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P038 | Floor filter holder — RemovableIntakeFilterR | 1 | MODULAR_SECONDARY | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |

- **P037** — Nominal dimensions: {"world_bounds_mm":[65.0,625.0,10.0,235.0,795.0,18.0],"world_size_mm":[170.0,170.0,8.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; RemovableIntakeFilterL. Secondary substitution only after nesting trigger and quality/load/joint qualification.
- **P038** — Nominal dimensions: {"world_bounds_mm":[365.0,625.0,10.0,535.0,795.0,18.0],"world_size_mm":[170.0,170.0,8.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; RemovableIntakeFilterR. Secondary substitution only after nesting trigger and quality/load/joint qualification.

### Stage 06 — Backbox shell and WPC interface

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| P028 | Rear bearing shelf — BACKBOX_BASE | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P042 | Backbox shell/frame — BB_SideL | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P043 | Backbox shell/frame — BB_SideR | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P044 | Backbox shell/frame — BB_Floor | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P045 | Backbox shell/frame — BB_Top | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P046 | Backbox shell/frame — BB_RearFrame | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P047 | Backbox shell/frame — BB_TopFrontRail | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |

- **P028** — Nominal dimensions: {"world_bounds_mm":[18.0,1127.125,578.9,582.0,1290.1,596.9],"world_size_mm":[564.0,162.9749999999999,18.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BACKBOX_BASE. Load path or positive retention: premium class cannot be automatically downgraded.
- **P042** — Nominal dimensions: {"world_bounds_mm":[-90.0,1054.1,596.9,-71.99999999999997,1302.1,1320.8],"world_size_mm":[18.00000000000003,248.0,723.9],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_SideL. Load path or positive retention: premium class cannot be automatically downgraded.
- **P043** — Nominal dimensions: {"world_bounds_mm":[672.0,1054.1,596.9,690.0,1302.1,1320.8],"world_size_mm":[18.0,248.0,723.9],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_SideR. Load path or positive retention: premium class cannot be automatically downgraded.
- **P044** — Nominal dimensions: {"world_bounds_mm":[-78.0,1146.0,596.9,678.0,1302.1,614.9],"world_size_mm":[756.0,156.0999999999999,18.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_Floor. Load path or positive retention: premium class cannot be automatically downgraded.
- **P045** — Nominal dimensions: {"world_bounds_mm":[-78.0,1120.0,1302.8,678.0,1302.1,1320.8],"world_size_mm":[756.0,182.0999999999999,18.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_Top. Load path or positive retention: premium class cannot be automatically downgraded.
- **P046** — Nominal dimensions: {"world_bounds_mm":[-90.0,1290.1,596.9,690.0,1308.1,1320.8],"world_size_mm":[780.0,18.0,723.9],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_RearFrame. Load path or positive retention: premium class cannot be automatically downgraded.
- **P047** — Nominal dimensions: {"world_bounds_mm":[-78.0,1055.1940737670948,1302.8,678.0,1112.0,1320.8],"world_size_mm":[756.0,56.80592623290522,18.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_TopFrontRail. Load path or positive retention: premium class cannot be automatically downgraded.

### Stage 07 — Upright locks and parking

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| P088 | Lock parking lamination — BB_UprightLockLParkingPad0 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P089 | Lock parking lamination — BB_UprightLockLParkingPad1 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P090 | Lock parking lamination — BB_UprightLockRParkingPad0 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P091 | Lock parking lamination — BB_UprightLockRParkingPad1 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |

- **P088** — Nominal dimensions: {"world_bounds_mm":[160.0,1252.0,614.9,210.0,1284.0,632.9],"world_size_mm":[50.0,32.0,18.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_UprightLockLParkingPad0. Load path or positive retention: premium class cannot be automatically downgraded.
- **P089** — Nominal dimensions: {"world_bounds_mm":[160.0,1252.0,632.9,210.0,1284.0,650.9],"world_size_mm":[50.0,32.0,18.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_UprightLockLParkingPad1. Load path or positive retention: premium class cannot be automatically downgraded.
- **P090** — Nominal dimensions: {"world_bounds_mm":[390.0,1252.0,614.9,440.0,1284.0,632.9],"world_size_mm":[50.0,32.0,18.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_UprightLockRParkingPad0. Load path or positive retention: premium class cannot be automatically downgraded.
- **P091** — Nominal dimensions: {"world_bounds_mm":[390.0,1252.0,632.9,440.0,1284.0,650.9],"world_size_mm":[50.0,32.0,18.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_UprightLockRParkingPad1. Load path or positive retention: premium class cannot be automatically downgraded.

### Stage 08 — Twin backbox doors

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| P079 | Backbox rear door — BB_DoorL | 1 | MODULAR_SECONDARY | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P080 | Backbox rear door — BB_DoorR | 1 | MODULAR_SECONDARY | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P085 | Continuous-hinge fixed cleat — BB_HingeCleatL | 1 | STRUCTURAL_PREMIUM | CNC_COMPONENT_BREAKDOWN_HOLD / REQUIRED_FLATPACK_HARDWARE |
| P086 | Continuous-hinge fixed cleat — BB_HingeCleatR | 1 | STRUCTURAL_PREMIUM | CNC_COMPONENT_BREAKDOWN_HOLD / REQUIRED_FLATPACK_HARDWARE |
| P087 | Center overlap strip — BB_CenterAstragal | 1 | MODULAR_SECONDARY | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |

- **P079** — Nominal dimensions: {"world_bounds_mm":[-52.0,1310.1,644.0,299.0,1322.1,1272.0],"world_size_mm":[351.0,12.0,628.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_DoorL. Secondary substitution only after nesting trigger and quality/load/joint qualification.
- **P080** — Nominal dimensions: {"world_bounds_mm":[301.0,1310.1,644.0,652.0,1322.1,1272.0],"world_size_mm":[351.0,12.0,628.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_DoorR. Secondary substitution only after nesting trigger and quality/load/joint qualification.
- **P085** — Nominal dimensions: {"world_bounds_mm":[-78.0,1308.1,644.0,-55.0,1322.1,1272.0],"world_size_mm":[23.0,14.0,628.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_HingeCleatL. Fused/stepped assembly needs explicit flatpack decomposition or CNC thickness plan; no new wood designed.
- **P086** — Nominal dimensions: {"world_bounds_mm":[655.0,1308.1,644.0,678.0,1322.1,1272.0],"world_size_mm":[23.0,14.0,628.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_HingeCleatR. Fused/stepped assembly needs explicit flatpack decomposition or CNC thickness plan; no new wood designed.
- **P087** — Nominal dimensions: {"world_bounds_mm":[282.0,1296.1,656.0,318.0,1308.1,1260.0],"world_size_mm":[36.0,12.0,604.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_CenterAstragal. Secondary substitution only after nesting trigger and quality/load/joint qualification.

### Stage 09 — Backbox blanks, filters and optional fans

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| P081 | Backbox intake filter frame — BB_IntakeFilterFrameL | 1 | MODULAR_SECONDARY | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P082 | Backbox intake filter frame — BB_IntakeFilterFrameR | 1 | MODULAR_SECONDARY | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P083 | Downward intake baffle assembly — BB_IntakeDownBaffleL | 1 | MODULAR_SECONDARY | CNC_COMPONENT_BREAKDOWN_HOLD / REQUIRED_FLATPACK_HARDWARE |
| P084 | Downward intake baffle assembly — BB_IntakeDownBaffleR | 1 | MODULAR_SECONDARY | CNC_COMPONENT_BREAKDOWN_HOLD / REQUIRED_FLATPACK_HARDWARE |
| P092 | Interchangeable fan blank — BB_FanBlankL | 1 | MODULAR_SECONDARY | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P093 | Interchangeable fan blank — BB_FanBlankR | 1 | MODULAR_SECONDARY | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |

- **P081** — Nominal dimensions: {"world_bounds_mm":[5.0,1322.1,688.0,245.0,1328.1,788.0],"world_size_mm":[240.0,6.0,100.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_IntakeFilterFrameL. Secondary substitution only after nesting trigger and quality/load/joint qualification.
- **P082** — Nominal dimensions: {"world_bounds_mm":[355.0,1322.1,688.0,595.0,1328.1,788.0],"world_size_mm":[240.0,6.0,100.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_IntakeFilterFrameR. Secondary substitution only after nesting trigger and quality/load/joint qualification.
- **P083** — Nominal dimensions: {"world_bounds_mm":[9.0,1268.1,686.0,241.0,1310.1,790.0],"world_size_mm":[232.0,42.0,104.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_IntakeDownBaffleL. Fused/stepped assembly needs explicit flatpack decomposition or CNC thickness plan; no new wood designed.
- **P084** — Nominal dimensions: {"world_bounds_mm":[359.0,1268.1,686.0,591.0,1310.1,790.0],"world_size_mm":[232.0,42.0,104.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_IntakeDownBaffleR. Fused/stepped assembly needs explicit flatpack decomposition or CNC thickness plan; no new wood designed.
- **P092** — Nominal dimensions: {"world_bounds_mm":[91.0,1322.1,1096.0,219.0,1328.1,1224.0],"world_size_mm":[128.0,6.0,128.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/blank-fans.FCStd; BB_FanBlankL. Secondary substitution only after nesting trigger and quality/load/joint qualification.
- **P093** — Nominal dimensions: {"world_bounds_mm":[381.0,1322.1,1096.0,509.0,1328.1,1224.0],"world_size_mm":[128.0,6.0,128.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/blank-fans.FCStd; BB_FanBlankR. Secondary substitution only after nesting trigger and quality/load/joint qualification.

### Stage 10 — Display carrier and glass retention

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| P048 | Padded lower glass rail — BB_GlassLowerRail | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P049 | Positive glass top retainer — BB_GlassTopRetainer | 1 | STRUCTURAL_PREMIUM | CNC_COMPONENT_BREAKDOWN_HOLD / REQUIRED_FLATPACK_HARDWARE |
| P050 | Monitor structural carrier member — BB_MonitorRail0 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P051 | Monitor structural carrier member — BB_MonitorRailCleatL0 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P052 | Monitor structural carrier member — BB_MonitorRailCleatR0 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P053 | Monitor structural carrier member — BB_MonitorRail1 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P054 | Monitor structural carrier member — BB_MonitorRailCleatL1 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P055 | Monitor structural carrier member — BB_MonitorRailCleatR1 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P056 | Monitor structural carrier member — BB_MonitorCarrier0 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P057 | Monitor structural carrier member — BB_MonitorDepthShoe00 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P058 | Monitor structural carrier member — BB_MonitorDepthShoe01 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P059 | Monitor structural carrier member — BB_MonitorCarrier1 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P060 | Monitor structural carrier member — BB_MonitorDepthShoe10 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P061 | Monitor structural carrier member — BB_MonitorDepthShoe11 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P062 | Replaceable load-carrying VESA plate — BB_ReplaceableVESAPlate | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P063 | Replaceable display bezel — BB_DisplayReplaceableBezel | 1 | MODULAR_SECONDARY | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P064 | Monitor stop block — BB_MonitorStopBlock0 | 1 | STRUCTURAL_PREMIUM | CNC_COMPONENT_BREAKDOWN_HOLD / REQUIRED_FLATPACK_HARDWARE |
| P065 | Monitor stop block — BB_MonitorStopBlock1 | 1 | STRUCTURAL_PREMIUM | CNC_COMPONENT_BREAKDOWN_HOLD / REQUIRED_FLATPACK_HARDWARE |
| P066 | Monitor stop contact pad — BB_MonitorStopContact0 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P067 | Monitor stop contact pad — BB_MonitorStopContact1 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |

- **P048** — Nominal dimensions: {"world_bounds_mm":[-72.0,1108.0,822.0,672.0,1126.0,840.0],"world_size_mm":[744.0,18.0,18.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_GlassLowerRail. Load path or positive retention: premium class cannot be automatically downgraded.
- **P049** — Nominal dimensions: {"world_bounds_mm":[-78.0,1104.0,1307.0,678.0,1141.0,1332.8],"world_size_mm":[756.0,37.0,25.799999999999955],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_GlassTopRetainer. Fused/stepped assembly needs explicit flatpack decomposition or CNC thickness plan; no new wood designed.
- **P050** — Nominal dimensions: {"world_bounds_mm":[-72.0,1268.0,816.0,672.0,1286.0,858.0],"world_size_mm":[744.0,18.0,42.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_MonitorRail0. Load path or positive retention: premium class cannot be automatically downgraded.
- **P051** — Nominal dimensions: {"world_bounds_mm":[-72.0,1248.0,786.0,-54.0,1286.0,816.0],"world_size_mm":[18.0,38.0,30.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_MonitorRailCleatL0. Load path or positive retention: premium class cannot be automatically downgraded.
- **P052** — Nominal dimensions: {"world_bounds_mm":[654.0,1248.0,786.0,672.0,1286.0,816.0],"world_size_mm":[18.0,38.0,30.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_MonitorRailCleatR0. Load path or positive retention: premium class cannot be automatically downgraded.
- **P053** — Nominal dimensions: {"world_bounds_mm":[-72.0,1268.0,1248.0,672.0,1286.0,1290.0],"world_size_mm":[744.0,18.0,42.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_MonitorRail1. Load path or positive retention: premium class cannot be automatically downgraded.
- **P054** — Nominal dimensions: {"world_bounds_mm":[-72.0,1248.0,1218.0,-54.0,1286.0,1248.0],"world_size_mm":[18.0,38.0,30.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_MonitorRailCleatL1. Load path or positive retention: premium class cannot be automatically downgraded.
- **P055** — Nominal dimensions: {"world_bounds_mm":[654.0,1248.0,1218.0,672.0,1286.0,1248.0],"world_size_mm":[18.0,38.0,30.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_MonitorRailCleatR1. Load path or positive retention: premium class cannot be automatically downgraded.
- **P056** — Nominal dimensions: {"world_bounds_mm":[135.0,1240.0,870.0,185.0,1258.0,1236.0],"world_size_mm":[50.0,18.0,366.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_MonitorCarrier0. Load path or positive retention: premium class cannot be automatically downgraded.
- **P057** — Nominal dimensions: {"world_bounds_mm":[135.0,1240.0,858.0,185.0,1290.0,876.0],"world_size_mm":[50.0,50.0,18.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_MonitorDepthShoe00. Load path or positive retention: premium class cannot be automatically downgraded.
- **P058** — Nominal dimensions: {"world_bounds_mm":[135.0,1240.0,1230.0,185.0,1290.0,1248.0],"world_size_mm":[50.0,50.0,18.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_MonitorDepthShoe01. Load path or positive retention: premium class cannot be automatically downgraded.
- **P059** — Nominal dimensions: {"world_bounds_mm":[415.0,1240.0,870.0,465.0,1258.0,1236.0],"world_size_mm":[50.0,18.0,366.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_MonitorCarrier1. Load path or positive retention: premium class cannot be automatically downgraded.
- **P060** — Nominal dimensions: {"world_bounds_mm":[415.0,1240.0,858.0,465.0,1290.0,876.0],"world_size_mm":[50.0,50.0,18.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_MonitorDepthShoe10. Load path or positive retention: premium class cannot be automatically downgraded.
- **P061** — Nominal dimensions: {"world_bounds_mm":[415.0,1240.0,1230.0,465.0,1290.0,1248.0],"world_size_mm":[50.0,50.0,18.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_MonitorDepthShoe11. Load path or positive retention: premium class cannot be automatically downgraded.
- **P062** — Nominal dimensions: {"world_bounds_mm":[120.0,1228.0,949.0,480.0,1240.0,1179.0],"world_size_mm":[360.0,12.0,230.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_ReplaceableVESAPlate. Load path or positive retention: premium class cannot be automatically downgraded.
- **P063** — Nominal dimensions: {"world_bounds_mm":[-70.0,1120.0,842.0,670.0,1126.0,1299.0],"world_size_mm":[740.0,6.0,457.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_DisplayReplaceableBezel. Secondary substitution only after nesting trigger and quality/load/joint qualification.
- **P064** — Nominal dimensions: {"world_bounds_mm":[185.0,1230.0,899.0,223.0,1258.0,929.0],"world_size_mm":[38.0,28.0,30.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_MonitorStopBlock0. Fused/stepped assembly needs explicit flatpack decomposition or CNC thickness plan; no new wood designed.
- **P065** — Nominal dimensions: {"world_bounds_mm":[377.0,1230.0,899.0,415.0,1258.0,929.0],"world_size_mm":[38.0,28.0,30.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_MonitorStopBlock1. Fused/stepped assembly needs explicit flatpack decomposition or CNC thickness plan; no new wood designed.
- **P066** — Nominal dimensions: {"world_bounds_mm":[205.0,1228.0,945.0,223.0,1240.0,949.0],"world_size_mm":[18.0,12.0,4.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_MonitorStopContact0. Load path or positive retention: premium class cannot be automatically downgraded.
- **P067** — Nominal dimensions: {"world_bounds_mm":[377.0,1228.0,945.0,395.0,1240.0,949.0],"world_size_mm":[18.0,12.0,4.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_MonitorStopContact1. Load path or positive retention: premium class cannot be automatically downgraded.

### Stage 11 — DMD/speaker cassette

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| P068 | Lower cassette frame — BB_LowerCassetteFrame | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P069 | Replaceable speaker baffle — BB_SpeakerBaffleL | 1 | MODULAR_SECONDARY | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P070 | Replaceable speaker baffle — BB_SpeakerBaffleR | 1 | MODULAR_SECONDARY | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P071 | Replaceable DMD bezel — BB_DMDReplaceableBezel | 1 | MODULAR_SECONDARY | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P072 | Load-carrying DMD rear adapter — BB_DMDRearAdapter | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P073 | DMD depth tie — BB_DMDDepthTie0 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P074 | DMD depth tie — BB_DMDDepthTie1 | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P075 | Cassette fixed cleat — BB_CassetteFixedCleatL0 | 1 | STRUCTURAL_PREMIUM | CNC_COMPONENT_BREAKDOWN_HOLD / REQUIRED_FLATPACK_HARDWARE |
| P076 | Cassette fixed cleat — BB_CassetteFixedCleatL1 | 1 | STRUCTURAL_PREMIUM | CNC_COMPONENT_BREAKDOWN_HOLD / REQUIRED_FLATPACK_HARDWARE |
| P077 | Cassette fixed cleat — BB_CassetteFixedCleatR0 | 1 | STRUCTURAL_PREMIUM | CNC_COMPONENT_BREAKDOWN_HOLD / REQUIRED_FLATPACK_HARDWARE |
| P078 | Cassette fixed cleat — BB_CassetteFixedCleatR1 | 1 | STRUCTURAL_PREMIUM | CNC_COMPONENT_BREAKDOWN_HOLD / REQUIRED_FLATPACK_HARDWARE |

- **P068** — Nominal dimensions: {"world_bounds_mm":[-70.0,1156.0,620.0,670.0,1174.0,820.0],"world_size_mm":[740.0,18.0,200.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_LowerCassetteFrame. Load path or positive retention: premium class cannot be automatically downgraded.
- **P069** — Nominal dimensions: {"world_bounds_mm":[-70.0,1144.0,620.0,90.0,1156.0,820.0],"world_size_mm":[160.0,12.0,200.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_SpeakerBaffleL. Secondary substitution only after nesting trigger and quality/load/joint qualification.
- **P070** — Nominal dimensions: {"world_bounds_mm":[510.0,1144.0,620.0,670.0,1156.0,820.0],"world_size_mm":[160.0,12.0,200.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_SpeakerBaffleR. Secondary substitution only after nesting trigger and quality/load/joint qualification.
- **P071** — Nominal dimensions: {"world_bounds_mm":[90.0,1144.0,626.0,510.0,1156.0,806.0],"world_size_mm":[420.0,12.0,180.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_DMDReplaceableBezel. Secondary substitution only after nesting trigger and quality/load/joint qualification.
- **P072** — Nominal dimensions: {"world_bounds_mm":[80.0,1219.0,704.0,520.0,1231.0,800.0],"world_size_mm":[440.0,12.0,96.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_DMDRearAdapter. Load path or positive retention: premium class cannot be automatically downgraded.
- **P073** — Nominal dimensions: {"world_bounds_mm":[80.0,1174.0,710.0,98.0,1219.0,780.0],"world_size_mm":[18.0,45.0,70.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_DMDDepthTie0. Load path or positive retention: premium class cannot be automatically downgraded.
- **P074** — Nominal dimensions: {"world_bounds_mm":[502.0,1174.0,710.0,520.0,1219.0,780.0],"world_size_mm":[18.0,45.0,70.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_DMDDepthTie1. Load path or positive retention: premium class cannot be automatically downgraded.
- **P075** — Nominal dimensions: {"world_bounds_mm":[-72.0,1174.0,629.0,-50.0,1206.0,653.0],"world_size_mm":[22.0,32.0,24.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_CassetteFixedCleatL0. Fused/stepped assembly needs explicit flatpack decomposition or CNC thickness plan; no new wood designed.
- **P076** — Nominal dimensions: {"world_bounds_mm":[-72.0,1174.0,789.0,-50.0,1206.0,813.0],"world_size_mm":[22.0,32.0,24.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_CassetteFixedCleatL1. Fused/stepped assembly needs explicit flatpack decomposition or CNC thickness plan; no new wood designed.
- **P077** — Nominal dimensions: {"world_bounds_mm":[650.0,1174.0,629.0,672.0,1206.0,653.0],"world_size_mm":[22.0,32.0,24.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_CassetteFixedCleatR0. Fused/stepped assembly needs explicit flatpack decomposition or CNC thickness plan; no new wood designed.
- **P078** — Nominal dimensions: {"world_bounds_mm":[650.0,1174.0,789.0,672.0,1206.0,813.0],"world_size_mm":[22.0,32.0,24.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; BB_CassetteFixedCleatR1. Fused/stepped assembly needs explicit flatpack decomposition or CNC thickness plan; no new wood designed.

### Stage 12 — Matrix and front interfaces

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| P039 | Matrix seat — MX_WoodSeatL | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P040 | Matrix seat — MX_WoodSeatR | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |
| P041 | Removable matrix carrier — MatrixCarrier | 1 | MODULAR_SECONDARY | DESIGN_GEOMETRY_ONLY / REQUIRED_FLATPACK_HARDWARE |

- **P039** — Nominal dimensions: {"world_bounds_mm":[35.99999999999999,1075.0,540.0,54.00000000000001,1190.0,578.9],"world_size_mm":[18.000000000000014,115.0,38.89999999999998],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; MX_WoodSeatL. Load path or positive retention: premium class cannot be automatically downgraded.
- **P040** — Nominal dimensions: {"world_bounds_mm":[545.9999999999999,1075.0,540.0,564.0000000000001,1190.0,578.9],"world_size_mm":[18.000000000000227,115.0,38.89999999999998],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; MX_WoodSeatR. Load path or positive retention: premium class cannot be automatically downgraded.
- **P041** — Nominal dimensions: {"world_bounds_mm":[29.999999999999996,1033.6144756704912,535.4516895886093,570.0,1125.125,586.6345997465683],"world_size_mm":[540.0,91.51052432950883,51.182910157958986],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; MatrixCarrier. Secondary substitution only after nesting trigger and quality/load/joint qualification.

### Stage 13 — Later electronics and adapters

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| P033 | Replaceable shaker carrier — SSF_BST_Carrier | 1 | STRUCTURAL_PREMIUM | DESIGN_GEOMETRY_ONLY / USER_ADAPTER_HARDWARE |

- **P033** — Nominal dimensions: {"world_bounds_mm":[210.0,170.0,36.0,390.0,350.0,48.0],"world_size_mm":[180.0,180.0,12.0],"note":"Installed AABB, NOT nesting or stock dimensions; inclined/stepped parts require local profile extraction."}. Physical measurement: YES. Source: exports/generated/backbox-lock-integration-v32/play.FCStd; SSF_BST_Carrier. Load path or positive retention: premium class cannot be automatically downgraded.

## BOM 2 — Required mechanical hardware

### Stage 01 — Cabinet shell and legs

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| B13 | Metal threaded leg backing plate | 4 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F06 | Cabinet shell/floor/cleat joint fasteners | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F37 | Matched pinball leg bolts | 8 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F38 | Leg backing plate retention screws | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| G01 | Plywood joint adhesive | TBD | wood adhesive; specification/coverage TBD | PURCHASE_BEFORE_ASSEMBLY / REQUIRED_FLATPACK_HARDWARE |
| H18 | Real pinball leg | 4 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| H19 | Leg leveler and jam-nut assembly | 4 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |

- **B13** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. 4 existing envelopes; measured matched bolts mandatory.58 mm candidate differs from57.15 mm WPC reference; HOLD.
- **F06** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT SIDE/FRONT/REAR/FLOOR/FLOOR_CLEAT interfaces. Captured joinery exists; permanent mechanical reinforcement schedule is not specified. Quantity and family HOLD; not replaced by guessed dense screws.
- **F37** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Thread, shoulder, length and head unselected. No M10 substitution into imperial backing thread.
- **F38** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Quantity/pitch supplied by purchased backing; not primary leg bolts.
- **G01** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. At least lock parking laminations require glue; volume depends on final joint schedule. Not a structural screw substitute.
- **H18** — Nominal dimensions: TBD. Physical measurement: YES. Source: config/panel_closure_v32.json#legs. Reference A-19514,28.5 in; actual revision required. Not modeled as fabricated wood/steel substitute.
- **H19** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Purchased matched thread; height/foot load unqualified.

### Stage 02 — Shelf supports and crossmembers

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| B02 | Commodity support angle, 40 ×40 ×50 ×3 reserve | 6 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F03 | Shelf top-release M5 screw | 12 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F04 | Fixed shelf-support wood screw | 12 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F05 | Crossmember guide attachment screws | 24 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F07 | PCBase flush M5 floor anchors | 4 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F52 | M5-family crossmember support-angle bolts | 12 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| I01 | M5 shelf captive insert | 12 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| I02 | PCBase M5 retaining nuts | 4 | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / REQUIRED_FLATPACK_HARDWARE |
| I14 | Crossmember angle captive-thread/retention set | 12 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| W01 | M5 load-spreading washer, current Ø12 ×1 | 12 | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / REQUIRED_FLATPACK_HARDWARE |
| W02 | Ø4 clearance washer, Ø9 ×1 | 12 | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / REQUIRED_FLATPACK_HARDWARE |
| W03 | PCBase M5 underside backing washers | 4 | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / REQUIRED_FLATPACK_HARDWARE |

- **B02** — Nominal dimensions: TBD. Physical measurement: YES. Source: exports/generated/cabinet-v32/build_v32.py. 6 fittings. Rated commodity part and attachment pattern unselected; do not fabricate custom brackets from envelope.
- **F03** — Nominal dimensions: {"diameter_mm":5,"length_mm":25,"head_diameter_mm":9,"head_height_mm":4,"head":"pan"}. Physical measurement: YES. Source: config/simple_shelves_v32.json.
- **F04** — Nominal dimensions: {"diameter_mm":4,"length_mm":55,"head_diameter_mm":8,"head_height_mm":3,"head":"pan"}. Physical measurement: YES. Source: config/support_leg_machining_v32.json#anchor.
- **F05** — Nominal dimensions: TBD. Physical measurement: YES. Source: exports/generated/cabinet-v32/build_v32.py: guide anchoring loop. 4 existing anchor holes per guide ×6; shank/head/length and wall thread retention unresolved.
- **F07** — Nominal dimensions: {"diameter_mm":5,"length_mm":null,"head":"countersunk","clearance_mm":5.5}. Physical measurement: YES. Source: config/consolidated_audio_v32.json#pc_base. 4 holes exist; bolt length/nut/washer stack not modeled. 36 mm combined boards. Future chassis mounting is separate.
- **F52** — Nominal dimensions: {"diameter_mm":5,"length_mm":null}. Physical measurement: YES. Source: exports/generated/cabinet-v32/build_v32.py: support-angle loop. 2 installed bolts per angle ×6; three height choices are NOT6 bolts per angle.
- **I01** — Nominal dimensions: {"thread":"M5","outer_diameter_mm":8,"length_mm":10}. Physical measurement: YES. Source: config/simple_shelves_v32.json. Bore Ø8.5 is an existing design candidate, not a generic M5-insert standard.
- **I02** — Nominal dimensions: {"thread":"M5"}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Captive or locking form and length stack pending; no chosen torque.
- **I14** — Nominal dimensions: {"thread":"M5"}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Guide12 mm remaining web; purchased thread/washer strategy unselected.
- **W01** — Nominal dimensions: {"inner_diameter_mm":5.5,"outer_diameter_mm":12,"thickness_mm":1}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction.
- **W02** — Nominal dimensions: {"inner_diameter_mm":4.5,"outer_diameter_mm":9,"thickness_mm":1}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Same nominal family as rear M4 fan washers; additional optional quantities listed separately.
- **W03** — Nominal dimensions: {"thread":"M5","outer_diameter_mm":null}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction.

### Stage 03 — Wooden playfield pivot

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| B01 | Commercial saddle strap for Ø32 wooden dowel | 4 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F01 | Cradle support wood screw | 6 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F02 | Saddle-strap wood screw | 8 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| H01 | Wooden pivot dowel | 1 | STRUCTURAL_PREMIUM | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |

- **B01** — Nominal dimensions: TBD. Physical measurement: YES. Source: tools/wood_dowel_pivot_v32_entry.py. 4 straps, 2 screws each. No bearing, metal shaft, custom journal or custom plate.
- **F01** — Nominal dimensions: {"diameter_mm":4.5,"length_mm":30,"head_diameter_mm":9,"head":"countersunk"}. Physical measurement: YES. Source: config/wood_dowel_pivot_v32.json#fixing. 6 unchanged coordinates. Torx candidate; exact bit/hardness and pilots await purchase.
- **F02** — Nominal dimensions: {"diameter_mm":3.4,"length_mm":12,"head_diameter_mm":6.4,"head_height_mm":2,"head":"pan"}. Physical measurement: YES. Source: tools/wood_dowel_pivot_v32_entry.py: saddle strap loop. CURRENT cylinder is Ø3.4 ×12, not a selected standard screw. Candidate Ø3.5 ×12 requires strap/pilot/engagement check; NO substitution made.
- **H01** — Nominal dimensions: {"diameter_mm":32,"length_mm":560}. Physical measurement: YES. Source: config/wood_dowel_pivot_v32.json.

### Stage 04 — Main rear service door

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| B03 | Main rear lock keeper | 1 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F08 | M4 ×20 handle screw | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F09 | Main rear hinge fixing screws | 8 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F53 | Main rear keeper fixing screws | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| H02 | Main rear door hinge assembly | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| H03 | Main rear keyed cam-lock assembly | 1 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| H04 | Main rear door handle | 1 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| W02-use4 | Ø4 clearance washer, Ø9 ×1 | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / REQUIRED_FLATPACK_HARDWARE |

- **B03** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Ordinary flat strike; selection and fixing require measurement.
- **F08** — Nominal dimensions: {"diameter_mm":4,"length_mm":20,"head":"pan","head_diameter_mm":8,"head_height_mm":3}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction.
- **F09** — Nominal dimensions: TBD. Physical measurement: YES. Source: tools/rear_door_v32_entry.py: hinge leaf loop. 2 holes per leaf ×2 leaves ×2 hinges; length/diameter and12 mm door engagement unselected.
- **F53** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Keeper attachment count and stack unresolved.
- **H02** — Nominal dimensions: TBD. Physical measurement: YES. Source: config/rear_door_v32.json. Two short hinges, not the backbox piano-hinge family. Each consists of two leaves and one pin.
- **H03** — Nominal dimensions: TBD. Physical measurement: YES. Source: config/rear_door_v32.json.
- **H04** — Nominal dimensions: TBD. Physical measurement: YES. Source: config/rear_hardware_v32.json#handle.
- **W02-use4** — Nominal dimensions: {"inner_diameter_mm":4.5,"outer_diameter_mm":9,"thickness_mm":1}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Main rear handle washers have exact same CURRENT B-rep radii4.5/2.25 and1 mm thickness as W02.

### Stage 05 — Main ventilation and filter interfaces

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| B05 | Floor intake lower guard | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F12 | M4 ×16 floor-filter screw | 8 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F13 | Short floor lower-guard attachment screws | 8 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| G03 | Floor intake replaceable filter media | 2 | serviceable mesh/filter; permeability TBD | PURCHASE_BEFORE_ASSEMBLY / REQUIRED_FLATPACK_HARDWARE |
| I04 | M4 blind floor-filter insert | 8 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |

- **B05** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Retained for passive intake protection even without fan. Current lower guard is a rotated packaging box, not a solid air-blocking plate.
- **F12** — Nominal dimensions: {"diameter_mm":4,"length_mm":16,"head":"pan","head_diameter_mm":8,"head_height_mm":3}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction.
- **F13** — Nominal dimensions: TBD. Physical measurement: YES. Source: config/notch_floor_fans_v32.json#fans.lower_guard_fixing. 4 per guard on rotated105 mm pitch; diameter/head/length unselected; 8 mm frame prevents using long screws blindly.
- **G03** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction.
- **I04** — Nominal dimensions: {"thread":"M4","outer_diameter_mm":6,"length_mm":8}. Physical measurement: YES. Source: config/notch_floor_fans_v32.json. 10 mm remaining floor skin in nominal 18 mm stock; purchased insert must fit existing reserve.

### Stage 06 — Backbox shell and WPC interface

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| B16 | WPC floor backing plate | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F14 | WPC 4322-01139-12B pivot bolt | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F15 | WPC floor attachment fasteners | 6 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F16 | Backbox shell/frame/rail joint screws | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F54 | Backbox side-to-floor joint screws | 6 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| H08 | WPC 01-9011-L left | 1 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| H09 | WPC 01-9011-R right | 1 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| H10 | WPC 02-4352 bushing | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| W06 | WPC pivot/floor washer and nut stack | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |

- **B16** — Nominal dimensions: TBD. Physical measurement: YES. Source: studies/wpc-fold-v32/README.md. Documented backing relationship; purchased plate dimensions/holes/material unmeasured, not a custom fabricated design.
- **F14** — Nominal dimensions: TBD. Physical measurement: YES. Source: config/wpc_kinematics_v32.json; studies/wpc-fold-v32/README.md. PHYSICAL MEASUREMENT HOLD. No metric substitution of a mating imperial thread. No CNC drilling released.
- **F15** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. 3 per arm; measured hole/thread/head/length and access needed. Rare cassette removal allowed for hinge maintenance only.
- **F16** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Shell, rear frame, hinge cleats, monitor rail cleats and cassette cleats require joint schedule. Counts/pilots not implied by envelopes.
- **F54** — Nominal dimensions: {"diameter_mm_max_planning":4,"floor_thread_reach_mm":20}. Physical measurement: YES. Source: config/backbox_structure_review_v32.json#joint_planning. 3 per side provisional planning; glued captured joint. Separate from remaining shell joints F16.
- **H08** — Nominal dimensions: TBD. Physical measurement: YES. Source: config/wpc_kinematics_v32.json; studies/wpc-fold-v32/README.md. PHYSICAL MEASUREMENT HOLD. No metric substitution of a mating imperial thread. No CNC drilling released.
- **H09** — Nominal dimensions: TBD. Physical measurement: YES. Source: config/wpc_kinematics_v32.json; studies/wpc-fold-v32/README.md. PHYSICAL MEASUREMENT HOLD. No metric substitution of a mating imperial thread. No CNC drilling released.
- **H10** — Nominal dimensions: TBD. Physical measurement: YES. Source: config/wpc_kinematics_v32.json; studies/wpc-fold-v32/README.md. PHYSICAL MEASUREMENT HOLD. No metric substitution of a mating imperial thread. No CNC drilling released.
- **W06** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Unresolved content and count; do not add metric nuts to unknown WPC threads.

### Stage 07 — Upright locks and parking

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| B07 | Positive tether slack keeper | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / REQUIRED_FLATPACK_HARDWARE |
| B08 | Parking-block tether anchor | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F17 | Parking-pad countersunk wood screw | 4 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| H11 | M8 ×40 captive upright-lock hand knob | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| H12 | Mechanical knob tether, 200 mm | 2 | flexible loss-protection tether | PURCHASE_BEFORE_ASSEMBLY / REQUIRED_FLATPACK_HARDWARE |
| H13 | Rotating loss-protection ring | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / REQUIRED_FLATPACK_HARDWARE |
| I05 | M8 metal-backed shelf captive receiver | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| I06 | M8 metal parking insert | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| W07 | Captive upright-lock load washer | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| W08 | Captive washer retention ring | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / REQUIRED_FLATPACK_HARDWARE |

- **B07** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Reusable mechanical cord keeper. Fold requires slack secured around knob.
- **B08** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Ordinary eye/clamp with positive mounting; selected stack and screws unresolved.
- **F17** — Nominal dimensions: {"diameter_mm":4,"length_mm":48,"head_diameter_mm":9,"head":"countersunk"}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. 48 mm modeled envelope, not a chosen stock SKU; two screws per laminated block.
- **H11** — Nominal dimensions: {"diameter_mm":8,"length_mm":40,"head_diameter_mm":40,"head_height_mm":26}. Physical measurement: YES. Source: config/backbox_lock_integration_v32.json. L130/R470,Y1260. Architecture family only; rotating loss-protection ring purchased with compatible shaft.
- **H12** — Nominal dimensions: {"length_mm":200}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Not electrical wiring. Installed shape includes stored corridor, not exact strand geometry.
- **H13** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. May be supplied with H11; included flag must suppress duplicate purchase.
- **I05** — Nominal dimensions: {"thread":"M8","outer_diameter_mm":12,"length_mm":12,"backing_diameter_mm":32,"backing_thickness_mm":3}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Backing is included in receiver assembly; do not buy separate duplicate backing. Anti-rotation/retention unresolved.
- **I06** — Nominal dimensions: {"thread":"M8","outer_diameter_mm":12,"length_mm":12}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. X185/X415,Y1268; parking only, not structural backbox clamping.
- **W07** — Nominal dimensions: {"inner_diameter_mm":9,"outer_diameter_mm":32,"thickness_mm":3}. Physical measurement: YES. Source: config/backbox_lock_integration_v32.json.
- **W08** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Compatible ordinary retaining hardware required; groove/stack not frozen. Loose washers not allowed.

### Stage 08 — Twin backbox doors

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| F18 | Backbox piano-hinge fixing screws | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F19 | Backbox latch/astragal fasteners | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| G04 | Backbox perimeter door gasket | 2 | replaceable closed-cell foam / EPDM | PURCHASE_BEFORE_ASSEMBLY / REQUIRED_FLATPACK_HARDWARE |
| G05 | Backbox center meeting-line gasket | 1 | replaceable closed-cell foam / EPDM | PURCHASE_BEFORE_ASSEMBLY / REQUIRED_FLATPACK_HARDWARE |
| H14 | 628 mm continuous backbox door hinge | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| H15 | Backbox active-door keyed cam lock | 1 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| H16 | Backbox passive-leaf retaining bolt | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |

- **F18** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Quantity from purchased hole pitch on both leaves of both hinges; maximum engagement limited by12 mm door.
- **F19** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Count/length pending hardware and joint schedule; no permanent center mullion.
- **G04** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. 2 cut sets; supply length includes waste only after supplier selection. 2 mm compressed reserve.
- **G05** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction.
- **H14** — Nominal dimensions: TBD. Physical measurement: YES. Source: config/backbox_service_v32.json#rear. 628 mm envelope; leaf widths23/20,1.5 thick,knuckleØ5 provisional. Final hole pitch not frozen.
- **H15** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. One purchased mechanism incl tongue; does not substitute main rear door lock without fit review.
- **H16** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Upper and lower bolt. Purchased strike/attachment stack included but unmeasured.

### Stage 09 — Backbox blanks, filters and optional fans

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| F21 | M4 backbox blank-station fixing | 8 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F22 | Backbox intake frame/baffle/filter fixings | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| G07 | Backbox low-intake filter/mesh | 2 | serviceable insect mesh/filter | PURCHASE_BEFORE_ASSEMBLY / REQUIRED_FLATPACK_HARDWARE |
| I07 | M4 station captive nut/insert | 8 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| W02-use3 | Ø4 clearance washer, Ø9 ×1 | 16 | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / REQUIRED_FLATPACK_HARDWARE |

- **F21** — Nominal dimensions: {"diameter_mm":4,"length_mm":null,"head":"pan"}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. 4 per existing blank; same105 mm pitch as fan. Basic kit includes blanks; fan bolts replace these, not additive at same station.
- **F22** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. 2 serviceable intakes; count/length and mesh clamping not defined by current assembly.
- **G07** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction.
- **I07** — Nominal dimensions: {"thread":"M4"}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Captive form must preserve interchangeable fan/blank and12 mm leaf. No insert bore invented.
- **W02-use3** — Nominal dimensions: {"inner_diameter_mm":4.5,"outer_diameter_mm":9,"thickness_mm":1}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Planning2 per backbox station for fan OR blank, counted once; bought with basic blank station. Washer stack HOLD.

### Stage 10 — Display carrier and glass retention

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| F24 | Backglass top-retainer M6-family fastener | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F25 | Monitor depth-position M6 through bolt | 4 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F26 | Monitor alignment M6 clamp bolt | 4 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F27 | Monitor M6 adjustable lower stop | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F28 | Monitor ladder/stop/cleat wood joints | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| G08 | Backglass side U-liners | 2 | felt/EPDM/U liner | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| G09 | Backglass lower and top pads | 2 | felt/EPDM | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| I08 | Top-retainer captive metal thread | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| I09 | Monitor M6 positive-retention nuts | 8 | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / REQUIRED_FLATPACK_HARDWARE |
| I10 | M6 stop captive thread | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| I11 | M6 stop locknut | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / REQUIRED_FLATPACK_HARDWARE |
| W09 | Monitor M6 large clamping washer | 16 | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / REQUIRED_FLATPACK_HARDWARE |

- **F24** — Nominal dimensions: {"diameter_mm":6,"length_mm":30,"head":"unselected"}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Ø6×30 reserve only, head/captive thread not selected. No unretained glass during fold.
- **F25** — Nominal dimensions: {"diameter_mm":6,"length_mm":72,"head":"unselected"}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. 72 mm is corridor/shank envelope, not stock SKU length. Rail/shoe retention independent of display.
- **F26** — Nominal dimensions: {"diameter_mm":6,"length_mm":null,"head":"unselected"}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. 4 clamps; existing Ø18×36 objects are washer/tool stack reserves, NOT Ø18 bolts.
- **F27** — Nominal dimensions: {"diameter_mm":6,"length_mm":46,"head":"unselected"}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. 46 mm reference cylinder, not final screw length; positive stop with locknut.
- **F28** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Carrier shoes, stop blocks, contact pads and fixed rail cleats need attachment schedule; quantity unresolved.
- **G08** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction.  Selected component must qualify the existing station/channel before CNC; optional classification does not waive the hold if fitted.
- **G09** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction.  Selected component must qualify the existing station/channel before CNC; optional classification does not waive the hold if fitted.
- **I08** — Nominal dimensions: {"thread":"M6"}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Repeated removal; purchased retention/stock engagement unresolved.
- **I09** — Nominal dimensions: {"thread":"M6"}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction.
- **I10** — Nominal dimensions: {"thread":"M6"}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction.
- **I11** — Nominal dimensions: {"thread":"M6"}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction.
- **W09** — Nominal dimensions: {"thread":"M6","outer_diameter_mm":18,"thickness_mm":null}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Planning2 per8 through clamps/depth bolts; final bolt head may integrate washer. Not a selected DIN dimension.

### Stage 11 — DMD/speaker cassette

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| F30 | Lower cassette M4 positive attachment | 4 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F31 | Replaceable baffle/bezel and DMD-adapter fixings | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| I12 | Cassette M4 captive receiver | 4 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| W10 | Cassette M4 load washer | 4 | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / REQUIRED_FLATPACK_HARDWARE |

- **F30** — Nominal dimensions: {"diameter_mm":4,"length_mm":65,"head":"unselected"}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. 4 attachments,65 mm reference envelope; selected bolt/washer/thread stack must fit. No cassette geometry change.
- **F31** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Retention of blank modules required even without electronics. Counts/lengths unresolved; cannot assume four cassette bolts also secure inserts.
- **I12** — Nominal dimensions: {"thread":"M4"}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction.
- **W10** — Nominal dimensions: {"thread":"M4"}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction.

### Stage 12 — Matrix and front interfaces

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| B12 | Playfield glass side channel | 2 | replaceable channel; material/SKU TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F34 | M4 ×20 matrix thumb screw | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F35 | 4 ×50 countersunk matrix-support screw | 4 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F36 | Playfield channel/lockdown fixing hardware | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| F39 | Front-door frame fixing set | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| G12 | Playfield glass channel liner/seal | 2 | replaceable soft liner | PURCHASE_BEFORE_ASSEMBLY / REQUIRED_FLATPACK_HARDWARE |
| H20 | 600 mm body lockdown bar | 1 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| H21 | WPC-compatible lockdown receiver | 1 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| H22 | Front coin-door/frame/keyed access assembly | 1 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |
| I13 | M4 matrix support insert | 2 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / REQUIRED_FLATPACK_HARDWARE |

- **B12** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Separate from backglass liners; do not infer stock channel from envelope.
- **F34** — Nominal dimensions: {"diameter_mm":4,"length_mm":20,"head_diameter_mm":12,"head_height_mm":4}. Physical measurement: YES. Source: config/matrix_cassette_v32.json.
- **F35** — Nominal dimensions: {"diameter_mm":4,"length_mm":50,"head":"countersunk","head_diameter_mm":8}. Physical measurement: YES. Source: config/matrix_cassette_v32.json.
- **F36** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Permanent holes depend on channel and actual receiver; count unresolved.
- **F39** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Count/thread from selected front door; no historical mounting count assumed.
- **G12** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. 2 side runs; lengths and front/rear pads from selected channel/bar.
- **H20** — Nominal dimensions: TBD. Physical measurement: YES. Source: config/panel_closure_v32.json#lockdown. Existing accepted custom-width outsourced bar strategy. V33 adds no custom metal; no fabrication drawing generated.
- **H21** — Nominal dimensions: TBD. Physical measurement: YES. Source: config/panel_closure_v32.json#lockdown. A-16673-1 / A-9174-4 references, not two purchases. Pattern/lever service/width to measure.
- **H22** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Closure/interface required; coin mechanisms/electrics optional. Front reserve is a study, not selected purchased door.
- **I13** — Nominal dimensions: TBD. Physical measurement: YES. Source: tools/matrix_cassette_v32_entry.py.

## BOM 3 — Optional mechanical accessories

### Stage 01 — Cabinet shell and legs

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| H26 | Optional mobility skate set | 1 | steel; finish/grade TBD | OPTIONAL / OPTIONAL_FLATPACK_HARDWARE |

- **H26** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. External removable PinSkates-style only; no integrated wheels.

### Stage 04 — Main rear service door

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| G02 | Main rear door contact felt | TBD | adhesive furniture felt | OPTIONAL / OPTIONAL_FLATPACK_HARDWARE |
| H05 | Optional main rear door limiter set | 1 | steel; finish/grade TBD | OPTIONAL / OPTIONAL_FLATPACK_HARDWARE |
| H06 | Optional main rear slide bolt | 1 | steel; finish/grade TBD | OPTIONAL / OPTIONAL_FLATPACK_HARDWARE |

- **G02** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Owner adds at actual contact; not a restraint. Quantity/size determined at assembly.
- **H05** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Accessory only; no new mechanism designed.
- **H06** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction.

### Stage 05 — Main ventilation and filter interfaces

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| B04 | 120 mm main rear fan finger guard | 4 | steel; finish/grade TBD | OPTIONAL / OPTIONAL_FLATPACK_HARDWARE |
| B06 | Floor fan upper finger guard | 2 | steel; finish/grade TBD | OPTIONAL / OPTIONAL_FLATPACK_HARDWARE |
| F10 | M4 ×55 main rear fan bolt | 8 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / OPTIONAL_FLATPACK_HARDWARE |
| F11 | M4 ×50 floor fan bolt | 8 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / OPTIONAL_FLATPACK_HARDWARE |
| H07 | 120 mm main/floor optional fan | 4 | fan assembly; no electrical interface selected | PURCHASE_BEFORE_CNC / OPTIONAL_FLATPACK_HARDWARE |
| I03 | M4 fan nut | 16 | steel; finish/grade TBD | OPTIONAL / OPTIONAL_FLATPACK_HARDWARE |
| W02-use1 | Ø4 clearance washer, Ø9 ×1 | 16 | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / OPTIONAL_FLATPACK_HARDWARE |
| W02-use2 | Ø4 clearance washer, Ø9 ×1 | 16 | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / OPTIONAL_FLATPACK_HARDWARE |

- **B04** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. 4 guards; purchased finger protection/free area not certified.
- **B06** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction.
- **F10** — Nominal dimensions: {"diameter_mm":4,"length_mm":55,"head":"pan","head_diameter_mm":8,"head_height_mm":3}. Physical measurement: YES. Source: config/fixed_rear_services_v32.json.  Selected component must qualify the existing station/channel before CNC; optional classification does not waive the hold if fitted.
- **F11** — Nominal dimensions: {"diameter_mm":4,"length_mm":50,"head":"pan","head_diameter_mm":8,"head_height_mm":3}. Physical measurement: YES. Source: config/notch_floor_fans_v32.json.  Selected component must qualify the existing station/channel before CNC; optional classification does not waive the hold if fitted.
- **H07** — Nominal dimensions: {"width_mm":120,"height_mm":120,"depth_mm":25,"pitch_mm":105}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. 4 optional fans. Passive floor filtration remains possible; thermal qualification is separate. Selected component must qualify the existing station/channel before CNC; optional classification does not waive the hold if fitted.
- **I03** — Nominal dimensions: {"thread":"M4","outer_diameter_mm":8,"length_mm":3.2}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction.
- **W02-use1** — Nominal dimensions: {"inner_diameter_mm":4.5,"outer_diameter_mm":9,"thickness_mm":1}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Rear fan stack only; not mandatory when fans omitted.
- **W02-use2** — Nominal dimensions: {"inner_diameter_mm":4.5,"outer_diameter_mm":9,"thickness_mm":1}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Floor fan washer requirement in config, omitted from current CAD;2 per bolt. Stack fit HOLD.

### Stage 09 — Backbox blanks, filters and optional fans

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| B09 | Backbox fan finger guard | 2 | steel; finish/grade TBD | OPTIONAL / OPTIONAL_FLATPACK_HARDWARE |
| B10 | Flexible fan-cable clamp/strain relief | 4 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / OPTIONAL_FLATPACK_HARDWARE |
| B11 | Optional downward fan dust hood | 2 | steel; finish/grade TBD | OPTIONAL / OPTIONAL_FLATPACK_HARDWARE |
| F20 | M4 backbox fan-station bolt, length pending | 8 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / OPTIONAL_FLATPACK_HARDWARE |
| F23 | Fan-loop clamp screws | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / OPTIONAL_FLATPACK_HARDWARE |
| F55 | Optional dust-hood service screws | 4 | steel; finish/grade TBD | OPTIONAL / OPTIONAL_FLATPACK_HARDWARE |
| G06 | Backbox fan dust mesh/filter | 2 | mesh/filter | OPTIONAL / OPTIONAL_FLATPACK_HARDWARE |
| H17 | Optional 120 mm backbox door fan | 2 | fan assembly | PURCHASE_BEFORE_CNC / OPTIONAL_FLATPACK_HARDWARE |

- **B09** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction.
- **B10** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Two fixed and two door attachment points; only two door reserves modeled. Connector choice remains builder-defined.
- **B11** — Nominal dimensions: {"width_mm":140,"depth_mm":19,"height_mm":140}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Owner-accepted accessory reserve in service source; not installed CURRENT geometry.
- **F20** — Nominal dimensions: {"diameter_mm":4,"length_mm":null,"head":"pan"}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. 12 mm door +25 mm fan +accessories; do not copy main55 mm bolt automatically. Selected component must qualify the existing station/channel before CNC; optional classification does not waive the hold if fitted.
- **F23** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Clamp SKU controls number and screw length; electrical connectors excluded.
- **F55** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Two per optional hood in service concept; hole and screw geometry remain unselected.
- **G06** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Exhaust pressure loss unresolved; no zero-restriction assumption.
- **H17** — Nominal dimensions: {"width_mm":120,"height_mm":120,"depth_mm":25,"pitch_mm":105}. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Fan state replaces blank; no manufacturer/connector required. Selected component must qualify the existing station/channel before CNC; optional classification does not waive the hold if fitted.

### Stage 12 — Matrix and front interfaces

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| F40 | Button bracket mounting fasteners | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / OPTIONAL_FLATPACK_HARDWARE |
| H23 | Coin mechanism/tray mounting set | 1 | steel; finish/grade TBD | OPTIONAL / OPTIONAL_FLATPACK_HARDWARE |
| H24 | Optional pinball button mechanical set | 8 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / OPTIONAL_FLATPACK_HARDWARE |

- **F40** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. 4 side brackets, exact number of screws unselected.
- **H23** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Optional1 set of2 mechanisms/tray/supports; no duplicate part purchase for CAD components.
- **H24** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. 4 side +4 front bodies, side nuts/brackets included. Hole shapes remain existing references; builder may choose later buttons.

### Stage 13 — Later electronics and adapters

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| H25 | Optional removable toy shelf | 1 | plywood accessory; not in current installed CAD | OPTIONAL / OPTIONAL_FLATPACK_HARDWARE |

- **H25** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Study only; no mandatory toy shelf. No unvalidated production cut part generated.

## BOM 4 — Future electronics / references

### Stage 13 — Later electronics and adapters

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| B14 | Protected mains inlet enclosure reference | 1 | insulating/protective enclosure | PURCHASE_BEFORE_CNC / FUTURE_ELECTRONICS_HARDWARE |
| E01 | Playfield display | 1 | electronic reference; model selected later | PURCHASE_BEFORE_ASSEMBLY / FUTURE_ELECTRONICS_HARDWARE |
| E02 | Backglass display | 1 | electronic reference; model selected later | PURCHASE_BEFORE_ASSEMBLY / FUTURE_ELECTRONICS_HARDWARE |
| E03 | DMD display | 1 | electronic reference; model selected later | PURCHASE_BEFORE_ASSEMBLY / FUTURE_ELECTRONICS_HARDWARE |
| E04 | Backbox speakers | 2 | electronic reference; model selected later | PURCHASE_BEFORE_ASSEMBLY / FUTURE_ELECTRONICS_HARDWARE |
| E05 | PC open chassis and computer | 1 | electronic reference; model selected later | PURCHASE_BEFORE_ASSEMBLY / FUTURE_ELECTRONICS_HARDWARE |
| E06 | SSF exciter | 4 | electronic reference; model selected later | PURCHASE_BEFORE_ASSEMBLY / FUTURE_ELECTRONICS_HARDWARE |
| E07 | Bass shaker | 1 | electronic reference; model selected later | PURCHASE_BEFORE_ASSEMBLY / FUTURE_ELECTRONICS_HARDWARE |
| E08 | Subwoofer | 1 | electronic reference; model selected later | PURCHASE_BEFORE_ASSEMBLY / FUTURE_ELECTRONICS_HARDWARE |
| E09 | Amplifier | 1 | electronic reference; model selected later | PURCHASE_BEFORE_ASSEMBLY / FUTURE_ELECTRONICS_HARDWARE |
| E10 | Protected power supply | 1 | electronic reference; model selected later | PURCHASE_BEFORE_ASSEMBLY / FUTURE_ELECTRONICS_HARDWARE |
| E11 | USB sound interface | 1 | electronic reference; model selected later | PURCHASE_BEFORE_ASSEMBLY / FUTURE_ELECTRONICS_HARDWARE |
| E12 | Matrix LED panel | 6 | electronic reference; model selected later | PURCHASE_BEFORE_ASSEMBLY / FUTURE_ELECTRONICS_HARDWARE |
| E13 | Button switches/contacts | 6 | electronic reference; model selected later | PURCHASE_BEFORE_ASSEMBLY / FUTURE_ELECTRONICS_HARDWARE |
| E14 | Optional toys/controllers/LED/relays | TBD | electronic reference; model selected later | PURCHASE_BEFORE_ASSEMBLY / FUTURE_ELECTRONICS_HARDWARE |
| R01 | Cable / connector routing reserves | 0 | nonphysical clearance | PURCHASE_BEFORE_ASSEMBLY / REFERENCE_ONLY_NOT_FROZEN |
| R02 | Button service approach reserves | 0 | nonphysical clearance | PURCHASE_BEFORE_ASSEMBLY / REFERENCE_ONLY_NOT_FROZEN |
| R03 | Future toy mounting volumes | 0 | nonphysical clearance | PURCHASE_BEFORE_ASSEMBLY / REFERENCE_ONLY_NOT_FROZEN |
| R04 | Unpopulated equipment/payload/plunger reserves | 0 | nonphysical clearance | PURCHASE_BEFORE_ASSEMBLY / REFERENCE_ONLY_NOT_FROZEN |

- **B14** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Safety-critical electrical interface, not general low-voltage hardware. No exposed terminals; no wiring design in V33.
- **E01** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Not in mandatory flatpack; dimensions from CURRENT occupied envelope only.
- **E02** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Not in mandatory flatpack; dimensions from CURRENT occupied envelope only.
- **E03** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Not in mandatory flatpack; dimensions from CURRENT occupied envelope only.
- **E04** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Not in mandatory flatpack; dimensions from CURRENT occupied envelope only.
- **E05** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Not in mandatory flatpack; dimensions from CURRENT occupied envelope only.
- **E06** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Not in mandatory flatpack; dimensions from CURRENT occupied envelope only.
- **E07** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Not in mandatory flatpack; dimensions from CURRENT occupied envelope only.
- **E08** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Not in mandatory flatpack; dimensions from CURRENT occupied envelope only.
- **E09** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Not in mandatory flatpack; dimensions from CURRENT occupied envelope only.
- **E10** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Not in mandatory flatpack; dimensions from CURRENT occupied envelope only.
- **E11** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Not in mandatory flatpack; dimensions from CURRENT occupied envelope only.
- **E12** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Not in mandatory flatpack; dimensions from CURRENT occupied envelope only.
- **E13** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Not in mandatory flatpack; dimensions from CURRENT occupied envelope only.
- **E14** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Not in mandatory flatpack; dimensions from CURRENT occupied envelope only.
- **R01** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. NOT A PURCHASE. CAD solids are clearance envelopes; retain in exploded metadata as hidden guides.
- **R02** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. NOT A PURCHASE. CAD solids are clearance envelopes; retain in exploded metadata as hidden guides.
- **R03** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. NOT A PURCHASE. CAD solids are clearance envelopes; retain in exploded metadata as hidden guides.
- **R04** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. NOT A PURCHASE. CAD solids are clearance envelopes; retain in exploded metadata as hidden guides.

## BOM 5 — User-specific adapters

### Stage 10 — Display carrier and glass retention

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| G10 | User-supplied backbox tempered glass | 1 | tempered glass | PURCHASE_BEFORE_CNC / USER_ADAPTER_HARDWARE |

- **G10** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. 752×465×4 current reserve; supplier confirms3–4 mm, edges and channel/liner fit before order.

### Stage 12 — Matrix and front interfaces

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| G11 | User-supplied playfield glass | 1 | tempered glass | PURCHASE_BEFORE_CNC / USER_ADAPTER_HARDWARE |

- **G11** — Nominal dimensions: TBD. Physical measurement: YES. Source: config/panel_closure_v32.json#glass_study. 575×1100×5 study, not glass order; front/rear capture remains lockdown-dependent.

### Stage 13 — Later electronics and adapters

| ID | Description | Qty | Material | Status / class |
| --- | --- | ---: | --- | --- |
| B15 | Playfield replaceable VESA attachment | 1 | adapter interface; exact construction TBD | PURCHASE_BEFORE_CNC / USER_ADAPTER_HARDWARE |
| F29 | Display VESA mounting screws and spacers | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / USER_ADAPTER_HARDWARE |
| F32 | Selected speaker mounting screws | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / USER_ADAPTER_HARDWARE |
| F33 | Selected DMD mounting hardware | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / USER_ADAPTER_HARDWARE |
| F42 | Subwoofer floor mounting bolts | 8 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / USER_ADAPTER_HARDWARE |
| F43 | Bass-shaker carrier floor anchors | 4 | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / USER_ADAPTER_HARDWARE |
| F44 | Bass-shaker to carrier fasteners | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / USER_ADAPTER_HARDWARE |
| F45 | Exciter IMS mounting fasteners | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / USER_ADAPTER_HARDWARE |
| F46 | PC chassis/base and component restraints | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / USER_ADAPTER_HARDWARE |
| F47 | Electronics board shelf standoffs and screws | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / USER_ADAPTER_HARDWARE |
| F48 | Matrix panel mounting fasteners | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / USER_ADAPTER_HARDWARE |
| F49 | Toy mounting board fasteners | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / USER_ADAPTER_HARDWARE |
| F50 | Mains/network flange and enclosure fasteners | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_CNC / USER_ADAPTER_HARDWARE |
| F51 | Playfield display-to-adapter fasteners | TBD | steel; finish/grade TBD | PURCHASE_BEFORE_ASSEMBLY / USER_ADAPTER_HARDWARE |

- **B15** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. CURRENT envelope is not a CNC wood part or selected bracket; no metal pivot introduced.
- **F29** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Exact display thread, insertion depth and count from selected monitor; not automatically M6.
- **F32** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Speaker-specific holes only in replaceable baffles.
- **F33** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. VESA/non-VESA adapters; no permanent model-specific pattern.
- **F42** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Selected equipment controls thread/length/retention. Existing holes/reserves remain provisional; not included in basic flatpack.
- **F43** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Selected equipment controls thread/length/retention. Existing holes/reserves remain provisional; not included in basic flatpack.
- **F44** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Selected equipment controls thread/length/retention. Existing holes/reserves remain provisional; not included in basic flatpack.
- **F45** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Selected equipment controls thread/length/retention. Existing holes/reserves remain provisional; not included in basic flatpack.
- **F46** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Selected equipment controls thread/length/retention. Existing holes/reserves remain provisional; not included in basic flatpack.
- **F47** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Selected equipment controls thread/length/retention. Existing holes/reserves remain provisional; not included in basic flatpack.
- **F48** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Selected equipment controls thread/length/retention. Existing holes/reserves remain provisional; not included in basic flatpack.
- **F49** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Selected equipment controls thread/length/retention. Existing holes/reserves remain provisional; not included in basic flatpack.
- **F50** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Selected equipment controls thread/length/retention. Existing holes/reserves remain provisional; not included in basic flatpack.
- **F51** — Nominal dimensions: TBD. Physical measurement: YES. Source: CURRENT V32 B-reps / owner V33 inventory instruction. Supplier-defined VESA screw depth/count; independent of eight saddle screws.

---
CERN-OHL-S-2.0 · Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet
