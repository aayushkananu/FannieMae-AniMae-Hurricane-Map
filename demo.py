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

# Filter for a specific region to simplify the initial visualization
# For example, let's visualize the trend for "New York, NY"
new_orleans_prices = df_long[df_long['RegionName'] == "New Orleans, LA"]

# Plot 1: Housing Price Trend for New Orleans with Katrina Highlight
plt.figure(figsize=(12, 6))
sns.lineplot(data=new_orleans_prices, x='Date', y='HousingPrice', label='Monthly Housing Prices')
plt.axvline(pd.to_datetime('2005-08-29'), color='r', linestyle='--', lw=2, label='Hurricane Katrina')
plt.title('Housing Price Trend for New Orleans, LA (Highlighting Hurricane Katrina)')
plt.xlabel('Date')
plt.ylabel('Housing Price')
plt.legend()
plt.xticks(rotation=45)
plt.show()

# Plot 2: Year-over-Year Change in Housing Prices
new_orleans_prices['Year'] = new_orleans_prices['Date'].dt.year
yearly_prices = new_orleans_prices.groupby('Year')['HousingPrice'].mean().pct_change().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=yearly_prices, x='Year', y='HousingPrice', palette='coolwarm')
plt.axhline(0, color='grey', linestyle='--')
plt.title('Year-over-Year Percentage Change in Housing Prices for New Orleans, LA')
plt.xlabel('Year')
plt.ylabel('Percentage Change')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot 3: Pre and Post Katrina Price Distributions
pre_katrina = new_orleans_prices[new_orleans_prices['Date'] < '2005-08-29']
post_katrina = new_orleans_prices[new_orleans_prices['Date'] > '2005-08-29']

plt.figure(figsize=(10, 6))
sns.histplot(pre_katrina['HousingPrice'], color='blue', kde=True, label='Pre-Katrina', alpha=0.6)
sns.histplot(post_katrina['HousingPrice'], color='red', kde=True, label='Post-Katrina', alpha=0.6)
plt.title('Distribution of Housing Prices in New Orleans, LA Before and After Hurricane Katrina')
plt.xlabel('Housing Price')
plt.legend()
plt.tight_layout()
plt.show()


# Setting up the headers
headers = {
    'Authorization': api_key,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# The body of the POST request
payload = {
    "m": "2022.1",
    "facilities": [{
        "id": "1",
        "name": "berkeley office",
        "activity": "office",
        "street1": "2000 hearst avenue",
        "city": "berkeley",
        "state": "ca",
        "postal_code": "94709",
        "country": "united states",
        "latitude": 37.8734494,
        "longitude": -122.2706614
    }]
}

# Making the POST request to create a job
response = requests.post(f'https://{host_name}/AppsServices/api/v1/score-facilities-impact/jobs', json=payload, headers=headers)

# Checking the response
if response.status_code == 200:
    print("Job created successfully.")
    job_id = response.json()['job_id']
    print("Job ID:", job_id)
else:
    print("Failed to create job. Status Code:", response.status_code)
