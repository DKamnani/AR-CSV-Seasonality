#Code to find the spatial correlation between the different consistency algorithms
import numpy as np
import glob
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import warnings
import dask.array as da
import dask
import matplotlib as mpl
import xarray as xr
import numpy.ma as ma

#Read the consistency scale values from the different algorithms
Cascade_bard=np.load('CBcsv.npy')
Mundhenk=np.load('MDcsv.npy')
ClimateNet_DL=np.load('CNcsv.npy')
Reid=np.load('RDcsv.npy')
Guan_Waliser=np.load('GWcsv.npy')
#WA=np.load('WAcsv.npy')
IVT=np.load('IVTcsv.npy')
IVT16=np.load('IVTcsv16yrs.npy')
WA16=np.load('WAcsv16yrs.npy')
print(Guan_Waliser.shape)

# Put your datasets in a list
datasets = [IVT, Cascade_bard, Mundhenk, Guan_Waliser, Reid, ClimateNet_DL,IVT16,WA16]

# Calculate the number of datasets
num_datasets = len(datasets)

# Initialize an empty correlation matrix
correlation_matrix = np.zeros((num_datasets, num_datasets))

# Calculate the correlation coefficients
for i in range(num_datasets):
    for j in range(num_datasets):
        data1 = datasets[i]
        data2 = datasets[j]
        
        # Filter out NaN values from both datasets
        valid_indices = ~np.logical_or(np.isnan(data1), np.isnan(data2))
        data1_valid = data1[valid_indices]
        data2_valid = data2[valid_indices]
        
        # Calculate the correlation coefficient for the valid data
        correlation_matrix[i, j] = np.corrcoef(data1_valid, data2_valid)[0, 1]

# Algorithm labels
algorithm_labels = ["IVT","TECA-BARD v1.0.1", "Mundhenk", "Guan and Waliser", "Reid et al." ,"ClimateNet","IVT16","WA16"]

# Print the correlation matrix
print("Correlation Matrix:")
print(correlation_matrix)

"""
# Optional: Print the correlation matrix with labels
print("Correlation Matrix with Labels:")
for i in range(num_datasets):
    for j in range(num_datasets):
        print(f"{algorithm_labels[i]} vs {algorithm_labels[j]}: {correlation_matrix[i, j]}")
"""
"""
# Create a figure and axis for the heatmap
fig, ax = plt.subplots()
cax = ax.matshow(correlation_matrix, cmap='coolwarm')

# Set the axis labels and tick positions
ax.set_xticks(np.arange(num_datasets))
ax.set_yticks(np.arange(num_datasets))
ax.set_xticklabels(algorithm_labels, rotation=45, ha="right")
ax.set_yticklabels(algorithm_labels)

# Display the colorbar
cbar = plt.colorbar(cax)

# Set the title and show the plot
plt.title('Correlation Matrix of Consistency Algorithms')
plt.show()
"""
# Set the upper triangular part of the correlation matrix to NaN
correlation_matrix[np.triu_indices(num_datasets, 1)] = np.nan
#correlation_matrix[np.triu_indices(num_datasets, 1)] = np.nan
# Create a figure and axis for the heatmap
fig, ax = plt.subplots(figsize=(8,7.5))
cax = ax.matshow(correlation_matrix, cmap='viridis')

# Set the axis labels and tick positions
#Set x ticks at the bottom of the plot
ax.xaxis.set_ticks_position('bottom')
ax.set_xticks(np.arange(num_datasets))
ax.set_yticks(np.arange(num_datasets))
ax.set_xticklabels(algorithm_labels,rotation=45,fontsize=10)
ax.set_yticklabels(algorithm_labels,fontsize=10)


# Display the colorbar
cbar = plt.colorbar(cax)

fig.subplots_adjust(bottom=0.2, top=0.95, left=0.01, right=1.05,
                    wspace=-0.2, hspace=0.25)

# Set the title and show the plot
#plt.title('Correlation matrix for the Consistency Scale Values of different algorithms and IVT')
plt.show()
plt.tight_layout()
#plt.savefig('/N/u/dkamnani/BigRed200/Paper plots/Group meeting updates/Correlation_matrixfinal.png')




