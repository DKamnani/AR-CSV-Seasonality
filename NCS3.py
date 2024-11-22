#Code to find out which season is the one peaking in Consistent and Highly Consistent areas
#Continuation from NCS2.py for Figure 5

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
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.cm import get_cmap
#Done for all algorithms 
#Reading the csv values of an algorithm
csv=np.load('CBcsv.npy')
#print(csv)


#adding lat and lon values and converting from numpy array to xarray Saved from earlier
lat=np.load('lat.npy')
lon=np.load('lon.npy')


#Reading x and y data
x=np.load('CBx.npy')
y=np.load('CBy.npy')


#Find the mean of the x and y coordinates 
xmean=x.mean(axis=0)
ymean=y.mean(axis=0)

#Copying the mean files
selected_x = np.copy(xmean)
selected_y = np.copy(ymean)
#Defining the consistent and highly consistent arrays as a copy of the mean file and then modifying it based on the conditions
consistent_x=np.copy(selected_x)
consistent_y=np.copy(selected_y)
highly_consistent_x=np.copy(selected_x)
highly_consistent_y=np.copy(selected_y)


#print(csv.shape)
#applying consistent consistency scale value condition to create a mask and setting all values in copied array to zero outside the mask
between_mask = (csv >= 0.6) & (csv < 0.8)
print(csv[between_mask])
consistent_x[~between_mask] = np.nan
consistent_y[~between_mask] = np.nan

#Doing the same for highly consistent as well
between_mask2 = (csv >= 0.8) & (csv <= 1)  
print(csv[between_mask2])
highly_consistent_x[~between_mask2] = np.nan
highly_consistent_y[~between_mask2] = np.nan


#Finding the angle
# Calculate the angle for each data point for consistent grid points
#Finds the angle in radians and converts to degree
angle_rad1 = np.arctan2(consistent_y, consistent_x)
angle_deg1 = np.degrees(angle_rad1)
#Changing to 360 degree system
angle_deg1 = np.where(angle_deg1 < 0, angle_deg1 + 360, angle_deg1)
np.save('CBCangle.npy',angle_deg1)

# Calculate the angle for each data point for highly consistent grid points
angle_rad2 = np.arctan2(highly_consistent_y, highly_consistent_x)
angle_deg2 = np.degrees(angle_rad2)
angle_deg2 = np.where(angle_deg2 < 0, angle_deg2 + 360, angle_deg2)
print(angle_deg2)
np.save('CBHCangle.npy',angle_deg2)


