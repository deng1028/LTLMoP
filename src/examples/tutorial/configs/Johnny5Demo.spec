# This is a specification definition file for the LTLMoP toolkit.
# Format details are described at the beginning of each section below.


======== SETTINGS ========

Actions: # List of action propositions and their state (enabled = 1, disabled = 0)
standUp, 0
takeBow, 1
highFive, 1

CompileOptions:
convexify: True
parser: structured
fastslow: False
decompose: True
use_region_bit_encoding: True

CurrentConfigName:
Demo

Customs: # List of custom propositions

RegionFile: # Relative path of region description file
../Johnny5Demo.regions

Sensors: # List of sensor propositions and their state (enabled = 1, disabled = 0)
findMe, 1


======== SPECIFICATION ========

RegionMapping: # Mapping between region names and their decomposed counterparts
r4 = p2
r0 = p6
r1 = p5
r2 = p4
r3 = p3
others = p7, p8, p9, p10, p11, p12, p13, p14, p15

Spec: # Specification in structured English
group Map is r0, r1, r2, r3, r4
robot starts in any Map with false

#do takeBow
visit all Map

if you are sensing findMe then stay there
do highFive if and only if you are sensing findMe
infinitely often not findMe

