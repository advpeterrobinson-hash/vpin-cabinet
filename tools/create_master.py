import FreeCAD as App
import os

project = os.path.expanduser("~/Projetos/vpin-cabinet")
output = os.path.join(project, "cad/master/vpin-master.FCStd")

doc = App.newDocument("VPinMaster")

sheet = doc.addObject("Spreadsheet::Sheet", "Parameters")
sheet.Label = "MASTER PARAMETERS"

rows = [
    ("PARAMETER",          "VALUE",      "DESCRIPTION"),
    ("CabOuterWidth",      "558.80 mm",  "Williams external cabinet width"),
    ("WoodMain",           "18.00 mm",   "Nominal main plywood thickness"),
    ("CabInnerWidth",      "=B2-2*B3",   "Derived cabinet inside width"),
    ("CabSideLength",      "1308.10 mm", "Reference cabinet side length envelope"),
    ("CabSideHeightEnv",   "596.90 mm",  "Reference side height envelope"),

    ("", "", ""),

    ("BackboxWidthRef",    "730.25 mm",  "Reference backbox overall width"),
    ("BackboxDepthRef",    "254.00 mm",  "Reference backbox overall depth"),
    ("BackboxHeightRef",   "723.90 mm",  "Reference backbox overall height"),

    ("", "", ""),

    ("OLEDWidth",          "0.00 mm",    "Selected LG C5 exact physical width"),
    ("OLEDHeight",         "0.00 mm",    "Selected LG C5 exact physical height"),
    ("OLEDDepth",          "0.00 mm",    "Selected LG C5 maximum physical depth"),
    ("OLEDWeight",         "0.00 kg",    "Selected LG C5 mass without stand"),
    ("OLEDClearance",      "2.00 mm",    "Initial installation clearance"),

    ("", "", ""),

    ("PCFrameWidth",       "440.00 mm",  "Open-frame PC chassis"),
    ("PCFrameDepth",       "265.00 mm",  "Open-frame PC chassis"),
    ("PCFrameBareHeight",  "128.00 mm",  "Bare chassis only"),
    ("PCServiceWidth",     "470.00 mm",  "Reserved service envelope"),
    ("PCServiceDepth",     "400.00 mm",  "Reserved service envelope"),
    ("PCServiceHeight",    "230.00 mm",  "Reserved service envelope"),

    ("", "", ""),

    ("CNCBitDiameter",     "6.00 mm",    "Placeholder until Cutter CNC consultation"),
    ("JointClearance",     "0.20 mm",    "Initial placeholder"),
    ("PocketClearance",    "0.20 mm",    "Initial placeholder"),
]

for row, values in enumerate(rows, start=1):
    for col, value in zip(("A", "B", "C"), values):
        sheet.set(f"{col}{row}", value)

# Aliases for usable parameter cells.
aliases = {
    2: "CabOuterWidth",
    3: "WoodMain",
    4: "CabInnerWidth",
    5: "CabSideLength",
    6: "CabSideHeightEnv",

    8: "BackboxWidthRef",
    9: "BackboxDepthRef",
    10: "BackboxHeightRef",

    12: "OLEDWidth",
    13: "OLEDHeight",
    14: "OLEDDepth",
    15: "OLEDWeight",
    16: "OLEDClearance",

    18: "PCFrameWidth",
    19: "PCFrameDepth",
    20: "PCFrameBareHeight",
    21: "PCServiceWidth",
    22: "PCServiceDepth",
    23: "PCServiceHeight",

    25: "CNCBitDiameter",
    26: "JointClearance",
    27: "PocketClearance",
}

for row, alias in aliases.items():
    sheet.setAlias(f"B{row}", alias)

sheet.setStyle("A1:C1", "bold", "add")
sheet.setColumnWidth("A", 180)
sheet.setColumnWidth("B", 110)
sheet.setColumnWidth("C", 360)

doc.recompute()

os.makedirs(os.path.dirname(output), exist_ok=True)
doc.saveAs(output)

print(f"Created: {output}")
print(f"Inside width: {sheet.get('B4')}")
