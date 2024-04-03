from nilearn import input_data, connectome, datasets
import numpy as np
import pandas as pd
import argparse
import os

# Parse the input arguments
parser = argparse.ArgumentParser(description='Extract functional connectivity matrix')
parser.add_argument('--bids_root_dir', default='/Users/ppwang/Data/ACT_UR_BIDS', type=str, help='Root directory of the BIDS dataset')
parser.add_argument('--subject', default='0105', type=str, help='Subject ID')
parser.add_argument('--session', default='01', type=str, help='Session ID')

args = parser.parse_args()

# Define the atlas you are using (for example, the Harvard-Oxford atlas)
atlas = datasets.fetch_atlas_harvard_oxford('cort-maxprob-thr25-2mm')
atlas_filename = atlas['maps']
labels = atlas['labels']

# Create a masker to extract time-series from the atlas regions
masker = input_data.NiftiLabelsMasker(labels_img=atlas_filename, standardize=True)

# Preprocessed fMRI data
fmri_filenames = os.path.join(args.bids_root_dir, 'derivatives', 'fmriprep', 'sub-%s' % args.subject, 'ses-%s' % args.session, 'func', 'sub-%s_ses-%s_task-rest_space-MNI152NLin2009cAsym_res-2_desc-preproc_bold.nii.gz' % (args.subject, args.session))
counfounds = os.path.join(args.bids_root_dir, 'derivatives', 'fmriprep', 'sub-%s' % args.subject, 'ses-%s' % args.session, 'func', 'sub-%s_ses-%s_task-rest_desc-confounds_timeseries.tsv' % (args.subject, args.session))
print('fMRI data is located at: %s' % fmri_filenames)
print('Confounds file is located at: %s' % counfounds)

# load coufound file
confounds = pd.read_csv(counfounds, sep='\t')
# Identify and replace 'inf' and 'NaN' values
counfounds = confounds.replace([np.inf, -np.inf], np.nan, inplace=True)  # Replace 'inf' with 'NaN'
counfounds = confounds.fillna(confounds.mean(), inplace=True)  # Replace 'NaN' with the mean of each column

# Extract the time-series
time_series = masker.fit_transform(fmri_filenames,
                                      confounds=counfounds)

# Calculate correlation matrix
correlation_matrix = connectome.ConnectivityMeasure(kind='correlation').fit_transform([time_series])[0]

# Optionally, apply Fisher Z-transformation
z_matrix = np.arctanh(correlation_matrix)

# Save the correlation matrix to a file
np.savetxt('fc_matrix_sub-{}_ses-{}.npy'.format(args.subject, args.session), correlation_matrix)