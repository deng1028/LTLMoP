# This is a specification definition file for the LTLMoP toolkit.
# Format details are described at the beginning of each section below.


======== SETTINGS ========

Actions: # List of action propositions and their state (enabled = 1, disabled = 0)
grabLeftHand, 1
grabRightHand, 1
liftLeftArm, 1
liftRightArm, 1

CompileOptions:
convexify: True
parser: structured
symbolic: False
use_region_bit_encoding: True
synthesizer: jtlv
fastslow: True
decompose: True

CurrentConfigName:
demo

Customs: # List of custom propositions

RegionFile: # Relative path of region description file
Johnny5Demo.regions

Sensors: # List of sensor propositions and their state (enabled = 1, disabled = 0)
findMe, 1
itemInLeftHand, 1
itemInRightHand, 1


======== SPECIFICATION ========

RegionMapping: # Mapping between region names and their decomposed counterparts
r1 = p6, p7
r2 = p2
r3 = p8, p9
Upload = p4
Charge = p5
others = 

Spec: # Specification in structured English
# setup initial conditions
robot starts with grabLeftHand and not liftLeftArm
robot starts with grabRightHand and not liftRightArm

if you are sensing findMe then stay there
infinitely often not findMe

# keep hands closed and down when moving
if you are not sensing findMe then do (grabLeftHand and not liftLeftArm)
if you are not sensing findMe then do (grabRightHand and not liftRightArm)

# raise arms if findMe is true
if you are not in (Charge or Upload) and you are sensing findMe and you are not sensing itemInLeftHand then do liftLeftArm
if you are not in (Charge or Upload) and you are sensing findMe and you are not sensing itemInRightHand then do liftRightArm

# after raising arm, open hands if not sensing item in hand
if you are not in (Charge or Upload) and  you were activating (liftLeftArm and grabLeftHand) and you are not sensing itemInLeftHand and you are sensing findMe then do not grabLeftHand
if you are not in (Charge or Upload) and  you were activating (liftRightArm and grabRightHand) and you are not sensing itemInRightHand and you are sensing findMe then do not grabRightHand

# close hand and try to grab item
if you are not in (Charge or Upload) and you were not activating grabLeftHand and you are sensing findMe then do grabLeftHand
if you are not in (Charge or Upload) and you were not activating grabRightHand and you are sensing findMe then do grabRightHand

# if sensing item in hand, put down arm and keep closing hand
if you are not in (Charge or Upload) and you are sensing itemInLeftHand then do (grabLeftHand and not liftLeftArm)
if you are not in (Charge or Upload) and you are sensing itemInRightHand then do (grabRightHand and not liftRightArm)

# if robot arrive in designated region, release item in hand
if you are in Charge and you are sensing findMe then do (liftLeftArm and not grabLeftHand and grabRightHand)
if you are in Upload and you are sensing findMe then do (liftRightArm and not grabRightHand and grabLeftHand)

if you are sensing itemInLeftHand then visit Charge
if you are sensing itemInRightHand then visit Upload
if you are not sensing (itemInLeftHand or itemInRightHand) then visit r1

