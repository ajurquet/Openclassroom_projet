"""
Écrivez un script Python qui visite cette page et en extrait les informations suivantes :

product_page_url
universal_product_code (upc)
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

import requests
from bs4 import BeautifulSoup
import csv


url = "http://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html"
req = requests.get(url)

if req.ok:

    soup = BeautifulSoup(req.content, features="html.parser")

    titre = soup.title.text
    titre = soup.find("ul", class_="breadcrumb")
    titre = soup.find("li", class_="active").text

    tableau = soup.find("table", class_="table table-striped")
    tableau = tableau.find_all("td")

    upc = tableau[0].text

    prix_ht = tableau[2].text
    prix_ht = prix_ht.replace("£", "")
    prix_ht = float(prix_ht)

    prix_ttc = tableau[3].text
    prix_ttc = prix_ttc.replace("£", "")
    prix_ttc = float(prix_ttc)

    stock = tableau[5].text
    stock = stock.replace("In stock (", "").replace(" available)", "")
    stock = int(stock)

    nb_etoiles = soup.find("p", class_="star-rating")["class"]
    nb_etoiles = nb_etoiles[1]
    if nb_etoiles == "One":
        nb_etoiles = 1
    elif nb_etoiles == "Two":
        nb_etoiles = 2
    elif nb_etoiles == "Three":
        nb_etoiles = 3
    elif nb_etoiles == "Four":
        nb_etoiles = 4
    elif nb_etoiles == "Five":
        nb_etoiles = 5

    description = soup.find_all("p")
    description = description[3].text

    img_url = soup.find("img").get("src")
    img_url = img_url.replace("../..", "http://books.toscrape.com")

    categorie = soup.find("ul", class_="breadcrumb").find_all("li")
    categorie = categorie[2].text.strip()


# Création d'un fichier csv et copie des données
liste_titre = ["product_page_url", "universal_ product_code (upc)", "title", "price_including_tax",
               "price_excluding_tax", "number_available", "product_description", "category",
               "review_rating", "image_url"]
liste_donnees = [url,
                 upc,
                 titre,
                 prix_ht,
                 prix_ttc,
                 stock,
                 description,
                 categorie,
                 nb_etoiles,
                 img_url
                 ]

with open("P2_01_Scrap_page_livre.csv", "w", encoding="utf-8-sig") as csv_file:

    csv_file_writer = csv.writer(csv_file)
    csv_file_writer.writerow(liste_titre)
    csv_file_writer.writerow(liste_donnees)
