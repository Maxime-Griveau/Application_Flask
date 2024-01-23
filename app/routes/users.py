from ..app import app, db, login
from flask import render_template, request, flash, abort, redirect, url_for, abort 
from ..models.factbook import Country, Resources, Map
from ..models.formulaires import InsertionPays, InsertionUsers, Connexion
from ..utils.transformations import clean_arg
from ..models.users import Users

from flask_login import  current_user, logout_user, login_user

@app.route("/connexion", methods=['GET', 'POST'])
@app.route("/connexion/<int:page>", methods=['GET', 'POST'])
def connexion(page=1):
    
    form = Connexion()
    utilisateur = ""
    try:
       
        donnees = [] # Initialiser données comme une liste vide

        if form.validate_on_submit():
            print("YOUPIII")
            
            mot_de_passe = clean_arg(request.form.get("mot_de_passe", None))
            
            mail = clean_arg(request.form.get("mail", None))
            print(mail)
            if current_user.is_authenticated is False:
                if mail and mot_de_passe: 
                        
                        utilisateur = Users().Identification(mail=mail, password=mot_de_passe)
                        if utilisateur:
                            login_user(utilisateur)

                            flash(f"{utilisateur.mail} est désormais connecté.", 'success')
                        
                else:
                        flash(f"Impossible de vous connecter, merci de merci vos informations de connexion.", 'error')
            else:
                flash("Merci d'indiquer votre identifiant (prénom) et mot de passe.", 'info')
     
    
    except Exception as e:
            print("Une erreur est surveneue : " + str(e))#Ça c'est l'erreur qui s'affichera dans les logs (back office)
            flash("Une erreur s'est produite lors de l'ajout de l'utilisateur, avez-vous respecté les contraintes de saisie ?" + str(e), 'info') #ça c'est pour notre utilisateur ('error' ne produit pas de résultats semble-il)
            db.session.rollback() #on fait un rollback pour éviter de lock la base
            
          

    return render_template("pages/connexion.html", sous_titre="Recherche", donnees=donnees, form=form, utilisateur=utilisateur)

@app.route("/utilisateurs/deconnexion", methods=["POST", "GET"]) #route pour la déconnexion
def deconnexion():
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté", "info")
    return redirect(url_for("accueil"))

login.login_view = "connexion" #permet de rediriger l'utilisateur vers la page de connexion quand il essaie d'accéder à une page de connexion et qu'il n'est pas connecté 