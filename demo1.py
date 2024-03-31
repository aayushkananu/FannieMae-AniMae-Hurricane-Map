import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import requests

# Your API key and host name
api_key = 'ahp-NeDVrcXNJhGKfRG&L&THOdhZ2_N7Jq7R-ag'
host_name = 'api-use1.rms.com'  # or 'api-use1.rms.com' based on your region

# Step 1: Load the CSV
df = pd.read_csv('zillow_housing_data.csv')

# Step 2: Melt the DataFrame to convert it from wide to long format
df_long = pd.melt(df, id_vars=['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName'],
                  var_name='Date', value_name='HousingPrice')

# Convert 'Date' to datetime
df_long['Date'] = pd.to_datetime(df_long['Date'])

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Assuming 'df_long' is already loaded and contains the relevant housing data
# Step 1: Filter data for a specific region in Texas potentially affected by Hurricane Harvey
# For the sake of this example, let's consider Houston, TX
houston_prices = df_long[df_long['RegionName'] == "Houston, TX"]

# Step 2: Highlighting the period around Hurricane Harvey
# Harvey hit Texas in late August 2017

# Plot 1: Housing Price Trend for Houston with Harvey Highlight
plt.figure(figsize=(12, 6))
sns.lineplot(data=houston_prices, x='Date', y='HousingPrice', label='Monthly Housing Prices')
plt.axvline(pd.to_datetime('2017-08-25'), color='r', linestyle='--', lw=2, label='Hurricane Harvey')
plt.title('Housing Price Trend for Houston, TX (Highlighting Hurricane Harvey)')
plt.xlabel('Date')
plt.ylabel('Housing Price')
plt.legend()
plt.xticks(rotation=45)
plt.show()

# Plot 2: Year-over-Year Change in Housing Prices
houston_prices['Year'] = houston_prices['Date'].dt.year
yearly_prices_houston = houston_prices.groupby('Year')['HousingPrice'].mean().pct_change().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=yearly_prices_houston, x='Year', y='HousingPrice', palette='coolwarm')
plt.axhline(0, color='grey', linestyle='--')
plt.title('Year-over-Year Percentage Change in Housing Prices for Houston, TX')
plt.xlabel('Year')
plt.ylabel('Percentage Change')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot 3: Pre and Post Harvey Price Distributions
pre_harvey = houston_prices[houston_prices['Date'] < '2017-08-25']
post_harvey = houston_prices[houston_prices['Date'] > '2017-08-25']

plt.figure(figsize=(10, 6))
sns.histplot(pre_harvey['HousingPrice'], color='blue', kde=True, label='Pre-Harvey', alpha=0.6)
sns.histplot(post_harvey['HousingPrice'], color='red', kde=True, label='Post-Harvey', alpha=0.6)
plt.title('Distribution of Housing Prices in Houston, TX Before and After Hurricane Harvey')
plt.xlabel('Housing Price')
plt.legend()
plt.tight_layout()
plt.show()

corr_df = df.set_index('Year').corr()

# Plotting the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr_df, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation between Housing Prices and Climate Risk Scores')
plt.show()
