import os
from datetime import datetime, timedelta

from woocommerce import API
import pandas as pd
from login import login
from output import create_excel_file, create_producer_price_table

# Informations de connexion à votre boutique WooCommerce

#creer les fichier avec les credentials

wcapi = API(
    url=login['url'],
    consumer_key=login['consumer_key'],
    consumer_secret=login['consumer_secret'],
    version=login['version']
)
df_achat = pd.DataFrame(columns=['order_id', 'produit', 'quantite', 'producteur', 'prix'])

data = {'search': 'chou'}


def get_list_de_vendeurs():
    """
    on recupère la liste des vendeurs
    avec le role seller
    sans l'id 10 de jean nicolas
    on retourne un liste de producteurs
    [
    {id, first_name, username}
        ]
    """
    sellers = wcapi.get("customers", params={'role': 'seller', 'filter[limit]': -1}, ).json()
    df = pd.DataFrame(sellers)
    seller_df = df[['id', 'first_name', 'username']]
    seller_list = seller_df.to_dict(orient='records')
    return seller_list


def obtenir_dernier_dimanche():
    # Obtenir la date actuelle
    aujourd_hui = datetime.now()

    # Calculer la différence de jours pour atteindre le dernier dimanche
    dernier_dimanche = aujourd_hui - timedelta(days=aujourd_hui.weekday() + 1)

    # Si aujourd'hui est déjà un dimanche, revenir à la semaine précédente
    if aujourd_hui.weekday() == 6:
        dernier_dimanche = aujourd_hui - timedelta(days=7)

    return dernier_dimanche.strftime('%Y-%m-%dT00:00:00')


# Utilisation de la fonction
print("Dernier dimanche :", obtenir_dernier_dimanche())

def retrieve_main_order():
    """
    on recupère les commandes non validées (on-hold)
    et on return une liste d'id de mini commande
    """

    response = wcapi.get("orders",
                         params={'status': 'on-hold', 'parent': 0, 'after': obtenir_dernier_dimanche(), 'per_page': 100})
    orders_df = pd.DataFrame(response.json())
    id_list = orders_df['id'].tolist()
    return id_list


#on recupère la liste des vendeurs
# vendeur_list = get_list_de_vendeurs()
# id_list = retrieve_main_order()
# # [1629, 1625, 1621, 1615, 1612, 1605, 1599, 1593, 1577, 1532]


def trouver_vendeur_par_id(vendeurs, id_recherche):
    for vendeur in vendeurs:
        if vendeur['id'] == id_recherche:
            return vendeur['first_name']
    return None  # Si l'id n'est pas trouvé, retourner None


def get_order_by_customer_by_vendor(parent):

    response = wcapi.get("orders", params={'parent': parent, 'per_page': 100})
    orders_df = pd.DataFrame(response.json())
    # Filtrer le DataFrame pour ne garder que les lignes où parent_id est égal à 0

    # Sélectionner les colonnes spécifiques
    result_df = orders_df[['id', 'billing', 'meta_data','line_items', 'total']]

    line_items_list = []
    billing = {}
    for index, row in result_df.iterrows():
        billing = row['billing']
        for item in row['line_items']:
            ligne = {
                'order_id': row['id'],
                'produit': item['name'],
                'quantite': item['quantity'],
                'prix': (float(item['subtotal']) + float(item['subtotal_tax'])),
                'producteur' :  trouver_vendeur_par_id(vendeur_list, int(row['meta_data'][0]['value']))
            }
            line_items_list.append(ligne)
    line_items_list.sort(key=lambda x: x['producteur'])
    return line_items_list, billing

if __name__ == '__main__':
    user_home = os.path.expanduser("~")
    df_achat = pd.DataFrame(columns=['order_id', 'produit', 'quantite', 'producteur', 'prix'])
    vendeur_list = get_list_de_vendeurs()
    id_list = retrieve_main_order()
    # [1629, 1625, 1621, 1615, 1612, 1605, 1599, 1593, 1577, 1532]
    command_list =[]
    for parent in retrieve_main_order():
        command = get_order_by_customer_by_vendor(parent)
        product = command[0]
        client = command[1]
        df_temp = pd.DataFrame(product)
        data_tab = {'command' :
                        {
                            'numero': parent,
                            'client': f'{client["first_name"]} {client["last_name"]}',
                            'produits': product
                         }
        }
        command_list.append(data_tab)
        df_achat = pd.concat([df_achat, df_temp], ignore_index=True)
    main_path = fr'{user_home}/nayral_du_zenith'
    now_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    create_excel_file(command_list, fr'{main_path}/client_{now_date}.xlsx')
    create_producer_price_table(df_achat, fr'{main_path}/producteur_{now_date}.xlsx')

