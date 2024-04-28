import os
import argparse
import glob

# set up the argument parser
parser = argparse.ArgumentParser(description='Quality control for fmriprep outputs')
parser.add_argument('--bids_root_dir', type=str, help='The root directory of the BIDS dataset')
args = parser.parse_args()

bids_root_dir = args.bids_root_dir
fmriprep_dir = os.path.join(bids_root_dir, 'derivatives', 'fmriprep')

# get subject list under bids_root_dir
subject_list = [x.split('/')[-1] for x in glob.glob(os.path.join(bids_root_dir, 'sub-*'))]
subject_list = [x.split('-')[-1] for x in subject_list]

qc_results = []
for subject in subject_list:
    # check if exist session folder
    session_list = [x.split('/')[-1] for x in glob.glob(os.path.join(bids_root_dir, 'sub-%s' % subject, 'ses-*'))]
    session_list = [x.split('-')[-1] for x in session_list]

    for session in session_list:
        # check if exist fmriprep output
        if os.path.exists(os.path.join(fmriprep_dir, 'sub-%s' % subject, 'ses-%s' % session)):
            # get all files under func folder, and check if exist desc-preproc_bold.nii.gz
            func_files = glob.glob(os.path.join(fmriprep_dir, 'sub-%s' % subject, 'ses-%s' % session, 'func', '*'))
            if any('desc-preproc_bold.nii.gz' in x for x in func_files):
                qc_results.append('sub-%s_ses-%s: PASS' % (subject, session))
            else:
                qc_results.append('sub-%s_ses-%s: FAIL' % (subject, session))
        else:
            qc_results.append('sub-%s_ses-%s: FAIL' % (subject, session))

print(qc_results)