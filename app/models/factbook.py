from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String
from ..app import app, db



class Country(db.Model): #transformation de la Table Country en objet Python
    id = db.Column(db.String(10), primary_key = True)  #la colonne id prend la valeur de notre BDD
    Introduction = db.Column(db.Text)
    name = db.Column(db.String(500))
    type = db.Column(db.String(100))