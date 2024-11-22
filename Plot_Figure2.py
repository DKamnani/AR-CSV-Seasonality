#Max Season Files saved from NCS1.py are used to generate Figure 1
#Code to plot the multiple masked out plots for different algorithms for three years
import numpy as np
import glob
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import warnings
import dask.array as da
import dask
import matplotlib as mpl
print("Done")
import xarray as xr
import cartopy.feature as cfeature
import cartopy.mpl.ticker as cticker
from matplotlib.colors import ListedColormap
from matplotlib.colors import ListedColormap
import string
CB1985=xr.open_dataset('/N/u/dkamnani/BigRed200/Paper plots/cascade_bard1985.nc').drop_vars('year')
CB2005=xr.open_dataset('/N/u/dkamnani/BigRed200/Paper plots/cascade_bard2005.nc').drop_vars('year')
CB2015=xr.open_dataset('/N/u/dkamnani/BigRed200/Paper plots/cascade_bard2015.nc').drop_vars('year')
IVT1985=xr.open_dataset('/N/u/dkamnani/BigRed200/Paper plots/Mundhenk1985.nc').drop_vars('year')
IVT2005=xr.open_dataset('/N/u/dkamnani/BigRed200/Paper plots/Mundhenk2005.nc').drop_vars('year')
IVT2015=xr.open_dataset('/N/u/dkamnani/BigRed200/Paper plots/Mundhenk2015.nc').drop_vars('year')
CB=np.vstack([CB1985.to_array(),CB2005.to_array(),CB2015.to_array(),IVT1985.to_array(),IVT2005.to_array(),IVT2015.to_array()])
names=["(a) TECA-BARD v1.0.1 : 1985", "(b) TECA-BARD v1.0.1 : 2005","(c) TECA-BARD v1.0.1 : 2015","(d) Mundhenk : 1985", "(e) Mundhenk : 2005","(f) Mundhenk : 2015"]

lat=CB1985.lat
lon=CB1985.lon
fig, axs = plt.subplots(nrows=2,ncols=3,
                        subplot_kw={'projection': ccrs.PlateCarree()},
                        figsize=(17,7))
           
lab=["(a)","(b)","(c)","(d)","(e)","(f)"]             
# axs is a 2 dimensional array of `GeoAxes`.  We will flatten it into a 1-D array
axs=axs.flatten()
for i in range(0,6):

        data=CB[i]+0.5
        
        #cm = (mpl.colors.ListedColormap(['white','powderblue', 'khaki', 'olive','coral']))
        #norm = mpl.colors.BoundaryNorm([0,1,2,3,4,5], cm.N) 
        #cm=plt.cm.get_cmap('cubehelix', 4)
        # Contour plot
        cs=axs[i].contourf(lon,lat,data,
                          transform = ccrs.PlateCarree(),
                          levels=[0,1,2,3,4,5],
                          #colors=['white','powderblue', 'khaki', 'olive','coral'],
						  colors=['white','steelblue', 'plum', 'tomato','yellowgreen'],
                          extend='neither',edgecolor='none')
        
        # Title each subplot with the name of the model
        axs[i].set_title(names[i])

        # Draw the coastines for each subplot
        axs[i].coastlines()
        
        # Longitude labels
        axs[i].set_xticks(np.arange(-180,181,60), crs=ccrs.PlateCarree())
        lon_formatter = cticker.LongitudeFormatter()
        axs[i].xaxis.set_major_formatter(lon_formatter)
        axs[i].tick_params(axis='x', labelsize=12)

        # Latitude labels
        axs[i].set_yticks(np.arange(-90,91,30), crs=ccrs.PlateCarree())
        lat_formatter = cticker.LatitudeFormatter()
        axs[i].yaxis.set_major_formatter(lat_formatter)
        axs[i].tick_params(axis='y', labelsize=12)
        #Annotate plot
        axs[i].set_title(names[i],fontsize=14)

fig.subplots_adjust(bottom=0.10, top=1.0, left=0.05, right=0.95,
                    wspace=0.15, hspace=-0.1)

# Add a colorbar axis at the bottom of the graph
cbar_ax = fig.add_axes([0.2, 0.07, 0.6, 0.02])

# Draw the colorbar
cbar=plt.colorbar(cs,cax=cbar_ax, orientation="horizontal",pad=0.1,shrink=0.8)
cbar.set_ticks([0.5,1.5,2.5,3.5,4.5])
cbar.set_ticklabels(["None","DJF","MAM","JJA","SON"],fontsize=14)
plt.show()
#plt.savefig("IVT_years")
