import ase.io
# from ase import Atoms
# import numpy as np
from POSCAR_Parser import parse_poscar

filepath = input("Enter Input Poscar Coordinate File Path: ")
# atoms = ase.io.read(filename=filepath, format='vasp')
atoms = ase.io.read(filename=filepath, format='lammps-data')

# masses = {'Si': 28.086, 'O': 15.999, 'B': 10.811, 'Na': 22.990, 'Al': 26.982}
# for atom in atoms:
#     atom.mass = masses.get(atom.symbol)

filepath_out = filepath
lammps_file = f"{filepath_out}.data"
vasp_file = f"POSCAR-{filepath_out}"
# ase.io.write(filename=lammps_file, images=atoms, format='lammps-data',
#              specorder=['Si', 'O', 'B', 'Na', 'Al'], atom_style='charge', masses=True, atom_type_labels=True)

ase.io.write(filename=vasp_file, images=atoms, format='vasp')

# supercell_atoms = atoms

# data = parse_poscar(filepath)
# my_frac_positions = data['atomic_frac_positions']
# my_lattice_matrix = data['lattice_matrix']

# atoms.rotate((1, 0, 0), (1, 0, 0))
#atomsSuper = ase.build.make_supercell(atoms, [[3,0,0], [0,3,0], [0,0,3]])

# def generate_cells(atomic_frac_positions, lattice_matrix):
#     cells = {}
#     """
#     Generates a 3x3x3 supercell and a master list of all atoms for efficient analysis.
#     """
#     print("Generating coordinates for 27 cells...")
#     for i in range(-1, 2):
#         for j in range(-1, 2):
#             for k in range(-1, 2):
#                 cell_vector = np.array([i, j, k])
#                 cell = f"cell_{i}_{j}_{k}"
#                 current_cell_coords = {}
#                 for atom_type, frac_coords in atomic_frac_positions.items():
#                     translated_frac_coords = frac_coords + cell_vector
#                     cart_coords = np.dot(translated_frac_coords, lattice_matrix)
#                     current_cell_coords[atom_type] = cart_coords
#                 cells[cell] = current_cell_coords
#
#     print("Building master atom list for analysis...")
#     temp_list = []
#     for cell_key, cell_data in cells.items():
#         for atom_type, coords_array in cell_data.items():
#             for j, coords in enumerate(coords_array):
#                 temp_list.append({"type": atom_type, "index": j, "cell": cell_key, "coords": coords})
#     all_atoms_list = temp_list
#     return all_atoms_list
#
# all_atoms_list = generate_cells(my_frac_positions, my_lattice_matrix)
# new_lattice = my_lattice_matrix * 3
#
# symbols = [item['type'] for item in all_atoms_list]
# positions = [item['coords'] for item in all_atoms_list]
#
# supercell_atoms = Atoms(symbols=symbols, positions=positions, cell=new_lattice, pbc=True)
# supercell_atoms.wrap()

