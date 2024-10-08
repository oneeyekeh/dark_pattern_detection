import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Read the CSV file
csv_file = '/Users/mohammad.yekeh/Desktop/Dev/Thesis-Dev/Aggrigator/third_experiment/aggregated_dpd_results.csv'
data = pd.read_csv(csv_file)

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

# Sort dataframe by median darkness
df_sorted = df_summed.sort_values('median_darkness', ascending=False)

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 16))
plt.figure(figsize=(18, 12))  # Adjust figure size for better resolution and space
sns.set(style="whitegrid")  # Set the background style for better readability
# Box plot for darkness of websites (sorted and anonymized)
sns.boxplot(x='website', y='darkness', data=df_sorted, ax=ax1, order=df_sorted['website'].unique())
ax1.set_title('Darkness of Websites Across Runs (Sorted, Failed Results Ignored)')
ax1.set_xlabel('Websites (Anonymized)')
ax1.set_ylabel('Darkness (Sum of 5 Categories per Run)')
ax1.set_xticklabels([])  # Remove x-axis labels

# Box plot for overall darkness across all websites
sns.boxplot(y='darkness', data=df_sorted, ax=ax2)
ax2.set_title('Overall Darkness Across All Websites (Failed Results Ignored)')
ax2.set_xlabel('All Websites')
ax2.set_ylabel('Darkness (Sum of 5 Categories per Run)')

plt.tight_layout()
plt.savefig(f"overall_darkness_across_all_websites.png", dpi=300)  # Save the plot as a high-resolution image
plt.show()


# Print sorted median darkness scores and number of successful runs
print("Sorted Median Darkness Scores and Successful Runs:")
for i, (website, group) in enumerate(df_sorted.groupby('website'), 1):
    median_darkness = group['median_darkness'].iloc[0]
    successful_runs = group['darkness'].count()
    print(f"Website {i}: Median Darkness = {median_darkness:.2f}, Successful Runs = {successful_runs}")