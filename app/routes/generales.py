from ..app import app, db
from flask import render_template, request, flash, abort #flash permet l'affichage conditionnel d'informations à l'utilisateur (il faut avoir inséré le code pour Flash dans notre container)
from sqlalchemy import or_, text, any_
from ..models.factbook import Country, Resources, Map, Area, Boundaries
from ..utils.transformations import  clean_arg
from ..models.formulaires import Recherche, AjoutRessource, SuppressionRessource, SuppressionPays



@app.route("/")
@app.route("/pays")
@app.route("/pays/<int:page>")
def pays(page=1):
    return render_template("pages/pays.html", 
        sous_titre="Pays", 
        donnees= Country.query.order_by(Country.name).paginate(page=page, per_page=app.config["PAYS_PER_PAGE"]))

@app.route("/pays/<string:nom_pays>")
def un_pays(nom_pays):
    try: #on essaie
        resultats = Country.query.filter(Country.name == nom_pays).first() #Si mon résultat

        if resultats is None: #est égal à non (donc si ma requête ne donne aucun résultat)
            # Si le pays n'est pas trouvé, déclencher une exception personnalisée
            abort(500) #et bien j'aborte ! et je déclenche l'erreur 500 

        return render_template("pages/un_pays.html", sous_titre=nom_pays, donnees=resultats)



    except Exception as e: #et puis si vraiment il y a un soucis, eh bien erreur 404 ; le rolleback n'est pas nécessaire car cette requête ne modifie pas la base (non ?)
        print("Une erreur est survenue :", str(e))
        abort(404)
        





@app.route("/continents")
@app.route("/continents/<int:page>")
def continents(page=1):
    # on va créer un dictionnaire (JSON) avec en clé les continents et en valeur une liste de pays
    # il faut initialiser ce dictionnaire au début 
    pays_par_continent = {}

    for pays in Country.query.all():
        for continent in pays.maps:
            # si la clé (continent) existe déjà dans le dictionnaire, alors il est simplement nécessaire 
            # d'ajouter le pays s'il n'est pas déjà présent
            if continent.name in pays_par_continent:
                if pays.name not in pays_par_continent[continent.name]:
                    pays_par_continent[continent.name].append(pays.name)
            # sinon il faut créer la clé et initialiser la valeur
            else:
                pays_par_continent[continent.name] = [pays.name]

    return render_template("pages/continents.html",
        sous_titre="Continents",
        donnees=Map.query.paginate(page=page, per_page=app.config["PAYS_PER_PAGE"]),
        donnees_generales=pays_par_continent)

@app.route("/continents/<string:nom_continent>")
def un_continent(nom_continent):
    continent = Map.query.filter(Map.name == nom_continent).first()

    return render_template("pages/un_continent.html", 
        sous_titre=nom_continent, 
        donnees= Country.query.filter(Country.maps.contains(continent)).order_by(Country.name).all())

@app.route("/ressources")
@app.route("/ressources/<int:page>")
def ressources(page=1):
    # on va créer un dictionnaire (JSON) avec en clé les continents et en valeur une liste de pays
    # il faut initialiser ce dictionnaire au début 
    pays_par_ressource = {}

    for pays in Country.query.all():
        for ressource in pays.resources:
            # si la clé (ressource) existe déjà dans le dictionnaire, alors il est simplement nécessaire 
            # d'ajouter le pays s'il n'est pas déjà présent
            if ressource.name in pays_par_ressource:
                if pays.name not in pays_par_ressource[ressource.name]:
                    pays_par_ressource[ressource.name].append(pays.name)
            # sinon il faut créer la clé et initialiser la valeur
            else:
                pays_par_ressource[ressource.name] = [pays.name]
    
    return render_template("pages/ressources.html",
        sous_titre="Ressources",
        donnees=Resources.query.paginate(page=page, per_page=app.config["RESOURCES_PER_PAGE"]),
        donnees_generales=pays_par_ressource)

@app.route("/ressources/<string:nom_ressource>")
def une_ressource(nom_ressource):
    ressource = Resources.query.filter(Resources.name == nom_ressource).first()

    return render_template("pages/une_ressource.html", 
        sous_titre=nom_ressource, 
        donnees= Country.query.filter(Country.resources.contains(ressource)).order_by(Country.name).all())

@app.route("/recherche_rapide")
@app.route("/recherche_rapide/<int:page>")
def recherche_rapide(page=1):
    chaine =  request.args.get("chaine", None)
    if chaine:
        resources = db.session.execute(text("""select a.id from country a 
            inner join country_resources b on b.id = a.id 
            inner join resources c on c.name = b.resource
            and (c.name like '%"""+chaine+"""%' or  c.id like '%"""+chaine+"""%')
            """)).fetchall()
        maps = db.session.execute(text("""select a.id from country a 
            inner join country_map b on b.id = a.id 
            inner join map  c on c.name = b.map_ref 
            and (c.name like '%"""+chaine+"""%' or  c.id like '%"""+chaine+"""%')
            """)).fetchall()
        resultats = Country.query.filter(
                or_(
                    Country.name.ilike("%"+chaine+"%"),
                    Country.type.ilike("%"+chaine+"%"),
                    Country.Introduction.ilike("%"+chaine+"%"),
                    Country.id.in_([r.id for r in resources] + [m.id for m in maps])
                )
            ).distinct(Country.name).order_by(Country.name).\
            paginate(page=page, per_page=app.config["PAYS_PER_PAGE"])
    else:
        resultats = None     
    return render_template("pages/resultats_recherche_pays.html", 
            sous_titre= "Recherche | " + chaine, donnees=resultats,requete=chaine)

@app.route("/recherche", methods=['GET', 'POST'])
@app.route("/recherche/<int:page>", methods=['GET', 'POST'])
def recherche(page=1):
    
    form = Recherche()
    try:
        nom_pays = clean_arg(request.form.get("nom_pays", None))
        ressources = clean_arg(request.form.getlist("ressources", None)) #Il faut faire getlist car le champ est multipleField


        donnees = [] # Initialiser données comme une liste vide
        if form.validate_on_submit():
            if nom_pays or ressources:
                query_results = Country.query

            if nom_pays:
                query_results = query_results.filter(Country.name.ilike("%" + nom_pays + "%")) #si "nom_pays" saisi par l'utilisateur est présent dans l'un des noms de pays alors il sera renvoyé  

            if ressources:
                resource = Country.query.join(Country.resources).filter(Resources.id.in_(ressources)) #on fait la jointure entre Country et Ressource pour que la liste des pays possédant telle ou telle ressource soit renvoyée
                query_results = query_results.filter(Country.id.in_([r.id for r in resource] )) #query_resultats prend la valeur des noms de pays qui contiennent dans leur id la liste "r" de tous les résultats de recherche. NB. la recherche agit comme un "ou" et pas un "et"
                



            donnees = query_results.order_by(Country.name).paginate(page=page, per_page=app.config["PAYS_PER_PAGE"])
            
            form.nom_pays.data = nom_pays
            form.ressources.data = ressources
            flash("La recherche retourne les résultats suivants :", 'success')
    
    except Exception as e:
            print("Une erreur est surveneue : " + str(e))#Ça c'est l'erreur qui s'affichera dans les logs (back office)
            flash("Une erreur s'est produite lors de la recherche " + " : " + str(e), 'error')

    return render_template("pages/resultats_recherche.html", sous_titre="Recherche", donnees=donnees, form=form)

@app.route("/insertion_ressource", methods=['GET', 'POST'])
@app.route("/insertion_ressource/<int:page>", methods=['GET', 'POST'])
def insertion_ressource(page=1):
    
    form = AjoutRessource()
    nouvelle_ressource = None
    try:
        nom_ressource = clean_arg(request.form.get("nom_ressource", None))
        code_ressource = clean_arg(request.form.get("code_ressource", None))


        donnees = [] # Initialiser données comme une liste vide
        if form.validate_on_submit():
            if nom_ressource and code_ressource: #ici on veut un AND et non un or car on ne veut pas de valeur nulles dans notre base 
                nouvelle_ressource = Resources(name= nom_ressource, id = code_ressource)
                
                db.session.add(nouvelle_ressource)

                db.session.commit()
                
            donnees = Resources.query.all()#on récupère notre base pour afficher à l'utilisateur son ajout 
 
            
            form.nom_ressource.data = nom_ressource
            form.code_ressource.data = code_ressource
            flash("Votre ressource a bien été ajoutée en base :", 'success')
    
    except Exception as e:
            print("Une erreur est surveneue : " + str(e))#Ça c'est l'erreur qui s'affichera dans les logs (back office)
            flash("Une erreur s'est produite lors de l'ajout en base, avez-vous bien renseigné le code (3 caractères) ET le nom de la ressource ? (si la ressource existe déjà, vous ne pouvez pas l'ajouter)" + " : " + str(e), 'error') #ça c'est pour notre utilisateur
            db.session.rollback() #on fait un rollback pour éviter de lock la base
            

    return render_template("pages/resultats_ajout_ressource.html", sous_titre="Recherche", donnees=donnees, form=form, nouvelle_ressource=nouvelle_ressource)



@app.route("/suppression_ressource", methods=['GET', 'POST'])
@app.route("/suppression_ressource/<int:page>", methods=['GET', 'POST'])
def suppression_ressource(page=1):
    
    form = SuppressionRessource()
    ressource_supprimee = ""
    try:
        nom_ressource = clean_arg(request.form.get("nom_ressource_del", None))

        donnees = [] # Initialiser données comme une liste vide
        if form.validate_on_submit():

            if nom_ressource: 
                    
                    Resources.query.filter(Resources.name == nom_ressource).delete()
                    db.session.commit()
                    flash(f"La ressource '{nom_ressource}' a bien été supprimée de la base.", 'success')
            else:
                    flash(f"La ressource '{nom_ressource}' n'existe pas dans la base de données.", 'info')
        else:
            flash("Veuillez fournir le nom de la ressource à supprimer.", 'info')
                
            donnees = Resources.query.all()#on récupère notre base pour afficher à l'utilisateur son ajout 
 
            
            form.nom_ressource_del.data = nom_ressource
    
    except Exception as e:
            print("Une erreur est surveneue : " + str(e))#Ça c'est l'erreur qui s'affichera dans les logs (back office)
            flash("Une erreur s'est produite lors de la suppression, la ressource existe-elle dans la base ?" + str(e), 'info') #ça c'est pour notre utilisateur ('error' ne produit pas de résultats semble-il)
            db.session.rollback() #on fait un rollback pour éviter de lock la base
            abort(500)

    return render_template("pages/resultats_suppression_ressource.html", sous_titre="Recherche", donnees=donnees, form=form, ressource_supprimee=ressource_supprimee)


@app.route("/suppression_pays", methods=['GET', 'POST'])
@app.route("/suppression_pays/<int:page>", methods=['GET', 'POST'])
def suppression_pays(page=1):
    
    form = SuppressionPays()
    pays_supprimee = ""
    try:
        nom_pays = clean_arg(request.form.get("nom_pays_del", None))

        donnees = [] # Initialiser données comme une liste vide

        if form.validate_on_submit():

            if nom_pays: 
                    
                    Country.query.filter(Country.name == nom_pays).delete()
                    db.session.commit()
                    flash(f"Le pays '{nom_pays}' a bien été supprimée de la base.", 'success')
            else:
                    flash(f"Le pays '{nom_pays}' n'existe pas dans la base de données.", 'info')
        else:
            flash("Veuillez fournir le nom du pays à supprimer.", 'info')
                
            donnees = Country.query.all()#on récupère notre base pour afficher à l'utilisateur son ajout 
 
            
            form.nom_pays_del.data = nom_pays
       
    
    except Exception as e:
            print("Une erreur est surveneue : " + str(e))#Ça c'est l'erreur qui s'affichera dans les logs (back office)
            flash("Une erreur s'est produite lors de la suppression, le pays existe-il dans la base ?" + str(e), 'info') #ça c'est pour notre utilisateur ('error' ne produit pas de résultats semble-il)
            db.session.rollback() #on fait un rollback pour éviter de lock la base
            abort(500)

    return render_template("pages/resultats_suppression_pays.html", sous_titre="Recherche", donnees=donnees, form=form, pays_supprimee=pays_supprimee)



