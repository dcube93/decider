from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, DecisionForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Template, Choice
from werkzeug.urls import url_parse
import random

@app.route('/')
@app.route('/index')
@login_required
def index():
    form = DecisionForm()
    return render_template('index.html', title='Home', form=form)

@app.route('/decide/<templateID>', methods=['POST','GET'])
@login_required
def decide_template(templateID):
    #templateID = request.args.get("id")
    if templateID is not None:
        template = Template.query.get(templateID)
        if template is not None:
            if template.user_id == current_user.id:
                temp_options = template.choices.all()
                options = []
                for temp_option in temp_options:
                    options.append(temp_option.value)
                selection = random.choice(options)
            else:
                #back to index
                return redirect(url_for('index'))
        else:
                #back to index
                return redirect(url_for('index'))
    else:
        #options = list(filter(bool, request.form['options'].splitlines()))
        #flash(options)
        return redirect(url_for('index'))

    
    
    return render_template('decide_result.html', selection=selection, options=options)

@app.route('/decide', methods=['POST','GET'])
@login_required
def decide():
    """"
    templateID = request.args.get("id")
    if templateID is not None:
        template = Template.query.get(templateID)
        if template.user_id == current_user.id:
            temp_options = template.choices.all()
            options = []
            for temp_option in temp_options:
                options.append(temp_option.value)
            flash(options)
        else:
            #back to index
            return redirect(url_for('index'))
    else:
        options = list(filter(bool, request.form['options'].splitlines()))
        flash(options)
    """
    options = list(filter(bool, request.form['options'].splitlines()))
    selection = random.choice(options)
    flash(selection)
    name = request.form['name']
    
    if name is not None:
        t = Template(name=name, owning_u=current_user)
        db.session.add(t)
        
        for option in options:
            c = Choice(value=option, owning_t=t)
            db.session.add(c)
        
        db.session.commit()
        flash('Template saved to profile.')
    
    return render_template('decide_result.html', selection=selection, options=options, name=name)

@app.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    templates = user.templates.all()
    return render_template('profile.html', user=user, templates=templates)
    
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