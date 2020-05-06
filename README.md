# membraneNetPressureGenerator

- The python script is a customized workflow I am using to post-process the result of OpenFOAM CFD simulation to extract and generate net pressure on membrane surface for engineering calculation
- The data can be directly produced right after the simulation converged
- The point pressure interpolation is done based on kdTree function from scipy
- LoadCase_.xyzp is the resulted file, ready to be plotted to the structural model for wind load calculation
