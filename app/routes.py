from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from app.forms import LoginForm, RegistrationForm, DecisionForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Template, Choice
from werkzeug.urls import url_parse
import random

# Startseite
# Quelle: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world & Eigenentwicklung
@app.route('/')
@app.route('/index')
# Der Benutzer muss angemeldet sein um die Seite anzuzeigen.
@login_required
def index():
    form = DecisionForm()
    return render_template('index.html', title='Startseite', form=form)

# Entscheidung basierend auf Vorlage. Vorlage ID wird von vorheriger Webseite via URL übergeben.
# Eigenentwicklung
@app.route('/decide/<templateID>', methods=['POST','GET'])
@login_required
def decide_template(templateID):
    # Abfrage ob Vorlage ID übermittelt wurde.
    if templateID is not None:
        # Vorlage von DB in Variable speichern.
        template = Template.query.get(templateID)
        # Abfrage ob Vorlage von DB in Variable gespeichert wurde. 
        if template is not None:
            # Abfrage ob die Vorlage dem angemeldeten Benutzer gehört.
            if template.user_id == current_user.id:
                # Hohlt alle Auswahlmöglichkeiten der Vorlage aus DB und für deren Wert zur Variable options hinzu.
                temp_options = template.choices.all()
                options = []
                for temp_option in temp_options:
                    options.append(temp_option.value)
                # Ermittelt zufällige Auswahl.
                selection = random.choice(options)
            # Falls die Vorlage nicht dem angemeldeten Benutzer gehört, zurück zur Startseite.
            else:
                return redirect(url_for('index'))
        # Falls kein Vorlage aus der DB in die Variable gespeichert wurde, zurück zur Startseite.
        else:
                return redirect(url_for('index'))
    # Falls keine Vorlagen ID übermittelt wurde, zurück zur Startseite.
    else:
        return redirect(url_for('index'))

    # Übergabe and die HTML WebSeite.
    return render_template('decide_result.html', title='Entscheidung', selection=selection)

# Entscheidung basierend auf Eingabe durch Benutzer.
# Eigenentwicklung
@app.route('/decide', methods=['POST','GET'])
# Der Benutzer muss angemeldet sein um die Seite anzuzeigen.
@login_required
def decide():
    # Die Auswahlmöglichkeiten werden aus der übergebenen Liste extrahiert. Sie sind mittels Zeilenumbruch getrennt.
    options = list(filter(bool, request.form['options'].splitlines()))
    # Ermittelt zufällige Auswahl.
    selection = random.choice(options)
    # Falls ein Namen für eine Vorlage eingegeben wurde, wird dieser hier abgefragt.
    name = request.form['name']
    
    # Falls ein Name übermittelt wurde, wird eine Vorlage erstellt.
    if name != '':
        # Die Daten für die Vorlage (Name und zugehöriger Benutzer) werden abgefüllt.
        t = Template(name=name, owning_u=current_user)
        db.session.add(t)
        
        # Jede Auswahlmöglichkeit wird der Vorlage zugeordned und abgefüllt. 
        for option in options:
            c = Choice(value=option, owning_t=t)
            db.session.add(c)
        
        # Daten werden in die DB geschreiben.
        db.session.commit()
        
        # Meldung an den Benutzer, dass die Vorlage im Profil gespeichert wurde.
        flash('Die Vorlage wurde Ihrem Profil hinzugefügt.')
        
    # Übergabe and die HTML WebSeite.
    return render_template('decide_result.html', title='Entscheidung', selection=selection)

# Profil Seite
# Quelle: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vi-profile-page-and-avatars & Eigenentwicklung
@app.route('/profile')
# Der Benutzer muss angemeldet sein um die Seite anzuzeigen.
@login_required
def profile():
    # Hohlt Daten des Benutzers aus der DB.
    user = User.query.filter_by(username=current_user.username).first_or_404()
    
    # Hohlt Vorlagen des Benutzers aus der DB.
    templates = user.templates.all()
    
    # Übergabe and die HTML WebSeite.
    return render_template('profile.html', title='Profil', user=user, templates=templates)
    
# Login Seite
# Quelle: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Prüft ob Benutzer bereits angemeldet ist. Falls ja, wird er auf die Startseite umgeleitet.
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # Prüft ob Eingaben korrekt sind. Ansonsten wird eine Fehlermeldung ausgegeben.
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    # Übergabe and die HTML WebSeite.
    return render_template('login.html', title='Anmelden', form=form)

# Seite für Abmeldung
# Quelle: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
@app.route('/logout')
def logout():
    # Benutzer wird abgemeldet.
    logout_user()
    # Zur Startseite.
    return redirect(url_for('index'))

# Registrierungs Webseite
# Quelle: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Prüft ob Benutzer bereits angemeldet ist. Falls ja, wird er auf die Startseite umgeleitet.
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Benutzer Registration. Hier wird der Benutzer angelegt.
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # Meldung an den Benutzer, dass der Benutzer registriert wurde.
        flash('Gratulation, Sie sind nun registriert!')
        # Zur Startseite.
        return redirect(url_for('login'))
    # Übergabe and die HTML WebSeite.
    return render_template('register.html', title='Register', form=form)

# API um eigene Vorlagen auszulease
# Eigenentwicklung
@app.route('/API/<Username>', methods=['GET'])
@login_required
def API(Username):
    # Abfrage ob Benutzername übermittelt wurde.
    if Username is not None:
        # Benutzer von DB in Variable speichern.
        U = User.query.filter_by(username=Username).first()
        # Abfrage ob Benutzer von DB in Variable gespeichert wurde. 
        if U is not None:
            # Abfrage ob der Benutzer dem angemeldeten Benutzer entspricht.
            if U.id == current_user.id:
                # Hohlt alle Vorlagen und Auswahlmöglichkeiten DB und fügt deren Werte zur Variable mylist hinzu.
                mylist = list()
                temp_templates = U.templates.all()
                for temp_template in temp_templates:
                    temp_options = temp_template.choices.all()
                    temp_option_list = list()
                    for temp_option in temp_options:
                        temp_option_list.append(temp_option.value)
                    mylist.append( [{'Vorlage:': temp_template.name, 'Auswahlmoeglichkeiten:': temp_option_list}] )
            # Falls die Benutzername nicht dem angemeldeten Benutzer gehört, zurück zur Startseite.
            else:
                return redirect(url_for('index'))
        # Falls kein Benutzer aus der DB in die Variable gespeichert wurde, zurück zur Startseite.
        else:
            return redirect(url_for('index'))
    # Falls keine Benutzername übermittelt wurde, zurück zur Startseite.
    else:
        return redirect(url_for('index'))

    # Übergabe an jsonify.
    return jsonify(str(mylist))