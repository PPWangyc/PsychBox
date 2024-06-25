#!/bin/bash
#SBATCH --job-name=wmh_flair
#SBATCH --output=wmh_flair"%j".out
#SBATCH --error=wmh_flair."%j".err
#SBATCH --partition=normal
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=64G
T1_PATH=${1}
FLAIR_PATH=${2}
THREASHOLD=${3}
cd ..
module load matlab
matlab -nodisplay -r "t1_path='${T1_PATH}'; flair_path='${FLAIR_PATH}'; threshold=${THREASHOLD}; run('run_lga.m');exit;"
cd lga