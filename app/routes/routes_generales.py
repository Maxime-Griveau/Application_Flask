from flask import render_template
from ..app import app


@app.route("/")
def accueil():
    return "Racine"

@app.route("/pays/<string:nom>") #route /pays/str et indique le nom du pays requêté dans la page  
def pays(nom):

    donnees = [{
        "nom":"France",
        "capitale":"Paris",
        "continent":"Europe"
    },{
        "nom":"Etats-Unis",
        "capitale":"Washington",
        "continent":"Amérique"
    },{
        "nom":"Egypte",
        "capitale":"Le Caire",
        "continent":"Afrique"
    },{
        "nom":"Chine",
        "capitale":"Pékin",
        "continent":"Asie"
    }]
    return render_template("accueil.html", pays = nom, dict = donnees)


@app.route("/ville/<string:nom_ville>")
def ville(nom_ville):
    return render_template("datas.html", nom_ville = nom_ville)



