from ase.io import read, write
import numpy as np

filepath = input("Enter Input Poscar File Path: ")
atoms = read(filename=filepath, format='lammps-data')

type_map = {'Si': 1, 'O': 2, 'B': 3, 'Na': 4, 'Al': 5}
element_charges = {'Si': 4, 'O': -2, 'B': 3, 'Na': 1, 'Al': 3}
types = [type_map[atom.symbol] for atom in atoms]
charges = [element_charges[atom.symbol] for atom in atoms]
atoms.numbers = np.array(types)
atoms.set_initial_charges(charges)

restore_map = {1: 14, 2: 8, 3: 5, 4: 11, 5: 13}
atoms.numbers = np.array([restore_map[n] for n in atoms.numbers])

write(filename='POSCAR-RelaxedSlabV2', images=atoms, format='vasp')