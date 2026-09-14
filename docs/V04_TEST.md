# v0.4 local test

After fetching the branch:

```bash
bash tools/run_playfield_v04.sh
freecad cad/master/vpin-master.FCStd
```

In FreeCAD select **PLAYFIELD SERVICE v0.4 - PROVISIONAL** and use an axonometric view + Fit All.

Expected visual result: the solid/less-transparent OLED remains in the closed playfield position; a highly transparent ghost rotates upward about the rear hinge axis by 70 degrees; matching cradle and gas-strut ghosts show the service geometry.

Do not manually edit the generated v0.4 objects. Report any FreeCAD console error or obviously inverted/open-downward geometry; the build script will be corrected instead.
