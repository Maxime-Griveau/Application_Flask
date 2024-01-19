from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, validators
from wtforms.validators import Regexp

class Recherche(FlaskForm): #création d'un formulaire de recherche
    nom_pays = StringField("nom_pays", validators=[]) #il aura deux champs : l'un sera une recherche libre l'autre une sélection parmis une liste de valeurs 
    ressources = SelectMultipleField("ressources", choices=[('', ''), ('PET', 'Pétrole'), ('GOL', 'Or')])

class AjoutRessource(FlaskForm):
    nom_ressource = StringField("nom_ressource", validators=[])
    code_ressource = StringField("code_ressource", validators=[validators.Length(min=3, max=3, message="Le code de la ressource doit avoir exactement trois caractères")])

class SuppressionRessource(FlaskForm):
    nom_ressource_del = StringField("nom_ressource_del")

class SuppressionPays(FlaskForm):
    nom_pays_del = StringField("nom_pays_del")
    

    