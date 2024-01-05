import os

# Load environment variables
wordpress_url = os.environ.get('WORDPRESS_URL')
username = os.environ.get('WORDPRESS_USERNAME')
password = os.environ.get('WORDPRESS_PASSWORD')
realstate_api_url = "http://127.0.0.1:8888/getdata"

# URL's to load
urls = [
  "https://www.kwportugal.pt/Apartamento-Venda-Venteira-2203-1939"
]
# urls = [
#   "https://www.kwportugal.pt/Apartamento-Venda-Venteira-2203-1939",
#   "https://www.kwportugal.pt/Apartamento-Venda-Venteira-1208-4434"
# ]