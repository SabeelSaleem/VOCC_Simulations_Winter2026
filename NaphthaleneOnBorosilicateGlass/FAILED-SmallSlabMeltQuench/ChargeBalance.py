from ase.io import read, write
import numpy as np

# 1. LOAD & WRAP
# ---------------------------------------------------------
filepath = input("Enter Input Poscar Coordinate File Path: ")
atoms = read(filename=filepath, format='vasp')
atoms.wrap()

# 2. EXACT CHARGES (The Fix)
# ---------------------------------------------------------
# These values sum to EXACTLY zero with Oxygen (-0.945).
charges = {
    'Si': 4,
    'O': -2,
    'B': 3,
    'Na': 1,
    'Al': 3
}

type_map = {'Si': 1, 'O': 2, 'B': 3, 'Na': 4, 'Al': 5}

my_types = [type_map[atom.symbol] for atom in atoms]
my_charges = [charges[atom.symbol] for atom in atoms]

atoms.set_initial_charges(my_charges)
atoms.numbers = np.array(my_types)

# 3. CUT SLAB
# ---------------------------------------------------------
# Keep 60% of the box. This is plenty for a rigid slab.
z_length = atoms.cell[2, 2]
z_cutoff = z_length * 0.40
atoms = atoms[atoms.positions[:, 2] < z_cutoff]

atoms.cell[2, 2] = z_cutoff # Add Vacuum

initial_count = len(atoms)
print(f"Atoms after cutting slab: {initial_count}")

# 4. NEUTRALIZE SURFACE (With Safety Brake)
# ---------------------------------------------------------
max_iter = 1000

for i in range(max_iter):
    current_charges = atoms.get_initial_charges()
    net_charge = sum(current_charges)

    # A. Success Check
    if abs(net_charge) < 0.02:
        print(f"SUCCESS: Neutralized at step {i}. Final Charge: {net_charge:.5f}")
        break

    # B. Safety Brake (Stop if we delete too many)
    if (initial_count - len(atoms)) > 100:
        print("STOPPING: Deleting too many atoms! The slab is becoming unstable.")
        break

    # C. Find Surface Atoms (Top 3 Angstroms)
    z_positions = atoms.positions[:, 2]
    top_z = np.max(z_positions)
    surface_indices = [idx for idx, z in enumerate(z_positions) if z > top_z - 3.0]

    # D. Selection Logic
    if net_charge > 0:
        candidates = [idx for idx in surface_indices if atoms[idx].number != 2] # Remove Cation
    else:
        candidates = [idx for idx in surface_indices if atoms[idx].number == 2] # Remove Anion

    if not candidates:
        print("Warning: Stuck! No surface atoms found to remove.")
        break

    # E. Delete Highest
    highest = max(candidates, key=lambda idx: atoms.positions[idx, 2])
    del atoms[highest]

# 5. SAVE OUTPUTS
# ---------------------------------------------------------
print(f"Final Atom Count: {len(atoms)}")
atoms.wrap()

# LAMMPS Data
write(filename='NeutralSlab.data', images=atoms, format='lammps-data', atom_style='charge')

# POSCAR (Restore real atomic numbers)
restore_map = {1: 14, 2: 8, 3: 5, 4: 11, 5: 13}
atoms.numbers = np.array([restore_map[n] for n in atoms.numbers])
write(filename='POSCAR_NeutralSlab', images=atoms, format='vasp')

print("Done. Created 'NeutralSlab.data'")