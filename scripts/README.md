# Scripts to aid preparing inputs for SANS

In this folder we have the scripts:
 - `cg_scatlen.py` reads a `.map` file generated with [CG Builder](https://jbarnoud.github.io/cgbuilder/) and number of molecules in the system to generate a file containing the scattering lengths for each bead of the system.
 - `select_q_sigmas.ipynb` is a Jupyter Notebook that helps you preparing input for the PLUMED SANS calculations (using or not metainference) based on a file containing the experimental data.