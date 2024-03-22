from nilearn import input_data, connectome, datasets
import numpy as np

# Define the atlas you are using (for example, the Harvard-Oxford atlas)
atlas = datasets.fetch_atlas_harvard_oxford('cort-maxprob-thr25-2mm')
atlas_filename = atlas['maps']
labels = atlas['labels']

print('Atlas ROIs are located in nifti image (4D) at: %s' % atlas_filename)

# Create a masker to extract time-series from the atlas regions
masker = input_data.NiftiLabelsMasker(labels_img=atlas_filename, standardize=True)

# Preprocessed fMRI data
fmri_filenames = '/Users/ppwang/Data/ACT_UR_BIDS/derivatives/sub-0105/ses-01/func/sub-0105_ses-01_task-rest_space-MNI152NLin2009cAsym_res-2_desc-preproc_bold.nii.gz'
counfounds = '/Users/ppwang/Data/ACT_UR_BIDS/derivatives/sub-0105/ses-01/func/sub-0105_ses-01_task-rest_desc-confounds_timeseries.tsv'

# load coufound file
import pandas as pd
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
np.savetxt('correlation_matrix.npy', correlation_matrix)