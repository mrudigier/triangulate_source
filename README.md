# triangulate_source

GUI tool to estimate the position of a source given a set of intensity measurements.
The programme is written for the special case of the FATIMA array of the DESPEC setup
at GSI/FAIR.

python3, uses tkinter

## main branch:
The main branch uses inverse square law of geometric efficiency (as well
as projection of the effective area). This apprximation is only a good estimate if the
source is not too close to the detector.

## tof branch:
The tof branch simply calculates the time of flight difference between opposite detectors.
This can be used to verify a position if time measurements are available.

