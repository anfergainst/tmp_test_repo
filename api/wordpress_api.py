import requests
from requests.auth import HTTPBasicAuth
import json
from config import wordpress_url, username, password

# Function to create a post
def create_post(title, content, status="publish"):
    api_url = f"https://{wordpress_url}/wp-json/wp/v2/posts"
    auth = HTTPBasicAuth(username, password)
    headers = {'Content-Type': 'application/json'}

    data = {
        "title": title,
        "content": content,
        "status": status
    }

    response = requests.post(api_url, headers=headers, json=data, auth=auth)

    # Logging the response
    print("Status Code:", response.status_code)
    print("Response Body:", json.dumps(response.json(), indent=4))

    return response.json()

# Example usage

print(wordpress_url)
print(username)
print(password)

title = "Post Title"
content_template = "Hello, this is a post about {}."
content = content_template.format("Python and WordPress")

post = create_post(title, content)
