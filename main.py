import requests
from requests.auth import HTTPBasicAuth
from odf.opendocument import OpenDocumentText
from odf.text import P, H, List, ListItem

top_url = "https://www.nayral-du-zenith.fr"
# Informations de connexion à votre boutique WooCommerce
# url = "https://www.nayral-du-zenith.fr/wp-json/wc/v3/orders"  # URL debase de l'API WooCommerce
url_orders = "https://www.nayral-du-zenith.fr/wp-json/wc/v3/orders"  # URL pour récupérer les commandes
url_users = "https://www.nayral-du-zenith.fr/wp-json/wp/v2/users"
consumer_key = "ck_988fb8a57951155b55dc103d89124f7c838c835f"  # Remplacez par votre clé API
consumer_secret = "cs_192424c7e361d6ebf6c79135e2f6702f2ab240ba"  # Remplacez par votre secret API

params = {
    "status": "on-hold",  # Filtre pour les commandes complétées
    "per_page": 20  # Limite le nombre de commandes à 20 par page
}


def get_report():
    url_report = "/wp-json/wc/v3/reports"
    response = requests.get(
        f"{top_url}{url_report}",
        auth=HTTPBasicAuth(consumer_key, consumer_secret)
    )
    if response.status_code == 200:
        vendor = response.json()
        pass
    else:
        return f"Vendeur ID  non trouvé"


# Fonction pour récupérer les détails d'un vendeur à partir de son ID
def get_vendor_name(vendor_id):
    try:
        # Requête à l'API WordPress pour récupérer les détails del'utilisateur (vendeur)
        response = requests.get(
            f"{url_users}/{vendor_id}",
            auth=HTTPBasicAuth(consumer_key, consumer_secret)
        )

        # Vérifie si la requête est réussie
        if response.status_code == 200:
            vendor = response.json()
            return vendor.get('name', f"Vendeur ID {vendor_id}")  # Retourne le nom du vendeur
        else:
            return f"Vendeur ID {vendor_id} non trouvé"
    except Exception as e:
        return f"Erreur lors de la récupération du vendeur : {e}"


# Fonction pour récupérer les commandes depuis WooCommerce
def get_woocommerce_orders():
    doc = OpenDocumentText()
    try:
        # Requête à l'API WooCommerce pour obtenir les commandes
        response = requests.get(
            url_orders,
            auth=HTTPBasicAuth(consumer_key, consumer_secret)
        )

        # Vérifie si la requête est réussie
        if response.status_code == 200:
            orders = response.json()
            doc.text.addElement(H(outlinelevel=1, text=f"Nombre de commandes récupérées : {len(orders)}"))

            # Parcourt chaque commande récupérée
            for order in orders:
                doc.text.addElement(H(outlinelevel=2, text=f"---\nCommande ID : {order['id']}, Statut :{order['status']}, Total : {order['total']} {order['currency']}"))

                # Récupère et affiche le nom du client
                if 'billing' in order and 'first_name' in order['billing'] and 'last_name' in order['billing']:
                    customer_name = f"{order['billing']['first_name']}{order['billing']['last_name']}"
                    doc.text.addElement(P(text=f"Client : {customer_name}"))
                else:
                    print("Client : Inconnu")

                # Récupère et affiche les articles de la commande
                commande_list = List()
                if 'line_items' in order:
                    doc.text.addElement(P(text="Articles dans la commande :"))
                    for item in order['line_items']:
                        item_odt = ListItem()
                        doc.text.addElement(
                            P(text=f"- Produit : {item['name']}, Quantité :{item['quantity']}, Total : {item['total']} {order['currency']}"))
                        commande_list.addElement(item_odt)
                    doc.text.addElement(commande_list)
                # Récupère les vendeurs (si applicable) depuis les métadonnées de la commande
                # if 'meta_data' in order:
                #     vendors = [meta['value'] for meta in order['meta_data'] if 'vendor' in meta['key'].lower()]
                #     if vendors:
                #         doc.text.addElement(P(text="Vendeurs associés à cette commande :"))
                #         for vendor_id in vendors:
                #             vendor_name = get_vendor_name(vendor_id)  # Récupère le nom du vendeur à partir de son ID
                #             doc.text.addElement(P(text=f"- {vendor_name}"))
                #     else:
                #         print("Aucun vendeur associé à cette commande.")
                doc.text.addElement(P(text=f""))
                doc.text.addElement(P(text=f"---"))
                doc.text.addElement(P(text=f""))
        else:
            print(f"Erreur : Impossible de récupérer les commandes.Statut HTTP : {response.status_code}")
        doc.save('mon_fichier.odt')
    except Exception as e:
        print(f"Une erreur est survenue : {e}")


# Appel de la fonction pour afficher les commandes
# get_woocommerce_orders()
def get_total_order():
    #url = 'https://www.nayral-du-zenith.fr/wp-json/wc/v3/orders'
    url = 'https://www.nayral-du-zenith.fr/wp-json/wc/v3/orders/1203'
    response = requests.get(
        f"{url}",
        auth=HTTPBasicAuth(consumer_key, consumer_secret)
    )

    # Vérifie si la requête est réussie
    if response.status_code == 200:
        vendor = response.json()
        pass
        for item in vendor:
            billing = item['billing']
            print(billing['first_name'], billing['last_name'])
        pass


def create_doc():
    doc = OpenDocumentText()

    # Ajouter un paragraphe
    p = P(text="Voici un paragraphe dans un fichier ODT.")
    doc.text.addElement(p)

    # Sauvegarder le fichier
    doc.save('mon_fichier.odt')


if __name__ == '__main__':
     get_total_order()
    # get_report()
    #get_woocommerce_orders()
