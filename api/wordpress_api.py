import requests
from requests.auth import HTTPBasicAuth
import json
from config import wordpress_url, username, password

auth = HTTPBasicAuth(username, password)

######################################
# fetch template to create new posts
######################################
def fetch_template_post(template_post_id):
    api_url = f"https://{wordpress_url}/wp-json/wp/v2/posts/{template_post_id}"
    response = requests.get(api_url, auth=HTTPBasicAuth(username, password))
    if response.status_code == 200:
        return response.json()['content']['rendered']
    else:
        return None

def get_tag_id(tag_name):
    # Check if the tag exists and get its ID
    headers = {'Content-Type': 'application/json'}
    auth = HTTPBasicAuth(username, password)
    tag_check_url = f"https://{wordpress_url}/wp-json/wp/v2/tags?search={tag_name}"
    tag_check_response = requests.get(tag_check_url, auth=HTTPBasicAuth(username, password))
    if tag_check_response.status_code == 200 and tag_check_response.json():
        # Tag exists, return its ID
        return tag_check_response.json()[0]['id']
    else:
        # Tag doesn't exist, create it
        tag_create_url = f"https://{wordpress_url}/wp-json/wp/v2/tags"
        tag_data = {"name": tag_name}
        tag_create_response = requests.post(tag_create_url, json=tag_data, headers=headers, auth=auth)
        if tag_create_response.status_code == 201:
            # Return the new tag's ID
            return tag_create_response.json()['id']
    return None

def get_category_id(category_name):
    headers = {'Content-Type': 'application/json'}
    # Check if the category exists and get its ID
    category_check_url = f"https://{wordpress_url}/wp-json/wp/v2/categories?search={category_name}"
    category_check_response = requests.get(category_check_url, auth=HTTPBasicAuth(username, password))
    if category_check_response.status_code == 200 and category_check_response.json():
        # Category exists, return its ID
        return category_check_response.json()[0]['id']
    else:
        # Category doesn't exist, create it
        category_create_url = f"https://{wordpress_url}/wp-json/wp/v2/categories"
        category_data = {"name": category_name}
        category_create_response = requests.post(category_create_url, json=category_data, headers=headers, auth=HTTPBasicAuth(username, password))
        if category_create_response.status_code == 201:
            # Return the new category's ID
            return category_create_response.json()['id']
    return None

def create_post(title, content, tag_names=None, category_ids=None, status="publish"):
    api_url = f"https://{wordpress_url}/wp-json/wp/v2/posts"
    headers = {'Content-Type': 'application/json'}
    tag_ids = [get_tag_id(tag) for tag in tag_names] if tag_names else []

    data = {
        "title": title,
        "content": content,
        "status": status,
        "tags": tag_ids  # Attach tag IDs
    }

    # Add category IDs if provided
    if category_ids:
        data["categories"] = category_ids

    response = requests.post(api_url, headers=headers, json=data, auth=HTTPBasicAuth(username, password))

    # Logging the response
    print("Status Code:", response.status_code)
    print("Response Body:", json.dumps(response.json(), indent=4))

    return response.json()
