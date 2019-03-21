from .. app import db


Jointure_Saint_Oeuvre= db.Table('Jointure_Saint_Oeuvre',
                          db.Column('Oeuvre_IdOeuvre', db.Integer, db.ForeignKey('oeuvre.IdOeuvre'), primary_key=True),
                          db.Column('Saint_IdSaint', db.Integer, db.ForeignKey('saint.IdSaint'),primary_key=True))

Jointure_Manuscrit_Realisation=db.Table('Jointure_Manuscrit_Realisation',
                                        db.Column('Manuscrit_IdManuscrit',db.Integer, db.ForeignKey('Manuscrit.IdManuscrit'),primary_key=True),
                                        db.Column('Realisation_IdRealisation',db.Integer,db.ForeignKey('Realisation.IdRealisation'),primary_key=True))
Jointure_Oeuvre_Realisation=db.Table('Jointure_Oeuvre_Realisation',
                                     db.Column('Realisation_IdRealisation',db.Integer,db.ForeignKey('Realisation.IdRealisation'),primary_key=True),
                                     db.Column('Oeuvre_IdOeuvre',db.Integer,db.ForeignKey('Oeuvre.IdOeuvre'),primary_key=True))
# On crée notre modèle
class Oeuvre(db.Model):
#Création de la classe centrale oeuvre
    __tablename__="oeuvre"
    IdOeuvre = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    Titre = db.Column(db.Text)
    Auteur=db.Column(db.Text)
    Langue=db.Column(db.Text)
    Incipit=db.Column(db.Text)
    Excipit=db.Column(db.Text)
    Lien_site = db.Column(db.Text)
    Folios=db.Column(db.Text)
    saints = db.relationship('Saint', secondary=Jointure_Saint_Oeuvre, backref='oeuvres')

class Saint(db.Model):
    __tablename__ = "saint"
    IdSaint = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    Nom_saint=db.Column(db.Text)
    Biographie=db.Column(db.Text)
    oeuvre = db.relationship('Oeuvre', secondary=Jointure_Saint_Oeuvre, backref='saint')

class Institution(db.Model):
    __tablename__="institution"
    IdInstitution=db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    Nom_institution=db.Column(db.Text)
    Localisation_IdLocalisation= db.Column(db.Integer, db.ForeignKey('Localisation.IdLocalisation'))

class Manuscrit(db.Model):
    __tablename__="manuscrit"
    IdManuscrit=db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    Cote=db.Column(db.Text)
    Titre=db.Column(db.Text)
    Nb_feuillets=db.Column(db.Integer)
    Provenance=db.Column(db.Text)
    Support=db.Column(db.Text)
    Hauteur=db.Column(db.Text)
    Largeur=db.Column(db.Text)
    Institution_IdInstitution= db.Column(db.Integer, db.ForeignKey('Localisation.IdLocalisation'))

class Realisation (db.Model):
    __tablename__="realisation"
    IdRealisation=db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    Date_production=db.Column(db.Text)
    Lieu_production=db.Column(db.Text)
    Copiste=db.Column(db.Text)

class Images_numeriques (db.Model):
    _tablename__="images_numeriques"
    IdImage=db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    Lien_ark_gallica=db.Column(db.TEXT)
    Legende_image=db.Column(db.TEXT)
    IdOeuvre=db.Column(db.Integer, db.ForeignKey('Oeuvre.IdOeuvre'))

class Localisation (db.Model):
    __tablename="localisation"
    IdLocalisation=db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    Ville=db.Column(db.TEXT)

class User (db.Model) :
    __tablename = "user"
    user_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    user_nom = db.Column(db.TEXT)
    user_login = db.Column(db.TEXT)
    user_email = db.Column(db.TEXT)
    user_password = db.Column(db.TEXT)
    authorships = db.Column(db.TEXT)