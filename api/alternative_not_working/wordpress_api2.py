import requests
from requests.auth import HTTPBasicAuth
import json
from config import wordpress_url, username, password

auth = HTTPBasicAuth(username, password)
headers = {'Content-Type': 'application/json'}

######################################
# fetch template to create new posts
######################################
def fetch_template_post(template_post_id):
    # import pdb; pdb.set_trace() # DEBUG
    api_url = f"{wordpress_url}/wp-json/wp/v2/posts/{template_post_id}"
    print(api_url)
    api_url_response = requests.get(api_url, headers=headers, auth=auth)
    print(api_url_response)
    if api_url_response.status_code == 200:
        return api_url_response.json()['content']['rendered']
    else:
        return None

def get_tag_id(tag_name):
    # import pdb; pdb.set_trace() # DEBUG
    # Check if the tag exists and get its ID
    tag_check_url = f"{wordpress_url}/wp-json/wp/v2/tags?search={tag_name}"
    print(tag_check_url)
    tag_check_response = requests.get(tag_check_url, headers=headers, auth=auth)
    print(tag_check_response)
    if tag_check_response.status_code == 200 and tag_check_response.json():
        # Tag exists, return its ID
        return tag_check_response.json()[0]['id']
    else:
        # Tag doesn't exist, create it
        tag_create_url = f"{wordpress_url}/wp-json/wp/v2/tags"
        tag_data = {"name": tag_name}
        tag_create_response = requests.post(tag_create_url, json=tag_data, headers=headers, auth=auth)
        print(tag_create_response)
        if tag_create_response.status_code == 201:
            # Return the new tag's ID
            return tag_create_response.json()['id']
    return None

def get_category_id(category_name):
    # import pdb; pdb.set_trace() # DEBUG
    # Check if the category exists and get its ID
    category_check_url = f"{wordpress_url}/wp-json/wp/v2/categories?search={category_name}"
    print(category_check_url)
    category_check_response = requests.get(category_check_url, headers=headers, auth=auth)
    print(category_check_response)
    if category_check_response.status_code == 200 and category_check_response.json():
        # Category exists, return its ID
        return category_check_response.json()[0]['id']
    else:
        # Category doesn't exist, create it
        category_create_url = f"{wordpress_url}/wp-json/wp/v2/categories"
        print(category_create_url)
        category_data = {"name": category_name}
        category_create_response = requests.post(category_create_url, json=category_data, headers=headers, auth=auth)
        print(category_create_response)
        if category_create_response.status_code == 201:
            # Return the new category's ID
            return category_create_response.json()['id']
    return None

    # response = requests.get(category_check_url, headers=headers, auth=auth)
    #     print("API Response:", response.text)

    #     if response.status_code == 200:
    #         categories = response.json()

    #         # If categories is not empty and we expect only one category with this name
    #         if categories:
    #             return categories[0]['id']

    #     return None

    # category_check_response = requests.get(category_check_url, headers=headers, auth=auth)
    # print("Resposta da API:", category_check_response.text)
    # if category_check_response.status_code == 200:
    #     try:
    #         # Tenta decodificar o JSON
    #         return category_check_response.json()['id']
    #     except json.JSONDecodeError:
    #         print("Falha ao decodificar JSON")
    #         return None

def create_post(title, content, tag_names=None, category_ids=None, custom_meta=None, status="publish"):
    # import pdb; pdb.set_trace() # DEBUG
    api_url = f"{wordpress_url}/wp-json/wp/v2/posts"
    tag_ids = [get_tag_id(tag) for tag in tag_names] if tag_names else []

    data = {
        "title": title,
        "content": content,
        "status": status,
        "tags": tag_ids  # Attach tag IDs
    }

    # Include custom meta data
    if custom_meta:
        data["meta"] = custom_meta

    # Add category IDs if provided
    if category_ids:
        data["categories"] = category_ids

    response = requests.post(api_url, json=data, headers=headers, auth=auth)

    # Logging the response
    print("Status Code:", response.status_code)
    print("Response Body:", json.dumps(response.json(), indent=4))

    return response.json()

def create_wordpress_post(post_data, wordpress_url):
    # import pdb; pdb.set_trace() # DEBUG
    site_url = f"{wordpress_url}/wp-json/meuapp/v1/create-post/"
    print(site_url)

    response = requests.post(site_url, json=post_data, headers=headers, auth=auth)
    print(response)

    if response.status_code != 200:
        return f"Erro: {response.text}"

    return response.json()