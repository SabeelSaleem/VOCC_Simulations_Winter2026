import numpy as np
import pandas as pd

def calculate_pah_persistence(df, temp_K, A_factor=1e12):
    """
    Calculates K2-SURF based desorption and persistence metrics for a DataFrame of PAHs.

    Parameters:
    - df: Pandas DataFrame containing 'Molecule', 'E_binding', and 'Slab_Area_A2'
    - temp_K: Temperature in Kelvin (Scalar or numpy array)
    - A_factor: Pre-exponential factor (s^-1) (For physisorbed species, A = 10^12. For chemisorbed species, A = 10^14.)
    - K_Chem_Loss: First-order chemical decay rate coefficient (s^-1) (Look at literature, k_s,PAH,max in K2-SURF)

    Returns:
    - A new DataFrame with all the calculated metrics added as columns.
    """
    # Constants
    kb_eV = 8.617333262145e-5  # Boltzmann constant in eV/K
    kJ_eV = 1/96.485           # (eV/molecule)/(kJ/mol)

    # Make a copy of the dataframe to avoid modifying the original input
    results = df.copy()

    # 1. Desorption Rate Coefficient (k_d) The magnitude of the binding energy is the activation barrier for desorption
    activation_energy = np.abs(results['E_binding'])
    results['k_d (s^-1)'] = A_factor * np.exp((-activation_energy * kJ_eV) / (kb_eV * temp_K))

    # 2. Desorption Lifetime (tau_d) in days (np.where safely handles scenarios where k_d is effectively 0)
    results['tau_d (seconds)'] = np.where(results['k_d (s^-1)'] > 0, (1 / results['k_d (s^-1)']), np.inf)

    # 3. Surface Concentration and Flux (Convert area from Angstroms^2 to cm^2)
    area_cm2 = results['Slab_Area_A2'] * (10**-8)**2
    results['Surface_Conc (molec/cm^2)'] = results['Num_Molecules'] / area_cm2

    # Desorption Flux J_des = k_d * [PAH]_s (Flux of Naphthalene molecules leaving the surface)
    results['J_des (flux)'] = results['k_d (s^-1)'] * results['Surface_Conc (molec/cm^2)']

    # 4. Overall Persistence (Half-Life in days) Total loss = thermal desorption + chemical degradation
    k_total_loss = results['k_d (s^-1)'] + results['K_Chem_Loss']
    results['Overall_Half_Life (days)'] = (np.log(2) / k_total_loss) / 86400

    return results

# 1. Simulate loading your Quantum Espresso outputs into a Pandas DataFrame.
# (In the future, you can easily replace this with: df_pahs = pd.read_csv('my_qe_outputs.csv'))
data = {
    'Molecule': ['Naphthalene', 'Phenanthrene', 'Pyrene', 'Benzo[a]pyrene'],
    'Substrate': ['Graphene', 'Octanol', 'Octanol', 'Soot Aerosol'],
    'K_Chem_Loss': [0.0009, 0.0006, 0.0015, 0.0154],
    'Num_Molecules': [10, 1, 1, 1],
    'E_binding': [-86.8365, -75.5, -76.3, -86],  # deltaH_ads (kJ/mol) (PLACEHOLDERS FOR NOW)
    'Slab_Area_A2': [352.68, 352.68, 352.68, 352.68]  # Slab Surface Areas in Angstroms^2
}
df_pahs = pd.DataFrame(data)
temp_K = 234

# 2. Calculate Results at Room Temperature (300 K)
room_temp_results = calculate_pah_persistence(df_pahs, temp_K=temp_K, A_factor=1e17)

# 3. Display the results nicely
print(f"--- K2-SURF Persistence Results at {temp_K}K ---")
pd.options.display.float_format = '{:.2e}'.format
print(room_temp_results[['Molecule', 'Substrate', 'E_binding', 'k_d (s^-1)', 'tau_d (seconds)',
                         'Overall_Half_Life (days)']].to_string(index=False))