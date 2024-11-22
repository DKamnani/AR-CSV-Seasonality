#This code will store the values for the consistency scale after calculating the mean magnitude of the vectors as consistency scale values
#We do this for all algorithms and IVT
#Plotting the csv values for each algorithm will give us Figure 4
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

#Read the x and y binary files from existing folder
x=np.load('CBx.npy')
y=np.load('CBy.npy')


#Find the mean of the x and y coordinates 
xmean=x.mean(axis=0)
ymean=y.mean(axis=0)

#Square x and y corrdinates, add the squares and then take the square root
xmean=xmean**2
ymean=ymean**2
#csv stands for consistency scale vealue
csv=xmean+ymean
csv=(csv**0.5)


np.save('CBcsv.npy',csv)


