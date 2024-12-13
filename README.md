# Advanced Visualization of Molecular Dynamics

In this project different computational techniques were used to provide a dynamic view of protein conformation and amino acid interactions in molecular dynamic simulations and protein conformational ensembles, producing an animated output to visualize the dynamic interactin patterns in proteins.

## Repository Overview

The code takes molecular dynamics frames (in PDB format) and contact frames (in ringEdges format) to generate output animations, like the two shown here below.

![Ionic in P16](https://github.com/riccaran/structural_bioinformatics/blob/main/output/p16/animations/p16_IONIC.gif)

![Van der Waals in antibody](https://github.com/riccaran/structural_bioinformatics/blob/main/output/antibody/animations/antibody_VDW.gif)

Distinct animations are made for each type of bond, including hydrogen bonds (HBOND), π-π stackings (PIPISTACK), van der Waals interactions (VDW), and others. The left panel presents a contact map where each colored point denotes a specific bond-type between amino acid residues (the color gradient determine the distance of the interaction in ångströms), while the right panel presents a 3D visualization of the protein itself. In this way the changing conformations and the interactions pattern of the contact map are animated over the course of the simulation and can be directly compared with each other for every simulation frame.

## Structure and Tools

The code processes each frame of the molecular dynamics simulation using three different python scripts:
1. `make_contacts_frames.py` - this Python script makes the contact maps frames
2. `make_dynamics_frames.py` - this Python script makes the molecular dynamics animation and must be run as a ChimeraX module by using the command `run /usr/local/bin/make_dynamics_frames.py`
3. `gif_maker.py` - this Python script makes the final GIFs

## Tools Used

UCSF ChimeraX 1.7.1 (with Chimerax 1.8 Python module), Python 3.8.8, NumPy 1.23.5, Pandas 1.5.3, Matplotlib 3.7.1, Seaborn 0.12.2, Imageio 2.34.0
