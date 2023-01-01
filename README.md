
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

The core dependencies are scipy and numpy,
and additionally matplotlib for the examples.

Validation
----------
The validation of the current physics model is based on data provided
in the thesis of Bloemendaal, B.F. (2009) for the Big Air model
of roller coaster by Dutch manufacturer Vekoma.
See the figure below for a comparison of the Hamiltonian (total energy)
of the system as a function of time.

<p align="center">
<img src="https://raw.githubusercontent.com/tijssen/pycoaster/main/docs/validation.png">
</p>

The code to produce this figure can be found in `examples/validate.py`.
Other examples can also be found in that folder.
Note that some functionality is currently undocumented (todo).

To-do
-----
High priority:
- Write a rationale on the physics and mathematics behind PyCoaster,
- Add more track geometries and examples,
- Improve code quality/add features.

Low priority (may never happen):
- Implement a control system,
- High-fidelity animations using OpenGL,
- More options/tools to create/add tracks.

Copyright
---------
Copyright (C) 2022, 2023 Luuk Tijssen

License: GNU General Public License version 3 and above.

