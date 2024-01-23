from ..app import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import or_

class Users(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement= True)
    prenom = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(100), nullable = False)
    mail = db.Column(db.String(100), nullable = False)

    def get_id(self): #permet de récupérer les id 
        return self.id

    @login.user_loader #décorateur sur user_loader qui permet de récupérer les utilisateurs par leur id 
    def get_user_by_id(id):
        return Users.query.get(int(id))     


    @staticmethod
    def Ajout(prenom, password, mail):
        erreurs = []
        if not prenom:
            erreurs.append("Le prénom est vide")
        if not mail:
            erreurs.append("Le mail est vide ou ne respecte pas les contraintes de saisie")
        if not password or len(password) < 6:
            erreurs.append("Le mot de passe est vide ou trop court")

        unique_prenom = Users.query.filter(
            db.or_(Users.prenom == prenom)
        ).count()

        if unique_prenom > 0:
            erreurs.append("Le prénom existe déjà")

        unique_mail = Users.query.filter(
            db.or_(Users.mail == mail)
        )
        
        if len(erreurs) > 0: 
            return None, erreurs  

        utilisateur = Users(
            mail = mail, 
            prenom=prenom,
            password=generate_password_hash(password)
        )

        try:
            db.session.add(utilisateur)
            db.session.commit()
            return utilisateur, None 
        
        except Exception as erreur:
            return None, [str(erreur)]

    
    @staticmethod    
    def Identification(password, mail): #méthode statique d'identification, on a besoin que du mail et du mot de passe 
 
        utilisateur_mail = Users.query.filter(Users.mail == mail).first()

      
        if utilisateur_mail and check_password_hash(utilisateur_mail.password, password): #on vérifie le mot de passe à partir du mail
            return utilisateur_mail
        else:
            return None

        
