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

fail_list = []
for subject in subject_list:
    try:
        flair_path = os.path.join(bids_root_dir, 'sub-{}'.format(subject), 'ses-*', 'anat', 'sub-{}*FLAIR.nii.gz'.format(subject))
        flair_files = glob.glob(flair_path)
        assert len(flair_files) == 1, 'Incorrect number of FLAIR files found for subject {}: {}'.format(subject, flair_files)
        session = flair_files[0].split('/')[-3]
        # make directory for each subject in derivatives folder
        new_flair_dir = os.path.join(bids_root_dir, 'derivatives', 'spm', 'sub-{}'.format(subject), '{}'.format(session), 'anat')
        os.makedirs(new_flair_dir, exist_ok=True)
        # copy the flair file to the new directory
        os.system('cp {} {}'.format(flair_files[0], new_flair_dir))
        # gunzip the flair file
        os.system('gunzip {}'.format(os.path.join(new_flair_dir, flair_files[0].split('/')[-1])))
        # get the path of the gunzipped flair file
        new_flair_path = os.path.join(new_flair_dir, flair_files[0].split('/')[-1].replace('.gz', ''))
        command = 'sbatch flair_preproc.sh {}'.format(new_flair_path)
        print(command)
        os.system(command)
    except Exception as e:
        print('Error processing subject {}: {}'.format(subject, e))
        fail_list.append(subject)

if len(fail_list) > 0:
    print('Failed to process the following subjects: {}'.format
            (fail_list))
else:
    print('All subjects processed successfully!')

print('Done!')
