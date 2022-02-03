# Openclassroom_projet_02


Auteur : Alexandre Jurquet.
Date de création : Mars 2021.

Code du projet 02 de la formation "Développeur d'application - Python" du site Openclassrooms.


## Résumé

Dans ce projet on est dans la peau d'un analyste marketing dans l'entreprise "Book Online", une librairie en ligne. On doit suivre les prix des livres d'occasions d'un site conccurent.

Il faut donc "scraper", c'est à dire aspirer les données du site "http://books.toscrape.com/", et de les sauvegarder dans un ou des fichiers.

Pour cela nous utiliserons la librairie "BeautifulSoup", spécialisée pour le web scrapping.



Le premier fichier "P2_01_Scrap_page_livre.py" aspire les différentes données d'une page de livre (titre, prix, stock, etc.), et les copie dans un fichier csv.

Le second fichier "P2_02_Scrap_categorie.py" utilise le code du précédent fichier, et l'applique à tous le livres d'une catégorie. Il copie toutes le données dans un fichier csv.

Le troisième fichier "P2_03_Scrap_toutes_categories.py" utilise également le code des fichiers précédents, mais cette fois-ci, il aspire toutes les pages de toutes les catégories,
et copie les données dans des fichiers.

Le dernier fichier "P2_04_Scrap_images.py" reprend le code précédent, et aspire en plus toutes les images de chaque produit.


## Prérequis

Vous devez installer python, la dernière version se trouve à cette adresse :
https://www.python.org/downloads/


Les scripts python se lancent depuis un terminal, pour ouvrir un terminal sur Windows, pressez ``` touche windows + r``` et entrez ```cmd```.

Sur Mac, pressez ```touche command + espace``` et entrez ```terminal```.

Sur Linux, vous pouvez ouvrir un terminal en pressant les touches ```Ctrl + Alt + T```.

Le programme utilise plusieurs librairies externes, et modules de Python, qui sont répertoriés dans le fichier ```requirements.txt```


Il est préférable d'utiliser un environnement virtuel, vous pouvez l'installer via la commande :  
```bash
pip install pipenv
```

Vous devez ensuite créer et activer un environnement en entrant les commandes suivantes dans le terminal :

##LINUX MACOS

Naviguez où vous souhaitez créer votre environnement virtuel, puis entrez :

```bash
pipenv install
```
puis :
```bash
pipenv shell
```
et enfin :

```bash
pip install -r requirement.txt
```
afin d'installer toutes les librairies.

##WINDOWS

Naviguez où vous souhaitez créer votre environnement virtuel, puis entrez :

```bash
pipenv install
```
puis :
```bash
pipenv shell
```
et enfin :

```bash
pip install -r requirement.txt
```
afin d'installer toutes les librairies.


## Rapport flake8

Le programme est conforme à la PEP8, le repository contient un rapport flake8 nommé "flake-report", qui n'affiche aucune erreur. Il est possible d'en générer un nouveau en installant le module ```flake8-html``` et en entrant dans le terminal :

```bash
 flake8
```

Le fichier ```setup.cfg``` à la racine contient les paramètres concernant la génération du rapport.
