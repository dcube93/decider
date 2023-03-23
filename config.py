import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Hier werden Konfigurations Objekte definiert.
# Quelle: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
# Quelle: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False