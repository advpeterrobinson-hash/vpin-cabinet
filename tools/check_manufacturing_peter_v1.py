"""Supplier/coupon release-gate regression tests; synthetic measurements only in temporary files.
CERN-OHL-S-2.0.
"""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import manufacturing_peter_v1 as m


def main():
    p=m.read(m.PROFILE);checks=[]
    def check(name, condition):
        m.require(condition,name);checks.append(name)
    def rejects(name, func):
        try:func()
        except (ValueError,KeyError):check(name,True)
        else:raise AssertionError(name)
    m.validate_profile(p)
    check('Confirmed supplier profile ready for preparation',p['status']=='COMPLETE_FOR_MANUFACTURING_PREPARATION')
    # Exercise the unknown-input path even after the owner later records real data.
    # Only this in-memory fixture is reset; the supplier profile is never edited.
    p=copy.deepcopy(p)
    p['stock'].update(actual_thickness_mm=None,production_lot_id=None,thickness_measurements_mm=[])
    p['coupon'].update(validation_status='NOT_CUT_OR_VALIDATED',selected_fit_clearance_mm=None,
                       accepted_corner_strategy=None,validated_package_sha256=None,results=None)
    check('Unknown-thickness fixture never substitutes nominal18',p['stock']['actual_thickness_mm'] is None)
    with tempfile.TemporaryDirectory(prefix='peter-coupon-tests-') as temp:
        out=Path(temp);preview=m.coupon(p,out)
        check('Nominal preview cannot emit cutting file',not (out/'coupon-cut.svg').exists())
        rejects('Measured coupon rejects nominal-only profile',lambda:m.coupon(p,out,True))
        test=copy.deepcopy(p)
        test['stock'].update(actual_thickness_mm=17.8, production_lot_id='SYNTHETIC_TEST_NOT_A_REAL_LOT',
                             thickness_measurements_mm=[17.78,17.80,17.82])
        test['coupon']['screw_interface']['purchased_hardware_dimensions']={
            'part_reference':'SYNTHETIC_TEST_ONLY', 'shank_diameter_mm':4.5,'length_mm':30,
            'pilot_diameter_mm':3,'pilot_depth_mm':12,'countersink_diameter_mm':9,
            'countersink_included_angle_deg':90,'countersink_depth_mm':2}
        manifest=m.coupon(test,out,True)
        check('Measured slot zero uses actual 17.8, not nominal18',manifest['features'][4]['nominal_slot_width_mm']==17.8)
        check('Six clearance variants with measured zero',len([f for f in manifest['features'] if f['id'].startswith('SLOT_')])==6)
        xml=ET.parse(out/'coupon-cut.svg')
        check('Cut SVG contains no text/labels',not xml.findall('.//{'+m.NS+'}text'))
        check('All operations same face',all(f['face']=='A' for f in manifest['features']))
        reg=m.register(out)
        check('Every current wood component gets a release status',len(reg['parts'])==93)
        check('Unreviewed parts never marked ready',all(x['manufacturing_status'].startswith('BLOCKED_') for x in reg['parts']))
        result=m.read(out/'coupon-results-template.json')
        result.update(production_lot_id=test['stock']['production_lot_id'],package_sha256=m.fingerprint(test),
                      cut_svg_sha256=manifest['cut_svg_sha256'],machine_cam_run_reference='SYNTHETIC',
                      tested_by='TEST',tested_on='TEST',selected_fit_clearance_mm=.1,
                      measured_pocket_depth_mm=6,measured_locator_depth_mm=.5,screw_test_notes='SYNTHETIC')
        for key,val in list(result.items()):
            if val is False:result[key]=True
        for i,d in enumerate(test['coupon']['clearance_trials_mm']):
            result['measured_slot_widths_mm'][f'SLOT_{i+1}']=17.8+d
            result['fit_observations'][f'SLOT_{i+1}']='Synthetic fit result'
        bad=copy.deepcopy(result);bad['production_lot_id']='wrong'
        rejects('Wrong lot cannot validate coupon',lambda:m.record_results(test,bad,manifest))
        bad=copy.deepcopy(result);bad['tbone_fit_accepted']=False
        rejects('Failed corner test cannot validate coupon',lambda:m.record_results(test,bad,manifest))
        bad=copy.deepcopy(result);bad['selected_fit_clearance_mm']=.8
        rejects('Untested clearance cannot be selected',lambda:m.record_results(test,bad,manifest))
        m.record_results(test,result,manifest)
        check('Valid synthetic coupon acceptance still does not release sheets',test['release_policy']['full_sheet_release'] is False)
        errors=m.release_blockers(test,reg)
        check('Coupon acceptance does not bypass part/hardware/owner gates',len(errors)>=95)
        good=copy.deepcopy(reg)
        for row in good['parts']:
            row.update(manufacturing_status='ONE_SIDE_CNC_READY',operation_audit_complete=True,cnc_face='A',
                       cnc_operations=[{'type':'SYNTHETIC_TEST_ONLY','face':'A'}])
        check('Synthetic fully-qualified path exercises positive control',m.release_blockers(test,good,True,True)==[])
        bad=copy.deepcopy(good);bad['parts'][0]['cnc_operations'].append({'face':'B','flip':True})
        check('Opposite-face/flip operation blocks release',bool(m.release_blockers(test,bad,True,True)))
        bad=copy.deepcopy(good);bad['parts'][0]['manufacturing_status']='ONE_SIDE_CNC_PLUS_MANUAL_FINISH'
        check('Manual finish needs explicit instructions',bool(m.release_blockers(test,bad,True,True)))
        bad=copy.deepcopy(test);bad['stock']['thickness_measurements_mm'][0]=17.79
        check('Changed lot input invalidates coupon',any('invalidated' in e for e in m.release_blockers(bad,good,True,True)))
        bad=copy.deepcopy(test);bad['coupon']['results']['owner_coupon_accepted']=False
        check('Fabricated validation flag cannot bypass missing acceptance',any('Invalid recorded' in e for e in m.release_blockers(bad,good,True,True)))
        bad=copy.deepcopy(test);bad['stock']['actual_thickness_mm']=18.1
        rejects('Greater than18 exceeds supplier spacing scope',lambda:m.validate_profile(bad,True))
        bad=copy.deepcopy(p);bad['machine']['two_sided_machining']=True
        rejects('Two-sided profile forbidden',lambda:m.validate_profile(bad))
        m.coupon(p,out)
        check('Preview rerun removes stale owned cut SVG',not (out/'coupon-cut.svg').exists())
        reg['parts'][0]['note']='Preserve reviewed notes';m.write(out/'one-side-part-register.json',reg)
        check('Regeneration preserves reviewed part register',m.register(out)['parts'][0]['note']=='Preserve reviewed notes')
    # Every pre-task byte, including CURRENT geometry, viewer and V33 library, is protected.
    base='2129f4b1a301fdb072bdc550dd577bee080aa4b2';count=0
    for line in subprocess.check_output(['git','ls-tree','-r','-z',base],cwd=m.ROOT).split(b'\0'):
        if not line:continue
        info,name=line.split(b'\t');mode,kind,sha=info.split()
        if kind!=b'blob':continue
        data=(m.ROOT/name.decode()).read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        m.require(actual==sha,'Pre-task file changed: '+name.decode());count+=1
    check('All pre-task files byte-identical',count>0)
    m.OUT.mkdir(parents=True,exist_ok=True)
    m.write(m.OUT/'validation.json',{'pass':True,'checks':checks,'unchanged_starting_head_files':count,
            'source_head':base,'full_sheet_release':False,'synthetic_measurements_written_to_profile':False})
    print('PETER_SUPPLIER_GATES_PASS',len(checks),'checks;',count,'starting files byte-identical')


if __name__=='__main__':main()
