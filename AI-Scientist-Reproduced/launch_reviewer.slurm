#!/bin/bash
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=long
#SBATCH --output=./%x_%j.out

module load singularity
singularity exec --env-file .env -B ./data/AI-Scientist:/app --pwd /app -C aiScientist.sif python -u launch_reviewer.py