source "$Project_Root_Dir/scripts/VOCC_Project_Paths.sh"
source "$Project_Root_Dir/scripts/VOCC_Project_Modules.sh"

echo "--- Module Loading and Creating Conda Environment in \$Env_Name ---"

source "\$(conda info --base)/etc/profile.d/conda.sh"
conda create -n \$Env_Name python=\$Python_Ver -y
conda activate \$Env_Name

echo "--- Installing Python Libraries and Pseudopotentials ---"

pip install --upgrade pip
pip install --upgrade ase
pip install --upgrade pymatgen
pip install --upgrade mp_api

echo "--- Python Environment $Env_Name Created ---"