"""
Ensuite, étendez votre travail à l'écriture d'un script qui consulte le site de Books to Scrape,
extrait toutes les catégories de livres disponibles, puis extrait les informations produit de tous
les livres appartenant à toutes les différentes catégories, ce serait fantastique  !
Vous devrez écrire les données dans un fichier CSV distinct pour chaque catégorie de livres.
"""

from bs4 import BeautifulSoup
import requests


liste_urls_livres = []
liste_urls_categories = []
fin_url = "index.html"
nom_fichier_csv = ""

def copie_urls_livre(url_a_parcourir):
    """
    Fonction qui parcours l'url de la catégorie donnée en paramètre,
    et copie les liens vers chaque page "livre" dans la liste "liste_urls_livres"
    """
    global fin_url
    req = requests.get(url_a_parcourir)
    soup = BeautifulSoup(req.text, features="html.parser")
    url_boucle = soup.findAll("h3")
    url_courte = url_a_parcourir.replace(fin_url, "")

    for i in url_boucle: # parcours l'url et copie tous les liens pointant vers une page "livre" dans une liste
        lien = i.find("a")
        lien = lien["href"]
        lien = lien.replace("../../..", "http://books.toscrape.com/catalogue")
        liste_urls_livres.append((lien))

    if soup.find("li", {"class": "next"}): # si il y a un bouton "next sur la page, relance la fonction avec la page suivante
        bouton_next = soup.find("li", {"class": "next"})
        url_next_page = bouton_next.find("a")
        url_next_page = url_next_page["href"]
        fin_url = url_next_page
        url_next_page = url_courte + url_next_page
        copie_urls_livre(url_next_page)

def scrap_page_livre(url_page_livre):
    """
    Fonction qui visite une page "livre" et en extrait des informations
    """

    req = requests.get(url_page_livre)

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
        categorie = '"' + categorie.text.replace("\n","") + '"'

        review_rating = '"' + liste_carac_livre[6].text + '"'

        image_source = soup.find("img").get("src")
        image_source = image_source.replace("../..", "http://books.toscrape.com")


        # donne en résultat les informations demandées, séparées par des virgules.
        return (url_page_livre + "," + upc + "," + titre + "," + price_including_tax + "," + price_excluding_tax +
                            "," + stock + "," + product_description + "," + categorie + "," + review_rating + "," + image_source + "\n")

def copie_urls_cat():
    """
    Copie toutes les urls des catégories dans la liste "liste_urls_categories
    """

    global liste_urls_categories
    url_de_base = "http://books.toscrape.com/"
    req = requests.get(url_de_base)
    soup = BeautifulSoup(req.text, features="html.parser")
    cats = soup.find("ul", class_="nav").findAll("a")

    for i in cats:
        i = i["href"]
        i = url_de_base + i
        i = i.replace("'", '"')
        liste_urls_categories.append(i)
    del (liste_urls_categories[0])


copie_urls_cat()

for i in liste_urls_categories:
    # Trouve le texte de la catégorie pour nom du fichier csv
    print(i)
    req = requests.get(i)
    if req.ok:
        soup = BeautifulSoup(req.text, features="html.parser")
        nom_fichier_csv = soup.find("h1").text

        copie_urls_livre(i)

        with open(nom_fichier_csv.lower().replace(" ", "_") + ".csv", "w", encoding="utf-8") as cat_csv:
            cat_csv.write("product_page_url, universal_ product_code (upc), title, price_including_tax,"
                            "price_excluding_tax, number_available, product_description, category, review_rating, image_url" "\n\n")
            for url in liste_urls_livres:
                cat_csv.write(scrap_page_livre(url))
        liste_urls_livres = []

