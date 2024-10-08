import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import io
import time
import logging
import json
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s'
)

# Add FileHandler for output-logs.txt
file_handler = logging.FileHandler('output-logs.txt')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s'))
logging.getLogger('').addHandler(file_handler)

def take_screenshot(url, width=1024, height=768, resize_factor=0.5):
    logging.info(f"Taking screenshot of {url}")
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument(f"--window-size={width},{height}")
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        
        time.sleep(3)  # Adjust based on the time it takes for the website to load
        logging.info("Website loaded, taking screenshot")
        screenshot = driver.get_screenshot_as_png()
        
        driver.quit()
        
        # Resize the screenshot
        logging.info("Resizing the screenshot")
        image = Image.open(io.BytesIO(screenshot))
        resized_image = image.resize((int(image.width * resize_factor), int(image.height * resize_factor)))
        
        output = io.BytesIO()
        resized_image.save(output, format="PNG")
        logging.info("Screenshot resized and saved")
        return output.getvalue()
    except Exception as e:
        logging.error(f"Error taking screenshot: {str(e)}")
        return None

def upload_image_to_server(image_data, image_name):
    logging.info(f"Uploading image {image_name} to the server")
    try:
        upload_url = "https://app.433-cloud.com/api/user/upload-image"  # Replace with the actual upload URL
        files = {'image': (image_name, image_data, 'image/png')}
        response = requests.post(upload_url, files=files)
        
        if response.status_code == 201:
            logging.info(f"Image {image_name} uploaded successfully")
            return response.json().get('image_url')
        else:
            logging.error(f"Failed to upload image. Status code: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Error uploading image: {str(e)}")
        return None

def analyze_image_with_openai(image_url, api_token):
    refined_description_prompt = """
      You are a dark pattern detector agent. You will process the website image that sent and detect and describe any dark patterns, including their categories. 
      Note this, all websites tends to have darkpatterns, so be as precise as possible and be critical about every elements.
      Also it is good if in your final output assign 0 to 10 to each categories.
            
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
      Please return your output in json like this format
      {
  "website_analysis": {
    "category_scores": {
      "Asymmetric": {
        "score": 7
      },
      "Covert": {
        "score": 4
      },
      "Deceptive": {
        "score": 6
      },
      "Hides Information": {
        "score": 8
      },
      "Restrictive": {
        "score": 9
      }
    },
    "overall_assessment": {
      "total_score": 34,
      "max_possible_score": 50,
      "summary": "The website employs several dark patterns, with particularly high scores in Restrictive and Hides Information categories. The presentation is noticeably biased, and important information is often obscured or only revealed late in the process."
    }
  }
}
      --------------------

     
    """

    logging.info(f"Analyzing image at {image_url} with GPT-4V")
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_token}"
            },
            json={
                "model": "gpt-4o",
                "messages": [
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
                                    "url": image_url
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 1000
            }
        )

        if response.status_code == 200:
            data = response.json()
            logging.info("Image analysis successful")
            return data["choices"][0]["message"]["content"]
        else:
            error_message = f"Image analysis failed. Status code: {response.status_code}, Response: {response.text}"
            logging.error(error_message)
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

def process_websites(websites, api_token):
    logging.info("Processing websites")
    final_result = []
    
    for site in websites:
        title = site.get('title')
        link = site.get('link')
        
        try:
            # Take a screenshot of the webpage
            screenshot = take_screenshot(link)
            if screenshot is None:
                logging.error(f"Failed to take screenshot for {title}. Skipping to next website.")
                continue
            
            # Upload the screenshot to the server and get the image URL
            image_url = upload_image_to_server(io.BytesIO(screenshot), f'{title}.png')
            if image_url is None:
                logging.error(f"Failed to upload image for {title}. Skipping to next website.")
                continue
            
            # Send the image URL to OpenAI for analysis
            analysis_result = analyze_image_with_openai(image_url, api_token)
            if analysis_result is None:
                logging.error(f"Failed to analyze image for {title}. Skipping to next website.")
                continue
            
            # Parse the scores from the analysis result
            parsed_result = parse_scores(analysis_result)
            parsed_result["website"] = title
            final_result.append(parsed_result)
            
            logging.info(f"Successfully processed {title}")
        except Exception as e:
            logging.error(f"Error processing {title}: {str(e)}")
            continue
    
    logging.info("All websites processed")
    return final_result

def write_results_to_file(results, filename='output_dpd.txt'):
    logging.info(f"Writing results to {filename}")
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
        logging.info(f"Results written to {filename}")
    except Exception as e:
        logging.error(f"Error writing results to file: {str(e)}")

def read_ecommerce_urls(filename='ecommerce_urls.json'):
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
        results = process_websites(websites, api_token)
        logging.info("Results obtained successfully")
        write_results_to_file(results)
    else:
        logging.error("No websites to process. Check the ecommerce_urls.json file.")