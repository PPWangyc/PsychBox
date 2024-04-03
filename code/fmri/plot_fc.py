# plot functional connectivity matrix
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from nilearn import plotting
from nilearn import datasets
import argparse

# Parse the input arguments
parser = argparse.ArgumentParser(description='Plot functional connectivity matrix')
parser.add_argument('--fc_matrix', default='fc_matrix.npy', type=str, help='Functional connectivity matrix')
args = parser.parse_args()

# Load the correlation matrix
correlation_matrix = np.loadtxt(args.fc_matrix)

# load atlas
atlas = datasets.fetch_atlas_harvard_oxford('cort-maxprob-thr25-2mm')
atlas_filename = atlas['maps']
labels = atlas['labels']

# Plot the correlation matrix
sns.set(style='white')
plt.figure(figsize=(18, 14))
sns.heatmap(correlation_matrix, xticklabels=labels, yticklabels=labels, annot=False, cmap='coolwarm')
plt.title('Functional connectivity matrix')
plt.savefig('correlation_matrix.png')

