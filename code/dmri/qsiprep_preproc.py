import os
import sys
import glob
import argparse
import subprocess
import pandas as pd

bids_root_dir = 'PATH_TO_YOUR_BIDS_DATASET'
nthreads = 16
mem = 128
# get subject list under bids_root_dir
subject_list = [x.split('/')[-1] for x in glob.glob(os.path.join(bids_root_dir, 'sub-*'))]
subject_list = [x.split('-')[-1] for x in subject_list]
print(subject_list)
# check if bids_root_dir has derivatives folder
if not os.path.exists(os.path.join(bids_root_dir, 'derivatives')):
    os.mkdir(os.path.join(bids_root_dir, 'derivatives'))
# check if bids_root_dir/derivatives has qsiprep folder
if not os.path.exists(os.path.join(bids_root_dir, 'derivatives', 'qsiprep')):
    os.mkdir(os.path.join(bids_root_dir, 'derivatives', 'qsiprep'))

for subject in subject_list:
    command = 'sbatch qsiprep_singularity.sh {} {} {} {}'.format(bids_root_dir, subject, nthreads, mem)
    print(command)
    os.system(command)

print('Done!')
