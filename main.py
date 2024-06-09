import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV file
data = pd.read_csv('NFDB_point_20240605.txt')

# Check the first few rows of the DataFrame
print(data.head())

# Simple visualization: a scatter plot of the fire sizes (SIZE_HA) over the days of the year they were reported
data['REP_DATE'] = pd.to_datetime(data['REP_DATE'])  # Convert REP_DATE to datetime

print("Earliest record date:", data['REP_DATE'].min())
print("Earliest record date:", data['REP_DATE'].max())

data['DayOfYear'] = data['REP_DATE'].dt.dayofyear  # Add a new column for the day of the year

plt.figure(figsize=(10, 6))
plt.scatter(data['DayOfYear'], data['SIZE_HA'], color='red', alpha=0.5)
plt.title('Fire Sizes by Day of Year')
plt.xlabel('Day of Year')
plt.ylabel('Size in Hectares')
plt.grid(True)
plt.show()
