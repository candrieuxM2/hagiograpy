from flask import render_template

from .app import app
from .modeles.donnees import Oeuvre, Saint, Manuscrit, Realisation, Localisation, Institution
from .modeles.utilisateurs import User
from .constantes import RESULTS_PER_PAGE
from flask_login import login_user, current_user, logout_user
from flask import flash, redirect, request
from sqlalchemy import or_


@app.route("/")
def accueil():
    oeuvres = Oeuvre.query.all()
    return render_template("pages/accueil.html", nom="Site", oeuvres=oeuvres)

@app.route("/oeuvre/<int:vie_id>")
def oeuvre(vie_id):

    """Création d'une page pour une vie de Saint
    :param vie_id: Id de la vie clé primaire de la table oeuvre dans la base de données
    :type vie_id: texte
    :returns: création de page
    :rtype: page HTML de la vie souhaitée"""

    unique_vie=Oeuvre.query.filter(Oeuvre.IdOeuvre==vie_id).first()
    # On fait la requête sur la table Saint mais on l'a filtre en récupérant dans la base à travers la relation oeuvres
    # n'importe qu'elle valeur dont Oeuvre.idOeuvre correspond à la valeur d'entrée
    saint_vie1 = Saint.query.filter(Saint.oeuvres.any(Oeuvre.IdOeuvre == vie_id)).first()
    saint_vie2 = Saint.query.filter(Saint.oeuvres.any(Oeuvre.IdOeuvre == vie_id)).all()
    return render_template("pages/vie.html", nom="Site", oeuvre=unique_vie, saints=saint_vie2,saint=saint_vie1)


@app.route('/rechercheavancee')
def rechercheavancee():
    """Route permettant de créer le formulaire de recherche avancée"""
    saint = Saint.query.order_by(Saint.Nom_saint).all()
    texte = Oeuvre.query.order_by(Oeuvre.Titre).all()
    cote = Manuscrit.query.order_by(Manuscrit.Cote).all()
    institution = Institution.query.order_by(Institution.Nom_institution).all()
    ville = Localisation.query.order_by(Localisation.Ville).all()
    date_prod = Realisation.query.order_by(Realisation.Date_production).all()
    lieu_prod = Realisation.query.order_by(Realisation.Lieu_production).all()
    # Les variables ci-dessus permettent de stocker les valeurs des tables concernées,
    # ce qui nous permet par la suite de les faire apparaître dans des menus déroulants dans notre page recherche.html
    return render_template("pages/rechercheavancee.html", saint=saint, texte=texte, cote=cote, institution=institution, ville=ville, date_prod=date_prod, lieu_prod=lieu_prod)




@app.route("/register", methods=["GET", "POST"])
def inscription():
    """ Route gérant les inscriptions
    """
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        statut, donnees = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if statut is True:
            flash("Enregistrement effectué. Identifiez-vous maintenant", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")


@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """ Route gérant les connexions
    """
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté-e", "info")
        return redirect("/")
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        utilisateur = User.identification(
            login=request.form.get("login", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if utilisateur:
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect("/")
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")
    return render_template("pages/connexion.html")


@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté-e", "info")
    return redirect("/")