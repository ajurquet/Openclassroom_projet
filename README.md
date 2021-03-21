# Openclassroom_projet_02

Auteur : Alexandre Jurquet.
Date de création : Mars 2021.


  Code du projet 02 de la formation "Développeur d'application - Python" du site Openclassrooms.


  Ce projet consiste à scraper les données du site "http://books.toscrape.com/", et de les sauvegarder dans un ou des fichiers.

Le premier fichier "P2_01_Scrap_page_livre.py" aspire les différentes données d'une page de livre (titre, prix, stock, etc.), et les copie dans un fichier csv.

Le second fichier "P2_02_Scrap_categorie.py" utilise le code du précédent fichier, et l'applique à tous le livres d'une catégorie. Il copie toutes le données dans un fichier csv.

Le troisième fichier "P2_03_Scrap_toutes_categories.py" utilise également le code des fichiers précédents, mais cette fois-ci, il aspire toutes les pages de toutes les catégories,
et copie les données dans des fichiers.

Le dernier fichier "P2_04_Scrap_images.py" reprend le code précédent, et aspire en plus toutes les images de chaque produit.


  Pour lire ces fichiers, vous aurez besoin de créer un environnement virtuel via un terminal. Il suffit de taper dans le terminal la commande "python -m venv env"
(sans les guillements), dans le repertoire de votre choix.

Vous devrez ensuite installer les différents paquets requis pour que les scripts soient utilisable. Ils sont listés dans le fichier "requirements.txt". Il suffite de taper la 
commande "pip install -r requirements.txt" pour que tous les paquets nécéssaires soient installés.

Il suffit ensuite de taper la commande "python" suivi du nom du fichier pour le lancer.
  
  


