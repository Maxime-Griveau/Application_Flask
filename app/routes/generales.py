from ..app import app, db
from flask import render_template, request
from ..models.factbook import Country, Resources
from sqlalchemy import or_, and_
from sqlalchemy.orm import aliased





@app.route("/generique") #route générique qui retourne tous les résulats 
def generique():
    resultats = Country.query.all() 
    return render_template("pages/generique.html", donnees = resultats)


@app.route("/le_premier_pays") #retourne uniquement le premier résultat
def premierpays():
    resultats = Country.query.first() 
    return render_template("pages/generique.html", donnees = [resultats])


@app.route("/pays_differents_de_souverain") #retourne tous les pays qui ne sont pas "sovereign"
def souverain():
    resultats = Country.query.filter(Country.type!='sovereign').all()
    return render_template("pages/generique.html", donnees = resultats)

@app.route("/condition_or_autre_condition") #retourne tous les pays souverains ou dont l'ID est "ay" 
def condition():
    resultats = Country.query.filter(or_(Country.type == 'sovereign',  Country.id == 'ay')).all()
    return render_template("pages/generique.html", donnees = resultats)


@app.route("/add_country/<string:id>/<string:name>/<string:type>/<string:description>") #ajout d'un pays à la base en fonction des critères définis dans l'url

def add(id, name, type, description):
    nouveau_pays = Country(id = id, name = name , type = type, Introduction = description)

    db.session.add(nouveau_pays)
    db.session.commit()
    return "OK"


@app.route("/get_pays/<string:id>") #récupération d'un pays en fonction de son id avec get
def get_pays(id):
    resultats = Country.query.get({"id" : id})
    return render_template("pages/generique.html", donnees = [resultats])


@app.route("/delete_pays/<string:id>") #suppression d'un pays en fonction de son id 
def delete_pays(id):
    Country.query.filter(Country.id == id).delete()
    db.session.commit()
    return "OK"

#Pagination 


@app.route("/pays_paginate") #pour définir une valeur par défault (éviter que l'utilisateur se prenne un 404) 
@app.route("/pays_paginate/<int:page>")

def pays_paginate(page=1):
    per_page = app.config["PAYS_PER_PAGE"]
    
    tous_resultats = Country.query.paginate(page=page, per_page=per_page)

    return render_template("pages/pays_paginate.html", pagination=tous_resultats, sous_titre="Tous les pays")


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