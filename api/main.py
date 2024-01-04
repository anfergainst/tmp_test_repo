from wordpress_api import create_post
from wordpress_realstate_api import get_api_data, format_listing_details
from config import urls

def create_tags(api_data):
    tags = []

    # Add each feature as a tag
    for feature in api_data.get("features", []):
        tags.append(feature)

    # Add specific json_ld properties as tags
    json_ld = api_data.get("json_ld", {})
    for key in ["productID", "productionDate"]:
        if key in json_ld:
            tags.append(json_ld[key])

    # Add each listing_details_transformed item as a tag
    for key, value in api_data.get("listing_details_transformed", {}).items():
        tags.append(f"{key} {value}")

    # Add specific listing_details item (e.g., "quartos") as a tag
    quartos = api_data.get("listing_details", {}).get("quartos")
    if quartos:
        tags.append(quartos)

    return tags

# Iterate over each URL in the 'urls' list
for url in urls:
    # Fetch data for the current URL
    api_data = get_api_data(url)
    if api_data:
        # Format the data into an HTML block
        listing_html = format_listing_details(api_data)

        # Set the title from json_ld data
        title = api_data.get("json_ld", {}).get("name", "Default Title")

        # Create tags
        tags = create_tags(api_data)

        # Create and publish the WordPress post
        create_post(title, listing_html, tag_names=tags)
