from wordpress_api2 import get_category_id, fetch_template_post, create_wordpress_post
from wordpress_realstate_api import get_api_data, format_listing_details
from config import urls, wordpress_url

# Define the ID of your template post
template_post_id = 1046
api_address = 'http://home.devops.click:8888/getdata'

# Fetch the template post content
template_content = fetch_template_post(template_post_id)

def create_tags(api_data):
    # import pdb; pdb.set_trace() # DEBUG
    tags = []

    # Add 'json_ld.productID' as a tag
    json_ld = api_data.get("json_ld", {})
    product_id = json_ld.get("productID")
    if product_id:
        tags.append(product_id)

    # Add specific 'listing_details' items as tags
    listing_details = api_data.get("listing_details", {})

    quartos = listing_details.get("quartos")
    if quartos:
        tags.append(quartos)

    for key in ["ano_de_construcao", "casas_de_banho", "cozinhas", "piso", "salas_de_refeicao"]:
        value = listing_details.get(key)
        if value:
            tags.append(f"{key.replace('_', ' ')} {value}")

    return tags

# Iterate over each URL in the 'urls' list
for url in urls:
    # import pdb; pdb.set_trace() # DEBUG
    # Fetch data for the current URL
    api_data = get_api_data(url)
    print(url)
    if api_data:
        # Extract address and create a location block - TEMPLATES - PREPARE DYNAMIC CONTENT
        address = api_data.get("address", "Default Address")
        rooms = api_data.get("listing_details", {}).get("quartos", "Default Rooms")

        location_block = f"<h2>Location</h2><p>{address}</p>"

        # Create a category for the address
        address_category_id = get_category_id(address)

        # # Create a category for the address
        # category_id = get_category_id(address)

        # Extract number of rooms and create a category for it
        quartos = api_data.get("listing_details", {}).get("quartos")
        if quartos:
            rooms_category_id = get_category_id(quartos)

        # Format the data into an HTML block
        listing_html = format_listing_details(api_data)
        full_content = location_block + listing_html  # Combine location and listing details

        # Set the title from json_ld data
        title = api_data.get("json_ld", {}).get("name", "Default Title")

        ### TEMPLATES - Replace placeholders in the template
        post_content = template_content
        # post_content = template_content.replace("{{address}}", address)
        # post_content = post_content.replace("{{rooms}}", rooms)

        # Create tags
        tags = create_tags(api_data)

        # Create and publish the WordPress post
        category_ids = [cid for cid in [address_category_id, rooms_category_id] if cid]

        # DEBUGGING - After performing the substitutions
        # print("Final HTML Content:")
        # print(post_content)

        # create_post(title, post_content, tag_names=tags, category_ids=category_ids)

        api_data = {
            'title': title,
            'rooms': rooms,
            'address': address,
            'category_ids': category_ids,
            'tags': tags,
        }

        # Dados do post
        post_data = {
            'template_post_id': template_post_id,
            'api_data': api_data,
            'api_address': api_address
        }

        result = create_wordpress_post(post_data, wordpress_url)
        print(result)
