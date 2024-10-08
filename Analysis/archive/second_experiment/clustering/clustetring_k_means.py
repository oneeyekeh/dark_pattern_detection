import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load data
csv_file = '/Users/mohammad.yekeh/Desktop/Dev/Thesis-Dev/Aggrigator/second_experiment/aggregated_dpd_results.csv'
data = pd.read_csv(csv_file)

# Define categories and aggregate scores across runs
categories = ["Asymmetric", "Covert", "Deceptive", "Hides Information", "Restrictive"]

# Initialize dictionary for aggregated data
aggregated_data = {}

# Aggregate scores for each category across runs
for category in categories:
    cols = [f"{category}_run{i+1}" for i in range(9)]
    
    # Convert to numeric and ignore errors
    data[cols] = data[cols].apply(pd.to_numeric, errors='coerce')
    
    # Drop rows with NaN values in these columns
    data = data.dropna(subset=cols)
    
    # Calculate mean for each category
    aggregated_data[category] = data[cols].mean(axis=1)

# Create a DataFrame with aggregated data
aggregated_df = pd.DataFrame(aggregated_data)
aggregated_df['website'] = data['website'].reset_index(drop=True)

# Print basic statistics
print("Aggregated Data:")
print(aggregated_df.describe())

# Print the number of samples
print("\nNumber of samples in the dataset:")
print(len(aggregated_df))

# Print cluster centers
scaler = StandardScaler()
scaled_data = scaler.fit_transform(aggregated_df.drop('website', axis=1))

kmeans = KMeans(n_clusters=3, n_init=20, random_state=42)
clusters = kmeans.fit_predict(scaled_data)
aggregated_df['Cluster'] = clusters

print("\nCluster Centers:")
print(pd.DataFrame(kmeans.cluster_centers_, columns=aggregated_df.columns[:-2], index=[f"Cluster {i}" for i in range(3)]))

# Save heatmap and scatterplot
plt.figure(figsize=(12, 8))
sns.heatmap(aggregated_df.set_index('website').drop('Cluster', axis=1), cmap='viridis', annot=True, fmt=".1f")
plt.title('Heatmap of Dark Pattern Scores Across Websites')
plt.savefig('heatmap_dark_patterns.png', dpi=300)
plt.show()

# Pairplot for visualizing clusters
sns.pairplot(aggregated_df, hue='Cluster', palette='viridis')
plt.savefig('pairplot_dark_patterns.png', dpi=300)
plt.show()
