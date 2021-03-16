"""
Écrivez un script Python qui visite cette page et en extrait les informations suivantes :

product_page_url
universal_ product_code (upc)
title
price_including_tax
price_excluding_tax
number_available
product_description
category
review_rating
image_url

Écrivez les données dans un fichier CSV qui utilise les champs ci-dessus comme en-têtes de colonnes.
"""

from bs4 import BeautifulSoup
import requests

url = "http://books.toscrape.com/catalogue/the-secret-of-dreadwillow-carse_944/index.html"
req = requests.get(url)

if req.ok:

    soup = BeautifulSoup(req.text, features="html.parser")

    titre = '"' + soup.find("h1").string + '"'

    liste_carac_livre = soup.findAll("td")
    upc = '"' + liste_carac_livre[0].text + '"'
    price_including_tax = '"' + liste_carac_livre[3].text.replace("Â", "") + '"'
    price_excluding_tax = '"' + liste_carac_livre[2].text.replace("Â", "") + '"'
    stock = '"' + liste_carac_livre[5].text + '"'

    description = soup.find("div", id="product_description")
    if description is not None:
        description = description.nextSibling.nextSibling.string
    else:
        description = ""

    product_description = '"' + description.replace('"', '*') + '"'

    categorie = soup.find("li")
    categorie = categorie.nextSibling.nextSibling.nextSibling.nextSibling
    categorie = '"' + categorie.text.replace("\n", "") + '"'

    review_rating = '"' + liste_carac_livre[6].text + '"'

    image_source = soup.find("img").get("src")
    image_source = image_source.replace("../..", "http://books.toscrape.com")

    # Création d'un fichier csv et copie des données
    nom_fichier_csv = soup.find("h1").text
    with open(nom_fichier_csv.lower().replace(" ", "_") + ".csv", "w", encoding="utf-8") as fiche_livre:
        fiche_livre.write("product_page_url, universal_ product_code (upc), title, price_including_tax,"
                      "price_excluding_tax, number_available, product_description, category, review_rating, image_url" "\n\n")
        fiche_livre.write(url + "," + upc + "," + titre + "," + price_including_tax + "," + price_excluding_tax +
            "," + stock + "," + product_description + "," + categorie + "," + review_rating + "," + image_source + "\n")