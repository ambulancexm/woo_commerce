import requests
from requests.auth import HTTPBasicAuth
from woocommerce import API
import pandas as pd

#import pandas as pd

# Informations de connexion à votre boutique WooCommerce
# url = "https://www.nayral-du-zenith.fr/wp-json/wc/v3/orders"  # URL de base de l'API WooCommerce
wcapi = API(
    url="https://www.nayral-du-zenith.fr",  # Remplace par l'URL de ton site
    consumer_key="ck_988fb8a57951155b55dc103d89124f7c838c835f",  # Remplace par ta Consumer Key
    consumer_secret="cs_192424c7e361d6ebf6c79135e2f6702f2ab240ba",  # Remplace par ta Consumer Secret
    version="wc/v3"  # La version de l'API WooCommerce
)

data = {'search': 'chou'}

# products = wcapi.get("products", ).json()
#
# for product in products:
#     print(product['store'])
#     print()

sellers = wcapi.get("customers", params={'role': 'seller', 'filter[limit]': -1}, ).json()


for seller in sellers:
    if seller['id'] != 10:
        print(seller, '\n')


         # """
         # liste producteurs par id
         # liste des commandes par client par la liste des producteurs
         # """

# # Récupérer tous les utilisateurs (vendeurs)
#
# response = wcapi.get("customers")
# vendors = response.json()
#
# # Vérifier si la requête a réussi
# if response.status_code == 200:
#     print("Vendeurs récupérés avec succès.")
# else:
#     print("Erreur lors de la récupération des vendeurs:", response.status_code, response.text)
#
# # Affichage des vendeurs dans un tableau
# print(f"{'ID':<10} {'Nom':<30} {'Email':<30}")
# print("="*70)
# for vendor in vendors:
#     # Filtrer pour n'afficher que les vendeurs
#     if 'seller' in vendor.get('role', []):  # Assure-toi que 'vendor' est le bon rôle pour tes utilisateurs
#         print(f"{vendor['id']:<10} {vendor['username']:<30} {vendor['email']:<30}")