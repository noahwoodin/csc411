import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the weather data
weather_data = pd.read_csv('BC_combined_weather_data.csv', low_memory=False)

# Load the fire data with correct delimiter and header
fire_data = pd.read_csv('NFDB_point_20240605.txt',
                        delimiter=',', skipinitialspace=True, low_memory=False)

# Strip any leading/trailing whitespace from column names
fire_data.columns = fire_data.columns.str.strip()

# Ensure column names are lowercase to avoid case sensitivity issues
fire_data.columns = fire_data.columns.str.lower()

# Print the first few rows of the fire_data to check column names
print(fire_data.head())

# Convert the date columns to datetime
weather_data['Date/Time'] = pd.to_datetime(weather_data['Date/Time'])
fire_data['rep_date'] = pd.to_datetime(fire_data['rep_date'])

# Extract year and month for aggregation
weather_data['year_month'] = weather_data['Date/Time'].dt.to_period('M')
fire_data['year_month'] = fire_data['rep_date'].dt.to_period('M')

# Map the cause codes to 'Human' and 'Natural'
cause_mapping = {'H': 'Human', 'H-PB': 'Human',
                 'N': 'Natural', 'RE': 'Natural', 'U': 'Unknown'}
fire_data['cause_mapped'] = fire_data['cause'].map(cause_mapping)

# Calculate average monthly temperature
avg_monthly_temp = weather_data.groupby(
    'year_month')['Mean Temp (°C)'].mean().reset_index()

# Calculate monthly total of forest fires by cause
fire_counts_by_cause = fire_data.pivot_table(
    index='year_month', columns='cause_mapped', values='fid', aggfunc='count', fill_value=0).reset_index()

# Print the first few rows of fire_counts_by_cause to check data
print(fire_counts_by_cause.head())

# Merge the dataframes on year_month
merged_data = pd.merge(avg_monthly_temp, fire_counts_by_cause,
                       on='year_month', how='outer').fillna(0)

# Focus on a smaller time range for better clarity
merged_data = merged_data[merged_data['year_month'] > '2020-01']

# Print the first few rows of merged_data to check data
print(merged_data.head())

# Create the combined plot
fig, ax1 = plt.subplots(figsize=(16, 8))

# Line chart for average monthly temperature
ax1.set_xlabel('Month')
ax1.set_ylabel('Average Temperature (°C)', color='tab:blue')
ax1.plot(merged_data['year_month'].astype(
    str), merged_data['Mean Temp (°C)'], color='tab:blue', marker='o')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Bar chart for monthly total of forest fires by cause
ax2 = ax1.twinx()
ax2.set_ylabel('Number of Fires', color='tab:red')

# Grouped bar chart
bar_width = 0.35
bar_positions = np.arange(len(merged_data))
human_fires = merged_data.get('Human', 0)
natural_fires = merged_data.get('Natural', 0)

# Check if the values are correct
print("Human fires:", human_fires)
print("Natural fires:", natural_fires)

ax2.bar(bar_positions - bar_width / 2, human_fires, bar_width,
        alpha=0.6, color='red', label='Human-caused')
ax2.bar(bar_positions + bar_width / 2, natural_fires, bar_width,
        alpha=0.6, color='green', label='Naturally-caused')

# Set x-ticks and x-tick labels
ax2.set_xticks(bar_positions)
ax2.set_xticklabels(merged_data['year_month'].astype(str))

ax2.tick_params(axis='y', labelcolor='tab:red')

# Display fewer x-axis labels
ax1.set_xticks(ax1.get_xticks()[::3])  # Display every 3rd label

# Add grid lines for better reference
ax1.grid(True)
ax2.grid(False)

# Add legend
ax2.legend(loc='upper right')

plt.title('Average Monthly Temperature and Number of Forest Fires by Cause')
fig.tight_layout()

plt.show()
