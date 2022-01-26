# triangulate_source

GUI tool to estimate the position of a source given a set of intensity measurements.
The programme is written for the special case of the FATIMA array of the DESPEC setup
at GSI/FAIR.

python3, uses tkinter

## main branch:
The main branch uses inverse square law of geometric efficiency (as well
as projection of the effective area). This apprximation is only a good estimate if the
source is not too close to the detector.

Requires and input file for geometry (detector distances in mm) and a reference file
with intensities (comparable peak area in all detectors). The name of a reference intesity file
can be given. It is loaded by pressing the LOAD REF button. The programme will then
display the difference of intensity ratios of opposite detectors in FATIMA. By changing
the source position using the slider the difference can be minimised to determine a
most likely source position based on the approximations.
In the bottom right corner the current rms is displayed. The best rms found so far, as well
as the respective source position values are also displayed. The best position can be
reloaded by pressing the respective button.

## tof branch:
The tof branch simply calculates the time of flight difference between opposite detectors.
This can be used to verify a position if time measurements are available.

