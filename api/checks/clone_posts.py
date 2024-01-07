import requests
import json
from requests.auth import HTTPBasicAuth
import os

# Load environment variables
wordpress_url = os.environ.get('WORDPRESS_URL')
username = os.environ.get('WORDPRESS_USERNAME')
password = os.environ.get('WORDPRESS_PASSWORD')

def clone_wordpress_post(source_post_id, target_post_id, wordpress_url, username, password):
    # Fetch the original post data
    get_url = f"{wordpress_url}/wp-json/wp/v2/posts/{source_post_id}"
    auth = (username, password)
    # response = requests.get(get_url, auth=auth) # DISABLED TO ENABLE RAW CONTENT
    response = requests.get(f"{wordpress_url}/wp-json/wp/v2/posts/{source_post_id}?context=edit", auth=auth)
    if response.status_code != 200:
        return f"Failed to get original post. Status Code: {response.status_code}"

    original_post = response.json()

    # Prepare the new post data
    new_post_data = {
        'title': original_post['title']['rendered'],
        # 'content': original_post['content']['rendered'],
        # 'content': original_post['content']['raw'],
        'guid': original_post['guid']['rendered'],
        # 'content': original_post['content']['protected'],
        'excerpt': original_post['excerpt']['rendered'],
        # # 'excerpt': original_post['excerpt']['protected'],
        'author': original_post['author'],
        # 'modified': original_post['modified'],
        # 'modified_gmt': original_post['modified_gmt'],
        'comment_status': original_post['comment_status'],
        'featured_media': original_post['featured_media'],
        'sticky': original_post['sticky'],
        'uagb_featured_image_src': original_post['uagb_featured_image_src'],
        'uagb_author_info': original_post['uagb_author_info'],
        'uagb_comment_info': original_post['uagb_comment_info'],
        'uagb_excerpt': original_post['uagb_excerpt'],
        'type': original_post['type'],
        # 'ping_status': original_post['ping_status'],
        'template': original_post['template'],
        'format': original_post['format'],
        'meta': original_post['meta'],
        # 'tags': original_post['tags'],
        # '_links': original_post['_links'],
        # For spectra_custom_meta, assuming it's a dictionary and we're copying its sub-keys
        'spectra_custom_meta': original_post['spectra_custom_meta'],
        # 'spectra_custom_meta': {
        #     'ast-site-content-layout': original_post.get('spectra_custom_meta', {}).get('ast-site-content-layout', ''),
        #     'site-content-style': original_post.get('spectra_custom_meta', {}).get('site-content-style', ''),
        #     'ast-banner-title-visibility': original_post.get('spectra_custom_meta', {}).get('ast-banner-title-visibility', ''),
        #     'theme-transparent-header-meta': original_post.get('spectra_custom_meta', {}).get('theme-transparent-header-meta', ''),
        #     'adv-header-id-meta': original_post.get('spectra_custom_meta', {}).get('adv-header-id-meta', ''),
        #     'stick-header-meta': original_post.get('spectra_custom_meta', {}).get('stick-header-meta', ''),
        #     'astra-migrate-meta-layouts': original_post.get('spectra_custom_meta', {}).get('astra-migrate-meta-layouts', ''),
        #     'footnotes': original_post.get('spectra_custom_meta', {}).get('footnotes', ''),
        #     'site-post-title': original_post.get('spectra_custom_meta', {}).get('site-post-title', ''),
        #     'site-sidebar-style': original_post.get('spectra_custom_meta', {}).get('site-sidebar-style', ''),
        #     'footer-sml-layout': original_post.get('spectra_custom_meta', {}).get('footer-sml-layout', ''),
        #     '_uag_page_assets': original_post.get('spectra_custom_meta', {}).get('_uag_page_assets', ''),
        # },
        'status': 'publish'  # or 'draft' # You might want to change this as per your need
    }

    # Convert dictionary to a JSON formatted string and print it
    # print(json.dumps(original_post, indent=4))
    print(json.dumps(new_post_data, indent=4))

    # Create a new post
    create_url = f"{wordpress_url}/wp-json/wp/v2/posts/{target_post_id}"
    create_response = requests.post(create_url, json=new_post_data, auth=auth)

    if create_response.status_code != 201:
        return f"Failed to create new post. Status Code: {create_response.status_code}"

    return f"New post created successfully. Post ID: {create_response.json()['id']}"

# Example usage
source_post_id = 1046  # Replace with the ID of the post you want to clone
target_post_id = 1179  # Replace with the ID of the new post

result = clone_wordpress_post(source_post_id, target_post_id, wordpress_url, username, password)
print(result)

