import os

# Load environment variables
wordpress_url = os.environ.get('WORDPRESS_URL')
username = os.environ.get('WORDPRESS_USERNAME')
password = os.environ.get('WORDPRESS_PASSWORD')
realstate_api_url = "http://127.0.0.1:8888/getdata"

# URL's to load
urls = [
  # "https://www.kwportugal.pt/Apartamento-Venda-Vialonga-1208-4617",
  "https://www.kwportugal.pt/Apartamento-Venda-Alhos-Vedros-1208-4613",
  "https://www.kwportugal.pt/Apartamento-Venda-Odivelas-1208-4493",
  # "https://www.kwportugal.pt/Apartamento-Venda-Charneca-de-Caparica-e-Sobreda-1208-4492",
  # "https://www.kwportugal.pt/Moradia-Venda-Carregado-e-Cadafais-1208-4490",
  # "https://www.kwportugal.pt/Apartamento-Venda-Povoa-de-Santa-Iria-e-Forte-da-Casa-1208-4484",
  # "https://www.kwportugal.pt/Apartamento-Venda-Sao-Domingos-de-Rana-1208-4435",
  # "https://www.kwportugal.pt/Apartamento-Venda-Venteira-1208-4434",
  # "https://www.kwportugal.pt/Apartamento-Venda-Queluz-e-Belas-1208-4433",
]
# urls = [
#   "https://www.kwportugal.pt/Apartamento-Venda-Venteira-2203-1939",
#   "https://www.kwportugal.pt/Apartamento-Venda-Venteira-1208-4434"
# ]