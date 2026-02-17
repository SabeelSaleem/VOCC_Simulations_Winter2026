#!/bin/bash
#SBATCH --job-name=GlassGen
#SBATCH --partition=long         # Changed to long for 33 DFT Runs
#SBATCH --nodes=2                # 2 nodes for Large DFT simulation
#SBATCH --ntasks-per-node=20     # Uses all 20 cores on the standard node
#SBATCH --mem=8G                 # 16GB is plenty
#SBATCH --time=96:00:00          # 4 days (Safe limit for 'long' since max is 20 days)
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err

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

export OMP_NUM_THREADS=1 

# Define your site ID here
SITE_ID=1

echo "--- Starting 33 DFT Snapshots for Site $SITE_ID ---"

# Loop from 1 to 33
for i in {1..33}
do
    echo "Running Snapshot $i..."
    
    # Define filenames
    INFILE="NaphthaleneOnGlassSite${SITE_ID}Snapshot${i}.in"
    OUTFILE="NaphthaleneOnGlassSite${SITE_ID}Snapshot${i}.out"
    
    # Run Quantum Espresso
    # mpirun will automatically pick up the 40 cores from Slurm
    mpirun pw.x -in $INFILE > $OUTFILE
    
    echo "Snapshot $i complete."
done

echo "--- All Simulations finished ---"