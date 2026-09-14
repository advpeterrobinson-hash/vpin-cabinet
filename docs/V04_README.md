# Playfield v0.4 quickstart

This branch introduces a provisional hinged-playfield kinematic model.

Run locally:

```bash
git fetch origin
git switch feat/playfield-v04
git pull
bash tools/run_playfield_v04.sh
freecad cad/master/vpin-master.FCStd
```

The generated FreeCAD group is `PLAYFIELD SERVICE v0.4 - PROVISIONAL`.

A successful script run plus a mechanically sensible upward-opening ghost is the validation gate for merging this branch. The branch does not contain manufacturing approval.
