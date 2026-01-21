import ase.io
from ase.visualize import view

naphthalene_atoms = ase.io.read(filename='POSCAR-Naphthalene', format='vasp')
glass_atoms = ase.io.read(filename='POSCAR-Glass', format='vasp')

view(naphthalene_atoms)

