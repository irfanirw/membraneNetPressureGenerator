# membraneNetPressureGenerator
A program to extract, compute, interpolate, and generate structural-engineering-ready file for wind load simulation based on [vtk](https://vtk.org/Wiki/Main_Page) data.
- xyzp_generator.py is the file I used for a customized workflow for post-processing the result of OpenFOAM CFD simulation. This code works by to extracting and generating net pressure on membrane surface for engineering calculation.
- The data can be directly produced right after the simulation converged.
- The point pressure interpolation is done based on kdTree function from scipy.
- LoadCase_.xyzp is the resulted file, ready to be plotted to the structural model for wind load calculation.
