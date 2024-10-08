import json
import csv
import os

# List of JSON files
json_files = [f'output_dpd_run{i}.json' for i in range(1, 11)]

# Output CSV file
output_csv = 'aggregated_dpd_results.csv'

# Define the categories to be tracked
categories = ["Asymmetric", "Covert", "Deceptive", "Hides Information", "Restrictive"]

# Function to extract scores from a run
def extract_scores(json_data, run_number):
    results = {}
    for website_data in json_data:
        website = website_data.get("website", "unknown")
        analysis_result = website_data.get("analysis_result")
        
        if analysis_result:
            category_scores = analysis_result.get("category_scores", {})
            for category in categories:
                key = f"{category}_run{run_number}"
                score = category_scores.get(category, {}).get("score", "failed")
                results.setdefault(website, {})[key] = score
        else:
            # Mark as failed if there are no analysis results
            for category in categories:
                key = f"{category}_run{run_number}"
                results.setdefault(website, {})[key] = "failed"
    
    return results

# Collect data from all runs
all_results = {}
for i, json_file in enumerate(json_files, 1):
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            try:
                data = json.load(f)
                run_results = extract_scores(data, i)
                for website, scores in run_results.items():
                    if website not in all_results:
                        all_results[website] = {}
                    all_results[website].update(scores)
            except json.JSONDecodeError:
                print(f"Error decoding JSON from file: {json_file}")
    else:
        print(f"File not found: {json_file}")
        for website in all_results.keys():
            for category in categories:
                all_results[website][f"{category}_run{i}"] = "failed"

# Create the CSV file
with open(output_csv, 'w', newline='') as csvfile:
    fieldnames = ['website'] + [f"{category}_run{i}" for i in range(1, 11) for category in categories]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for website, scores in all_results.items():
        row = {"website": website}
        row.update(scores)
        writer.writerow(row)

print(f"CSV file '{output_csv}' created successfully.")
