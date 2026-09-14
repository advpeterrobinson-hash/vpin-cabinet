import FreeCAD as App
import Part
import os

project = os.path.expanduser("~/Projetos/vpin-cabinet")
path = os.path.join(project, "cad/master/vpin-master.FCStd")

doc = App.openDocument(path)
sheet = doc.getObject("Parameters")

if sheet is None:
    raise RuntimeError("MASTER PARAMETERS not found")


# ------------------------------------------------------------
# LG OLED42C5PSA
#
# Native TV orientation:
#   932 mm wide
#   540 mm high
#   41.1 mm max depth
#
# Pinball orientation:
#   cabinet X = 540 mm
#   cabinet Y = 932 mm
# ------------------------------------------------------------

sheet.set("B12", "932.00 mm")
sheet.set("B13", "540.00 mm")
sheet.set("B14", "41.10 mm")
sheet.set("B15", "9.80 kg")

sheet.set("B16", "1.00 mm")
sheet.set(
    "C16",
    "Per-side OLED installation clearance"
)

# Additional OLED-fit parameters
oled_rows = [
    (
        35,
        "OLEDInstalledWidth",
        "=B13+2*B16",
        "OLED cross-cabinet envelope including clearance"
    ),
    (
        36,
        "OLEDPocketDepth",
        "=(B35-B4)/2",
        "Required pocket depth into each cabinet side"
    ),
    (
        37,
        "OLEDRemainingSkin",
        "=B3-B36",
        "Plywood remaining outside OLED pocket"
    ),
    (
        38,
        "OLEDFrontSetback",
        "44.40 mm",
        "Provisional longitudinal position based on reference layout"
    ),
]

for row, alias, expression, description in oled_rows:
    sheet.set(f"A{row}", alias)
    sheet.set(f"B{row}", expression)
    sheet.set(f"C{row}", description)

    try:
        sheet.setAlias(f"B{row}", alias)
    except Exception:
        pass


# ------------------------------------------------------------
# Remove old fit mockups if script is rerun
# ------------------------------------------------------------

for name in [
    "OLED42C5Envelope",
    "OLED42C5ClearanceEnvelope",
    "OLED_Fit_Check",
]:
    obj = doc.getObject(name)
    if obj:
        doc.removeObject(name)

doc.recompute()


# ------------------------------------------------------------
# Fit-check group
# ------------------------------------------------------------

group = doc.addObject(
    "App::Part",
    "OLED_Fit_Check"
)
group.Label = "LG OLED42C5 FIT CHECK v0.3"


# Physical TV envelope
tv = doc.addObject(
    "Part::Box",
    "OLED42C5Envelope"
)
tv.Label = "LG OLED42C5 Physical Envelope"

# X = cross-cabinet dimension
tv.setExpression(
    "Length",
    "Parameters.OLEDHeight"
)

# Y = native TV width / playfield length
tv.setExpression(
    "Width",
    "Parameters.OLEDWidth"
)

# Z = TV thickness
tv.setExpression(
    "Height",
    "Parameters.OLEDDepth"
)

tv.setExpression(
    "Placement.Base.x",
    "(Parameters.CabOuterWidth - Parameters.OLEDHeight) / 2"
)

tv.setExpression(
    "Placement.Base.y",
    "Parameters.OLEDFrontSetback"
)

# Deliberately place it low for fit inspection.
# Final Z and rotation belong to the hinge/cradle design phase.
tv.setExpression(
    "Placement.Base.z",
    "Parameters.CabFrontHeight - Parameters.OLEDDepth"
)

group.addObject(tv)


# Clearance envelope
clearance = doc.addObject(
    "Part::Box",
    "OLED42C5ClearanceEnvelope"
)
clearance.Label = "C5 Required Cross-Width + Clearance"

clearance.setExpression(
    "Length",
    "Parameters.OLEDInstalledWidth"
)

clearance.setExpression(
    "Width",
    "Parameters.OLEDWidth"
)

clearance.setExpression(
    "Height",
    "Parameters.OLEDDepth"
)

clearance.setExpression(
    "Placement.Base.x",
    "(Parameters.CabOuterWidth - Parameters.OLEDInstalledWidth) / 2"
)

clearance.setExpression(
    "Placement.Base.y",
    "Parameters.OLEDFrontSetback"
)

clearance.setExpression(
    "Placement.Base.z",
    "Parameters.CabFrontHeight - Parameters.OLEDDepth"
)

group.addObject(clearance)


doc.recompute()
doc.save()


print()
print("=" * 72)
print("LG OLED42C5 FIT CHECK")
print("=" * 72)

for name in (
    "OLEDWidth",
    "OLEDHeight",
    "OLEDDepth",
    "OLEDClearance",
    "OLEDInstalledWidth",
    "OLEDPocketDepth",
    "OLEDRemainingSkin",
):
    try:
        print(
            f"{name:22}",
            sheet.get(name)
        )
    except Exception:
        pass

print()
print("NOTE:")
print("OLED position/rotation is intentionally provisional.")
print("No cabinet pockets have been cut in v0.3.")
print("Hinge sweep and gas-strut geometry come next.")

App.closeDocument(doc.Name)
