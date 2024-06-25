#!/bin/bash
#SBATCH --job-name=preproc_flair
#SBATCH --output=preproc_flair"%j".out
#SBATCH --error=preproc_flair."%j".err
#SBATCH --partition=normal
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=64G

FLAIR_PATH=${1}

module load matlab
cd ..
chmod +rx batch_preproc_structural_job.m
matlab -nodisplay -r "flair_path='${FLAIR_PATH}'; run('batch_preproc_structural.m');exit;"
cd lga