#!/bin/bash
#Template provided by Daniel Levitas of Indiana University
#Edits by Andrew Jahn, University of Michigan, 07.22.2020

#User inputs:
bids_root_dir=$HOME/Data/BREATHE_BIDS
subj=s106
nthreads=4
mem=20 #gb
container=docker #docker or singularity

#Begin:

#Convert virtual memory from gb to mb
mem=`echo "${mem//[!0-9]/}"` #remove gb at end
mem_mb=`echo $(((mem*1000)-5000))` #reduce some memory for buffer space during pre-processing

#export TEMPLATEFLOW_HOME=$HOME/.cache/templateflow
export FS_LICENSE=$HOME/Documents/fsl_license.txt

#Run fmriprep
qsiprep-docker $bids_root_dir $bids_root_dir/derivatives \
    participant \
    --participant-label $subj \
    --skip-bids-validation \
    --fs-license-file $FS_LICENSE \
    --nthreads $nthreads \
    --stop-on-first-crash \
    --output-resolution 1.2 \
    --mem_mb $mem_mb