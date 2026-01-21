Project_Name="VOCC_Simulation"
Env_Name="$Project_Name"
Python_Ver="3.12"
Project_Root_Dir=$(pwd)

echo "--- Beginning Installation for $Project_Name ---"
echo "--- Installation Directory: $Project_Root_Dir ---"

# Makes the Directories. Don't change these or move files around, the code will break.

mkdir -p "$Project_Root_Dir/scripts"
mkdir -p "$Project_Root_Dir/pseudopotentials"
mkdir -p "$Project_Root_Dir/pseudopotentials/SSSP_Efficiency"
mkdir -p "$Project_Root_Dir/pseudopotentials/SSSP_Precision"
mkdir -p "$Project_Root_Dir/inputs"
mkdir -p "$Project_Root_Dir/outputs"
mkdir -p "$Project_Root_Dir/calculations"
mkdir -p "$Project_Root_Dir/structures"

# Project_Root_Dir is defined in the VOCC_Initialization Script but not anywhere else.
# We need to make sure it gets added to all other scripts where:
# Project_Root_Dir="$Project_Root_Dir" Would write the EOT with Project_Root_Dir=Whatever/Project/Directory/Is/Defined/As
# Scripts_Dir="\$Project_Root_Dir/scripts" Would write the EOT with Scripts_Dir="$Project_Root_Dir/scripts
#Difference is the first has no \ and fills the variable while second has slash and doesn't fill what the variable means

# Example : source "$Project_Root_Dir/scripts/VOCC_Project_Paths.sh"                (Initialization.sh)
# Shows as: source "/home/sabeel/VOCC_Simulation/scripts/VOCC_Project_Paths.sh"     (HelperScriptVP.sh)


cat <<EOT > "$Project_Root_Dir/scripts/VOCC_Project_Paths.sh"
export Project_Name="$Project_Name"
export Env_Name="$Env_Name"
export Python_Ver="$Python_Ver"

export Project_Root_Dir="$Project_Root_Dir"
export Scripts_Dir="\$Project_Root_Dir/scripts"
export Pseudopotentials_Dir="\$Project_Root_Dir/pseudopotentials"
export Efficiency_Pseudopotentials_Dir="\$Pseudopotentials_Dir/SSSP_Efficiency"
export Precision_Pseudopotentials_Dir="\$Pseudopotentials_Dir/SSSP_Precision"
export Structures_Dir="\$Project_Root_Dir/structures"
export Inputs_Dir="\$Project_Root_Dir/inputs"
export Outputs_Dir="\$Project_Root_Dir/outputs"
export Calculations_Dir="\$Project_Root_Dir/calculations"
EOT

cat <<EOT > "$Project_Root_Dir/scripts/VOCC_Project_Modules.sh"
module purge

module load tbb/2021.13
module load compiler-rt/2024.2.1

module load compiler/2024.2.1
module load mkl/2024.2
module load mpi/2021.13

module load miniforge3/4.8.3-4-Linux-x86_64-gcc-13.2.0
EOT

# Pseudopotentials Downloader. Change the link to the latest download link for most up to date pseudopotentials.
cat <<EOT > "$Project_Root_Dir/scripts/VOCC_Project_PseudopotentialsDownloader.sh"
#!/bin/bash
source "$Project_Root_Dir/scripts/VOCC_Project_Paths.sh"

echo "--- Downloading Pseudopotentials ---"

echo "Downloading SSSP Efficiency to: \$Efficiency_Pseudopotentials_Dir"
URL_Eff="https://archive.materialscloud.org/api/records/rcyfm-68h65/files/SSSP_1.3.0_PBE_efficiency.tar.gz/content"
wget -O "\$Efficiency_Pseudopotentials_Dir/efficiency.tar.gz" "\$URL_Eff"
tar -xzvf "\$Efficiency_Pseudopotentials_Dir/efficiency.tar.gz" -C "\$Efficiency_Pseudopotentials_Dir"

echo "Downloading SSSP Precision to: \$Precision_Pseudopotentials_Dir"
URL_Prec="https://archive.materialscloud.org/api/records/rcyfm-68h65/files/SSSP_1.3.0_PBE_precision.tar.gz/content"
wget -O "\$Precision_Pseudopotentials_Dir/precision.tar.gz" "\$URL_Prec"
tar -xzvf "\$Precision_Pseudopotentials_Dir/precision.tar.gz" -C "\$Precision_Pseudopotentials_Dir"

echo "--- Download Complete ---"
EOT

# PyEnvCreate creates a python environment with the same name as Env Name which is defined at the top of initialization.
# Python Environment Libraries can be defined here. They can also be added manually within the environment.
cat <<EOT > "$Project_Root_Dir/scripts/VOCC_Project_PyEnvCreate.sh"
#!/bin/bash
source "$Project_Root_Dir/scripts/VOCC_Project_Paths.sh"
source "$Project_Root_Dir/scripts/VOCC_Project_Modules.sh"

echo "--- Module Loading and Creating Conda Environment in \$Env_Name ---"

source "\$(conda info --base)/etc/profile.d/conda.sh"
conda create -n \$Env_Name python=\$Python_Ver -y
conda activate \$Env_Name

echo "--- Installing Python Libraries and Pseudopotentials ---"

pip install --upgrade pip
pip install --upgrade ase pymatgen mp_api

echo "--- Python Environment \$Env_Name Created ---"
EOT

# Made this so "source SimStart.sh" starts up simulation environment and anything else I need automatically
cat <<EOT > "$Project_Root_Dir/SimStart.sh"
#!/bin/bash
source "$Project_Root_Dir/scripts/VOCC_Project_Paths.sh"
source "$Project_Root_Dir/scripts/VOCC_Project_Modules.sh"

source "\$(conda info --base)/etc/profile.d/conda.sh"
conda activate \$Env_Name

echo "--- VOCC Simulation Environment Activated ---"
EOT

echo "--- Moving Scripts to $Project_Root_Dir/scripts ---"
mv "$Project_Root_Dir/POSCAR_Parser.py" "$Project_Root_Dir/scripts/"
# Move all other .py files to scripts folder

echo "--- Running Initialization Scripts ---"
source "$Project_Root_Dir/scripts/VOCC_Project_PseudopotentialsDownloader.sh"
source "$Project_Root_Dir/scripts/VOCC_Project_PyEnvCreate.sh"
# Run all other .sh helper scripts

echo "--- Initialization Complete ---"
mv "$" "$Project_Root_Dir/scripts/"