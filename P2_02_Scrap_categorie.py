"""
Maintenant que vous avez obtenu les informations concernant un premier livre, vous pouvez essayer de récupérer toutes
les données nécessaires pour toute une catégorie d'ouvrages. Choisissez n'importe quelle catégorie sur le site de
Books to Scrape. Écrivez un script Python qui consulte la page de la catégorie choisie, et extrait l'URL de la
page Produit de chaque livre appartenant à cette catégorie. Combinez cela avec le travail que vous avez déjà effectué
afin d'extraire les données produit de tous les livres de la catégorie choisie, puis écrivez les données
dans un seul fichier CSV.

Remarque : certaines pages de catégorie comptent plus de 20 livres, qui sont donc répartis sur différentes pages
(«  pagination  »). Votre application doit être capable de parcourir automatiquement les multiples pages si présentes.
"""

from bs4 import BeautifulSoup
import requests

url_cat = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
liste_urls_livres = []
fin_url = "index.html"


def copie_urls_livre(url_a_parcourir):
    """
    Fonction qui parcours l'url de la catégorie donnée en paramètre,
    et copie les liens vers chaque page "livre" dans la liste "liste_urls_livres"
    """
    global fin_url
    req = requests.get(url_a_parcourir)
    soup = BeautifulSoup(req.content, features="html.parser")
    url_boucle = soup.find_all("h3")
    url_courte = url_a_parcourir.replace(fin_url, "")

    for i in url_boucle: # parcours l'url et copie tous les liens pointant vers une page "livre" dans la liste "liste_urls_livres"
        lien = i.find("a")
        lien = lien["href"]
        lien = lien.replace("../../..", "http://books.toscrape.com/catalogue")
        liste_urls_livres.append((lien))

    if soup.find("li", {"class": "next"}): # si il y a un bouton "next" sur la page, relance la fonction avec la page suivante
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

        soup = BeautifulSoup(req.content, features="html.parser")

        titre = '"' + soup.find("h1").string + '"'

        liste_carac_livre = soup.find_all("td")
        upc = '"' + liste_carac_livre[0].text + '"'
        price_including_tax = '"' + liste_carac_livre[3].text + '"'
        price_excluding_tax = '"' + liste_carac_livre[2].text + '"'
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


# Trouve le texte de la catégorie pour nom du fichier csv
req = requests.get(url_cat)
if req.ok:
    soup = BeautifulSoup(req.content, features="html.parser")
    nom_fichier_csv = soup.find("h1").text

copie_urls_livre(url_cat)
with open(nom_fichier_csv.lower().replace(" ", "_") + ".csv", "w", encoding="utf-8-sig") as cat_csv:
    cat_csv.write("product_page_url, universal_ product_code (upc), title, price_including_tax,"
                    "price_excluding_tax, number_available, product_description, category, review_rating, image_url" "\n\n")
    for url in liste_urls_livres:
        cat_csv.write(scrap_page_livre(url))



