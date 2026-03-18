#!/bin/bash
#SBATCH --job-name=NaphthaleneOnGlassSite2
#SBATCH --partition=long         # Changed to long for 33 DFT Runs
#SBATCH --nodes=4                # 4 nodes for Large DFT simulation
#SBATCH --ntasks-per-node=20     # Uses all 20 cores on the standard node
#SBATCH --mem=0                  # Let system decide memory
#SBATCH --time=240:00:00          # 4 days (Safe limit for 'long' since max is 20 days)
#SBATCH --array=1-35%5		 # Run 1-35, max 5 at a time
#SBATCH --output=slurm-%A_%a.out
#SBATCH --error=slurm-%A_%a.err

echo "Date              = $(date)"
echo "Hostname          = $(hostname)"
echo "Working Directory = $(pwd)"

module purge
module load tbb/2021.13
module load compiler-rt/2024.2.1
module load compiler/2024.2.1
module load mkl/2024.2
module load mpi/2021.13
module load glibc/2.34-gcc-13.2.0-dtclx3b
module load gcc-runtime/13.2.0-gcc-13.2.0-24uno5v
module load miniforge3/4.8.3-4-Linux-x86_64-gcc-13.2.0

# Define your site ID here
SITE_ID=2
ID=$SLURM_ARRAY_TASK_ID

echo "--- Starting Glass and Naphthalene on $(hostname) ---"

if [ "$ID" -le 33 ]; then
    INFILE="NaphthaleneOnGlassSite${SITE_ID}Snapshot${ID}.in"
    OUTFILE="NaphthaleneOnGlassSite${SITE_ID}Snapshot${ID}.out"
elif [ "$ID" -eq 34 ]; then
    INFILE="GlassSite${SITE_ID}Snapshot1.in"
    OUTFILE="GlassSite${SITE_ID}Snapshot1.out"
elif [ "$ID" -eq 35 ]; then
    INFILE="NaphthaleneSite${SITE_ID}Snapshot1.in"
    OUTFILE="NaphthaleneSite${SITE_ID}Snapshot1.out"
fi

echo "--- Starting $INFILE on $(hostname) ---"

# Run Quantum Espresso
mpirun pw.x -in $INFILE > $OUTFILE

    echo "Snapshot $ID complete."
