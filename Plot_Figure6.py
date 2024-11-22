#Plotting IVT and WA side by side 
import numpy as np
import glob
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import warnings
import dask.array as da
import dask
import matplotlib as mpl
import xarray as xr
import cartopy.feature as cfeature
import cartopy.mpl.ticker as cticker
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
import cartopy.feature as cfeature
import cartopy.mpl.ticker as cticker
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
from matplotlib.colorbar import ColorbarBase
from matplotlib.colors import BoundaryNorm

# Reading the consistency scale value datasets
IVT = np.load('IVTcsv16yrs.npy')
WA=np.load('WAcsv16yrs.npy')
CB=np.load('CBcsv.npy')
print(WA)
algorithms = np.stack([IVT,WA], axis=0)
print(algorithms.shape)
names = ["(a) IVT", "(b) WA"]


lat=np.load('lat.npy')
lon=np.load('lon.npy')
fig, axs = plt.subplots(nrows=1,ncols=2,
                        subplot_kw={'projection': ccrs.PlateCarree()},
                        figsize=(12,4),constrained_layout=False)
#Creating a colorbar
# Define the pre-existing colormaps you want to use
colormap_low = plt.get_cmap('Wistia')  # Low consistency
colormap_moderate = plt.get_cmap('Greys')  # Moderate consistency
colormap_high = plt.get_cmap('Blues')  # High consistency

# Define the number of colors per colormap
n_colors = 100

# Create lists of colors for each category by repeating the chosen colormaps
colormap_low_values = [colormap_low(i / n_colors) for i in range(n_colors)]
colormap_moderate_values = [colormap_moderate(0.2+i / (50)) for i in range(50)]
colormap_high_values = [colormap_high(0.4+i / n_colors) for i in range(n_colors)]

# Concatenate the colormaps
colormap_concatenated = mcolors.ListedColormap(
    colormap_low_values + colormap_moderate_values + colormap_high_values)


# axs is a 2 dimensional array of `GeoAxes`.  We will flatten it into a 1-D array
axs=axs.flatten()
for i in range(0,2):

        data=algorithms[i]
        print(i)
        
        # Contour plot ignoring nan values   
        cs=axs[i].contourf(lon,lat,data,
                          transform = ccrs.PlateCarree(),
                          cmap = colormap_concatenated,levels=300,vmin=0,vmax=1)
        
        # Title each subplot with the name of the model
        axs[i].set_title(names[i])

        # Draw the coastines for each subplot
        axs[i].coastlines()
        
        # Longitude labels
        axs[i].set_xticks(np.arange(-180,181,60), crs=ccrs.PlateCarree())
        lon_formatter = cticker.LongitudeFormatter()
        axs[i].xaxis.set_major_formatter(lon_formatter)

        # Latitude labels
        axs[i].set_yticks(np.arange(-90,91,30), crs=ccrs.PlateCarree())
        lat_formatter = cticker.LatitudeFormatter()
        axs[i].yaxis.set_major_formatter(lat_formatter)
        
        #Adding patches
        axs[i].add_patch(mpatches.Rectangle(xy=[-165, 30], width=50, height=30,
                                    alpha=0.5,
                                    lw=3,
                                    facecolor='None',
                                    edgecolor=(0.39, 1, 0),
                                    label='1',
                                    transform=ccrs.PlateCarree())
                 )
                 #-100,45
        axs[i].annotate("1",(-122,15),color=(0.39, 1, 0),fontsize=12)
        
        axs[i].add_patch(mpatches.Rectangle(xy=[-50, 25], width=30, height=50,
                                    alpha=0.5,
                                    lw=3,
                                    facecolor='None',
                                    edgecolor=(0.39, 1, 0),
                                    angle=-30,
                                    transform=ccrs.PlateCarree())
                 )
                 #-25,55
        axs[i].annotate("2",(-45,5),color=(0.39, 1, 0),fontsize=12)
        
        axs[i].add_patch(mpatches.Rectangle(xy=[30, 45], width=60, height=30,
                                    alpha=0.5,
                                    lw=3,
                                    facecolor='None',
                                    edgecolor=(0.39, 1, 0),
                                    transform=ccrs.PlateCarree())
                 )
                 #35,50
        axs[i].annotate("3",(90,35),color=(0.39, 1, 0),fontsize=12)
        
        axs[i].add_patch(mpatches.Rectangle(xy=[65, 15], width=25, height=20,
                                    alpha=0.5,
                                    lw=3,
                                    facecolor='None',
                                    edgecolor=(0.39, 1, 0),
                                    angle=-10,
                                    transform=ccrs.PlateCarree())
                 )
                 #-80,-61
        axs[i].annotate("4",(65,-1.5),color=(0.39, 1, 0),fontsize=12)
        
        axs[i].add_patch(mpatches.Rectangle(xy=[-70, -37], width=25, height=25,
        #xy=[-85, -63], width=30, height=50
                                    alpha=0.5,
                                    lw=3,
                                    facecolor='None',
                                    edgecolor=(0.39, 1, 0),
                                    transform=ccrs.PlateCarree())
                 )
                 #-80,-61
        axs[i].annotate("5",(-50,-50),color=(0.39, 1, 0),fontsize=12)
        #-96,-61     
        axs[i].add_patch(mpatches.Rectangle(xy=[30, -45], width=80, height=30,
                                    alpha=0.5,
                                    lw=3,
                                    facecolor='None',
                                    edgecolor=(0.39, 1, 0),
                                    angle=-10,
                                    transform=ccrs.PlateCarree())
                 )
                 #35,-40
        axs[i].annotate("7",(30,-60),color=(0.39, 1, 0),fontsize=12)
        
        axs[i].add_patch(mpatches.Rectangle(xy=[-40, -30], width=50, height=15,
        #xy=[140, -45], width=30, height=30
                                    alpha=0.5,
                                    lw=3,
                                    angle=-20,
                                    facecolor='None',
                                    edgecolor=(0.39, 1, 0),
                                    transform=ccrs.PlateCarree())
                 )
                 #157,-42
        axs[i].annotate("6",(0,-60),color=(0.39, 1, 0),fontsize=12)

#fig.delaxes(axs[5])

fig.subplots_adjust(bottom=0.0, top=1.2, left=0.05, right=0.98,
                    wspace=None, hspace=0.1)

# Add a colorbar axis at the bottom of the graph
#cbar_ax = fig.add_axes([0.2, 0.15, 0.6, 0.02])
cbar_ax = fig.add_axes([0.2, 0.16, 0.6, 0.04])

# Draw the colorbar
cbar=fig.colorbar(cs, cax=cbar_ax,orientation='horizontal') 
cbar.set_label('Consistency scale (0=Least consistent, 1= Most consistent)')
#cbar_ticks = [0.01, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
#cbar_tick_labels = ['Highly inconsistent(0-0.2)', 'Inconsistent(0.2-0.4)', 'Moderately Consistent(0.4-0.6)', 'Consistent(0.6-0.8)', 'Highly Consistent(0.8-1)']
cbar_ticks = [0.1,0.3, 0.5, 0.7, 0.9]
cbar_tick_labels = ['Highly inconsistent(0-0.2)', 'Inconsistent(0.2-0.4)',
                    'Moderately Consistent(0.4-0.6)', 'Consistent(0.6-0.8)', 'Highly Consistent(0.8-1)']
cbar.set_ticks(cbar_ticks)
cbar.set_ticklabels(cbar_tick_labels,fontsize=8)
plt.show()

