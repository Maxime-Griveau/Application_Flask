from flask import render_template
from ..app import app
from ..datas.JSON_data import datas





@app.route("/division/<int:nombre>/<int:diviseur>")
def division(nombre, diviseur):
    resultat = nombre/diviseur
    return render_template("exercices.html", resultat=resultat) #Il faut absolument faire resultat = resultat sinon ce n'est pas possible de return le resultat




@app.route("/parcs_eoliens")

def table():
  
    JSON = datas 
   

    return render_template("exercices.html", JSON = JSON)