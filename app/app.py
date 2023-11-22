from flask import Flask
from .config import Config #import de la configuration, liée à Config, lui même relié à .env

app = Flask(__name__) #l'application s'appelle du nom du dossier courant
app.config.from_object(Config) #la config de l'app est cong

