#!/bin/bash
#SBATCH -J first_level_analysis
#SBATCH --time=48:00:00
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=32G
##SBATCH -p normal,owners  # Queue names you can submit to
# Outputs ----------------------------------
#SBATCH -o log/%x-%A-%a.out

# echo start time
echo "Start time: $(date)"

FSF_FILE=$1

# Run the analysis
feat $FSF_FILE

# echo end time
echo "End time: $(date)"