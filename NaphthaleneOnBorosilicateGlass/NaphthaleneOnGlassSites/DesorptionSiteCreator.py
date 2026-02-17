from ase.io import read, write
import numpy as np

# --- CONFIGURATION SECTION ---
# Assumes files are named exactly 'NaphthaleneOnGlassSite1', etc.
site_id = 3
input_file = f'POSCAR-NaphthaleneOnGlassSite{site_id}'
input_prefix = "NaphthaleneOnGlassSite"

# Desorption settings
num_snapshots = 33
step_size = 0.5  # Angstroms to move in Z direction per snapshot

# Quantum Espresso Input Parameters
# YOU MUST EDIT THESE: ASE needs these to build a valid QE .in file
qe_input_data = {
    'control': {
        'calculation': 'scf',  # or 'relax' if you are constraining the slab
        'restart_mode': 'from_scratch',
        'pseudo_dir': '/home/sabeel/VOCC_Simulation/pseudopotentials/SSSP_Precision',
        'outdir': f'/home/sabeel/VOCC_Simulation/outputs/NaphthaleneOnGlassSite{site_id}',
        'tprnfor': True,
        'tstress': True,
        'disk_io': 'low'
    },
    'system': {
        'ecutwfc': 80,      # Set your cutoff
        'ecutrho': 360,     # Set your density cutoff
        # 'ibrav': 0        # ASE usually handles cell setup automatically
        'occupations': 'smearing',
        'smearing': 'gaussian',
        'degauss': 0.01,
        # 'assume_isolated': '2D', # Uncomment if you want slab corrections
    },
    'electrons': {
        'conv_thr': 1.0e-8,
        'mixing_beta': 0.3,
    }
}

# Define Pseudopotentials
# Map the element symbol to the filename of the PP you are using
pseudopotentials = {
    'C' : 'C.pbe-n-kjpaw_psl.1.0.0.UPF',
    'H' : 'H_ONCV_PBE-1.0.oncvpsp.upf',
    'Si': 'Si.pbe-n-rrkjus_psl.1.0.0.UPF',
    'B' : 'B_pbe_v1.01.uspp.F.UPF',
    'O' : 'O.pbe-n-kjpaw_psl.0.1.UPF',
    'Na': 'Na.paw.z_9.ld1.psl.v1.0.0-low.upf',
    'Al': 'Al.pbe-n-kjpaw_psl.1.0.0.UPF',
}

# K-Points
k_points = (1, 1, 1)  # Change to your desired grid, e.g., (2, 2, 1)



# --- MAIN SCRIPT ---
if not input_file:
    print("Error: No POSCAR or .vasp file found in this directory.")

print(f"--- Processing Site {site_id} ---")
print(f"Input File: {input_file}")

# 2. Read Structure
structure = read(filename=input_file, format='vasp')

# 3. Identify Molecule (C and H atoms)
symbols = np.array(structure.get_chemical_symbols())
mol_indices = [i for i, s in enumerate(symbols) if s in ['C', 'H']]

if not mol_indices:
    print("Error: No Carbon or Hydrogen atoms found to move.")

print(f"Moving {len(mol_indices)} atoms (C & H).")

# 4. Generate Snapshots
base_positions = structure.get_positions()

for i in range(1, num_snapshots + 1):
    # Calculate Shift
    z_shift = step_size * i

    # Apply Shift
    new_positions = base_positions.copy()
    new_positions[mol_indices, 2] += z_shift

    # Create Snapshot Object
    snapshot = structure.copy()
    snapshot.set_positions(new_positions)

    # Output Filename: NaphthaleneOnGlassSite1Snapshot1.in
    out_name = f"NaphthaleneOnGlassSite{site_id}Snapshot{i}.in"

    write(filename=out_name, images=snapshot, format='espresso-in', input_data=qe_input_data,
          pseudopotentials=pseudopotentials, kpts=k_points)

print(f"Success! Generated {num_snapshots} QE input files in this folder.")
