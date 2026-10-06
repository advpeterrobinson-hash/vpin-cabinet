"""V35 exact manufacturing members, mass and preliminary logistics. No CNC release."""
from widebody_v35_common import *
import copy,csv,collections
p=load(O/'candidate.FCStd');oldreg=json.loads((R/'exports/generated/backbox-v342/manufacturing-register.json').read_text());audit=json.loads((O/'width-audit.json').read_text());rows=[]
for src in oldreg['parts']:
 a=copy.deepcopy(src);n=a['source_component'];m=A.Matrix(*a['local_to_installed_matrix']);dx=audit[n]['translation_x_mm'] if n in audit else DX
 if n not in p:
  q=Part.Shape();q.read(str(R/a['finished_member_brep']));q.transformShape(m,True);p[n]=shift(q,x=DX);audit[n]={'classification':'RECENTERED','translation_x_mm':DX}
 if dx is not None:m.A14+=dx
 q=p[n].copy();q.transformShape(m.inverse(),True);fp=O/(a['instance_id']+'.brep');q.exportBrep(str(fp));back=q.copy();back.transformShape(m,True)
 # Compare simple manufacturing solid, not overlapped hardware compounds.
 err=back.cut(p[n]).Volume+p[n].cut(back).Volume
 b=q.BoundBox;t=a['nominal_stock_thickness_mm'];flat=[]
 for f in q.Faces:
  try:
   normal=f.normalAt(0,0)
   if abs(normal.z)>.999999:flat.append(Part.Face(f.OuterWire).Area)
  except Exception:pass
 a.update(version='V35',finished_member_brep=str(fp.relative_to(R)),local_to_installed_matrix=list(m.A),volume_mm3=q.Volume,finished_xy_bounds_mm=[b.XMin,b.YMin,b.XMax,b.YMax],reference_bounds_3d_mm=bb(q),reconstruction_difference_mm3=err,manufacturing_release=False,outer_contour_area_mm2=max(flat) if flat else None,source_component=n,geometry_authority='exports/generated/widebody-v35/candidate.FCStd#'+n)
 if audit[n]['classification'] not in ['UNCHANGED','RECENTERED','REPOSITIONED']:
  a['manufacturing_status']='ONE_SIDE_CNC_PLUS_MANUAL_FINISH';a['fit_dependent']=True;a['coupon_dependent']=True
  a['one_face_plan']='FACE_A: source face, regenerated lateral span and same captured interfaces. Final hardware and thickness/coupon fit HOLD. FACE_B: NO CNC.'
  if n.startswith('SIDE_'):a['one_face_plan']='FACE_A INSIDE: reference longitudinal glass-channel rebate. Actual commercial profile may require special tooling/manual finishing; final slot NULL. FACE_B NO CNC.'
  if n=='BACKBOX_BASE':a['one_face_plan']='FACE_A TOP: existing captures/through cuts plus local sloping reference rear-channel seat. Actual channel attachment and Ø4/R2 coupon HOLD. FACE_B NO CNC.'
  a['manual_finish']=[{'operation':'PURCHASE_AND_COUPON_HOLD','face_datum':'FACE_A','depth_mm':None,'instruction':'Regenerate measured channel/hardware/stock interfaces; no flip CNC.'}]
  for k in ['cnc_stage_brep','outer_contour_brep','cnc_outer_access_brep']:a[k]=None
  for k in ['feature_register','through_cuts','pockets','review_outline']:a.pop(k,None)
 rows.append(a)
reg=copy.deepcopy(oldreg);reg.update(version='V35',parts=rows,manufacturing_release=False,source_head=C['head_before']);dump('manufacturing-register',reg)
with (O/'manufacturing-bom.csv').open('w') as f:
 wr=csv.writer(f);wr.writerow(['ID','instance','source','quantity','stock_mm','material','bounds_mm','volume_mm3','status'])
 for a in rows:wr.writerow([a['manufacturing_part_id'],a['instance_id'],a['source_component'],1,a['nominal_stock_thickness_mm'],a['material_class'],a['finished_xy_bounds_mm'],a['volume_mm3'],a['manufacturing_status']])
# Shelf first-fit rectangles using actual local contour bounds; conservative (not optimized) placement.
nest={};WID=2460;HEI=1560;SP=15
for t in [18,12]:
 items=[a for a in rows if a['nominal_stock_thickness_mm']==t];sheets=[]
 for a in sorted(items,key=lambda a:(a['finished_xy_bounds_mm'][2]-a['finished_xy_bounds_mm'][0])*(a['finished_xy_bounds_mm'][3]-a['finished_xy_bounds_mm'][1]),reverse=True):
  x0,y0,x1,y1=a['finished_xy_bounds_mm'];w,h=x1-x0,y1-y0
  if w<h:w,h=h,w;rot=True
  else:rot=False
  assert w<=WID and h<=HEI,(a['instance_id'],w,h)
  placed=False
  for sh in sheets:
   for shelf in sh['rows']:
    if h<=shelf['h'] and shelf['x']+w<=WID:
     sh['parts'].append({'instance':a['instance_id'],'x':20+shelf['x'],'y':20+shelf['y'],'w':w,'h':h,'rotated':rot});shelf['x']+=w+SP;placed=True;break
   if placed:break
   yy=sum(r['h']+SP for r in sh['rows'])
   if yy+h<=HEI:
    sh['rows'].append({'y':yy,'h':h,'x':w+SP});sh['parts'].append({'instance':a['instance_id'],'x':20,'y':20+yy,'w':w,'h':h,'rotated':rot});placed=True;break
  if not placed:sheets.append({'rows':[{'y':0,'h':h,'x':w+SP}],'parts':[{'instance':a['instance_id'],'x':20,'y':20,'w':w,'h':h,'rotated':rot}]})
 area=sum(a['outer_contour_area_mm2'] or 0 for a in items);nest[str(t)]={'pieces':len(items),'sheets':sheets,'sheet_count':len(sheets),'outer_contour_area_m2':area/1e6,'sheet_area_m2':len(sheets)*4,'usable_area_m2':len(sheets)*2460*1560/1e6,'utilization_outer_percent':100*area/(len(sheets)*4e6),'grain':'stock face-grain must follow same primary part axis; rotations require sheet-grain confirmation; trial permits90°','method':'conservative rectangle shelf first-fit, actual contour bounds; not optimized','release':False}
vol=sum(a['volume_mm3'] for a in rows);oldvol=sum(a['volume_mm3'] for a in oldreg['parts']);mass={'basis':'actual finished B-rep volumes; no bounding-box mass','density_LOW_NOMINAL_HIGH':[550,650,750],'wood_LOW_kg':vol*550/1e9,'wood_NOMINAL_kg':vol*650/1e9,'wood_HIGH_kg':vol*750/1e9,'delta_nominal_kg':(vol-oldvol)*650/1e9,'wood_pieces':len(rows),'CNC_pieces':sum(a['nominal_stock_thickness_mm'] is not None for a in rows),'solid_blocks':sum(a['nominal_stock_thickness_mm'] is None for a in rows),'families':len({a['manufacturing_part_id'] for a in rows}),'reconstruction_max_mm3':max(a['reconstruction_difference_mm3'] for a in rows),'hardware_mass':'UNKNOWN_NOT_ZERO','glass_reference_mass_kg':p['CandidateGlass'].Volume*2500/1e9}
bundles=[]
for a in sorted(rows,key=lambda a:(not a['source_component'].startswith('BB_'),-a['volume_mm3'])):
 high=a['volume_mm3']*750/1e9
 eligible=[b for b in bundles if b['high_wood_kg']+high+1<=25 and b['assembly']==('backbox' if a['source_component'].startswith('BB_') else 'main')]
 if not eligible:bundles.append({'id':'PK'+str(len(bundles)+1).zfill(2),'assembly':'backbox' if a['source_component'].startswith('BB_') else 'main','parts':[],'high_wood_kg':0,'nominal_wood_kg':0,'L':0,'W':0,'H':0,'packaging_allowance_kg':1});eligible=[bundles[-1]]
 b=eligible[0];bd=a['reference_bounds_3d_mm'];ll,ww=sorted([bd[3]-bd[0],bd[4]-bd[1]],reverse=True);hh=bd[5]-bd[2]
 b['parts'].append({'id':a['instance_id'],'mass_nominal_kg':a['volume_mm3']*650/1e9,'stack_z_mm':b['H'],'thickness_envelope_mm':hh,'separator_above_mm':3});b['high_wood_kg']+=high;b['nominal_wood_kg']+=a['volume_mm3']*650/1e9;b['L']=max(b['L'],ll);b['W']=max(b['W'],ww);b['H']+=hh+3
for b in bundles:
 b['external_mm']=[b['L']+40,b['W']+40,b['H']+40];b['high_gross_kg']=b['high_wood_kg']+1;b['estimated_CG_mm']=[b['external_mm'][0]/2,b['external_mm'][1]/2,20+sum((a['stack_z_mm']+a['thickness_envelope_mm']/2)*a['mass_nominal_kg'] for a in b['parts'])/b['nominal_wood_kg']];b['CG_basis']='centered layers; uniform material assumption'
dump('mass-counts',mass);dump('nesting',nest);dump('packaging',{'bundles':bundles,'hardware':'SEPARATE BOX','glass_electronics_included':False,'status':'PRELIMINARY_NOT_PRODUCTION'})
print(mass,flush=True)
