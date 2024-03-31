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

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming you've already loaded the housing data as 'df_long'
# and also assuming you have a DataFrame 'df_risk_scores' with columns:
# 'Year', 'FloodRiskScore', 'HeatStressScore', 'HurricaneRiskScore', and 'AverageHousingPrice'

# Let's create a mock 'df_risk_scores' DataFrame for illustration purposes
data = {
    'Year': [2015, 2016, 2017, 2018, 2019, 2020],
    'FloodRiskScore': [2, 2.5, 3, 3.5, 4, 4.5],
    'HeatStressScore': [1, 1.5, 2, 2.5, 3, 3.5],
    'HurricaneRiskScore': [0.5, 1, 5, 1.5, 2, 2.5],
    'AverageHousingPrice': [200000, 210000, 220000, 230000, 240000, 250000]  # Mock data
}
df_risk_scores = pd.DataFrame(data)

# Calculate the correlation matrix
corr = df_risk_scores.corr()

# Generate a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap between Housing Prices and Climate Risk Scores')
plt.show()
