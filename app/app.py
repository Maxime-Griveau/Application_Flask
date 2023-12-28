from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(
    __name__, 
    template_folder='templates',
    static_folder='statics')
app.config.from_object(Config)

db = SQLAlchemy(app) #database liée à notre application (instanciée)





from .routes import generales
from .routes import exercices