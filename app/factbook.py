from flask import Flask
from .config import Config #import de la configuration, liée à Config, lui même relié à .env
from flask import render_template

app = Flask(__name__) #l'application s'appelle du nom donné entre parenthèses
app.config.from_object(Config) #la config de l'app est cong


@app.route("/home")
def home():
    return render_template("accueil.html")