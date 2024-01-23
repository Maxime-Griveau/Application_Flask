from ..app import app, db
from flask import render_template, request, flash, abort
from ..models.factbook import Country, Resources, Map
from ..models.formulaires import InsertionPays, InsertionUsers
from ..utils.transformations import clean_arg
from ..models.users import Users

@app.route("/insertions/pays", methods=['GET', 'POST'])
def insertion_pays():
    form = InsertionPays() 

    try:
        if form.validate_on_submit():
            nom_pays =  clean_arg(request.form.get("nom_pays", None))
            code_pays =  clean_arg(request.form.get("code_pays", None))
            type =  clean_arg(request.form.get("type", None))
            introduction =  clean_arg(request.form.get("introduction", None))
            ressources =  clean_arg(request.form.getlist("ressources", None))
            continent =  clean_arg(request.form.get("continent", None))

            nouveau_pays = Country(id=code_pays, 
                Introduction=introduction,
                name=nom_pays,
                type = type)

            for ressource in ressources:
                ressource = Resources.\
                    query.\
                    filter(Resources.id == ressource).\
                    first()
                nouveau_pays.resources.append(ressource)
            
            nouveau_pays.maps.append(Map.query.filter(Map.name==continent).first())

            db.session.add(nouveau_pays)
            db.session.commit()

            flash("L'insertion du pays "+ nom_pays + " s'est correctement déroulée", 'info')
    
    except Exception as e :
        flash("Une erreur s'est produite lors de l'insertion de " + nom_pays + " : " + str(e), "error")

        db.session.rollback()
    
    return render_template("pages/insertion_pays.html", 
            sous_titre= "Insertion pays" , 
            form=form)



@app.route("/insertion/utilisateur", methods=['GET', 'POST'])
@app.route("/insertion_utilisateur/<int:page>", methods=['GET', 'POST'])
def insertion_utilisateur(page=1):
    
    form = InsertionUsers()
    nouvel_utilisateur = ""
    try:
        donnees = [] # Initialiser données comme une liste vide

        if form.validate_on_submit():
            mail = clean_arg(request.form.get("mail", None))
            prenom = clean_arg(request.form.get("prenom", None))
            mot_de_passe = clean_arg(request.form.get("mot_de_passe", None))

            if mail and prenom and mot_de_passe: 
                
                    # Assurez-vous que la méthode Ajout renvoie correctement l'utilisateur et les erreurs
                    nouvel_utilisateur, erreurs = Users().Ajout(prenom=prenom, password=mot_de_passe, mail=mail) #si on ne met pas ", erreurs" ici python considère que notre variable est égale à un tuple car notre méthode renvoie un tuple avec l'erreur et le contenu de la notre requête
                    print(nouvel_utilisateur)
                    if nouvel_utilisateur:
                        flash(f"L'utilisateur {nouvel_utilisateur.prenom} a bien été ajouté dans la base.", 'success')
                    else:
                        flash(f"L'utilisateur n'a pas été ajouté dans la base. Erreurs : ", 'error')
        else:
            flash("Merci d'indiquer vos informations de création de compte.", 'info')
     
    
    except Exception as e:
            print("Une erreur est survenue : " + str(e))  # Ça c'est l'erreur qui s'affichera dans les logs (back office)
            flash("Une erreur s'est produite lors de l'ajout de l'utilisateur, avez-vous respecté les contraintes de saisie ?" + str(e), 'info')
            db.session.rollback()  # On fait un rollback pour éviter de lock la base
          

    return render_template("pages/ajout_utilisateur.html", sous_titre="Recherche", donnees=donnees, form=form, nouvel_utilisateur=nouvel_utilisateur)
