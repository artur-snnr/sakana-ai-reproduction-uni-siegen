#!/bin/bash
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=long
#SBATCH --output=./%x_%j.out

module load singularity
singularity exec --env-file .env -B ./data/AI-Scientist:/app --pwd /app -C aiScientist.sif python -u launch_scientist.py --model "gpt-4o-2024-05-13" --experiment knn --num-ideas 10 # --skip-idea-generation # <- Uncomment to skip idea generation