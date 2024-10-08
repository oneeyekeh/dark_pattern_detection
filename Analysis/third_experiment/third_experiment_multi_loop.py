import requests
import logging
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s'
)

def setup_logging(run_number):
    file_handler = logging.FileHandler(f'output-logs-run{run_number}.txt')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s'))
    
    for handler in logging.getLogger('').handlers[:]:
        logging.getLogger('').removeHandler(handler)
    
    logging.getLogger('').addHandler(file_handler)

def analyze_single_image(image_url, api_token):
    refined_description_prompt = """
      A dark pattern is a user interface design that deliberately manipulates or tricks users into making decisions they would not otherwise choose. These patterns often exploit cognitive biases and can mislead users, making interactions with websites or applications unfair or frustrating. Dark patterns typically fall into categories such as asymmetric choices, covert influences, deceptive information, hidden details, or restrictive actions.
        As a dark pattern detector, your task is to analyze the website screenshot provided and detect any dark patterns that fall into the following five categories. Assign a score from 0 to 10 for each category based on the guidelines below:
------------------
        Categories & Scoring:
        Asymmetric
        0-2: Equal visual and interactive prominence of choices.
        3-5: Mild bias; alternative choices less prominent but still visible.
        6-8: Noticeable bias; alternative choices are less intuitive or somewhat hidden.
        9-10: Extreme bias; alternative choices are almost hidden or difficult to find.
------------------
        Covert
        0-2: Transparent user choices with no hidden influences.
        3-5: Slight use of design elements to subtly influence decisions.
        6-8: Pronounced covert techniques (e.g., decoy effect) but not entirely misleading.
        9-10: Heavily manipulative design elements without the user's knowledge.
------------------
        Deceptive
        0-2: Information is accurate and straightforward.
        3-5: Some misinformation or partial truths, but not wholly deceptive.
        6-8: Misleading information with some truth; can cause confusion.
        9-10: Entirely false or misleading information, inducing false beliefs.
------------------
        Hides Information
        0-2: All necessary information is clear and accessible.
        3-5: Some information is delayed or requires extra steps to find.
        6-8: Important information is obscured or only available later in the process.
        9-10: Crucial information is hidden or revealed at the last possible moment.
------------------
        Restrictive
        0-2: Users have complete freedom in their choices.
        3-5: Some restrictions on choices, but alternatives are still available.
        6-8: Noticeable restrictions with limited alternatives.
        9-10: Extremely restrictive, forcing users into specific actions with no alternatives.
------------------
        Ethical Considerations:
        This research project complies with ethical standards, and all screenshots have been provided with explicit permission.
------------------    
      Return the analysis in valid JSON format like this:
      {
  "website_analysis": {
    "category_scores": {
      "Asymmetric": {
        "score": 
      },
      "Covert": {
        "score": 
      },
      "Deceptive": {
        "score": 
      },
      "Hides Information": {
        "score": 
      },
      "Restrictive": {
        "score": 
      }
    },
    "overall_assessment": {
      "total_score": ,
      "summary": ""
    }
  }
}
"""
    conversation_history = [
        {
            "role": "system",
            "content": refined_description_prompt
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                    }
                },
            ],
        }
    ]
    
    logging.info(f"Analyzing image at {image_url}")
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_token}"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": conversation_history,
                "response_format": {"type": "json_object"} 
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            response_text = data["choices"][0]["message"]["content"]
            logging.info("Image analysis successful")
            return response_text
        else:
            logging.error(f"Image analysis failed. Status code: {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        logging.error(f"Error analyzing image: {str(e)}")
        return None

def parse_scores(analysis_result):
    logging.info("Parsing JSON output from analysis result")
    try:
        analysis_data = json.loads(analysis_result)
        return analysis_data.get("website_analysis", {})
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from analysis result")
        return {}

def process_single_website(site, api_token):
    title = site.get('title')
    image_url = site.get('screenshots', [])[0]  # Get the single screenshot URL
    
    try:
        # Send the single image to OpenAI for analysis
        analysis_result = analyze_single_image(image_url, api_token)
        if analysis_result is None:
            logging.error(f"Failed to analyze image for {title}. Skipping to next website.")
            return None
        
        # Parse the scores from the final analysis result
        parsed_result = parse_scores(analysis_result)
        logging.info(f"Successfully processed {title}")
        return {
            "website": title,
            "analysis_result": parsed_result
        }
    except Exception as e:
        logging.error(f"Error processing {title}: {str(e)}")
        return None

def process_websites(websites, api_token, run_number):
    logging.info(f"Processing websites for run {run_number}")
    final_result = []
    
    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = [executor.submit(process_single_website, site, api_token) for site in websites]
        for future in as_completed(futures):
            result = future.result()
            if result:
                final_result.append(result)
    
    logging.info(f"All websites processed for run {run_number}")
    return final_result

def write_results_to_file(results, run_number):
    filename = f'output_dpd_run{run_number}.json'
    logging.info(f"Writing results to {filename}")
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
        logging.info(f"Results written to {filename}")
    except Exception as e:
        logging.error(f"Error writing results to file: {str(e)}")

def read_ecommerce_urls(filename='/Users/mohammad.yekeh/Desktop/Dev/Thesis-Dev/Aggrigator/ecommerce_urls_verified.json'):
    logging.info(f"Reading ecommerce URLs from {filename}")
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"File {filename} not found")
        return []
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from {filename}")
        return []

# Main execution
if __name__ == "__main__":
    api_token = "open_ai_api_key"
    websites = read_ecommerce_urls()
    if websites:
        for run in range(1, 11):  # 10 runs
            setup_logging(run)
            logging.info(f"Starting run {run}")
            results = process_websites(websites, api_token, run)
            logging.info(f"Results obtained successfully for run {run}")
            write_results_to_file(results, run)
            logging.info(f"Completed run {run}")
