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
import csv


url_categorie = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
liste_urls_livres = []
liste_titre = ["product_page_url", "universal_ product_code (upc)", "title", "price_including_tax",
               "price_excluding_tax", "number_available", "product_description", "category", "review_rating",
               "image_url"]
fin_url_a_remplacer = "index.html"


def copie_urls_livre(url_a_parcourir):
    """
    Fonction qui parcours l'url de la catégorie donnée en paramètre,
    et copie les liens vers chaque page "livre" dans la liste "liste_urls_livres"
    """
    global fin_url_a_remplacer
    req = requests.get(url_a_parcourir)
    soup = BeautifulSoup(req.content, features="html.parser")
    url_boucle = soup.find_all("h3")  # correspond à la fin de l'url de chaque livre de la catégorie
    url_raccourci = url_a_parcourir.replace(fin_url_a_remplacer, "")

    # parcours l'url de la categorie et copie tous les liens pointant vers une page "livre" dans la liste
    # [liste_urls_livres]
    for i in url_boucle:
        lien = i.find("a")
        lien = lien["href"]
        lien = lien.replace("../../..", "http://books.toscrape.com/catalogue")
        liste_urls_livres.append((lien))

    # si il y a un bouton "next" sur la page, relance la fonction avec la page suivante
    if soup.find("li", class_="next"):
        bouton_next = soup.find("li", class_="next")
        url_next_page = bouton_next.find("a")
        url_next_page = url_next_page["href"]
        fin_url_a_remplacer = url_next_page
        url_next_page = url_raccourci + url_next_page
        copie_urls_livre(url_next_page)


def scrap_page_livre(url_page_livre):
    """
    Fonction qui visite une page "livre" et en extrait des informations
    """
    req = requests.get(url_page_livre)

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

        liste_donnees = [url_page_livre,
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

        return (liste_donnees)


copie_urls_livre(url_categorie)  # appel de la fonction qui copie toutes les urls des livres dans une liste


with open("P2_02_Scrap_categorie.csv", "w", encoding="utf-8-sig", newline="") as cat_file:
    csv_file_writer = csv.writer(cat_file)
    csv_file_writer.writerow(liste_titre)  # copie les titres dans le csv
    for i in liste_urls_livres:
        csv_file_writer.writerow(scrap_page_livre(i))
