from odf.opendocument import OpenDocumentText
from odf.text import P
from odf.table import Table, TableRow, TableCell
from odf.style import Style, TextProperties

def create_order_summary(order_data):
    # Création du document ODT
    doc = OpenDocumentText()

    # Style pour le titre
    title_style = Style(name="TitleStyle", family="paragraph")
    title_style.addElement(TextProperties(attributes={"fontsize": "16pt", "fontweight": "bold"}))
    doc.styles.addElement(title_style)

    # Style pour les sous-titres
    subtitle_style = Style(name="SubtitleStyle", family="paragraph")
    subtitle_style.addElement(TextProperties(attributes={"fontsize": "12pt", "fontweight": "bold"}))
    doc.styles.addElement(subtitle_style)

    # Ajout du titre : Commande ID, Statut, Total
    title = P(stylename=title_style, text=f"Commande ID : {order_data['id']}, Statut : {order_data['status']}, Total : {order_data['total']} {order_data['currency']}")
    doc.text.addElement(title)

    # Ajout du sous-titre : Client
    client_name = f"{order_data['billing']['first_name']} {order_data['billing']['last_name']}"
    client_info = P(stylename=subtitle_style, text=f"Client : {client_name}")
    doc.text.addElement(client_info)

    # Création du tableau pour les produits
    table = Table()

    # En-tête du tableau
    header_row = TableRow()
    for header in ["Produit", "Quantité", "Total"]:
        cell = TableCell()
        cell.addElement(P(text=header))
        header_row.addElement(cell)
    table.addElement(header_row)

    # Ajout des lignes de produits
    # S'assurer que 'line_items' est une liste, même si une seule commande existe
    line_items = order_data.get('line_items', [])

    # Si c'est un dictionnaire (cas d'une seule commande), convertir en liste
    if isinstance(line_items, dict):
        line_items = [line_items]

    for item in line_items:
        row = TableRow()

        # Produit
        cell = TableCell()
        cell.addElement(P(text=item['name']))
        row.addElement(cell)

        # Quantité
        cell = TableCell()
        cell.addElement(P(text=str(item['quantity'])))
        row.addElement(cell)

        # Total
        cell = TableCell()
        cell.addElement(P(text=f"{item['total']} {order_data['currency']}"))
        row.addElement(cell)

        # Ajouter la ligne au tableau
        table.addElement(row)

    # Ajouter le tableau au document
    doc.text.addElement(table)

    # Sauvegarder le document
    doc.save("commande_emile_marco.odt")
    print("Fichier 'commande_emile_marco.odt' généré avec succès!")

# Exemple de données pour une commande
order_data = {
    "id": 1354,
    "status": "on-hold",
    "total": "15.80",
    "currency": "EUR",
    "billing": {
        "first_name": "Emile",
        "last_name": "MARCO"
    },
    "line_items": [
        {
            "name": "Basilic",
            "quantity": 1,
            "total": "1.00"
        },
        {
            "name": "Courgettes - 1 kg",
            "quantity": 1,
            "total": "2.76"
        },
        {
            "name": "Poireaux - 250 g",
            "quantity": 1,
            "total": "1.00"
        },
        {
            "name": "Poivrons les 0.5 kg",
            "quantity": 1,
            "total": "2.50"
        },
        {
            "name": "Tomate - 1 kg",
            "quantity": 2,
            "total": "8.00"
        }
    ]
}




if __name__ == '__main__':
    create_order_summary(order_data)