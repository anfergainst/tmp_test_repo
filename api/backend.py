from selenium import webdriver
from selenium.webdriver.common.by import By  # Import the By class
from selenium.webdriver.chrome.options import Options
from flask import Flask, jsonify
from flask_cors import CORS
import time
import logging
import json

url = ''

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

def format_keys(listing_details):
    formatted_details = {}
    for key, value in listing_details.items():
        formatted_key = key.replace(' ', '_').lower()
        formatted_key = formatted_key.replace('\u00e7', 'c').replace('\u00e3', 'a').replace('\u00fa', 'u')
        formatted_key = formatted_key.replace('(', '').replace(')', '').replace('\n', '')
        formatted_details[formatted_key] = value
    return formatted_details

def get_rendered_html(url):
    options = Options()
    options.headless = True
    with webdriver.Chrome(options=options) as browser:
        browser.get(url)
        time.sleep(5)  # Adjust this based on the time needed for the page to load

        # Initialize all data structures
        text_content = ''
        image_urls = []
        video_urls = []
        youtube_urls = []
        json_ld_data = {}
        listing_details = {}
        listing_details_transformed = {}
        features = []
        rooms = []
        energy_certificate = {}
        energy_rating_info = ''
        legal_disclaimer = ''

        ########################################
        # MEDIA BLOCKS INFO (Images, YouTube Videos, Other Videos)
        ########################################
        # CLEAN METHOD
        # # Extract images, videos, YouTube videos
        # image_urls = [img.get_attribute('src') for img in browser.find_elements(By.CSS_SELECTOR, 'img.img-responsive')]
        # video_urls = [video.get_attribute('src') for video in browser.find_elements(By.TAG_NAME, 'video')]
        # youtube_urls = [iframe.get_attribute('src') for iframe in browser.find_elements(By.CSS_SELECTOR, 'iframe.embed-responsive-item')]

       # Extract images
        try:
            images = browser.find_elements(By.CSS_SELECTOR, 'img.img-responsive')
            image_urls = [img.get_attribute('src') for img in images]
        except Exception as e:
            logging.error(f"Error fetching image URLs: {e}")

        # Extract videos
        try:
            video_elements = browser.find_elements(By.TAG_NAME, 'video')
            video_urls = [video.get_attribute('src') for video in video_elements]
        except Exception as e:
            logging.error(f"Error fetching video URLs: {e}")

        # Extract YouTube videos
        try:
            youtube_iframes = browser.find_elements(By.CSS_SELECTOR, 'iframe.embed-responsive-item')
            youtube_urls = [iframe.get_attribute('src') for iframe in youtube_iframes]
        except Exception as e:
            logging.error(f"Error fetching YouTube video URLs: {e}")


        ########################################
        # TEXT BLOCKS INFO
        ########################################
        # text_content
        try:
            elements = browser.find_elements(By.CLASS_NAME, 'desc-short')
            for element in elements:
                text_content += element.get_attribute('innerHTML').strip() + '\n'
            logging.debug(f"Fetched text content: {text_content[:500]}")  # Log the first 500 characters of the text content
        except Exception as e:
            logging.error(f"Error fetching text content: {e}")
            text_content = ''  # Set to empty string if not found

        # Extract text
        try:
            elements = browser.find_elements(By.CLASS_NAME, 'desc-short')
            all_text = [element.get_attribute('innerHTML').strip() for element in elements]
            text_content = "\n".join(all_text)

            # Splitting the text content into Portuguese and English
            if "EN" in text_content:
                pt_text, en_text = text_content.split("EN", 1)
            else:
                pt_text = text_content
                en_text = "English content not found"

            logging.debug(f"Fetched text content: {pt_text[:500]}")  # Log the first 500 characters of the Portuguese text content
        except Exception as e:
            logging.error(f"Error fetching text content: {e}")
            pt_text = ''
            en_text = ''

        ########################################
        # JSON LD INFO
        ########################################
        ## CLEAN METHOD
        # # Extract JSON-LD data
        # json_ld_data = None
        # try:
        #     script_tag = browser.find_element(By.XPATH, "//script[@type='application/ld+json']")
        #     json_ld_text = script_tag.get_attribute('innerHTML').strip()
        #     json_ld_data = json.loads(json_ld_text)
        # except Exception as e:
        #     logging.error(f"Error fetching JSON-LD data: {e}")

        # Extract JSON-LD data
        json_ld_data = None
        try:
            script_tag = browser.find_element(By.XPATH, "//script[@type='application/ld+json']")
            json_ld_text = script_tag.get_attribute('innerHTML').strip()
            json_ld_data = json.loads(json_ld_text)
        except Exception as e:
            logging.error(f"Error fetching JSON-LD data: {e}")

        # Extract JSON-LD data and split description
        try:
            # ... [Your existing JSON-LD extraction code]
            if "description" in json_ld_data and "EN" in json_ld_data["description"]:
                json_ld_data["pt_description"], json_ld_data["en_description"] = json_ld_data["description"].split("EN", 1)
            else:
                json_ld_data["pt_description"] = json_ld_data.get("description", "")
                json_ld_data["en_description"] = "English description not found"
        except Exception as e:
            logging.error(f"Error fetching JSON-LD data: {e}")

        ########################################
        # LISTING DETAILS BLOCK INFO
        ########################################
        # Extract listing details
        try:
            listing_detail_items = browser.find_elements(By.CLASS_NAME, 'attributes-data-item')
            for item in listing_detail_items:
                label = item.find_element(By.CLASS_NAME, 'data-item-label').text.strip(':')
                value = item.find_element(By.CLASS_NAME, 'data-item-value').text
                listing_details[label] = value
                listing_details_transformed[label] = value
            listing_details = format_keys(listing_details)
        except Exception as e:
            logging.error(f"Error fetching listing details: {e}")

        ########################################
        # FEATURES BLOCK INFO
        ########################################
        # Extract features
        try:
            feature_items = browser.find_elements(By.CLASS_NAME, 'feature-item')
            for item in feature_items:
                feature_text = item.text
                features.append(feature_text)
        except Exception as e:
            logging.error(f"Error fetching features: {e}")

        ########################################
        # ROOMS BLOCK INFO
        ########################################
        # Extract room details
        try:
            room_elements = browser.find_elements(By.CSS_SELECTOR, ".fw-room-no-images")
            for room_element in room_elements:
                # Extracting room name
                room_name = room_element.find_element(By.CSS_SELECTOR, ".fw-room-name h5").text.strip()

                # Checking for room description
                room_description_elements = room_element.find_elements(By.CSS_SELECTOR, ".fw-room-name div")
                room_description = room_description_elements[0].text.strip() if room_description_elements else "No description"

                # Checking for room size
                room_size_elements = room_element.find_elements(By.CSS_SELECTOR, ".room-value span")
                room_size = room_size_elements[0].text.strip() if room_size_elements else "Size not available"

                # Adding the room details to the list
                rooms.append({
                    "name": room_name,
                    "description": room_description,
                    "size": room_size
                })
            # Imprimir os detalhes dos quartos
            for room in rooms:
                print(room)
        except Exception as e:
            logging.error(f"Error fetching room details: {e}")

        ########################################
        # ENERGETIC BLOCK INFO
        ########################################
        # Extract energy certificate details
        try:
            energy_container = browser.find_element(By.CLASS_NAME, 'energy-container')
            if energy_container:
                # Extracting image URL
                energy_img = energy_container.find_element(By.TAG_NAME, 'img').get_attribute('src')
                energy_certificate['image'] = energy_img

                # Extracting other details
                energy_details = energy_container.find_elements(By.CLASS_NAME, 'energy-perf-detail')
                for detail in energy_details:
                    label = detail.find_element(By.TAG_NAME, 'span').text.strip(': ')
                    value = detail.find_element(By.CLASS_NAME, 'ng-binding').text
                    energy_certificate[label] = value
        except Exception as e:
            logging.error(f"Error fetching energy certificate details: {e}")

        # Extract energy rating info
        try:
            energy_rating_info_element = browser.find_element(By.CLASS_NAME, 'energy-rating-info')
            energy_rating_info = energy_rating_info_element.text if energy_rating_info_element else ''
        except Exception as e:
            logging.error(f"Error fetching energy rating info: {e}")

        # Extract legal disclaimer
        try:
            legal_disclaimer_element = browser.find_element(By.CLASS_NAME, 'energy-rating-disclaimer')
            legal_disclaimer = legal_disclaimer_element.text if legal_disclaimer_element else ''
        except Exception as e:
            logging.error(f"Error fetching legal disclaimer: {e}")

        return {
            # "text": text_content,
            "pt_text": pt_text,
            "en_text": en_text,
            "images": image_urls,
            "videos": video_urls,
            "youtube_videos": youtube_urls,
            "json_ld": json_ld_data,
            "listing_details": listing_details,
            "listing_details_transformed": listing_details_transformed,
            "features": features,
            "rooms": rooms,
            "energy_certificate": energy_certificate,
            "energy_rating_info": energy_rating_info,
            "legal_disclaimer": legal_disclaimer
        }

@app.route('/gettext')
def get_text():
    content = get_rendered_html(url)
    if content:
        logging.debug(f"Content to be returned: {content}")  # Log the content
        return jsonify(content)
    else:
        return jsonify({"error": "Unable to fetch content"})

if __name__ == '__main__':
    app.run(debug=True)
