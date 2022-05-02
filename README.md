# Enthic - Application de dataviz

![Logo d'enthic](static/enthic_without_bg.e0d245c1.png)

Ce repository contient le code de l'application Streamlit de visualisation des données d'[Enthic](https://enthic-dataviz.netlify.app/).

L'application est hébergé à l'aide du service Streamlit cloud sur le lien suivant : https://share.streamlit.io/lawiss/enthic-web-app/main/app.py.

# Structure de l'application

## `app.py`

Ce fichier est le point d'entrée de l'application. Il contient la mise en page et la déclaration de tous les éléments *frontend* de l'application ainsi que le chargement des données.

## `figures.py`

Ce fichier contient les fonctions de création des graphiques. Les graphiques sont construit à l'aide de la bibliothèque [Plotly](https://plotly.com/python/).

## `utils.py`

Ce fichier contient des fonctions utilitaires.

# Environnement de développement

Cette application est développé sous Python 3.9 avec streamlit 1.8.1.
Les autres dépendances sont listées dans le fichier `requirements.txt` et peuvent être installées avec pip : `pip install -r requirements.txt`.