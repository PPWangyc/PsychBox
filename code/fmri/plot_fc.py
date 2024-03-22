# plot functional connectivity matrix
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from nilearn import plotting
from nilearn import datasets

# Load the correlation matrix
correlation_matrix = np.loadtxt('correlation_matrix.npy')

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

