from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, Table, Column, Integer, String, relationship
from ..app import app, db






class user(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True) 
    # Définition d'une colonne 'id' dans la table 'user' avec le type 'String'  et étant la clé primaire de la table.
    user_name = db.Column(db.String(45))
    # Définition d'une colonne 'name' dans la table 'user' avec le type 'String' pouvant contenir 45 caractères maximum .
    user_firstname = db.Column(db.String(45))
    user_surname = db.Column(db.String(45))
    user_mail = db.Column(db.Text)
    user_password_hash = db.Column(db.Text)
    user_birthyear = db.Column(db.Integer)
    user_promotion_date = db.Column(db.String(45))
    user_description = db.Column(db.Text)
    user_last_seen = db.Column(db.DateTime)
    user_linkedin = db.Column(db.Text)
    user_github = db.Column(db.Text)
    user_inscription_date = db.Column(db.DateTime)



    #relations 

    
   
    # Syntaxe : [table] = relationship('[Nom module de la table'], back_populate = '[relation inverse : donc on indique le nom qu'on a défini dans l'autre table]')
    cv = relationship('CV', back_populate = 'user')
     # la table CV est en relation avec la table user [on définira la relation 'inverse' dans le module followers]
    post = relationship('Post', back_populate = 'user')
    comment = relationship('Comment', back_populate = 'user')
    message = relationship('Message', back_populate = 'expediteur', foreign_keys='Message.expediteur_id')
    #dans le cas de la table message, qui a deux relations avec la table user : il faut préciser (en  plus) les clés étrangères concernées ce sera pareil pour followers
    message = relationship('Message', back_populate = 'destinataire', foreign_keys ='Message.destinataire_id')
    followers = relationship('Followers', back_populate = 'follower', foreign_keys = 'Followers.follower_id') 
    followers = relationship('Followers', back_populate = 'followed', foreign_keys = 'Followers.followed_id')
    skills = relationship('Skills', back_populate = 'user')

class Followers(db.Model):
    __tablename__ = 'followers'
    follower_id = db.Column(db.Integer, ForeignKey('user.id') )
    #La clé primaire est la clé id de la table user
    followed_id = db.Column(db.Integer, ForeignKey('user.id'))
    #La clé primaire est la clé id de la table user

    user = relationship('User', back_populate = 'follower', foreign_keys = 'user.id')
    user = relationship('User', back_populate = 'followed', foreign_keys = 'user.id')
    

class CV(db.Model):
    __tablename__='CV'

    cv_id = db.Column(db.Integer, primary_key=True)
    cv_nom_poste = db.Column(db.Text)
    cv_nom_employeur = db.Column(db.Text)
    cv_ville = db.Column(db.String(45))
    cv_annee_debut = db.Column(db.Integer)
    cv_annee_fin = db.Column(db.Integer)
    cv_description_poste = db.Column(db.Text)
    cv_utilisateur_id = db.Column(db.Integer, ForeignKey('user.id'))
    #La clé primaire est la clé id de la table user


    user = relationship('User', back_populate = 'cv')

class Post(db.Model):
    __tablename__ = 'post'

    post_id = db.Column(db.Integer, primary_key = True)
    post_titre = db.Column(db.String(45))
    post_message = db.Column(db.Text)
    post_date = db.Column(db.DateTime)
    post_indentation = db.Column(db.String(45))
    html = db.Column(db.Text)
    post_auteur_id = db.Column(db.Integer, ForeignKey('user.id')) 
    #La clé primaire est la clé id de la table user




    user = relationship('User', back_populate = 'post')
    comment = relationship('Comment', back_populate = 'comment')

class Comment(db.Model):
    __tablename__ = 'comment'

    comment_id = db.Column(db.Integer, primary_key = True)
    comment_message = db.Column(db.Text)
    comment_html = db.Column(db.Text)
    comment_date = db.Column(db.DateTime)
    comment_post = db.Column(db.Integer, ForeignKey('post.post_id'))
    #la clé primaire est la clé post_id de la table Post
    comment_auteur = db.Column(db.Integer, ForeignKey('user.id'))
    #la clé primaire est la clé id de la table user




    post = relationship('Post', back_populate = 'comment')
    user = relationship('User', back_populate = 'comment')


class Message(db.Model):
    __tablename__ = 'message'

    message_id = db.Column(db.Integer, primary_key = True)
    message_message = db.Column(db.Text)
    message_html = db.Column(db.Text)
    message_date = db.Column(db.DateTime)
    message_expediteur = db.Column(db.Integer, ForeignKey('user.id'))
    #la clé primaire est la clé id de la table user
    message_destinataire = db.Column(db.Integer, ForeignKey('user.id'))
    #la clé primaire est la clé id de la table user




    user = relationship('User', back_populate = 'expediteur', foreign_keys='Message.expediteur_id')
    user = relationship('User', back_populate = 'destinataire', foreign_keys='Message.destinataire_id')


class Skills(db.Model):
    __tablename__= 'skills'
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    #la clé primaire est la clé id de la table user
    competence_id = db.Column(db.Integer, ForeignKey('user.id'))
    #la clé primaire est la clé competence_id de la table compétence 


    user = relationship('User', back_populate = 'skills')

    competence = relationship('Competence', back_populate = 'skills')

class Competence(db.Model):
    __tablename__ = 'competences'

    competence_id = db.Column(db.Integer, primary_key = True )
    competence_label = db.Column(db.String(45))



    skills = relationship('Skills', back_populate = 'competence')

