from ..app import app, db
from flask import render_template, request
from ..models.factbook import Country, Resources
from sqlalchemy import or_, and_
from sqlalchemy.orm import aliased

@app.route("/ressources")#pour définir une valeur par défaut (éviter que l'utilisateur se prenne un 404) 
@app.route("/ressources/<string:pays>")  #idem
@app.route("/ressources/<string:pays>/<int:page>")
#la valeur par défaut sera la page 1 du pays Algérie
def ressources_paginate(page=1, pays = "Algeria"):
    per_page = app.config["PAYS_PER_PAGE"]

## Requête SQL 
# SELECT country.name, resources.name
# FROM country
# INNER JOIN country_resources ON country.id = country_resources.id
# INNER JOIN resources ON country_resources.resource = resources.id;
    
## Requête SQL Alchemy 
    resultats = (    
    Country.query #Requête la table Country
    .join(Country.resources) #on récupère son instance resources (qui est la table de relation entre Country et Resources)
    .add_columns(Country.name, Resources.name) #on récupère les colonnes name de nos deux tables pour avoir tant les noms de pays que les nom de ressources
    .filter(Country.name == pays) #on filtre (notre jointure) sur le fait que le nom de pays soit celui saisi par l'utilisateur 
    .paginate(page=page, per_page=per_page)) #On pagine tout ça


    return render_template("pages/ressources.html", pagination = resultats, sous_titre="Tous les pays", pays = pays)
