"""Shared visible-object presets for PNG gallery and native FreeCAD review."""
def scenes(names):
 names=set(names)
 def pref(*p):return sorted(n for n in names if n.startswith(p))
 def existing(items):return [n for n in items if n in names]
 wood=pref('CabinetLeftSide','CabinetRightSide','CapturedFront','CapturedBottom','RearPanelWithCPU','LowCrossmember','RearShelf','BackboxFloor','BackboxTop','BackboxLeftSide','BackboxRightSide','BackboxRearFrame','BackboxServiceDoor','CradleSide','CradleCrossmember','CradlePivot','CradleRearBeam','ClosedSupportDoubler','RearCPUSupportRail','RearCPUShelfStowed','RearCPUServiceDoorClosed')
 cradle=pref('CradleSide','CradleCrossmember','CradlePivot','CradleRearBeam','PivotPlate','PivotJournal')
 closed_mechanics=cradle+pref('PropRod','PropFixed','PropLower','PropStow','SafetyStayNutPlate')+pref('PropReceiverLeftClosed','PropReceiverRightClosed')
 raised=pref('SafetyStayOpen','PropReceiverLeftOpen','PropReceiverRightOpen','PropUpperLockPin','PropPinKeeper')+existing(['CradleOpenGhostV18','GenericPlayfieldDisplayOpenGhostV18'])
 carriers=pref('ElectronicsCarrier','CarrierAngle','ElectronicsLeftPayload','ElectronicsRightPayload')
 ssf=pref('SSF')
 controls=pref('Control','CoinDoor','Plunger','HiddenService')
 bb=pref('BackboxFloor','BackboxTop','BackboxLeftSide','BackboxRightSide','BackboxRearFrame','BackglassRail','BackglassDisplay','BackboxDMD','BackboxSpeaker','BackboxLighting','BackboxDoorStop','BackboxDoorGasket','BackboxDoorHinge','BackboxExhaust')
 bbclosed=bb+existing(['BackboxServiceDoorV14','BackboxDoorLatchClosedV27'])
 bbopen=bb+existing(['BackboxDoorOpenV27','BackboxDoorLatchOpenV27'])
 cpu=pref('RearCPUSupportRail','RearCPUFixedSlide','CPURailAngle','CPURailBacking','RearCPUStowedRetainer')+existing(['RearCPUShelfStowedV24','RearCPUOpenCaseStowedV24','RearCPUServiceDoorClosedV24'])
 utilities=pref('UtilityAMainsCarrier','UtilityAEthernetCarrier','UtilityAMainsEnclosure')
 shell=existing(['CabinetLeftSide','CabinetRightSide','CapturedFrontPanelV20','CapturedBottomV20','RearPanelWithCPUHatchV24','RearShelfV14'])+pref('LowCrossmember','ClassicLegBracket','LegSpreader','ClosedSupportDoubler')
 base=shell+bbclosed+closed_mechanics+cpu+carriers+controls+utilities+existing(['GenericPlayfieldDisplayClosedV18','PlayfieldGlassTargetV20','LockdownBarEnvelopeV20'])+pref('SideRail','BottomFilter')
 interior=[n for n in shell if n not in ('CabinetRightSide','RearPanelWithCPUHatchV24')]+closed_mechanics+cpu+carriers+ssf+controls+utilities
 extended=[n for n in cpu if n not in ('RearCPUShelfStowedV24','RearCPUOpenCaseStowedV24','RearCPUServiceDoorClosedV24')]+existing(['RearCPUServiceDoorOpenGhostV24','RearCPUShelfServiceGhostV24','RearCPUOpenCaseServiceGhostV24','RearCPUServiceSlideLeftGhostV24','RearCPUServiceSlideRightGhostV24'])
 return [
 ('01-full-exterior','Full exterior / playable interfaces',base,24,-65,'Control shapes are packaging, not final bores. Manual playfield lift. External purchased leg outlines remain unmeasured.'),
 ('02-left-control-side','LEFT side / flipper and optional action',existing(['CabinetLeftSide'])+pref('ControlLeft','SSFFrontLeft','SSFRearLeft','ClassicLegBracketFL','ClassicLegBracketRL','CradleSideRailLeft','ClosedSupportDoublerLeft','PropRodLeft','PropFixedClevisLeft'),18,5,'Crosshair centers: Y255 Z270 primary; Y310 Z270 optional. HF-020 controls bore / flats / nut and switch depth.'),
 ('03-right-control-plunger','RIGHT side / flippers and right-front plunger',existing(['CabinetRightSide','CapturedFrontPanelV20'])+pref('ControlRight','Plunger','SSFFrontRight','SSFRearRight','CradleSideRailRight','ClosedSupportDoublerRight','ClassicLegBracketFR','ClassicLegBracketRR'),18,175,'Plunger center X520 Z215; body X500..540 / Y18..220 / Z195..235. HF-030 patterns remain blank.'),
 ('04-front-panel','FRONT / coin door, start, exit, launch, plunger',existing(['CapturedFrontPanelV20','LockdownBarEnvelopeV20','LockdownReceiverKeepoutV20'])+pref('ControlStart','ControlExit','ControlLaunch','CoinDoor','Plunger','HiddenService','ClassicLegBracketF'),14,-90,'Coin door HF-019, buttons HF-020, plunger HF-030. Hidden service / feedback-disable controls inside coin-door access.'),
 ('05-bottom-penetration-map','BOTTOM / actual slots and reserved hardware',[],0,0,'Dedicated penetration drawing'),
 ('06-interior-service','Interior / playfield removed for inspection',interior,42,-55,'Bottom and three LOW CROSSMEMBERS are structural. Rear shelf carries backbox. CPU rails carry slides; no broad electronics shelf.'),
 ('07-electronics-carriers','Two removable low-voltage electronics carriers',carriers+existing(['CapturedBottomV20','LowCrossmember1V20','LowCrossmember2V20','CentralServiceKeepoutV27'])+ssf,50,-55,'125 × 355 mm trays; 3 kg each planning envelope. Left DC distribution/control; right amps/controllers. Mains stays in separate enclosure.'),
 ('08-ssf-exciter-zones','Four SSF zones / solid plywood beneath exciters',existing(['CabinetLeftSide','CabinetRightSide'])+ssf+carriers+pref('RearCPUSupportRail','ClassicLegBracket'),27,-55,'Panel-coupled exciters: NO large speaker holes. No structural-bottom subwoofer opening. Local attachment adapters selected later.'),
 ('09-airflow-path','Bottom intake → main cabinet → passages → backbox exhaust',shell+bb+pref('BottomFilter','AirflowRoute')+carriers,23,-55,'18 generic bottom slots / removable dust filter. Matched rear shelf/floor passages. Fixed upper exhaust adapters. Packaging only; no thermal claim.'),
 ('10-playfield-raised-props','Playfield raised / BOTH captive prop rods pinned',shell+raised+pref('PropFixed','PropLower','SafetyStayNutPlate')+carriers,25,-55,'Straight 8 mm candidate rods, about 897 mm pin-to-pin. Each prop requires full-load proof. Captive lower pivots + upper pins/keepers; no friction.'),
 ('11-props-stowed','Both props stowed / captive positive clips',shell+closed_mechanics+ssf,35,-55,'Rods lie rearward in the outer-rail corridor, ending near Y977 at Z330. Stow clips close with captive transverse keepers.'),
 ('12-backbox-door-closed','BB-DOOR-001-R1 / CLOSED, gasketed and keyed',bbclosed,20,65,'520 × 460 × 15 door retained. Fixed frame carries shear. Fans remain in fixed upper frame; no moving fan harness.'),
 ('13-backbox-door-open','BB-DOOR-001-R1 / OPEN OUTWARD 105°',bbopen+existing(['BackboxRearAccessEnvelopeV27']),24,65,'Continuous hinge / latch / gasket are measured HF-029 interfaces. Rear hand/tool approach stays clear of the open door.'),
 ('14-backbox-service-access','Backbox / displays, DMD, speakers and wiring access',bbopen+existing(['BackglassFrontRemovalEnvelopeV27']),28,-55,'Rear access serves connectors and central rail mounts. Remove front bezel to replace the full 740 mm monitor; it cannot pass flat through the rear door.'),
 ('15-cpu-extended','CPU extended / carriers do not obstruct rear service',existing(['CapturedBottomV20','RearPanelWithCPUHatchV24','LowCrossmember3V20'])+extended+carriers+utilities,28,65,'One 285 × 460 board, 450 mm rearward travel. Shelf Z135; low hatch and outward CPU door retained. 20 kg proof remains required.'),
 ('16-structural-exploded','Exploded structural wood / separate removable carriers',wood+carriers,25,-55,'29 permanent structural wood records; 2 removable doors + CPU board = 32 wood records. 11 replaceable carriers counted separately; not 11 new wood parts.')]
