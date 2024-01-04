import requests
from requests.auth import HTTPBasicAuth
import json
from config import wordpress_url, username, password

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

def create_post(title, content, tag_names=None, status="publish"):
    api_url = f"https://{wordpress_url}/wp-json/wp/v2/posts"
    auth = HTTPBasicAuth(username, password)
    headers = {'Content-Type': 'application/json'}
    tag_ids = [get_tag_id(tag) for tag in tag_names] if tag_names else []

    data = {
        "title": title,
        "content": content,
        "status": status,
        "tags": tag_ids  # Attach tag IDs
    }

    response = requests.post(api_url, headers=headers, json=data, auth=auth)

    # Logging the response
    print("Status Code:", response.status_code)
    print("Response Body:", json.dumps(response.json(), indent=4))

    return response.json()
