from config import realstate_api_url
import requests

# Function to get data from your custom API
def get_api_data(url):
    response = requests.get(f"{realstate_api_url}?url={url}")
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data from API:", response.status_code)
        return None

# Function to format listing details into an HTML block
def format_listing_details(data):
    listing_details = data.get("listing_details", {})
    html_content = '<div class="real-state-listing-details">\n'

    for key, value in listing_details.items():
        formatted_key = key.replace("_", " ").capitalize()
        html_content += f"<p><strong>{formatted_key}:</strong> {value}</p>\n"

    html_content += '</div>'
    return html_content
