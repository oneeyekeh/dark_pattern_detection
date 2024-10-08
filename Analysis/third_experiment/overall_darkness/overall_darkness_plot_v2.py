import pandas as pd
import plotly.express as px
import numpy as np

# Read the CSV file
csv_file = '/Users/mohammadyekeh/Desktop/Dev/Thesis-Dev/Aggrigator/third_experiment/aggregated_dpd_results.csv'
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

# Sort dataframe by median darkness in ascending order (reversed)
df_sorted = df_summed.sort_values('median_darkness', ascending=True)

# Create a box plot with Plotly
fig = px.box(df_sorted, x='website', y='darkness', 
              title='Darkness of Websites Across Runs (Sorted)', 
              labels={'website': 'Websites Ordered by Darkness (Low to High)', 
                      'darkness': 'Darkness (0 - 50)'},
              color='website',  # Add color for better distinction
              hover_name='website')  # Add hover information for websites

# Highlight specific websites in orange
highlighted_websites = ["Amazon", "Costco", "Shein", "Fenty", "Birchbox", "Apple", "Nike", "Make", "PrettyLittleThing", "Amart"]

# Update the color for highlighted websites
for website in highlighted_websites:
    fig.add_traces(px.box(df_sorted[df_sorted['website'] == website], x='website', y='darkness').data)

# Change the fill color for highlighted websites
for trace in fig.data:
    if trace.name in highlighted_websites:
        trace.marker.color = 'orange'

# Show the figure
fig.show()

# Print sorted median darkness scores and number of successful runs
print("Sorted Median Darkness Scores and Successful Runs:")
for i, (website, group) in enumerate(df_sorted.groupby('website'), 1):
    median_darkness = group['median_darkness'].iloc[0]
    successful_runs = group['darkness'].count()
    print(f"Website {i}: Median Darkness = {median_darkness:.2f}, Successful Runs = {successful_runs}")
