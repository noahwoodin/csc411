# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np

# # Create a date range for one year
# dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')

# # Generate synthetic data for rainfall with seasonal variation
# rainfall = np.where(dates.month.isin([1, 2, 11, 12]), np.random.normal(loc=8, scale=2.5, size=len(dates)), 
#                     np.where(dates.month.isin([3, 4, 5, 9, 10]), np.random.normal(loc=4, scale=1.5, size=len(dates)),
#                              np.random.normal(loc=0.5, scale=0.3, size=len(dates))))
# rainfall = np.clip(rainfall, 0, None)  # Remove negative values for rainfall

# # Generate synthetic data for number of fires, adjusting to show dramatic seasonal differences
# fires = np.where(dates.month.isin([6, 7, 8]), np.random.poisson(lam=3, size=len(dates)), 
#                  np.random.poisson(lam=0.1, size=len(dates)))

# # Create a DataFrame to hold the data
# data = pd.DataFrame({
#     'Date': dates,
#     'Rainfall': rainfall,
#     'Fires': fires
# })

# # Calculate the cumulative rainfall and rolling average of fires over the last 7 days
# data['Cumulative Rainfall (Last 7 Days)'] = data['Rainfall'].rolling(window=7, min_periods=1).sum()
# data['Rolling Average Fires (Last 7 Days)'] = data['Fires'].rolling(window=7, min_periods=1).mean()

# # Create the plots
# fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))

# # Cumulative Rainfall plot
# color = 'tab:blue'
# ax1.set_xlabel('Date')
# ax1.set_ylabel('Cumulative Rainfall (mm, Last 7 Days)', color=color)
# ax1.plot(data['Date'], data['Cumulative Rainfall (Last 7 Days)'], color=color)
# ax1.tick_params(axis='y', labelcolor=color)
# ax1.set_title('Cumulative Rainfall over Last 7 Days in Victoria, BC')

# # Rolling Average Fires plot
# color = 'tab:red'
# ax2.set_xlabel('Date')
# ax2.set_ylabel('Rolling Average of Fires (Last 7 Days)', color=color)
# ax2.plot(data['Date'], data['Rolling Average Fires (Last 7 Days)'], color=color)
# ax2.tick_params(axis='y', labelcolor=color)
# ax2.set_title('Rolling Average of Forest Fires over Last 7 Days in Victoria, BC')

# # Improve layout
# plt.tight_layout()

# # Show plot
# plt.show()

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Create a date range for one year
dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')

# Generate synthetic data for rainfall with seasonal variation
rainfall = np.where(dates.month.isin([1, 2, 11, 12]), np.random.normal(loc=8, scale=2.5, size=len(dates)), 
                    np.where(dates.month.isin([3, 4, 5, 9, 10]), np.random.normal(loc=4, scale=1.5, size=len(dates)),
                             np.random.normal(loc=0.5, scale=0.3, size=len(dates))))
rainfall = np.clip(rainfall, 0, None)  # Remove negative values for rainfall

# Generate synthetic data for number of fires, adjusting to show dramatic seasonal differences
fires = np.where(dates.month.isin([6, 7, 8]), np.random.poisson(lam=3, size=len(dates)), 
                 np.random.poisson(lam=0.1, size=len(dates)))

# Generate synthetic data for the size of fires in hectares
fire_sizes = np.where(fires > 0, np.random.uniform(1, 100, size=len(dates)), 0)  # Fires range from 1 to 100 hectares

# Assign causes to the fires: 1 for human-caused, 0 for natural
fire_causes = np.where(fires > 0, np.random.choice([1, 0], p=[0.3, 0.7], size=len(dates)), 0)  # 30% human-caused, 70% natural

# Create a DataFrame to hold the data
data = pd.DataFrame({
    'Date': dates,
    'Rainfall': rainfall,
    'Fires': fires,
    'Fire Sizes': fire_sizes,
    'Fire Causes': fire_causes
})

# Calculate the cumulative rainfall over the last 7 days
data['Cumulative Rainfall (Last 7 Days)'] = data['Rainfall'].rolling(window=7, min_periods=1).sum()

# Create the plot
fig, ax = plt.subplots(figsize=(14, 6))

# Scatter plot for fires, color-coded by cause
for i in data[data['Fires'] > 0].index:
    if data.loc[i, 'Fire Causes'] == 1:  # Human-caused fires
        color = 'red'
    else:  # Natural fires
        color = 'green'
    ax.scatter(data.loc[i, 'Date'], data.loc[i, 'Cumulative Rainfall (Last 7 Days)'], 
               s=data.loc[i, 'Fire Sizes'], color=color, alpha=0.6)

ax.set_xlabel('Date')
ax.set_ylabel('Cumulative Rainfall (mm, Last 7 Days)')
ax.set_title('Forest Fires vs. Cumulative Rainfall over Last 7 Days in Victoria, BC, Colored by Cause')
ax.grid(True)

# Show plot
plt.show()

