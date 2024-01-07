import requests
from requests.auth import HTTPBasicAuth
import os
import json

# Load environment variables
wordpress_url = os.environ.get('WORDPRESS_URL')
username = os.environ.get('WORDPRESS_USERNAME')
password = os.environ.get('WORDPRESS_PASSWORD')

response = requests.get(
    # 'https://nagisa.com.br/wp-json/wp/v2/posts/1046',
    # 'https://nagisa.com.br/wp-json/wp/v2/posts/1121',
    # 'https://nagisa.com.br/wp-json/wp/v2/posts/1204',
    'https://nagisa.com.br/wp-json/wp/v2/posts/1193',
    auth=HTTPBasicAuth(username, password)
)
post_data = response.json()
# print(post_data) -> SHOW JSON SINGLE LINE

# Pretty print the JSON data
formatted_json = json.dumps(post_data, indent=4)
print(formatted_json) # -> SHOW WELL FORMATED JSON