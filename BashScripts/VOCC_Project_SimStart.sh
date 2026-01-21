source "$Project_Root_Dir/scripts/VOCC_Project_Paths.sh"
source "$Project_Root_Dir/scripts/VOCC_Project_Modules.sh"

source "\$(conda info --base)/etc/profile.d/conda.sh"
conda activate \$Env_Name

echo "--- VOCC Simulation Environment Activated ---"