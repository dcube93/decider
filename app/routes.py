from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, DecisionForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
import random

@app.route('/')
@app.route('/index')
@login_required
def index():
    form = DecisionForm()
    return render_template('index.html', title='Home', form=form)#, user=user, posts=posts)

@app.route('/decide', methods=['POST'])
@login_required
def decide():
    #options = request.form['options'].split(',')
    options = list(filter(bool, request.form['options'].splitlines()))
    selection = random.choice(options)
    return render_template('decide_result.html', selection=selection)
    
    """""
    options = []
    for key, value in request.form.items():
        if key.startswith('option-'):
            options.append(value)
    selection = random.choice(options)
    return render_template('decide_result.html', selection=selection)
    """
@app.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    return render_template('profile.html', user=user)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)