import numpy as np

def parse_poscar(filepath):
    """
    Parses a POSCAR file.
    """
    data = {}
    data['filepath'] = filepath
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    title = lines[0]
    data['title'] = title
    scaling_factor = float(lines[1])
    data['scaling_factor'] = scaling_factor
    a_vec = np.array([float(x) for x in lines[2].split()])
    b_vec = np.array([float(x) for x in lines[3].split()])
    c_vec = np.array([float(x) for x in lines[4].split()])
    lattice_matrix = np.array([a_vec, b_vec, c_vec]) * scaling_factor
    data['lattice_matrix'] = lattice_matrix
    atom_types = lines[5].split()
    data['atom_types'] = atom_types
    atom_counts = list(map(int, lines[6].split()))
    data['atom_counts'] = atom_counts
    data['atom_counts_dict'] = dict(zip(atom_types, atom_counts))

    coord_start_line = 7
    if lines[7].lower().startswith('s'):
        coord_start_line += 1
    positions_start_line = coord_start_line + 1
    total_atoms = sum(atom_counts)
    frac_positions_raw = lines[positions_start_line: positions_start_line + total_atoms]

    frac_positions_dict = {}
    index = 0
    for atom_type, count in zip(atom_types, atom_counts):
        temp_positions_list = []
        for _ in range(count):
            coords = list(map(float, frac_positions_raw[index].split()[:3]))
            temp_positions_list.append(coords)
            index += 1
        frac_positions_dict[atom_type] = np.array(temp_positions_list)
    atomic_frac_positions = frac_positions_dict
    data['atomic_frac_positions'] = atomic_frac_positions
    return data