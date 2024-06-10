import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Load the fire data with correct delimiter and header
fire_data = pd.read_csv('NFDB_point_20240605.txt',
                        delimiter=',', skipinitialspace=True, low_memory=False)

# Strip any leading/trailing whitespace from column names
fire_data.columns = fire_data.columns.str.strip()

# Ensure column names are lowercase to avoid case sensitivity issues
fire_data.columns = fire_data.columns.str.lower()

# Filter the data to include only relevant columns
fire_data = fire_data[['latitude', 'longitude', 'rep_date', 'cause']]

# Map the cause codes to 'Human' and 'Natural'
cause_mapping = {'H': 'Human', 'H-PB': 'Human',
                 'N': 'Natural', 'RE': 'Natural', 'U': 'Unknown'}
fire_data['cause_mapped'] = fire_data['cause'].map(cause_mapping)

# Convert rep_date to datetime
fire_data['rep_date'] = pd.to_datetime(fire_data['rep_date'])

# Filter the data to include only the years 2020 to the latest date
fire_data = fire_data[(fire_data['rep_date'].dt.year >= 2020)]

# Group by year and month to reduce the number of frames
fire_data['year_month'] = fire_data['rep_date'].dt.to_period('M')
fire_data = fire_data.groupby(
    ['year_month', 'latitude', 'longitude', 'cause_mapped']).size().reset_index(name='counts')

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(fire_data, geometry=gpd.points_from_xy(
    fire_data.longitude, fire_data.latitude))

# Load a base map of Canada
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
canada = world[world.name == "Canada"]

# Initialize the plot
fig, ax = plt.subplots(figsize=(10, 10))
canada.plot(ax=ax, color='whitesmoke', edgecolor='black')
plot = [ax.scatter([], [], c=[], alpha=0.6, s=10)]
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Create the legend
human_patch = plt.Line2D([0], [0], marker='o', color='w',
                         markerfacecolor='red', markersize=10, label='Human')
natural_patch = plt.Line2D([0], [0], marker='o', color='w',
                           markerfacecolor='green', markersize=10, label='Natural')
plt.legend(handles=[human_patch, natural_patch], loc='upper right')

# Function to update each frame with incremental data


def update(num, gdf, plot, year_text):
    print(f"Processing frame {num + 1}/{len(gdf['year_month'].unique())}")

    # Clear previous scatter plots
    for scat in plot:
        scat.remove()
    plot.clear()

    # Get data for the current year and month
    current_year_month = gdf['year_month'].unique()[num]
    current_data = gdf[gdf['year_month'] == current_year_month]

    # Plot the updated data
    scatter = ax.scatter(current_data.geometry.x, current_data.geometry.y, c=current_data['cause_mapped'].apply(
        lambda x: 'red' if x == 'Human' else 'green'), alpha=0.6, s=current_data['counts'] * 5)

    # Append the new scatter plot
    plot.append(scatter)

    # Update the year_month text annotation
    year_text.set_text(f'Date: {current_year_month}')


# Create the year_month text annotation
year_text = ax.text(0.02, 0.95, '', transform=ax.transAxes,
                    fontsize=12, verticalalignment='top')

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=len(gdf['year_month'].unique(
)), fargs=(gdf, plot, year_text), interval=500, repeat=False)

# Save the animation
ani.save('fire_animation_2020_to_2023_grouped.gif', writer='pillow')

plt.show()
