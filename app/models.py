from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    templates = db.relationship('Template', backref='author', lazy='dynamic') #change author? --> owning_u

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#    choices = db.relationship('Choice', backref='author', lazy='dynamic') #change author? --> owning_t
    
    def __repr__(self):
        return '<Template {}>'.format(self.name)
    
#class Choice(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    value = db.Column(db.String(128), index=True)
#    template_id = db.Column(db.Integer, db.ForeignKey('template.id'))
#
#    def __repr__(self):
#        return '<Choice {}>'.format(self.value)