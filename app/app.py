from flask import Flask
from .config import Config #import de la configuration, liée à Config, lui même relié à .env
from flask import render_template

app = Flask(__name__) #l'application s'appelle du nom donné entre parenthèses
app.config.from_object(Config) #la config de l'app est cong



from .routes import routes_generales #il faut importer les routes dans notre application, forcément après la configuration 
from .routes import routes_exercices #import des routes des exercices
from .datas import JSON_data
