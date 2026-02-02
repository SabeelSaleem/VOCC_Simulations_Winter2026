import ase.io

print("--- Starting Script to Convert sdf Coordinate File Format ---")

filepath = input("Enter Input Coordinate File Name (With .cif): ")

filepath_out = filepath.strip(".cif")
vasp_file = f"POSCAR-{filepath_out}"
QE_file = f"{filepath_out}.in"

atoms = ase.io.read(filename=filepath, format='cif')

# Lattice requirements for VASP
# atoms.center(vacuum=5.0, axis=(0, 1))   # Axis 0 = X, Axis 1 = Y
# atoms.center(vacuum=2.5, axis=2)        # Axis 3 = Z

# Psuedopotential requirements for QE
dummy_pseudos = {'B': 'B_Placeholder.upf', 'Si': 'Si_Placeholder.upf',
                 'O': 'O_Placeholder.upf', 'Al': 'Al_Placeholder.upf', 'Na': 'Na_Placeholder.upf'}

ase.io.write(filename=vasp_file, images=atoms, format='vasp')
ase.io.write(filename=QE_file, images=atoms, format='espresso-in', pseudopotentials=dummy_pseudos)

print("--- Conversion Complete ---")