#!/bin/bash
#SBATCH -J fmriprep
#SBATCH --time=48:00:00
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=32G
##SBATCH -p normal,owners  # Queue names you can submit to
# Outputs ----------------------------------
#SBATCH -o log/%x-%A-%a.out

#User inputs:
bids_root_dir=${1}
subj=${2}
nthreads=${3}
mem=${4} #gb

#Convert virtual memory from gb to mb
mem=`echo "${mem//[!0-9]/}"` #remove gb at end
mem_mb=`echo $(((mem*1000)-5000))` #reduce some memory for buffer space during pre-processing

#export TEMPLATEFLOW_HOME=$HOME/.cache/templateflow
export FS_LICENSE=$HOME/fsl_license.txt

unset PYTHONPATH

singularity run $OAK/ppwang/fmriprep_23.2.1.simg \
    $bids_root_dir $bids_root_dir/derivatives/fmriprep \
    participant \
    --participant-label $subj \
    --skip-bids-validation \
    --md-only-boilerplate \
    --fs-license-file $FS_LICENSE \
    --nthreads $nthreads \
    --stop-on-first-crash \
    --mem_mb $mem_mb \
    --work-dir $SCRATCH/Work
