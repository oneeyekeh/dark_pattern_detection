import json
import logging
from logging.handlers import RotatingFileHandler
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import io
import time
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Set up logging
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_file = 'screenshot_logs.txt'
log_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=2)
log_handler.setFormatter(log_formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

def resize_image(image_data, max_size=(1024, 1024)):
    img = Image.open(io.BytesIO(image_data))
    img.thumbnail(max_size)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG", optimize=True, quality=85)
    return buffered.getvalue()

def upload_image_to_server(image_data, image_name):
    logger.info(f"Uploading image {image_name} to the server")
    try:
        upload_url = "https://app.433-cloud.com/api/user/upload-image"
        resized_image_data = resize_image(image_data)
        files = {'image': (image_name, resized_image_data, 'image/png')}
        response = requests.post(upload_url, files=files)
        
        if response.status_code == 201:
            logger.info(f"Image {image_name} uploaded successfully")
            return response.json().get('image_url')
        else:
            logger.error(f"Failed to upload image. Status code: {response.status_code}")
            logger.error(f"Response content: {response.text}")
            return None
    except Exception as e:
        logger.error(f"Error uploading image: {str(e)}")
        return None

def bypass_blockers(driver):
    try:
        # Try to click on any "Accept Cookies" button
        accept_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'I agree')]")
        for button in accept_buttons:
            if button.is_displayed():
                button.click()
                logger.info("Clicked on 'Accept Cookies' button")
                time.sleep(2)
                break

        # Scroll down and up to simulate user behavior
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        # Randomly move the mouse
        action = ActionChains(driver)
        action.move_by_offset(random.randint(0, 500), random.randint(0, 500)).perform()

    except Exception as e:
        logger.warning(f"Error while trying to bypass blockers: {str(e)}")

def capture_screenshots(url, name):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        logger.info(f"Accessing URL: {url}")
        driver.get(url)
        time.sleep(5)  # Wait for page to load
        
        bypass_blockers(driver)
        
        screenshots = []
        
        for i in range(3):
            try:
                logger.info(f"Capturing screenshot {i+1} for {name}")
                driver.execute_script(f"window.scrollTo(0, {i * 1000});")
                time.sleep(2)  # Wait for scroll to complete
                
                screenshot = driver.get_screenshot_as_png()
                
                image_name = f"{name}_screenshot_{i+1}.png"
                image_url = upload_image_to_server(screenshot, image_name)
                
                if image_url:
                    screenshots.append(image_url)
                else:
                    logger.warning(f"Failed to upload screenshot {i+1} for {name}")
            except Exception as e:
                logger.error(f"Error capturing screenshot {i+1} for {name}: {str(e)}")
        
        return screenshots
    
    except Exception as e:
        logger.error(f"Error accessing URL for {name}: {str(e)}")
        return []
    
    finally:
        driver.quit()

def main():
    with open('ecommerce_urls.json', 'r') as f:
        ecommerce_urls = json.load(f)
    
    ecommerce_pictures = []
    
    for item in ecommerce_urls:
        name = item['title']
        url = item['link']
        
        logger.info(f"Processing {name}")
        screenshots = capture_screenshots(url, name)
        
        if screenshots:
            ecommerce_pictures.append({
                'name': name,
                'url': url,
                'screen_shot_urls': screenshots
            })
        else:
            logger.warning(f"No screenshots captured for {name}")
    
    with open('ecommerce_pictures.json', 'w') as f:
        json.dump(ecommerce_pictures, f, indent=2)
    
    logger.info("Process completed. Results saved in ecommerce_pictures.json")

if __name__ == "__main__":
    main()