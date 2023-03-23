from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

# Login Form: Hier werden die Felder und Buttons sowie deren Attribute definiert.
# Quelle: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
class LoginForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Anmeldung')
    
# Registrierung Form: Hier werden die Felder und Buttons sowie deren Attribute definiert.
# Quelle: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
class RegistrationForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    password2 = PasswordField(
        'Wiederholung Passwort', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registriere mich')

    # Validierung des Benutzernamens (muss Einzigartig sein).
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    # Validierung der E-Mail (muss Einzigartig sein).
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
    
# Entscheidungs Form: Hier werden die Felder und Buttons sowie deren Attribute definiert.
# Eigenentwicklung
class DecisionForm(FlaskForm):
    # Name der Vorlage. Nicht erzwungen, da falls leer keine Vorlage erstellt wird.
    name = StringField('TemplateName')
    # Auswahlmöglichkeiten für die Entscheidung. TextFeld welches mehere Zeilen unterstützt. Eine Eingabe ist nötig um fortzufahren.
    options = TextAreaField('Options', validators=[DataRequired()])
    submit = SubmitField('Entscheide für mich')

"""    
class ResultForm(FlaskForm):
    name = StringField('TemplateName')
    submit = SubmitField('Continue')
"""
