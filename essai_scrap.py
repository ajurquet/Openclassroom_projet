from bs4 import BeautifulSoup
import requests


liste_urls_livres = []
liste_noms_categories = []
fin_url = "index.html"


# Copie toutes les urls des catégories dans une liste
url_de_base = "http://books.toscrape.com/"
req = requests.get(url_de_base)
soup = BeautifulSoup(req.text, features="html.parser")
cats = soup.find("ul", class_="nav").findAll("a")
for i in cats:
    i = i["href"]
    i = url_de_base + i
    liste_noms_categories.append([i])
del(liste_noms_categories[0])


def copie_urls_liste(url_a_parcourir):
    """
    Parcours l'url donnée en paramètre, et copie les liens vers chaque page dans une liste
    """
    global fin_url
    req = requests.get(url_a_parcourir)
    soup = BeautifulSoup(req.text, features="html.parser")
    url_boucle = soup.findAll("h3")
    url_courte = url_a_parcourir.replace(fin_url, "")

    for i in url_boucle: #parcours l'url et copie tous les liens pointant vers une page "livre" dans une liste
        lien = i.find("a")
        lien = lien["href"]
        lien = lien.replace("../../..", "http://books.toscrape.com/catalogue")
        liste_urls_livres.append((lien))

    if soup.find("li", {"class": "next"}): # si il y a un bouton "next sur la page, relance la fonction avec la page suivante
        # if fin_url != "":
        #     url_courte = url_courte - fin_url
        bouton_next = soup.find("li", {"class": "next"})
        url_next_page = bouton_next.find("a")
        url_next_page = url_next_page["href"]
        fin_url = url_next_page
        url_next_page = url_courte + url_next_page
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


copie_urls_liste("http://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html")
print(liste_urls_livres)





