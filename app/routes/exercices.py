from ..app import app
from flask import render_template
from ..app import SQLAlchemy #import de SQLAlchemy depuis l'application (instance)
from sqlalchemy import text  #import de sqlaclchemy pour utiliser sa méthode text
from ..app import db #import de db (database)
from ..models.factbook import Country
from ..datas.datas_eol import datas
import requests #import du module request
from bs4 import BeautifulSoup #et de Bs4
import csv 



#rev3

@app.route("/parcs_eoliens")

def parcs():
    datas_eol = datas
    return render_template("pages/rev3.html", datas_eol= datas)


#rev5 (on aurait pu utiliser les données de rev5 pour faire rev3, çaurait d'ailleurs été plus logique)

@app.route("/parcs/<uuid>") #la route /parcs/uuid [le lien url_for de jinja] renvoie les pages correspondantes (générées de façon dynamique)
def parc_detail(uuid):

    datas_eol = datas

    for json in datas_eol: 
        if json["recordid"] == uuid: #vérifie : si "JSON" est égal à uuid [le nom de la page] alors les données correctes s'affichent
            id = json["recordid"]
            region = json["fields"]["nom_reg"]
            departement = json["fields"]["nom_dept"] 
            code_departement = json["fields"]["dep"]
            commune = json["fields"]["f_commune_pdl"]
            EPCI = json["fields"]["libepci"]
            date = json["fields"]["date_des_donnees"]
            longitude = json["fields"]["coordonnees"][0]
            lattitude = json["fields"]["coordonnees"][1]
            break #arrêt de la fonction une fois notre recordid trouvé 
    
    return render_template('/pages/rev5.html', id=id, region=region,departement=departement,code_departement=code_departement,commune=commune,EPCI=EPCI, date=date,longitude=longitude,lattitude=lattitude)

#app1

@app.route("/retrieve_wikidata/<string:id>") 

def wikidata(id):
    url = "https://www.wikidata.org/wiki" + "/"+ id #l'url est celle de wikidata + l'identifiant défini par l'utilisateur dans l'url qu'il a entrée
    response = requests.get(url) 

    page = response.text 
    page = BeautifulSoup(page, features="html.parser")
    
    return render_template("/pages/app1.html", id= id, page=page, url=url)
    

#app3 