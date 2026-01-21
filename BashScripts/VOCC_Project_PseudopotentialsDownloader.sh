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