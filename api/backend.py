from selenium import webdriver
from selenium.webdriver.common.by import By  # Import the By class
from selenium.webdriver.chrome.options import Options
from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import logging
import json
import html

url = ''

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

def process_key_replacements(content):
    replacements = {
        " "      : "_",
        "u002d"  : "-",
        "\\u00e7": "c",
        "\\u00e3": "a",
        "\\u00fa": "u",
        "\\u00b2": "2",
        "\\u00e9": "e",
        "\\u00ba": "o",
        "\\u00f3": "o",
        "\\u00f5": "o",
        "\\u00ea": "u",
        "\\u00ed": "i",
        "\\u00da": "e",
        "\\n"    : "e",
        ")"      : "",
        "("      : "",
        " m\\n2" : "",
        " m\n2"  : "",
        "\\u00c1": "a",
        "&#8364;": "€",  # Unicode for Euro symbol
        "\\u00a0": "\n",
        "ç": "c",
        "ã": "a",
        "á": "a",
        "ú": "u",
        "\\u00a0": "\n",
        "\\u00a0": "\n",
        "\\u00a0": "\n",
    }

    for old, new in replacements.items():
        content = content.replace(old, new)
    return content

def process_value_replacements(content):
    replacements = {
        "u002d": "-",
        " m\\n2" : "",
        " m\n2"  : "",
        "\\u00e7": "ç",
        "\\u00e3": "á",
        "\\u00fa": "ú",
        "\\u00b2": "²",
        "\\u00e9": "e",
        "\\u00ba": "o",
        "\\u00c1": "Á",
        "&#8364;": "€",  # Unicode for Euro symbol
        "\\u00a0": "\n",
    }

    for old, new in replacements.items():
        content = content.replace(old, new)
    return content


def format_keys(listing_details):
    formatted_details = {}
    for key, value in listing_details.items():
        formatted_key = key.lower()
        formatted_key = process_key_replacements(formatted_key)
        # formatted_key = formatted_key.replace('\u00e7', 'c').replace('\u00e3', 'a').replace('\u00fa', 'u').replace('\u00e1', 'a').replace('\u00e9', 'e').replace('\u00f3', 'o').replace('\u00f5', 'o').replace('\u00ea', 'e').replace('\u00ed', 'i').replace('\u00da', 'u').replace('\u00b2.', '- ').replace('\u00a0', '\n')
        # formatted_key = formatted_key.replace(' m\n2', '').replace('\u00e9', 'e').replace('\u00b2', '2').replace('\u00ba', 'o').replace('\u00c1', 'A')
        # formatted_key = formatted_key.replace('(', '').replace(')', '').replace('\n', '')
        # formatted_key = formatted_key.replace('&#8364;', '€')
        formatted_details[formatted_key] = value
    return formatted_details

def format_json_ld_keys(json_ld_data):
    formatted_data = {}
    for key, value in json_ld_data.items():
        formatted_key = key.lower()
        formatted_key = process_key_replacements(formatted_key)
        # formatted_key = formatted_key.replace('\u00e7', 'c').replace('\u00e3', 'a').replace('\u00fa', 'u').replace('\u00e1', 'a').replace('\u00e9', 'e').replace('\u00f3', 'o').replace('\u00f5', 'o').replace('\u00ea', 'e').replace('\u00ed', 'i').replace('\u00da', 'u').replace('\u00b2.', '- ').replace('\u00a0', '\n')
        # formatted_key = formatted_key.replace(' m\n2', '').replace('\u00e9', 'e').replace('\u00b2', '2').replace('\u00ba', 'o').replace('\u00c1', 'A')
        # formatted_key = formatted_key.replace('(', '').replace(')', '').replace('\n', '')
        # formatted_key = formatted_key.replace('&#8364;', '€')

        # Apply similar transformations to the value if needed
        if isinstance(value, str):
            formatted_value = value.replace('\u00e7', 'c')
            formatted_value = process_value_replacements(formatted_value)
            # formatted_value = formatted_value.replace('\u00e7', 'c').replace('\u00e3', 'a').replace('\u00fa', 'u').replace('\u00e1', 'a').replace('\u00e9', 'e').replace('\u00f3', 'o').replace('\u00f5', 'o').replace('\u00ea', 'e').replace('\u00ed', 'i').replace('\u00da', 'u').replace('\u00b2.', '- ').replace('\u00a0', '\n')
            # formatted_value = formatted_value.replace(' m\n2', '').replace('\u00e9', 'e').replace('\u00b2', '2').replace('\u00ba', 'o').replace('\u00c1', 'A')
            # formatted_value = formatted_value.replace('(', '').replace(')', '').replace('\n', '')
            # formatted_value = formatted_value.replace('&#8364;', '€')
        else:
            formatted_value = value # if value is not a string, leave it as is

        formatted_data[formatted_key] = formatted_value

    return formatted_data

# import html

# Preprocess function
def preprocess_data(data):
    # Decode HTML entities
    return html.unescape(data)

# # Use preprocess_data before sending to WordPress
# meta_post_data = preprocess_data(your_meta_post_data)
# # Send meta_post_data to WordPress


def get_rendered_html(url):
    options = Options()
    options.headless = True
    with webdriver.Chrome(options=options) as browser:
        browser.get(url)
        time.sleep(7)  # Adjust this based on the time needed for the page to load

        # Initialize all data structures
        text_content = ''
        image_urls = []
        video_urls = []
        youtube_urls = []
        json_ld_data = {}
        listing_details = {}
        listing_details_brute = {}
        features = []
        rooms = []
        energy_certificate = {}
        energy_rating_info = ''
        legal_disclaimer = ''
        address = ''

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

        # Apply html.unescape to decode HTML entities
        # text_content = html.unescape(text_content)
        print('\n\n\n\nBEFORE text_content preprocess_data ###########################################################################################################')
        print(text_content)
        preprocess_data(text_content)
        print('\n\n\n\nAFTER text_content preprocess_data ###########################################################################################################')
        print(text_content)

        # Extract text
        try:
            elements = browser.find_elements(By.CLASS_NAME, 'desc-short')
            all_text = [element.get_attribute('innerHTML').strip() for element in elements]
            print('\n\n\n\nBEFORE all_text preprocess_data ###########################################################################################################')
            preprocess_data(all_text)
            text_content = "\n".join(all_text)
            print('\n\n\n\nAFTER all_text preprocess_data ###########################################################################################################')
            print(text_content)

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
        # Example of using the function
        # formatted_json_ld_data = format_json_ld_keys(json_ld_data)
        # Extract JSON-LD data
        json_ld_data = None
        try:
            script_tag = browser.find_element(By.XPATH, "//script[@type='application/ld+json']")
            json_ld_text = script_tag.get_attribute('innerHTML').strip()
            # json_ld_data = format_json_ld_keys(json.loads(json_ld_text))
            print('\n\n\n\nBEFORE json_ld_text preprocess_data ###########################################################################################################')
            print(json_ld_text)
            json_ld_data = preprocess_data(format_json_ld_keys(json.loads(json_ld_text)))
            print('\n\n\n\nAFTER json_ld_text preprocess_data ###########################################################################################################')
            print(json_ld_text)
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
                label = html.unescape(item.find_element(By.CLASS_NAME, 'data-item-label').text.strip(':'))
                value = html.unescape(item.find_element(By.CLASS_NAME, 'data-item-value').text)
                listing_details[label] = value
                listing_details_brute[label] = value
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
                feature_text = html.unescape(item.text)
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
                room_name = html.unescape(room_element.find_element(By.CSS_SELECTOR, ".fw-room-name h5").text.strip())

                # Checking for room description
                room_description_elements = room_element.find_elements(By.CSS_SELECTOR, ".fw-room-name div")
                room_description = html.unescape(room_description_elements[0].text.strip()) if room_description_elements else "No description"

                # Checking for room size
                room_size_elements = room_element.find_elements(By.CSS_SELECTOR, ".room-value span")
                room_size = html.unescape(room_size_elements[0].text.strip()) if room_size_elements else "Size not available"

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
                    label = html.unescape(detail.find_element(By.TAG_NAME, 'span').text.strip(': '))
                    value = html.unescape(detail.find_element(By.CLASS_NAME, 'ng-binding').text)
                    energy_certificate[label] = value
        except Exception as e:
            logging.error(f"Error fetching energy certificate details: {e}")

        # Extract energy rating info
        try:
            energy_rating_info_element = browser.find_element(By.CLASS_NAME, 'energy-rating-info')
            energy_rating_info = html.unescape(energy_rating_info_element.text) if energy_rating_info_element else ''
        except Exception as e:
            logging.error(f"Error fetching energy rating info: {e}")

        # Extract legal disclaimer
        try:
            legal_disclaimer_element = browser.find_element(By.CLASS_NAME, 'energy-rating-disclaimer')
            legal_disclaimer = html.unescape(legal_disclaimer_element.text) if legal_disclaimer_element else ''
        except Exception as e:
            logging.error(f"Error fetching legal disclaimer: {e}")

        ########################################
        # ADDRESS BLOCK INFO
        ########################################
        # Extract address
        try:
            address_element = browser.find_element(By.CSS_SELECTOR, "p.ng-binding[ng-bind-html='vm.listing.listingAddress']")
            address = html.unescape(address_element.text) if address_element else ''
        except Exception as e:
            logging.error(f"Error fetching address: {e}")

        return {
            # "text": text_content,
            "pt_text": pt_text,
            "en_text": en_text,
            "images": image_urls,
            "videos": video_urls,
            "youtube_videos": youtube_urls,
            "json_ld": json_ld_data,
            "listing_details": listing_details,
            "listing_details_brute": listing_details_brute,
            "features": features,
            "rooms": rooms,
            "energy_certificate": energy_certificate,
            "energy_rating_info": energy_rating_info,
            "legal_disclaimer": legal_disclaimer,
            "address": address
        }

@app.route('/getdata', methods=['GET'])
def get_data():
    url_param = request.args.get('url') # Get URL parameter
    if not url_param:
        return jsonify({"error": "No URL provided"}), 400

    content = get_rendered_html(url_param) # Pass the URL to the function
    if content:
        logging.debug(f"Content to be returned: {content}")
        return jsonify(content)
    else:
        return jsonify({"error": "Unable to fetch content"})

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=8888)
