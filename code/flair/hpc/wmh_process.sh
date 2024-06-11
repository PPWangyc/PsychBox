#!/bin/bash
#SBATCH --job-name=wmh_flair
#SBATCH --output=wmh_flair"%j".out
#SBATCH --error=wmh_flair."%j".err
#SBATCH --partition=normal
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=64G

FLAIR_PATH=${1}

module load matlab
matlab -nodisplay -r "flair_path='${FLAIR_PATH}'; run('run_lst.m');exit;"