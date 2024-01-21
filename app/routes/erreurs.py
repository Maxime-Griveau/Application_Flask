from ..app import app, db
from flask import render_template, abort #abort sert à générer des erreurs http
from werkzeug.exceptions import BadRequest, BadHost, BadGateway, BadRequestKeyError
import json 




@app.errorhandler(404) #erreur 404 = url non trouvée
def page_not_found(e):
    return render_template('/pages/erreurs/404.html'), 404

@app.errorhandler(500) #erreur 500 = erreur serveur
def internal_server_error(e):
    return render_template('pages/erreurs/500.html'), 500

@app.errorhandler(403) #erreur 403 = l'utilisateur n'a pas le droit de faire ça ! 
def forbiden(e):
    return render_template('/pages/erreurs/403.html'), 403

@app.errorhandler(503) #erreur 503 = service inaccessible 

def service_unavailable(e):
    return render_template('/pages/erreurs/503.html'), 503




@app.route('/error_500')
def error_500():
    # Simule une erreur interne du serveur
    abort(500)

@app.route('/error_403')
def error_403():
    # Simule une erreur d'autorisation
    abort(403)

@app.route('/error_503')
def error_503():
    # Simule une erreur de service indisponible
    abort(503)

@app.route('/error_418')
def error_418():
    # juste pour tester ;) 
    abort(418) 