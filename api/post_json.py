import requests
from requests.auth import HTTPBasicAuth
import os

# Load environment variables
wordpress_url = os.environ.get('WORDPRESS_URL')
username = os.environ.get('WORDPRESS_USERNAME')
password = os.environ.get('WORDPRESS_PASSWORD')

# response = requests.get(
#     # 'https://nagisa.com.br/wp-json/wp/v2/posts/1046',
#     'https://nagisa.com.br/wp-json/wp/v2/posts/1121',
#     auth=HTTPBasicAuth(username, password)
# )
# post_data = response.json()
# print(post_data)

def read_meta_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()  # Read the file content and strip any leading/trailing whitespace
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

# Example usage
meta_file_path = 'post.data'
post_data = read_meta_from_file(meta_file_path)

# # Prepare your post data in JSON format
# post_data = {
#     "title": "Your Post Title",
#     "content": "Your post content here...",
#     "status": "publish",  # Use 'draft' to save as a draft
#     # Add other fields as needed
# }

# WordPress REST API endpoint for creating a post
api_url = f"{wordpress_url}/wp-json/wp/v2/posts"

# Make the HTTP POST request
response = requests.post(api_url, auth=HTTPBasicAuth(username, password), json=post_data)

# Check the response
if response.status_code == 201:
    print("Post created successfully.")
    print("Post ID:", response.json()["id"])
else:
    print("Failed to create post.")
    print("Status Code:", response.status_code)
    print("Response:", response.text)
