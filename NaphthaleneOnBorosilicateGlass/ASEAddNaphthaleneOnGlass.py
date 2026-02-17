from ase.io import read
from ase.visualize import view

filepath = input("Enter Input Poscar File Path: ")
atoms = read(filename=filepath, format='vasp')
atoms.wrap()

unique_elements = set(atoms.get_chemical_symbols())
print(f"ASE automatically detected these elements: {unique_elements}")

view(atoms)