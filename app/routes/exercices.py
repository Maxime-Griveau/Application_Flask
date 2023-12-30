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
import pandas as pd



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

@app.route("/permis/<int:depuis>/<int:jusque>")

def permis(jusque, depuis):


    jusque += 1
    
    datas = pd.read_csv("app/datas/auto-ecole-resultats.csv", delimiter=",", encoding='latin1') #encodage en latin1 pour respecter la norme ISO/CEI 8859-1
    
    nbr_candidats = datas["nbr_candidats"].tolist()
    reussite = datas["reussite"].tolist()

    #NOTA : les regex ne sont pas parfaites, certaines colonnes apparaissent vides "nan" mais ça suffira pour l'exercice.
    nom_ae = datas["localite_auto_ecole"].str.extract(r'(^[A-Z-\s]*)')[0].tolist() #les regex doivent forcément être insérés dans un groupe de capture (des parentèses)
    code_postal = datas["localite_auto_ecole"].str.extract(r'([0-9]{5})')[0].tolist()
    ville = datas["localite_auto_ecole"].str.extract(r'[0-9]{5}\s(.*)')[0].tolist() #Pour choisir un groupe de capture, il suffit de le mettre entre parenthèse, et lui seulement
    adresse = datas["localite_auto_ecole"].str.extract(r'([0-9].*)[0-9]{5}')[0].tolist()
    donnees_combinees = list(zip(nom_ae, code_postal, ville, adresse, nbr_candidats, reussite)) #ZIP permet de combiner nos données en des tuples pour pouvoir les utiliser dans jinja (sinon cela ferait faire des boucles for dans des boucles for) il faut ensuite remettre ces tuples dans une liste pour pouvoir itérer 
    
    
    return render_template("pages/app3-5.html", jusque=jusque, depuis=depuis, donnees_combinees = donnees_combinees)


    



#rev6 
