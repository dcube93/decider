from flask import render_template
from app import app, db

# Error handling: Dient dazu eigene Fehler Seiten verwenden.
# Quelle: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500