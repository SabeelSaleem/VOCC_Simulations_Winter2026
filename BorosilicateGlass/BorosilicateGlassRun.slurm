#!/bin/bash
#SBATCH --job-name=GlassGen
#SBATCH --partition=medium       # Changed to 'medium' based on your sinfo
#SBATCH --nodes=1                # 1 node is enough for ~4200 atoms
#SBATCH --ntasks-per-node=20     # Uses all 20 cores on the standard node
#SBATCH --mem=8G                 # 8GB is plenty
#SBATCH --time=04:00:00          # 4 hours (Safe limit for 'medium')
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

echo "--- Starting Simulation ---"
mpirun -np 20 lmp -in BorosilicateGlass_Buckingham.in
echo "--- Simulation finished ---"