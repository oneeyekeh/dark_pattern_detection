import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file generated by the previous script
csv_file = '/Users/mohammadyekeh/Desktop/Dev/Thesis-Dev/Aggrigator/third_experiment/aggregated_dpd_results.csv'
data = pd.read_csv(csv_file)

# Define the categories to be plotted
categories = ["Asymmetric", "Covert", "Deceptive", "Hides Information", "Restrictive"]

# Websites to highlight with different colors
highlighted_websites = ["Amazon", "Costco", "Shein", "Fenty", "Birchbox", "Apple", "Nike", "Make", "PrettyLittleThing", "Amart"]

# Prepare and plot the data for each category
for category in categories:
    # Extract columns related to the current category
    category_columns = [col for col in data.columns if category in col]
    
    # Create a DataFrame for the current category
    category_data = data[["website"] + category_columns]
    
    # Melt the DataFrame to long format
    category_melted = category_data.melt(id_vars=["website"], var_name="run", value_name="score")
    
    # Convert "failed" entries to NaN for proper plotting
    category_melted["score"] = pd.to_numeric(category_melted["score"], errors='coerce')
    
    # Calculate the average score for sorting websites
    avg_scores = category_melted.groupby('website')['score'].mean()
    sorted_websites = avg_scores.sort_values(ascending=True).index  # Reverse sorting here
    
    # Sort the DataFrame by website based on the reversed sorted list
    category_melted["website"] = pd.Categorical(category_melted["website"], categories=sorted_websites, ordered=True)
    
    # Plot the boxplot
    plt.figure(figsize=(18, 12))  # Adjust figure size for better resolution and space
    sns.set(style="whitegrid")  # Use a white background grid style
    ax = sns.boxplot(x='website', y='score', data=category_melted, fliersize=6, boxprops=dict(facecolor='lightgray'))  # Set default boxes to gray
    
    # Customize the plot
    plt.title(f"Dark Pattern Scores for {category}", fontsize=20, fontweight='bold')
    plt.xticks([])  # Remove x-axis labels for cleaner visualization
    plt.xlabel("Websites Ordered by Darkness (Low to High)", fontsize=18)  # X-axis label
    plt.ylabel(f"Darkness Score (0 - 10)", fontsize=18)  # Y-axis label
    plt.ylim(0, 10)  # Set y-axis limits from 0 to 10
    
    # Add gridlines for better readability
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    
    # Highlight specific websites with different colors
    for i, patch in enumerate(ax.patches):
        website = sorted_websites[i]
        if website in highlighted_websites:
            patch.set_edgecolor('grey')  # Change the edge color of the box
            patch.set_facecolor('orange')  # Customize with different color for highlighted websites
    
    # Improve the layout and save the figure
    plt.tight_layout()
    plt.savefig(f"{category}_boxplot_highlighted_reversed.png", dpi=300)  # Save the plot as a high-resolution image
    plt.show()