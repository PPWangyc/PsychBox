# plot functional connectivity matrix
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from nilearn import datasets
import abagen
import argparse
import pandas as pd

# Parse the input arguments
parser = argparse.ArgumentParser(description='Plot functional connectivity matrix')
parser.add_argument('--fc_matrix', default='fc_matrix.npy', type=str, help='Functional connectivity matrix')
parser.add_argument('--atlas', default='schaefer', type=str, help='Atlas used to generate the functional connectivity matrix')
args = parser.parse_args()

# Load the correlation matrix
correlation_matrix = np.loadtxt(args.fc_matrix)

# load atlas
if args.atlas == 'schaefer':
    schaefer_atlas = datasets.fetch_atlas_schaefer_2018(n_rois=400, yeo_networks=7, resolution_mm=2)
    labels = schaefer_atlas['labels']
elif args.atlas == 'desikan':
    desikan_atlas = abagen.fetch_desikan_killiany()
    labels = pd.read_csv(desikan_atlas['info'])['label'].values

# Plot the correlation matrix
sns.set(style='white')
plt.figure(figsize=(18, 14))
sns.heatmap(correlation_matrix, xticklabels=labels, yticklabels=labels, annot=False, cmap='coolwarm')
plt.title('Functional connectivity matrix')
plt.savefig(f'{args.atlas}_fc_matrix.png')

