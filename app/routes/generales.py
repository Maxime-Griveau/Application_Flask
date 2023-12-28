from ..app import app
from flask import render_template
from ..app import SQLAlchemy #import de SQLAlchemy depuis l'application (instance)
from sqlalchemy import text  #import de sqlaclchemy pour utiliser sa méthode text
from ..app import db #import de db (database)
from ..models.factbook import Country 


@app.route("/pays")
def pays():
    resultats = Country.query.all()

    donnees = []

    for r in resultats: #pour chaque r dans mes résultats 
        #print(r) #renvoie le contenu de Country avec le nom de colonne 
        #print(type(r)) #renvoie le type de r (objet de la classe country)
        #print(r.id) #renvoie le contenu de la colonne id
        #print(r.name) #renvoie le contenu de la colonne name 
        #renvoie le contenu de la colonne name
        #print(r.Introduction) #renvoie le contenu de l'introduction 
         
    
        donnees.append({ #mes données prennent la valeur 
    "nom":r.name, #du nom des pays 
    "capitale":"inconnue",
    "continent":"inconnu",
    })



   # query = text("SELECT * FROM country LIMIT 10") #on doit typer query en text [objet de SQL]
    # resultats = db.session.execute(query).fetchall() #fetchall pour afficher tous les résultats

    # print(resultats) #imprime nos résultats bruts 
    
    return render_template("pages/tous_pays.html", donnees=donnees, sous_titre="Tous les pays")

@app.route("/pays/<string:nom>")
def pays_specifique(nom):
    grandes_villes = []
    if nom =='France':
        grandes_villes = ['Paris', 'Lyon', 'Marseille']
    return render_template("pages/pays.html", pays=nom, grandes_villes=grandes_villes, sous_titre=nom)