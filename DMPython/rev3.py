from ..app import app, db
from datetime import datetime


#Table de relation 

traverse = db.Table(
    "traverse",
    db.Column('courseau', db.String(10), db.ForeignKey('courseau.id'), primary_key=True),
    db.Column('sousdivision_geographique', db.String(10), db.ForeignKey('sousdivision_geographique.id'), primary_key=True)
)


class CoursEau(db.Model):
    __tablename__ = "courseau"

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    denomination = db.Column(db.Text(45), unique = True, nullable = False)
    longueur = db.Column(db.Integer)
    type_id = db.Column(db.Integer)
    derniere_crue_majeure = db.Column(db.Date)
    est_affluent = db.Column(db.Boolean, nullable=False) #la table "Affluence" est remplacée par un booléen : s'il est True alors le Cours d'eau est Affluent, si False il est effluent

    # Propriétés de relation
    typecourseau = db.relationship('TypeCoursEau',  backref='typecourseau',  lazy=True)


    sousdivision_geographique = db.relationship(
    'SousDivision_Geographique',
    secondary="traverse",
    backref=db.backref('cours_eaux', lazy=True)  # Utilisation de 'cours_eaux' comme nom inverse pour l'appeler plus intuitivement
    )

    def __repr__(self): #définir __repr__ permet d'afficher aux personnes utilisant le modèle des information sur l'objet manipulé
        return '<CoursEau %r>' % (self.denomination) 

class TypeCoursEau(db.Model):
    __tablename__ = "typecourseau"

    id = db.Column(db.Integer, primary_key = True)
    label = db.Column(db.String(45), nullable = False)
    commentaire = db.Column(db.Text())

    # Propriétés de relation 

    courseau = db.relationship('CoursEau', backref='courseau', lazy=True)

    def __repr__(self): #définir __repr__ permet d'afficher aux personnes utilisant le modèle des information sur l'objet manipulé
        return '<TypeCoursEau %r>' % (self.label) 


class SousDivision_Geographique(db.Model):
    __tablename__ = "sousdivision_geographique"

    id = db.Column(db.Integer, primary_key = True) #relation par table de relation Traverse
    pays_id = db.Column(db.Integer) #relation avec la table Pays
    type_id = db.Column(db.Integer) #relation avec la table TypeSousDivision
    denomination = db.Column(db.String(45), nullable = False)
    code_officiel = db.Column(db.String(12))

    # Propriétés de relation 


    pays = db.relationship('Pays', backref="pays", lazy = True)
    typesousdivision = db.relationship('TypeSousDivision', backref="typesousdivision", lazy = True)

   
    courseau = db.relationship(
        'courseau',
        secondary = "traverse", 
        backref = db.backref('cours_eaux', lazy=True) #utilisation de 'cours_eaux' pour pouvoir appeler la relation plus facillement
    )

   

class TypeSousDivision(db.Model):
    __tablename__ = "typesousdivision"

    id = db.Column(db.Integer, primary_key = True) #relation avec la table SousDivision_Geographique
    label = db.Column(db.String(45), nullable = False)
    commentaire = db.Column(db.Text())

    # Propriétés de relation

    sousdivision_geographique = db.relationship('SousDivision_Geographique', backref="sousdivision_geographique", lazy=True)

    


class Pays(db.Model):
    __tablename__ = "pays"

    id = db.Column(db.Integer, primary_key = True) #Relation avec SousDivision_Geographique
    denomination = db.Column(db.String(45), nullable = False)

    # Propriétés de relation 

    sousdivision_geographique = db.relationship('SousDivision_Geographique', backref="sousdivision_geographique", lazy=True)