# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Read the CSV file
# csv_file = 'aggregated_dpd_results.csv'
# data = pd.read_csv(csv_file)

# # Function to convert to numeric and ignore failed results
# def to_numeric_ignore_failed(x):
#     return pd.to_numeric(x, errors='coerce')

# # Apply the function to all columns except 'website'
# for col in data.columns[1:]:
#     data[col] = to_numeric_ignore_failed(data[col])

# # Melt the dataframe to long format
# df_melted = data.melt(id_vars=['website'], var_name='run_category', value_name='score')

# # Split the 'run_category' column into 'run' and 'category'
# df_melted[['run', 'category']] = df_melted['run_category'].str.split('_', n=1, expand=True)

# # List of categories
# categories = df_melted['category'].unique()
# num_categories = len(categories)

# # Calculate the number of rows and columns for subplots
# num_rows = (num_categories + 1) // 2  # Round up to the nearest integer
# num_cols = 2 if num_categories > 1 else 1

# # Create a figure with subplots, one for each category
# fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5*num_rows))
# fig.suptitle('Distribution of Dark Pattern Categories Across Websites', fontsize=16)

# # Flatten the axes array if it's 2D
# if num_categories > 1:
#     axes = axes.flatten()

# # Create a box plot for each category
# for i, category in enumerate(categories):
#     category_data = df_melted[df_melted['category'] == category]
    
#     # Calculate median score for sorting
#     median_scores = category_data.groupby('website')['score'].median().sort_values(ascending=False)
#     sorted_websites = median_scores.index

#     # Create the box plot
#     ax = axes[i] if num_categories > 1 else axes
#     sns.boxplot(x='website', y='score', data=category_data, ax=ax, order=sorted_websites)
#     ax.set_title(f'Distribution of {category.capitalize()} Scores')
#     ax.set_xlabel('')
#     ax.set_ylabel('Score')
#     ax.set_xticklabels([])  # Remove x-axis labels

# # Remove any unused subplots
# if num_categories > 1:
#     for j in range(i+1, len(axes)):
#         fig.delaxes(axes[j])

# plt.tight_layout()
# plt.show()

# # Print summary statistics for each category
# print("Summary Statistics for Each Category:")
# for category in categories:
#     category_data = df_melted[df_melted['category'] == category]
#     print(f"\n{category.capitalize()}:")
#     summary = category_data.groupby('website')['score'].agg(['median', 'mean', 'std', 'min', 'max'])
#     summary = summary.sort_values('median', ascending=False)
#     for i, (website, stats) in enumerate(summary.iterrows(), 1):
#         print(f"Website {i}:")
#         print(f"  Median: {stats['median']:.2f}")
#         print(f"  Mean: {stats['mean']:.2f}")
#         print(f"  Std Dev: {stats['std']:.2f}")
#         print(f"  Min: {stats['min']:.2f}")
#         print(f"  Max: {stats['max']:.2f}")