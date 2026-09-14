"""FreeCADCmd entry point for the v0.4 playfield builder.

FreeCADCmd does not reliably set __name__ == '__main__' for positional Python
scripts in all supported builds. Import the implementation module explicitly
and invoke main() at top level so the builder always executes.
"""

from build_playfield_v04 import main

main()
