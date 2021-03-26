"""
Enfin, prolongez votre travail existant pour télécharger et enregistrer le fichier
image de chaque page Produit que vous consultez  !
"""

from bs4 import BeautifulSoup
import requests
import os
import csv
import urllib

liste_urls_livres = []
liste_urls_categories = []
fin_url_a_remplacer = "index.html"
nom_fichier_csv = ""
liste_titre = ["product_page_url", "universal_ product_code (upc)", "title", "price_including_tax",
                   "price_excluding_tax", "number_available", "product_description", "category", "review_rating",
                   "image_url"]

if not os.path.exists("books_to_scrape_csv"):
    os.mkdir("books_to_scrape_csv")
if not os.path.exists("images_scrap/"):
    os.mkdir("images_scrap")

def copie_urls_livre(url_a_parcourir):
    """
    Fonction qui parcours l'url de la catégorie donnée en paramètre,
    et copie les liens vers chaque page "livre" dans la liste "liste_urls_livres"
    """
    global fin_url_a_remplacer
    req = requests.get(url_a_parcourir)
    soup = BeautifulSoup(req.content, features="html.parser")
    url_boucle = soup.find_all("h3")
    url_raccourci = url_a_parcourir.replace(fin_url_a_remplacer, "")

    for i in url_boucle: # parcours l'url de la categorie et copie tous les liens pointant vers une page "livre" dans la liste "liste_urls_livres"
        lien = i.find("a")
        lien = lien["href"]
        lien = lien.replace("../../..", "http://books.toscrape.com/catalogue")
        liste_urls_livres.append((lien))

    if soup.find("li", class_="next"): # si il y a un bouton "next" sur la page, relance la fonction avec la page suivante
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

        nb_reviews = tableau[6].text
        nb_reviews = int(nb_reviews)

        description = soup.find_all("p")
        description = description[3].text

        img_url = soup.find("img").get("src")
        img_url = img_url.replace("../..", "http://books.toscrape.com")

        categorie = soup.find("ul", class_="breadcrumb").find_all("li")
        categorie = categorie[2].text.strip()

        image_source = soup.find("img").get("src")
        image_source = image_source.replace("../..", "http://books.toscrape.com")

        # utilise urllib pour télécharger l'image dans le dossier 'image_scrap", le nom du fichier est l'upc suivi du titre du livre
        urllib.request.urlretrieve(image_source,
                                   "images_scrap/" + upc + " - " + titre.replace('"', '').replace(":", ";").replace("*", " ").replace(
                                       "?", "").replace("/", " ") + ".jpg")

        liste_donnees = [url_page_livre, upc, titre, prix_ht, prix_ttc, stock, description, categorie, nb_reviews, img_url]

        return (liste_donnees)

def copie_urls_cat():
    """
    Copie toutes les urls des catégories dans la liste "liste_urls_categories
    """
    global liste_urls_categories
    url_de_base = "http://books.toscrape.com/"
    req = requests.get(url_de_base)
    soup = BeautifulSoup(req.text, features="html.parser")
    cats = soup.find("ul", class_="nav").find_all("a")

    for i in cats:
        i = i["href"]
        i = url_de_base + i
        i = i.replace("'", '"')
        liste_urls_categories.append(i)
    del (liste_urls_categories[0]) # efface le premier élément de la liste qui contient tous les livres du site

copie_urls_cat()

for i in liste_urls_categories: # parcourt chaque catégorie
    print(i)

    # Trouve le titre de la catégorie pour nom du fichier csv
    req = requests.get(i)
    if req.ok:
        soup = BeautifulSoup(req.content, features="html.parser")
        nom_fichier_csv = soup.find("h1").text.lower().replace(" ", "_")
        nom_fichier_csv = nom_fichier_csv + ".csv"

        copie_urls_livre(i)  # copie dans la liste les urls de chaque livre

    with open("books_to_scrape_csv/" + nom_fichier_csv, "w", encoding="utf-8-sig", newline="") as cat_csv:
        csv_file_writer = csv.writer(cat_csv)
        csv_file_writer.writerow(liste_titre)  # copie les titres au début du csv

        for url in liste_urls_livres:
            csv_file_writer.writerow(scrap_page_livre(url))  # copie les données de chaque livre dans le csv

    liste_urls_livres = []
    fin_url_a_remplacer = "index.html"