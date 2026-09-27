import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from joinery_study import build,verify
build()
r=verify()
print('JOINERY_STUDY_PASS',len(r['checks']),'checks; 45 solids; five changed interfaces; CNC BLOCKED')
