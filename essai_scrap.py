from bs4 import BeautifulSoup
import requests
import os
import csv

liste_urls_livres = []

"""
Maintenant que vous avez obtenu les informations concernant un premier livre, vous pouvez essayer de récupérer 
toutes les données nécessaires pour toute une catégorie d'ouvrages. Choisissez n'importe quelle catégorie sur 
le site de Books to Scrape. Écrivez un script Python qui consulte la page de la catégorie choisie, et extrait 
l'URL de la page Produit de chaque livre appartenant à cette catégorie. Combinez cela avec le travail que vous 
avez déjà effectué afin d'extraire les données produit de tous les livres de la catégorie choisie, puis écrivez 
les données dans un seul fichier CSV.

Remarque : certaines pages de catégorie comptent plus de 20 livres, qui sont donc répartis sur différentes 
pages («  pagination  »). Votre application doit être capable de parcourir automatiquement les multiples pages si présentes. 
"""

def copie_urls_liste(url_a_parcourir):
    """
    Parcours l'url donnée en paramètre, et copie les liens vers chaque page dans une liste

    """
    req = requests.get(url_a_parcourir)
    soup = BeautifulSoup(req.text, features="html.parser")

    url_boucle = soup.findAll("h3")
    for i in url_boucle:
        lien = i.find("a")
        lien = lien["href"]
        lien = lien.replace("../../..", "http://books.toscrape.com/catalogue")
        liste_urls_livres.append((lien))

    if soup.find("li", {"class": "next"}): # si il y a un bouton "next sur la page
        bouton_next = soup.find("li", {"class": "next"})
        url_next_page = bouton_next.find("a")
        url_next_page = url_next_page["href"]
        url_next_page = url_a_parcourir.replace("index.html", url_next_page)
        copie_urls_liste(url_next_page)


def scrap_page_livre(url_page_livre):
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
    #url de la page du livre à scrapper
    #url_livre = "http://books.toscrape.com/catalogue/i-know-what-im-doing-and-other-lies-i-tell-myself-dispatches-from-a-life-under-construction_704/index.html"
    req = requests.get(url_page_livre)

    if req.ok:
        soup = BeautifulSoup(req.text, features="html.parser")

        titre = soup.find("h1")

        liste_carac_livre = soup.findAll("td")

        description = soup.find("div", id="product_description")
        description = description.nextSibling.nextSibling.string # J'ai recherché le tag "div" avec l'id "product_description" et je me suis déplacé 2 fois pour trouver la description

        categorie = soup.find("li")
        categorie = categorie.nextSibling.nextSibling.nextSibling.nextSibling

        image_source = soup.find("img").get("src")

        with open(titre.text.replace(":", " ") + ".csv", "w", encoding="utf-8") as livre_csv:
            livre_csv.write("product_page_url, universal_ product_code (upc), title, price_including_tax,"
                            "price_excluding_tax, number_available, product_description, category, review_rating, image_url" "\n\n")
            livre_csv.write(url_page_livre + "," + liste_carac_livre[0].text + "," + titre.string + "," +
                            liste_carac_livre[3].text.replace("Â", "") + "," + liste_carac_livre[2].text.replace("Â", "") +
                            "," + liste_carac_livre[5].text + "," + '"' + description.replace('"', '^') + '"' + "," + categorie.text.replace("\n","") +
                            "," + liste_carac_livre[6].text + "," + image_source.replace("../..", "http://books.toscrape.com"))


copie_urls_liste("http://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html")
print(liste_urls_livres)



