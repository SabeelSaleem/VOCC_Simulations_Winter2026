from ase.io import read
from ase.visualize import view
import numpy as np

# 1. Load the file
print("Loading file...")
atoms = read('AmorphousBorosilicateGlassCube.data', format='lammps-data', style='charge')

# 2. Verify what ASE found
# This prints the unique elements ASE identified (likely {'Si', 'O', 'B', 'Na', 'Al'})
unique_elements = set(atoms.get_chemical_symbols())
print(f"ASE automatically detected these elements: {unique_elements}")

# 3. View the Structure
view(atoms)