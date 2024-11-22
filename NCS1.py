#First step towards Figure 1
#This code writes files for masked max season plot after replacing seasons with vectors
#Done for each algorithm individually 
 
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

#Reading data for one algorithm at a time
Path='/N/slate/dkamnani/Cascade_Bard/Data/*.nc4'
#Path='/N/slate/dkamnani/Mundhenk/*.nc4'
#Path='/N/slate/dkamnani/ClimateNet_DL/*.nc4'
#Path='/N/slate/dkamnani/reid250/*.nc4'
#Path='/N/slate/dkamnani/guan_waliser/*.nc4'
#DS=xr.open_mfdataset(Path,chunks={'time':2928})
#Path='/N/slate/dkamnani/IVT_MEERA/*.nc'
#Path='/N/scratch/dkamnani/vIVT/Final/*.nc'
print(Path)
DS=xr.open_mfdataset(Path, parallel=True)
Freq=DS.ar_binary_tag
#Freq=DS.IVT
#Freq=da.from_array(Freq)
#print("The initial dataset is")
print(Freq)

#Calculating the seasonal averages

#setting the months for each season
seasons = dict(
    DJF = [12,  1,  2],
    MAM = [ 3,  4,  5],
    JJA = [ 6,  7,  8],
    SON = [ 9, 10, 11])
# initialize the seasonal mean dataset as a list
seasonal_mean_dataset = []
# loop over seasons
for season in seasons:
    print(f"Working on {season}")
    
    # determine the month associated with each timestep
    data_month = Freq['time.month']
    
    # determine whether each time step is within the current season (True=yes, False=no)
    in_season = np.in1d(data_month, seasons[season])
    #print(in_season)
    
    # subset the data so that only includes months in the current season
    Freq_subset = Freq.sel(time = Freq['time'][in_season])
    #print(Freq['time'][in_season])
    
    # set the year values by which we'll group the data
    season_years = Freq['time.year']
    #print(season_years)
    
    # for DJF, D and JF have different years, meaning they would be grouped incorrectly
    # (Jan 2020, Feb 2020... and Dec 2020 would all be grouped into the same year, whereas we want
    #  Dec 2019 to be grouped instead)
    # The following artificially shifts the year for december to account for this, so that Dec 2019 becomes 'Dec 2020'
    if season == "DJF":
        # shift data in all decembers ahead by one year so they're grouped with the correct Jan and Feb
        season_years[data_month == 12] = season_years[data_month == 12] + 1
        
    # subset the the season_year variable so we only include months in the current season
    season_years = season_years.sel(time = Freq['time'][in_season])
        
        
    # group the data by year (accounting for seasons that span a year change)
    year_group = Freq_subset.groupby(season_years)
    
    # calculate the mean
    seasonal_mean = year_group.mean(dim = "time")*100
    
    # append the seasonal mean dataset to the list
    seasonal_mean_dataset.append(seasonal_mean)
    
# create an array of seasons
season_array = xr.DataArray(list(seasons), dims = ('season',))
#print(season_array)

# create a new dataset from the list of seasonal means (overwriting the list)
seasonal_mean_dataset = xr.concat(seasonal_mean_dataset, dim = season_array)
    
# show the dataset
#print(seasonal_mean_dataset)

#slicing the data
#removing the first and last year because we need December from the previous year and Jan and Feb from the next
seasonal_mean_1=seasonal_mean_dataset.isel(year=slice(1,37))
#print(seasonal_mean_1)

#Change season names to numbers
seasonal_mean_1=seasonal_mean_1.rename({'season':'season_number'})
seasonal_mean_1=seasonal_mean_1.assign_coords(season_number=[1,2,3,4])
#print(seasonal_mean_1)

#Saving lat and lon to file
lat=seasonal_mean_1.lat
lon=seasonal_mean_1.lon
lat=np.save('lat.npy',lat)
lon=np.save('lon.npy',lon)


#Optimized version of finding max season
# Create a mask for values greater than 0 to make sure we don't find max for regions that have had no AR activity
mask = seasonal_mean_1 > 0

# Finding the max season for each location directly using idxmax
a = seasonal_mean_1.where(mask).idxmax(dim="season_number", skipna=True)

# Fill NaN values with 0 using xarray's fillna method
a = a.fillna(0)
#print(a.sel(year=2000,lat=50.0,lon=-110,method='nearest').values)
# Print the result
print("done finding max season")
print(a)

#Following is data to generate figure 1. We save the max seasonal distribution for specific years and plotting is optional
"""
plot_years=[1985,2005,2015]
for y in plot_years:
	print(y)
	mean_spatial=a.sel(year=y)
	#mean_spatial.to_netcdf(path="GW%d.nc"%y,mode='w',format='NETCDF3_CLASSIC')


#uncomment later if necessary
#plotting the spatial distribution of max season
lat=a.lat
lon=a.lon
mean_spatial=(a.sel(year=2005))
#+0.5
ax = plt.axes(projection=ccrs.PlateCarree())
#mapping 0,1,2,3,4 to specific contour colors
plt.contourf(lon,lat,mean_spatial,levels=[0,1,2,3,4,5],colors=['white','powderblue', 'khaki', 'olive', 'coral'])
#plot colorbar at the bottom
cbar=plt.colorbar( orientation="horizontal",pad=0.1,shrink=0.8)
cbar.set_ticks([0.5,1.5,2.5,3.5,4.5])
cbar.set_ticklabels(["None","DJF","MAM","JJA","SON"])
ax.coastlines()
plt.title('vIVT')
#ax.coastlines()
ax.gridlines(draw_labels=True)
plt.savefig('Spatial_Distribution_max_vIVTseason.png')
"""

#Consistency scale development begins


# Define the shape of 'x' and 'y' based on 'a'.
print("start")
x = np.empty_like(a)
print("donex")
y = np.empty_like(a)
print("doney")
x.fill(0)
y.fill(0)
print("done with x and y")

# Create masks for each season
mask_djf = (a == 1)
print("done with djf")
mask_mam = (a == 2)
print("done with mam")
mask_jja = (a == 3)
print("done with jja")
mask_son = (a == 4)
print("done with son")

# Set NaN values for masked areas
x[a == 0] = np.nan
y[a == 0] = np.nan

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
print("Done")
#print(x)
#print(y)

#Write x and y 
x=np.save('CBx.npy',x)
y=np.save('CBy.npy',y)

