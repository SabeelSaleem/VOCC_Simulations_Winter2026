from ase.io import read, write
from ase.build import cut
import numpy as np

filepath = input("Enter Input Poscar File Path: ")
atoms = read(filename=filepath, format='vasp')
atoms.wrap()

# type_map = {'Si': 1, 'O': 2, 'B': 3, 'Na': 4, 'Al': 5}
element_charges = {'Si': 4, 'O': -2, 'B': 3, 'Na': 1, 'Al': 3}

# types = [type_map[atom.symbol] for atom in atoms]
charges = [element_charges[atom.symbol] for atom in atoms]
# atoms.numbers = np.array(types)
atoms.set_initial_charges(charges)

print(f"Original Count: {len(atoms)}")

# We DO NOT set target_z yet. We keep the full length.
# target_x = 12.0
# target_y = 12.0
#
# # Filter atoms
# atoms = atoms[atoms.positions[:, 0] < target_x]
# atoms = atoms[atoms.positions[:, 1] < target_y]
#
# # Shrink the box X and Y, Cut some Z
# atoms.cell[0, 0] = target_x
# atoms.cell[1, 1] = target_y
# atoms.cell[2, 2] = 20.0

# Center in X and Y
# atoms.center(axis=0)
# atoms.center(axis=1)

atoms = cut(atoms, a=(0.5, 0, 0), b=(0, 0.5, 0), c=(0, 0, 0.35), clength=None, origo=(0, 0, 0),
    nlayers=None, extend=1.0, tolerance=0.01, maxatoms=None)

initial_count = len(atoms)
print(f"Atoms after cutting slab: {initial_count}")

max_iter = 1000
for i in range(max_iter):
    current_charges = atoms.get_initial_charges()
    net_charge = sum(current_charges)

    # Success Check
    if abs(net_charge) < 0.25:  # Tolerance
        print(f"SUCCESS: Neutralized at step {i}. Final Charge: {net_charge:.5f}")
        break

    # Find Surface Atoms (Top 3 Angstroms)
    z_positions = atoms.positions[:, 2]
    top_z = np.max(z_positions)
    surface_indices = [idx for idx, z in enumerate(z_positions) if z > top_z - 3.0]

    # Selection Logic
    if net_charge > 0:
        candidates = [idx for idx in surface_indices if atoms[idx].charge != 2]     # Remove Cation
    else:
        candidates = [idx for idx in surface_indices if atoms[idx].charge == -2]    # Remove Anion

    if not candidates:
        print("Warning: Stuck! No surface atoms found to remove.")
        break

    # Delete Highest
    highest = max(candidates, key=lambda idx: atoms.positions[idx, 2])
    del atoms[highest]

print(f"New Count: {len(atoms)} (Ready for Melt-Quench)")

write_file = 'SlabV3'

write(filename=f"{write_file}.data", images=atoms, format='lammps-data',
      atom_style='charge', masses=True, atom_type_labels=True)
# restore_map = {1: 14, 2: 8, 3: 5, 4: 11, 5: 13}
# atoms.numbers = np.array([restore_map[n] for n in atoms.numbers])
write(filename=f'POSCAR-{write_file}', images=atoms, format='vasp')
print(f"Done. Created {write_file}' files.")