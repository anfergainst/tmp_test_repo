from wordpress_api import create_post
from wordpress_realstate_api import get_api_data, format_listing_details

# Fetch data from custom API
api_data = get_api_data()
if api_data:
    # Format the data into an HTML block
    listing_html = format_listing_details(api_data)

    # Create and publish the WordPress post
    title = "Real State - Listing Details"
    create_post(title, listing_html)
