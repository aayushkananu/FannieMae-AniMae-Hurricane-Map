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


headers = {
    'Authorization': f'Bearer {api_key}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

payload = {
    "m": "2022.1",
    "facilities": [{
        "id": "1",
        "name": "New Orleans Location",
        "activity": "residential",
        "city": "New Orleans",
        "state": "LA",
        "country": "United States",
        "latitude": 29.9511,
        "longitude": -90.0715
    }]
}

# Step 2: Make API request to get job ID
response = requests.post(f'https://{host_name}/AppsServices/api/v1/score-facilities-impact/jobs', json=payload, headers=headers)
job_details = response.json()
job_id = job_details['job_id']
print(f"Job ID: {job_id}")

# Step 3: Retrieve the results
# Note: In a real scenario, you would likely need to add a delay or polling mechanism to wait for the job to complete.
result_response = requests.get(f'https://{host_name}/AppsServices/api/v1/jobs/{job_id}', headers=headers)
job_results = result_response.json()

# Assuming the job has completed and results are available
print(job_results)