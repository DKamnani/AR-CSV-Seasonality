# TEsting if the plotting is done well 
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
from matplotlib.colorbar import ColorbarBase
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.colors as mcolors
from matplotlib.cm import get_cmap
import cartopy.mpl.ticker as cticker
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
import cartopy.feature as cfeature
import cartopy.mpl.ticker as cticker
import matplotlib.patches as mpatches

#loading data
#Reading the consistent values for different algorithms
CBC=np.load('CBCangle.npy')
CNC=np.load('CNCangle.npy')
MDC=np.load('MDCangle.npy')
RDC=np.load('RDCangle.npy')
GWC=np.load('GWCangle.npy')
IVTC=np.load('IVTCangle.npy')

#Reading the highly consistent values for different algorithms
CBHC=np.load('CBHCangle.npy')
CNHC=np.load('CNHCangle.npy')
MDHC=np.load('MDHCangle.npy')
RDHC=np.load('RDHCangle.npy')
GWHC=np.load('GWHCangle.npy')
IVTHC=np.load('IVTHCangle.npy')

#Removing nan values
IVTHC = np.ma.masked_invalid(IVTHC)
IVTC=np.ma.masked_invalid(IVTC)
CBHC = np.ma.masked_invalid(CBHC)
CBC=np.ma.masked_invalid(CBC)
CNHC = np.ma.masked_invalid(CNHC)
CNC=np.ma.masked_invalid(CNC)
RDHC = np.ma.masked_invalid(RDHC)
RDC=np.ma.masked_invalid(RDC)
MDHC=np.ma.masked_invalid(MDHC)
MDC=np.ma.masked_invalid(MDC)
GWHC = np.ma.masked_invalid(GWHC)
GWC=np.ma.masked_invalid(GWC)

#Reading the lat and lon values
lat=np.load('lat.npy')
lon=np.load('lon.npy')

#Defining a function to assign a season based on angle
def assign_numbers(angles):
    assigned_numbers = np.zeros_like(angles)
    assigned_numbers[(angles >= 0) & (angles <= 45) | (angles > 315) & (angles <= 360)] = 0
    assigned_numbers[(angles > 45) & (angles <= 135)] = 1
    assigned_numbers[(angles > 135) & (angles <= 225)] = 2
    assigned_numbers[(angles > 225) & (angles <= 315)] = 3
    return assigned_numbers

IVTHC = assign_numbers(IVTHC)
IVTC = assign_numbers(IVTC)
CBHC = assign_numbers(CBHC)
CBC=assign_numbers(CBC)
CNHC = assign_numbers(CNHC)
CNC=assign_numbers(CNC)
RDHC = assign_numbers(RDHC)
RDC=assign_numbers(RDC)
MDHC=assign_numbers(MDHC)
MDC=assign_numbers(MDC)
GWHC = assign_numbers(GWHC)
GWC=assign_numbers(GWC)

colors = [(0, 158/255, 115/255),(0, 0, 0), (230/255, 159/255, 0), (86/255, 180/255, 233/255)]
cmapplot=mcolors.ListedColormap(colors)
colors= [(0, 158/255, 115/255),(0.4, 0.4, 0.4), (230/255, 159/255, 0), (86/255, 180/255, 233/255)]
def lighten_color(color, factor=1.7):
    """
    Lightens the given color by multiplying each RGB channel by the given factor.
    """
    return tuple(min(channel * factor, 1.0) for channel in color)

# Lighter colors
lighter_colors = [lighten_color(color) for color in colors]
cmapplot2= mcolors.ListedColormap(lighter_colors)

# Create a new figure
fig = plt.figure(figsize=(18, 15))
projection = ccrs.PlateCarree()

# Define GeoAxes
ax1 = fig.add_subplot(3, 3, 1, projection=projection)
ax2 = fig.add_subplot(3, 3, 3, projection=projection)
ax3 = fig.add_subplot(3, 3, 4, projection=projection)
ax4 = fig.add_subplot(3, 3, 6, projection=projection)
ax5 = fig.add_subplot(3, 3, 7, projection=projection)
ax6 = fig.add_subplot(3, 3, 9, projection=projection)
axcb= fig.add_subplot(3, 3, 5, projection='polar',position=[0.26, 0.4, 0.5, 0.2])

# Plot GW
ax1.contourf(lon, lat, GWHC, cmap=cmapplot, transform=projection)
ax1.contourf(lon, lat, GWC, cmap=cmapplot2, transform=projection)
ax1.set_title('(a) Guan and Waliser')
#ax1.set_xlabel('Longitude')
#ax1.set_ylabel('Latitude')
ax1.coastlines()

# Plot MD
ax2.contourf(lon, lat, MDHC, cmap=cmapplot, transform=projection)
ax2.contourf(lon, lat, MDC, cmap=cmapplot2, transform=projection)
ax2.set_title('(b) Mundhenk')
#ax2.set_xlabel('Longitude')
#ax2.set_ylabel('Latitude')
ax2.coastlines()

# Plot RD
ax3.contourf(lon, lat, RDHC, cmap=cmapplot, transform=projection)
ax3.contourf(lon, lat, RDC, cmap=cmapplot2, transform=projection)
ax3.set_title('(c) Reid et al')
#ax3.set_xlabel('Longitude')
#ax3.set_ylabel('Latitude')
ax3.coastlines()

# Plot CB
ax4.contourf(lon, lat, CBHC, cmap=cmapplot, transform=projection)
ax4.contourf(lon, lat, CBC, cmap=cmapplot2, transform=projection)
ax4.set_title('(d) Cascade_bard')
#ax4.set_xlabel('Longitude')
#ax4.set_ylabel('Latitude')
ax4.coastlines()

# Plot CN
ax5.contourf(lon, lat, CNHC, cmap=cmapplot, transform=projection)
ax5.contourf(lon, lat, CNC, cmap=cmapplot2, transform=projection)
ax5.set_title('(e) ClimateNet')
#ax5.set_xlabel('Longitude')
#ax5.set_ylabel('Latitude')
ax5.coastlines()

# Plot IVT
ax6.contourf(lon, lat, IVTHC, cmap=cmapplot, transform=projection)
ax6.contourf(lon, lat, IVTC, cmap=cmapplot2, transform=projection)
ax6.set_title('(f) IVT')
#ax6.set_xlabel('Longitude')
#ax6.set_ylabel('Latitude')
ax6.coastlines()

#Plot the Polar color wheel
# Color map for the theta values(0.8-1)
# Colorblind-friendly colors
colors = [(0, 0, 0), (230/255, 159/255, 0), (86/255, 180/255, 233/255), (0, 158/255, 115/255)]
n_bins = [45,135, 225, 315,405]  # Angle bins
cmap_name = "polar_color_wheel"
cmap = mpl.colors.LinearSegmentedColormap.from_list(cmap_name, colors, N=len(n_bins) - 1)

#Color map for THE THETA VALUES (0.6-0.8)
# Colorblind-friendly colors
colors = [(0.5, 0.5, 0.5), (230/255, 159/255, 0), (86/255, 180/255, 233/255), (0, 158/255, 115/255)]

# Factor to make colors lighter (you can adjust this as needed)
lightening_factor =1.7  # Multiply by 0.75 to make them lighter

# Create lighter colors by multiplying each component by the factor
lighter_colors = [(r * lightening_factor, g * lightening_factor, b * lightening_factor) for r, g, b in colors]

n_bins = [45, 135, 225, 315, 405]  # Angle bins
cmap_name2 = "polar_color_wheel"
cmap2 = mpl.colors.LinearSegmentedColormap.from_list(cmap_name2, lighter_colors, N=len(n_bins) - 1)
# Define colormap normalization for 0 to 2*pi
norm = mpl.colors.Normalize(45*np.pi/180, 405*np.pi/180) 
# Plot a color mesh on the polar plot with the color set by the angle
n = 200 #the number of secants for the mesh
t = np.linspace(45*np.pi/180, 405*np.pi/180, n)   #theta values
r1 = np.linspace(.8, 1, 10)        #radius values change 0.6 to 0 for full circle
r2=np.linspace(.4,.6,10)
rg, tg = np.meshgrid(r1, t)      #create an r, theta meshgrid
rg2,tg2=np.meshgrid(r2,t)
c1 = tg                   #define color values as theta value
c2=tg2
im=axcb.pcolormesh(t, r1,c1.T, norm=norm, cmap=cmap)  #plot the colormesh on axis with colormap
im=axcb.pcolormesh(t, r2, c2.T, norm=norm, cmap=cmap2)  #plot the colormesh on axis with colormap
axcb.set_yticklabels([])                   #turn off radial tick labels (yticks)
axcb.tick_params(pad=15, labelsize=24)      #cosmetic changes to tick labels
axcb.spines['polar'].set_visible(False)  
axcb.set_title('Season based on angle', fontsize=16)
custom_ticks = [0, np.pi/4, np.pi / 2, (135/180)*np.pi , np.pi, (225/180)*np.pi, (3/2)*np.pi,(315/180)*np.pi]
custom_tick_labels = ['DJF', '45', 'MAM','135', 'JJA', '225', 'SON','315']
axcb.set_xticks(custom_ticks)
axcb.set_xticklabels(custom_tick_labels,fontsize=14)

radial_ticks = [.4, .8]  # You can adjust these values as needed
axcb.set_yticks(radial_ticks)
radial_ticks_labels = ['0.6-0.8', '0.8-1']  # You can adjust these values as needed
axcb.set_yticklabels(radial_ticks_labels, fontsize=12)

# Plot each subplot
for ax in [ax1, ax2, ax3, ax4, ax5, ax6]:  # Add all your subplot axes here
	# Set latitude and longitude labels
		ax.set_xticks(np.arange(-180, 181, 60), crs=ccrs.PlateCarree())
		ax.set_yticks(np.arange(-90, 91, 30), crs=ccrs.PlateCarree())
		ax.set_xticklabels(['180°W', '120°W', '60°W', '0°', '60°E', '120°E', '180°E'])  # Longitude labels
		ax.set_yticklabels(['90°S', '60°S', '30°S', '0°', '30°N', '60°N', '90°N'])  # Latitude labels
        #Adding patches
		ax.add_patch(mpatches.Rectangle(xy=[-165, 30], width=50, height=30,
        		                        alpha=0.5,
                                		lw=3,
                                		facecolor='None',
                                		edgecolor='black',
                                		#label='1',
                                		transform=ccrs.PlateCarree())
             		)

		ax.annotate("1",(-122,15),color='black',fontsize=10)

		ax.add_patch(mpatches.Rectangle(xy=[-50, 25], width=30, height=50,
                                 		alpha=0.5,
                                 		lw=3,
                                 		facecolor='None',
                                 		edgecolor='black',
                                		angle=-30,
                                 		transform=ccrs.PlateCarree())
             		)
# -25,55
		ax.annotate("2", (-45, 55), color='black', fontsize=10)

		ax.add_patch(mpatches.Rectangle(xy=[30, 45], width=60, height=30,
                                 		alpha=0.5,
                                 		lw=3,
                                 		facecolor='None',
                                 		edgecolor='black',
                                 		transform=ccrs.PlateCarree())
             		)
# 35,50
		ax.annotate("3", (20, 47), color='black', fontsize=10)

		ax.add_patch(mpatches.Rectangle(xy=[65, 15], width=25, height=20,
        		                        alpha=0.5,
                                 		lw=3,
                                 		facecolor='None',
                                 		edgecolor='black',
                                 		angle=-10,
                                 		transform=ccrs.PlateCarree())
             		)
# -80,-61
		ax.annotate("4", (90, 33), color='black', fontsize=10)

		ax.add_patch(mpatches.Rectangle(xy=[-70, -37], width=25, height=25,
                                 		alpha=0.5,
                                 		lw=3,
                                 		facecolor='None',
                                 		edgecolor='black',
                                 		transform=ccrs.PlateCarree())
             		)
# -80,-61
		ax.annotate("5", (-50, -50), color='black', fontsize=10)
# -96,-61
		ax.add_patch(mpatches.Rectangle(xy=[30, -45], width=80, height=30,
                                 		alpha=0.5,
                                 		lw=3,
                                 		facecolor='None',
                                 		edgecolor='black',
                                 		angle=-10,
                                 		transform=ccrs.PlateCarree())
             		)
# 35,-40
		ax.annotate("7", (30, -60), color='black', fontsize=10)

		ax.add_patch(mpatches.Rectangle(xy=[-40, -30], width=50, height=15,
                                 		alpha=0.5,
                                 		lw=3,
                                 		angle=-20,
                                 		facecolor='None',
                                 		edgecolor='black',
                                 		transform=ccrs.PlateCarree())
             		)
# 157,-42
		ax.annotate("6", (0, -60), color='black', fontsize=10)

plt.tight_layout()
plt.show()

"""
# Create a subplot with a specified axis
fig, ax = plt.subplots(figsize=(10, 6))

projection = ccrs.PlateCarree()

# Define GeoAxes
ax = fig.add_subplot(1, 1, 1, projection=projection)
# Plot assigned numbers on the specified axis
contourf = ax.contourf(lon, lat, IVTHC, levels=[-1, 0, 1, 2, 3], cmap=cmap, extend='neither',transform=projection)
contourf2 = ax.contourf(lon, lat, IVTC, levels=[-1, 0, 1, 2, 3], cmap=cmap2, extend='neither',transform=projection)
cb = plt.colorbar(contourf, ax=ax, label='Assigned Numbers')


# Add labels and title
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Assigned Numbers Contour Plot')
ax.coastlines()

plt.show()




"""

