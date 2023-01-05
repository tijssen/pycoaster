
<p align="center">
<img src="https://raw.githubusercontent.com/tijssen/pycoaster/main/docs/animation.gif">
</p>

PyCoaster
=========
PyCoaster is a Python library for the accurate definition and evaluation
of the equations of motion for rail-guided vehicles, such as roller coasters.

These equations can be used to model the motion of such vehicles.
It is not that hard to model the motion in a conservative system,
where you only have to consider gravity, with a known and constant acceleration.
What makes the model more tricky is when you consider a non-conservative system,
where frictional forces work on the vehicle,
dissipating the total energy of the system in the form of heat.
These forces depend on quantities that may be difficult or expensive to compute,
such as the velocity or normal acceleration of the vehicle.

It is at this point that many libraries (such as games) take a shortcut,
for instance modelling the friction as a constant loss of energy
as a function of time or traversed path length.
This may be good or bad, depending on your computational needs.
PyCoaster distinguishes itself because it does not take such shortcuts
and tries to stay true to the physics.

Installation
------------
Install PyCoaster and run an example:

	git clone https://github.com/tijssen/pycoaster
	cd pycoaster/examples
	python3 animate.py

The core dependencies are SciPy and NumPy.
You additionally need Matplotlib for the examples.

Validation
----------
The validation of the current physics model is based on data provided
in the MSc thesis of 
[Bloemendaal, B.F. (2009)](http://resolver.tudelft.nl/uuid:701f9c34-fc6b-46d2-8beb-c966041bc410)
for the [Big Air](https://rcdb.com/8656.htm)
model of roller coaster by Dutch manufacturer Vekoma.
See the figure below for a comparison of the Hamiltonian (total energy)
of the system as a function of time, as well as the ride stats.

<p align="center">
<img src="https://raw.githubusercontent.com/tijssen/pycoaster/main/docs/validation.png">
</p>

-  Length: 145.9 m
-   Speed: 112.7 km/h
- G-Force: 4.0

The code to produce this figure can be found in `examples/validate.py`.
Other examples can also be found in that folder.
Note that some functionality of PyCoaster is currently undocumented (todo).

See also
--------
[Pendrill, A-M.](https://tivoli.fysik.org/) has done excellent research
in the field, producing countless open-access articles and motion tracker data.
I highly recommend her articles, and they may provide opportunities for
additional validation cases in the future.

To-do
-----
- Write a rationale on the physics and mathematics behind PyCoaster,
- Document all features,
- Add more track geometries, examples and validation cases.

Copyright
---------
Copyright (C) 2022, 2023 Luuk Tijssen

License: GNU General Public License version 3 and above.

