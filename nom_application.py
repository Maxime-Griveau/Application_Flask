from flask import Flask #import de Flask
from app.factbook import app #dans le dossier app va cherche le module app et sa méthode app
from app.config import version
from app.config import Config 

if __name__ == "__main__": #vérifie
    print(version)
    app.run(debug=app.config["DEBUG"]) #lancement de l'application depuis le bon fichier
    #et indication que configuration en mode debug
    app.config['SERVER_NAME'] = "test"