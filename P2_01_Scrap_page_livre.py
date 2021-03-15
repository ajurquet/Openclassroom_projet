from bs4 import BeautifulSoup
import requests


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

url = "http://books.toscrape.com/catalogue/alice-in-wonderland-alices-adventures-in-wonderland-1_5/index.html"
req = requests.get(url)
soup = BeautifulSoup(req.text, features="html.parser")

titre = soup.find("h1")

liste_carac_livre = soup.findAll("td")

description = soup.find("div", id="product_description")
if description is not None:
    description = description.nextSibling.nextSibling.string # J'ai recherché le tag "div" avec l'id "product_description" et je me suis déplacé 2 fois pour trouver la description
else:
    description = ""


categorie = soup.find("li")
categorie = categorie.nextSibling.nextSibling.nextSibling.nextSibling

image_source = soup.find("img").get("src")


with open(titre.text.replace(":", " ") + ".csv", "w", encoding="utf-8") as livre_csv:
    livre_csv.write("product_page_url, universal_ product_code (upc), title, price_including_tax,"
                    "price_excluding_tax, number_available, product_description, category, review_rating, image_url" "\n\n")
    livre_csv.write(url + "," + liste_carac_livre[0].text + "," + titre.string + "," +
                    liste_carac_livre[3].text.replace("Â", "") + "," + liste_carac_livre[2].text.replace("Â", "") +
                    "," + liste_carac_livre[5].text + "," + '"' + description.replace('"', '^') + '"' + "," + categorie.text.replace("\n","") +
                    "," + liste_carac_livre[6].text + "," + image_source.replace("../..", "http://books.toscrape.com"))
