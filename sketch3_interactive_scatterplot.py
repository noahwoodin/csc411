import pandas as pd
import folium

# Load the fire data with correct delimiter and header
fire_data = pd.read_csv('NFDB_point_20240605.txt',
                        delimiter=',', skipinitialspace=True, low_memory=False)

# Strip any leading/trailing whitespace from column names
fire_data.columns = fire_data.columns.str.strip()

# Ensure column names are lowercase to avoid case sensitivity issues
fire_data.columns = fire_data.columns.str.lower()

# Filter the data to include only relevant columns and the year 2020
fire_data = fire_data[['latitude', 'longitude', 'cause', 'year']]
fire_data = fire_data[fire_data['year'] == 2020]

# Map the cause codes to 'Human' and 'Natural'
cause_mapping = {'H': 'Human', 'H-PB': 'Human',
                 'N': 'Natural', 'RE': 'Natural', 'U': 'Unknown'}
fire_data['cause_mapped'] = fire_data['cause'].map(cause_mapping)

# Initialize a map centered on Canada
m = folium.Map(location=[56.1304, -106.3468], zoom_start=4)

# Add scatter points to the map
for index, row in fire_data.iterrows():
    color = 'red' if row['cause_mapped'] == 'Human' else 'green'
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=3,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=f"Cause: {row['cause_mapped']}"
    ).add_to(m)

# Save and display the map
m.save('fire_scatterplot_2020.html')
m
