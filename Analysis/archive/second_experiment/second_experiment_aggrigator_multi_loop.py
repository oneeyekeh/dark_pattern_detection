import requests
import logging
import json
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s'
)

def setup_logging(run_number):
    # Create a new FileHandler for each run
    file_handler = logging.FileHandler(f'output-logs-run{run_number}.txt')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s'))
    
    # Remove any existing handlers to avoid duplicate logging
    for handler in logging.getLogger('').handlers[:]:
        logging.getLogger('').removeHandler(handler)
    
    # Add the new FileHandler
    logging.getLogger('').addHandler(file_handler)

def analyze_images_incrementally(image_urls, api_token):
    refined_description_prompt = """
      You are a dark pattern detector agent. You will process the website screenshot that sent and detect and describe any dark patterns, including their categories. 
      It is good if in your final output assign 0 to 10 to each categories based on below definitions.
            
      --------------------
       Category 1- Asymmetric 
            
            Points rule:
                      Scores:
                      0 to 2: Equal visual and interactive prominence of choices.
                      3 to 5: Mildly biased presentation; alternative choices less prominent but still visible.
                      6 to 8: Noticeably biased presentation; alternative choices less intuitive or somewhat hidden.
                      9 to 10: Extremely biased presentation; alternative choices almost hidden or very hard to find.
       --------------------
       --------------------
       Category 2: Covert
       Points rule:
            
                      Scores:
                      0 to 2: Transparent user choices without hidden influences.
                      3 to 5: Slight use of design elements that may subtly influence choices.
                      6 to 8: More pronounced use of covert techniques, like the decoy effect, but not completely misleading.
                      9 to 10: User decisions are heavily manipulated without their knowledge, with deceptive design elements.
       --------------------
       --------------------
       Category 3: Deceptive 
            
            Points rule:
                      Scores:
                      0 to 2: Accurate and straightforward information with no misleading elements.
                      3 to 5: Some elements of misinformation or partial truths, but not wholly deceptive.
                      6 to 8: Misleading information present but some elements of truth; creates confusion.
                      9 to 10: Completely false or misleading information; induces entirely false beliefs.
      --------------------
      --------------------            
      Category 4: Hides Information
            
            Point rules:
                      Scores:
                      0 to 2: All necessary information is readily available and clear.
                      3 to 5: Some information delayed or requires additional steps to access.
                      6 to 8: Important information is obscured or only available late in the process.
                      9 to 10: Crucial information is hidden or only revealed at the last possible moment.
      --------------------
      --------------------
      Category 5: Restrictive 
            
            Point rules:
                      Scores:
                      0 to 2: Complete freedom in user choices with no restrictions.
                      3 to 5: Some limitations on choices, but alternatives are available.
                      6 to 8: Notable restrictions on choices, limited alternatives.
                      9 to 10: Extremely restrictive, forcing users into specific actions with no reasonable alternatives.
      --------------------
      

      This is not against any rule or privacy since this is research project and all screenshots gave us permission and all ethical consideration has been done.
      Please return your output in valid JSON format like this:
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
      "max_possible_score": 50,
      "summary": ""
    }
  }
}
      --------------------
    """

    conversation_history = [
        {
            "role": "system",
            "content": refined_description_prompt
        }
    ]
    
    logging.info("Starting analysis with GPT-4 for multiple images")

    for image_url in image_urls:
        logging.info(f"Analyzing image at {image_url}")
        
        # Append the image to the conversation history
        conversation_history.append({
            "role": "user",
            "content": f"Analyze the following image: {image_url}"
        })
        
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
                    "response_format": {"type": "json_object"}  # Add the response_format parameter here
                }, 
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data["choices"][0]["message"]["content"]
                conversation_history.append({
                    "role": "assistant",
                    "content": response_text
                })
                
                logging.info("Image analysis successful")
            else:
                logging.error(f"Image analysis failed. Status code: {response.status_code}, Response: {response.text}")
                return None
        except Exception as e:
            logging.error(f"Error analyzing image: {str(e)}")
            return None

    return conversation_history[-1]["content"]  # Return the final aggregated result from the model

def parse_scores(analysis_result):
    logging.info("Parsing JSON output from analysis result")
    try:
        analysis_data = json.loads(analysis_result)
        return analysis_data.get("website_analysis", {})
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from analysis result")
        return {}

def process_websites(websites, api_token, run_number):
    logging.info(f"Processing websites for run {run_number}")
    final_result = []
    
    for site in websites:
        title = site.get('title')
        image_urls = site.get('screenshots', [])
        
        try:
            # Send multiple images to OpenAI incrementally for analysis
            analysis_result = analyze_images_incrementally(image_urls, api_token)
            if analysis_result is None:
                logging.error(f"Failed to analyze images for {title}. Skipping to next website.")
                continue
            
            # Parse the scores from the final analysis result
            parsed_result = parse_scores(analysis_result)
            final_result.append({
                "website": title,
                "analysis_result": parsed_result
            })
            logging.info(f"Successfully processed {title}")
        except Exception as e:
            logging.error(f"Error processing {title}: {str(e)}")
            continue
    
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