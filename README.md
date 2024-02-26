# Advanced Visualization of Molecular Dynamics: HBOND Interactions

In this repository some Python 3 based computational techniques are used to provide a dynamic view of protein conformation and amino aciid interactions in a molecular dynamic simulation, producing an animated output to visualize the change in conformation of a protein.

## Repository Overview

The code takes molecular dynamics frames (in PDB format) and contact frames (in ringEdges format) to generate output animations, like the two shown here below.

![Ionic in P16](https://github.com/riccaran/structural_bioinformatics/blob/main/output/p16/animations/p16_IONIC.gif)

![Van der Waals in antibody](https://github.com/riccaran/structural_bioinformatics/blob/main/output/antibody/animations/antibody_VDW.gif)

Distinct animations are made for each type of bonds, including hydrogen bonds (HBOND), π-π stackings (PIPISTACK), van der Waals interactions (VDW), and others. The left panel presents a contact map where each colored point denotes a specific bond-type between amino acid residues (the color gradient determine the distance of the interaction in ångströms), with the color gradient representing bond strength. The right panel presents 3D visualization of the protein itself, where the changing conformations and interactions are animated over the course of the simulation and can be directly compared with the changing pattern of the contact map on tthe left.

## Structure and tools

The code processes each frame of the molecular dynamics simulation using three different python scripts:
1. `make_contacts_frames.py` - 
2. `make_dynamics_frames.py` - 
3. `gif_maker.py` - 

## Tools used

Python , ChimeraX and libraries
