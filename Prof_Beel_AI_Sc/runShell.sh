#!/bin/bash
module load singularity
singularity shell -B ./data/AI-Scientist:/app --pwd /app -C aiScientist.sif
