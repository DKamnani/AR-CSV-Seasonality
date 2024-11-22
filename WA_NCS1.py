#Code to find the consistency scale for Sam's wave activity data part 1
#steps will involve ready the file and then finding the consistency scale
#might be comparable to NCS1.py file

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
import pandas as pd

Path='/N/slate/dkamnani/LHC_BUDGET/*.nc'
DS=xr.open_mfdataset(Path,parallel=True)
Freq=DS.AeLp
#print(Freq)
#Slice the Freq dataset to only include the time period 2000-2016
Freq=Freq.sel(time=slice('2000-01-01','2016-12-31'))
print(Freq)


#Find the month where moist wave activity peaks in the dataset a

# Find the coordinates (time and lat/lon) where 'value' peaks for each year
yearly_peaks = Freq.groupby('time.year').apply(lambda x: x.idxmax(dim='time',skipna=True))
#print(yearly_peaks)
#print(yearly_peaks.sel(year=2000, lat=45, lon=45, method='nearest').values)
#month=yearly_peaks.sel(year=2000, lat=45, lon=45, method='nearest').values.month
month=yearly_peaks.dt.month
#print(month.sel(year=2000, lat=35, lon=70, method='nearest').values)
#fill nan values with zeros in month
month= month.where(~np.isnan(month), 0)
print(month.sel(year=2005).values)


# Assuming 'a' is your input array with dimensions (lat, lon, year).

# Define the shape of 'x' and 'y' based on 'a'.
print("start")
x = np.empty_like(month)
print("donex")
y = np.empty_like(month)
print("doney")
x.fill(0)
y.fill(0)
print("done with x and y")

# Create masks for each season
mask_djf = (month == 12)
print("done with djf")
mask_mam = (month == 3)
print("done with mam")
mask_jja = (month == 6)
print("done with jja")
mask_son = (month == 9)
print("done with son")

# Set NaN values for masked areas
x[month == 0] = np.nan
y[month == 0] = np.nan

# Assign values based on seasons for all years simultaneously
x[mask_djf] = 1
y[mask_djf] = 0

x[mask_mam] = 0
y[mask_mam] = 1

x[mask_jja] = -1
y[mask_jja] = 0

x[mask_son] = 0
y[mask_son] = -1


# Print the resulting 'x' and 'y' arrays
#print(x)
#print(y)

#Write x and y 
x=np.save('WAx16yrs.npy',x)
y=np.save('WAy16yrs.npy',y)

