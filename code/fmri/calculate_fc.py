from nilearn import input_data, connectome, datasets
import numpy as np
import pandas as pd
import argparse
import os
import abagen

# Parse the input arguments
parser = argparse.ArgumentParser(description='Extract functional connectivity matrix')
parser.add_argument('--data_dir')
parser.add_argument('--output_dir')

args = parser.parse_args()

# Define the atlas you are using 
# Schaefer 400 parcellation
schaefer_atlas = datasets.fetch_atlas_schaefer_2018(n_rois=400, yeo_networks=7, resolution_mm=2)
schaefer_atlas_filename = schaefer_atlas.maps

desikan_atlas = abagen.fetch_desikan_killiany()
desikan_atlas_filename = desikan_atlas['image']

# Create a masker to extract time-series from the atlas regions
schaefer_masker = input_data.NiftiLabelsMasker(labels_img=schaefer_atlas_filename, standardize=True)
desikan_masker = input_data.NiftiLabelsMasker(labels_img=desikan_atlas_filename, standardize=True)

# Preprocessed fMRI data
data_dir = args.data_dir
output_dir = args.output_dir
os.makedirs(output_dir, exist_ok=True)
# get all files ending with .nii.gz
fmri_filenames = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.nii.gz')]
print('Found %d fMRI files' % len(fmri_filenames))
for fmri_filename in fmri_filenames:
    # load coufound file
    confounds = pd.read_csv(fmri_filename.replace('space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz', 'desc-confounds_timeseries.tsv'), sep='\t')
    # Identify and replace 'inf' and 'NaN' values
    confounds.replace([np.inf, -np.inf], np.nan, inplace=True)  # Replace 'inf' with 'NaN'
    confounds = confounds.fillna(confounds.mean(), inplace=True)  # Replace 'NaN' with the mean of each column
    print('fMRI data is located at: %s' % fmri_filename)
    time_series = schaefer_masker.fit_transform(fmri_filename, confounds=confounds)
    # Calculate correlation matrix
    correlation_matrix = connectome.ConnectivityMeasure(kind='correlation').fit_transform([time_series])[0]
    # Save the correlation matrix to a file
    save_path = os.path.join(output_dir, os.path.basename(fmri_filename).replace('space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz', 'schaefer400_correlation_matrix.npy'))

    print('Saving the schaefer400 correlation matrix to: %s' % save_path)
    np.savetxt(save_path, correlation_matrix)

    # Repeat the same process for the Desikan-Killiany atlas
    time_series = desikan_masker.fit_transform(fmri_filename, confounds=confounds)
    # Calculate correlation matrix
    correlation_matrix = connectome.ConnectivityMeasure(kind='correlation').fit_transform([time_series])[0]
    # Save the correlation matrix to a file
    save_path = os.path.join(output_dir, os.path.basename(fmri_filename).replace('space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz', 'desikan_correlation_matrix.npy'))

    print('Saving the correlation matrix to: %s' % save_path)
    np.savetxt(save_path, correlation_matrix)

print('Done!')