import os
import subprocess

# Initialize LAMMPS simulation
lammps_script = """
dimension    3
boundary     s p p
units        real
atom_style   full

# Atom Definition
pair_style    lj/cut/coul/cut 12 10
read_data     data.data

# Interatomic Potentials & Equilibrium Settings
velocity all create 300.0 12345

pair_coeff    1 1 0.1514 3.700 #CHO
pair_coeff    2 2 0.2323 3.859 #Average Value
pair_coeff    3 3 0.2765 4.043 #CHNOS
pair_coeff    4 4 0.2506 3.846 #CHON
pair_coeff    5 5 0.2506 3.846 #CHON
delete_atoms  overlap 0.5 all all
newton        on
thermo_modify lost ignore
min_style     cg
minimize      0.001 0.001 1000 1000
timestep      0.001
neighbor      0.3 bin
fix           1 all nvt temp 300 300 1
thermo        1000000
thermo_style  custom step temp ke pe etotal
dump          1 all xyz 1000000 DUMP.xyz
run 0
velocity all scale 300.0
"""

# Create a LAMMPS input file and write the script to it
with open('lammps_input.in', 'w') as lammps_input:
    lammps_input.write(lammps_script)

# Run LAMMPS with the input file
lammps_command = "lmp_serial -in lammps_input.in"
subprocess.call(lammps_command, shell=True)

# Simulation Step A
lammps_script_step_a = """
thermo_modify lost ignore
run 1000000000
"""

# Append the Step A script to the input file
with open('lammps_input.in', 'a') as lammps_input:
    lammps_input.write(lammps_script_step_a)

# Run LAMMPS with the updated input file
subprocess.call(lammps_command, shell=True)

# Simulation Step B
lammps_script_step_b = """
unfix 1
fix 2 all nve
region LEFT block INF -400 INF INF INF INF units box
region RIGHT block 400 INF INF INF INF INF units box
group LEFT region LEFT
group RIGHT region RIGHT
group Boundary union LEFT RIGHT
group Middle subtract all Boundary
fix 3 LEFT setforce -0.0001 0 0
fix 4 RIGHT setforce 0.0001 0 0
compute IF Middle group/group Boundary
thermo_style custom time lx c_IF
thermo_modify lost ignore
thermo_modify lost/bond ignore
run 1000000000
"""

# Append the Step B script to the input file
with open('lammps_input.in', 'a') as lammps_input:
    lammps_input.write(lammps_script_step_b)

# Run LAMMPS with the updated input file for Step B
subprocess.call(lammps_command, shell=True)
