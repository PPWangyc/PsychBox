import os
import glob
import pandas as pd
import argparse

# set up the argument parser
parser = argparse.ArgumentParser(description='Run fmriprep on all subjects in a BIDS dataset')
parser.add_argument('bids_root_dir', type=str, help='The root directory of the BIDS dataset')
parser.add_argument('nthreads', type=int, default=16, help='Number of threads to use for fmriprep')
parser.add_argument('mem', type=int, default=128, help='Amount of memory to use for fmriprep')
args = parser.parse_args()

bids_root_dir = args.bids_root_dir
nthreads = args.nthreads
mem = args.mem
# get subject list under bids_root_dir
subject_list = [x.split('/')[-1] for x in glob.glob(os.path.join(bids_root_dir, 'sub-*'))]
subject_list = [x.split('-')[-1] for x in subject_list]
print(subject_list)
# check if bids_root_dir has derivatives folder
if not os.path.exists(os.path.join(bids_root_dir, 'derivatives')):
    os.mkdir(os.path.join(bids_root_dir, 'derivatives'))
# check if bids_root_dir/derivatives has fmriprep folder
if not os.path.exists(os.path.join(bids_root_dir, 'derivatives', 'fmriprep')):
    os.mkdir(os.path.join(bids_root_dir, 'derivatives', 'fmriprep'))

for subject in subject_list:
    command = 'sbatch fmriprep_singularity.sh {} {} {} {}'.format(bids_root_dir, subject, nthreads, mem)
    print(command)
    os.system(command)

print('Done!')
