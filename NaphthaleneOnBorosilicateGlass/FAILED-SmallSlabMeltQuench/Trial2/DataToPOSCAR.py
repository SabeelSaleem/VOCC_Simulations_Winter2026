from ase import Atoms
from ase.io import read, write
import numpy as np

filepath = input("Enter Input Poscar File Path: ")
atoms = read(filename=filepath, format='lammps-data')

type_map = {'Si': 1, 'O': 2, 'B': 3, 'Na': 4, 'Al': 5}
charges  = {'Si': 1.890, 'O': -0.945, 'B': 1.418, 'Na': 0.473, 'Al': 1.418}

my_types = [type_map[atom.symbol] for atom in atoms]
my_charges = [charges[atom.symbol] for atom in atoms]

restore_map = {1: 14, 2: 8, 3: 5, 4: 11, 5: 13}
atoms.numbers = np.array([restore_map[n] for n in atoms.numbers])

write(filename='POSCAR-SmallPillar', images=atoms, format='vasp')