#Plot that changes the colorbar
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import xarray as xr
from matplotlib.colors import BoundaryNorm, ListedColormap

def plot_seasonal_max_cb(ax, Path, label):
    # Reading nc file
    DS = xr.open_dataset(Path)

    # Years
    years = DS.year.values

    # Selecting lat and lon values for California
    min_lat, max_lat = 32, 42
    min_lon, max_lon = -124.5, -114.5
    subset_data = DS.sel(lat=slice(min_lat, max_lat), lon=slice(min_lon, max_lon))

    # Calculate the number of grid points where the subset data has season number as 1,2,3,4 for each year
    season_number = subset_data.season_number

    # Initialize an empty list to store the number of grid points for each year
    num_points = []

    # Loop over each year
    for year in years:
        for i in range(1, 5):
            # Calculate the number of grid points where the season number is equal to i
            num_points.append(np.sum(season_number.sel(year=year) == i))

    # Reshape the list into a 2D array with shape (number of years, 4)
    num_points = np.array(num_points).reshape(len(years), 4)

    # Mask zero values to make them blank
    num_points_masked = np.where(num_points == 0, np.nan, num_points)

    # Define the color intervals
    bounds = np.arange(0, 351, 50)
    n_colors = len(bounds) - 1

    # Define colors for the colormap
    #colors = ['#D3D3D3', '#4E79A7', '#E15759', '#76B7B2', '#FF9D98', '#F28E2B', '#59A14F']
    #cmap = ListedColormap(colors[:n_colors])

    # Create a BoundaryNorm to map discrete values to colors
    norm = plt.Normalize(vmin=0,vmax=350)

    # Plot
    mesh = ax.pcolormesh(np.arange(5), np.arange(len(years) + 1), num_points_masked, cmap='Blues', norm=norm)

    # Set the x-axis and y-axis labels
    #ax.set_xlabel('Season')
    #ax.set_ylabel('Year')

    # Set the x-axis and y-axis ticks
    ax.set_xticks(np.arange(4) + 0.5)
    ax.set_yticks(np.arange(len(years)) + 0.5)

    # Set the x-axis and y-axis tick labels
    ax.set_xticklabels(['DJF', 'MAM', 'JJA', 'SON'])
    ax.set_yticklabels(years)

    # Set the title
    ax.set_title(f'{label}', fontsize=14)

    # Loop over data dimensions and create text annotations
    for i in range(len(years)):
        for j in range(4):
            value = int(num_points_masked[i, j]) if not np.isnan(num_points_masked[i, j]) else ''
            text = ax.text(j + 0.5, i + 0.5, value, ha='center', va='center', color='#FF69B4', fontsize=10)


    return mesh  # Return the mesh variable

# List of file paths and labels
file_paths = ['Seasonal_Max_GW.nc', 'Seasonal_Max_MD.nc', 'Seasonal_Max_RD.nc', 'Seasonal_Max_CB.nc', 'Seasonal_Max_CN.nc', 'Seasonal_Max_IVT.nc']
labels = ['(a) Guan and Waliser Algorithm', '(b) Mundhenk Algorithm', '(c) Reid et al Algorithm', '(d) TECA BARD v1.0.1 Algorithm', '(e) ClimateNet Algorithm','(f) IVT']
# Plotting for each file
fig, axes = plt.subplots(2, 3, figsize=(17, 17),constrained_layout=False)

meshes = []  # List to store the mesh variables

for ax, path, label in zip(axes.flatten(), file_paths, labels):
    meshes.append(plot_seasonal_max_cb(ax, path, label))


# Define colors for the colorbar
cmap = 'Blues'

#plt.tight_layout()
plt.subplots_adjust(left=0.05, right=0.98, top=0.95, bottom=0.1, wspace=0.3, hspace=0.1)

# Create a colorbar with discrete ticks for each unique value
bounds = [0, 50, 100, 150, 200, 250, 300, 350]
norm = BoundaryNorm(bounds, len(bounds) - 1)
cb_ax = fig.add_axes([0.1, 0.05, 0.8, 0.02])  # [left, bottom, width, height]
#cb_ax = fig.add_axes([0.93, 0.1, 0.02, 0.7])  # [left, bottom, width, height]
cb = plt.colorbar(meshes[0], cax=cb_ax, ticks=bounds, orientation='horizontal', cmap=cmap,norm=norm)  # Use the first mesh variable for the colorbar
cb.set_label('Number of Coordinates',fontsize=14)
# Set tick label font size
cb.ax.tick_params(labelsize=14)
plt.savefig('Seasonal_Max_combined_with_colorbar.png')
plt.show()



