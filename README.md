# Forces-Constants

This is a python program which can calculate first and second derivatives using molpro. 

You probably need mpiexec on your supercomputer for this to run. 

It should work for any XYZ geometry, just skip a line or edit the numpy.genfromtext parameters.

## Features
--------

- Automatically generates displacement geometries, then submits the jobs in molpro without filling up your disk with points.
- Extracts the energy, then calculates numerical force constants in Hartree/Angstoms^2

## Installation
------------

- Download the script and place it in the directory with the optimized geometry.
- Make sure to skip the first line and place the optimized geometry in geom.xyz
- Place the reference out in reference.out 

Support
-------

If you are having issues, please let me know.
Email me at mvee18@gmail.com and I can help you.
