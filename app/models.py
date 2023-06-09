from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

# Benutzer Klasse: Hier werden die Definitionen und die Datenbank Struktur der Klasse definiert.
# Quelle: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
# Quelle: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vi-profile-page-and-avatars
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    templates = db.relationship('Template', backref='owning_u', lazy='dynamic') # Eigenenwicklung

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=robohash&s={}'.format(digest, size)

# Vorlage Klasse: Hier wird die Datenbank Struktur der Klasse definiert
# Eigenentwicklung
class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    choices = db.relationship('Choice', backref='owning_t', lazy='dynamic')
    
    def __repr__(self):
        return '<Template {}>'.format(self.name)

# Auswahlmöglichkeiten Klasse: Hier wird die Datenbank Struktur der Klasse definiert
# Eigenentwicklung
class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(128), index=True)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'))

    def __repr__(self):
        return '<Choice {}>'.format(self.value)
    
# Benutzer Loader funktion
# Quelle: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
@login.user_loader
def load_user(id):
    return User.query.get(int(id))