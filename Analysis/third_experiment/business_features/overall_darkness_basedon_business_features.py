import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Load the CSV file with the website darkness data
csv_file = '/Users/mohammadyekeh/Desktop/Dev/Thesis-Dev/Aggrigator/third_experiment/aggregated_dpd_results.csv'
data = pd.read_csv(csv_file)

# Load the JSON file with audience gender and revenue source data
json_file = '/Users/mohammadyekeh/Desktop/Dev/Thesis-Dev/Aggrigator/ecommerce_urls_verified_with_business_features.json'

# Load the JSON data
with open(json_file, 'r') as f:
    json_data = json.load(f)

# Create a mapping of website to audience gender and revenue source
website_gender = {entry['title']: entry['Target Audience Gender'] for entry in json_data}
website_revenue = {entry['title']: entry['Online Revenue Source'] for entry in json_data}

# Function to convert to numeric and ignore failed results
def to_numeric_ignore_failed(x):
    return pd.to_numeric(x, errors='coerce')

# Apply the function to all columns except 'website'
for col in data.columns[1:]:
    data[col] = to_numeric_ignore_failed(data[col])

# Initialize an empty list to store the results
results = []

# Process each website
for _, row in data.iterrows():
    website = row['website']
    # Group the scores by run (excluding the website column)
    for i in range(1, len(row) - 1, 5):  # Step by 5 to group categories for each run
        run_scores = row[i:i+5]
        run_sum = run_scores.sum()
        if not np.isnan(run_sum):  # Only include if the sum is not NaN
            results.append({'website': website, 'darkness': run_sum})

# Create a new DataFrame from the results
df_summed = pd.DataFrame(results)

# Calculate median darkness for sorting
df_summed['median_darkness'] = df_summed.groupby('website')['darkness'].transform('median')

# Sort dataframe by median darkness in ascending order (reversed)
df_sorted = df_summed.sort_values('median_darkness', ascending=True)

# First Output: Color based on Target Audience Gender
df_sorted['gender_hue'] = df_sorted['website'].map(lambda x: website_gender.get(x, 'Not Certain'))
# Define a color palette for gender
gender_palette = {'Female': 'orange', 'Male': 'blue', 'Not Certain': 'lightgray'}

# Create the gender plot
plt.figure(figsize=(12, 8))
ax = sns.boxplot(x='website', y='darkness', data=df_sorted, hue='gender_hue', palette=gender_palette)
plt.title('Darkness of Websites Based on Gender')
ax.set(xlabel='Websites Ordered by Darkness (Low to High)', ylabel='Darkness (0 - 50)')
plt.ylim(0, 50)  # Set y-axis scale between 0 and 50

# Remove the website names from the x-axis ticks
ax.set_xticklabels(['']*len(ax.get_xticklabels()))  # Replace website names with empty strings
plt.legend(title='Target Audience Gender')

# Save the figure
plt.savefig('darkness_by_gender.png', bbox_inches='tight')

# Show the plot
plt.show()

# Second Output: Color based on Online Revenue Source
df_sorted['revenue_hue'] = df_sorted['website'].map(lambda x: website_revenue.get(x, 'Not Certain'))
# Define a color palette for revenue
revenue_palette = {'Yes': 'orange', 'No': 'blue', 'Not Certain': 'lightgray'}

# Create the revenue plot
plt.figure(figsize=(12, 8))
ax = sns.boxplot(x='website', y='darkness', data=df_sorted, hue='revenue_hue', palette=revenue_palette)
plt.title('Darkness of Websites Based on Online Revenue Source')
ax.set(xlabel='Websites Ordered by Darkness (Low to High)', ylabel='Darkness (0 - 50)')
plt.ylim(0, 50)  # Set y-axis scale between 0 and 50

# Remove the website names from the x-axis ticks
ax.set_xticklabels(['']*len(ax.get_xticklabels()))  # Replace website names with empty strings
plt.legend(title='Online Revenue Source')

# Save the figure
plt.savefig('darkness_by_revenue.png', bbox_inches='tight')

# Show the plot
plt.show()
