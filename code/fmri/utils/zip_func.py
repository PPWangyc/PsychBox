import os
import argparse
import zipfile
import glob

argparser = argparse.ArgumentParser(description='Zip preprocessed functional data from fmriprep')

argparser.add_argument('--bids_root_dir', type=str, help='Path to BIDS root directory')
argparser.add_argument('--output_dir', type=str, default='.', help='Output directory for zipped files')

args = argparser.parse_args()

bids_root_dir = args.bids_root_dir
output_dir = args.output_dir

# Get all functional folders in derivatives/fmriprep
func_folders = [os.path.join(root, name)
                for root, dirs, files in os.walk(os.path.join(bids_root_dir, 'derivatives', 'fmriprep'))
                for name in dirs
                if 'func' in name]

preproc_bold_files = []
preproc_confounds_files = []
for func_folder in func_folders:
    preproc_bold = os.path.join(func_folder, '*desc-preproc_bold.nii.gz')
    preproc_confounds = os.path.join(func_folder, '*desc-confounds_timeseries.tsv')
    assert len(glob.glob(preproc_bold)) == 1, f'Found {len(glob.glob(preproc_bold))} preprocessed bold files in {func_folder}'
    assert len(glob.glob(preproc_confounds)) == 1, f'Found {len(glob.glob(preproc_confounds))} preprocessed confounds files in {func_folder}'
    preproc_bold_files.extend(glob.glob(preproc_bold))
    preproc_confounds_files.extend(glob.glob(preproc_confounds))

print(f'Found {len(preproc_bold_files)} preprocessed bold files')
print(f'Found {len(preproc_confounds_files)} preprocessed confounds files')

# Zip preprocessed confounds files to 1 zip file
with zipfile.ZipFile(os.path.join(output_dir, 'preproc_confounds.zip'), 'w') as zipf:
    for preproc_confounds_file in preproc_confounds_files:
        zipf.write(preproc_confounds_file, os.path.basename(preproc_confounds_file))
print(f'Zipped {len(preproc_confounds_files)} preprocessed confounds files to {os.path.join(output_dir, "preproc_confounds.zip")}')

# Zip preprocessed bold files to 1 zip file
with zipfile.ZipFile(os.path.join(output_dir, 'preproc_bold.zip'), 'w') as zipf:
    for preproc_bold_file in preproc_bold_files:
        zipf.write(preproc_bold_file, os.path.basename(preproc_bold_file))
print(f'Zipped {len(preproc_bold_files)} preprocessed bold files to {os.path.join(output_dir, "preproc_bold.zip")}')

