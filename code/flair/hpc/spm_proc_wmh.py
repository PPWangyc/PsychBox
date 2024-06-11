import os
import glob
import argparse

# set up the argument parser
parser = argparse.ArgumentParser(description='Run fmriprep on all subjects in a BIDS dataset')
parser.add_argument('--bids_root_dir', type=str, help='The root directory of the BIDS dataset')
args = parser.parse_args()

bids_root_dir = args.bids_root_dir
# get subject list under bids_root_dir
subject_list = [x.split('/')[-1] for x in glob.glob(os.path.join(bids_root_dir, 'sub-*'))]
subject_list = [x.split('-')[-1] for x in subject_list]
print(subject_list)
# check if bids_root_dir has derivatives folder
if not os.path.exists(os.path.join(bids_root_dir, 'derivatives')):
    os.mkdir(os.path.join(bids_root_dir, 'derivatives'))
# check if bids_root_dir/derivatives has fmriprep folder
if not os.path.exists(os.path.join(bids_root_dir, 'derivatives', 'spm')):
    os.mkdir(os.path.join(bids_root_dir, 'derivatives', 'spm'))

for subject in subject_list:
    flair_path = os.path.join(bids_root_dir, 'derivatives','spm', 'sub-{}'.format(subject), 'ses-*', 'anat', 'wsub-{}*FLAIR_preproc.nii'.format(subject))
    flair_files = glob.glob(flair_path)
    print(flair_path)
    assert len(flair_files) == 1, 'Incorrect number of FLAIR files found for subject {}: {}'.format(subject, flair_files)
    session = flair_files[0].split('/')[-3]
    command = 'sbatch wmh_process.sh {}'.format(flair_files[0])
    print(command)
    os.system(command)

print('Done!')
