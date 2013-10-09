#!/usr/bin/env python
from app import app, db, lm, oid
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user,logout_user, current_user, login_required
from models import User, ROLE_USER, ROLE_ADMIN
from forms import LoginForm
import sys

@app.route('/')
@app.route('/index')
@login_required
def index():
	user = g.user
	#user = { 'nickname': 'GuitarNinja' }
	posts = [ #fake array of posts
		{
				'author' : {'nickname': 'John'},
				'body' : 'Beautiful day in the Bay Area'
			},
			{
				'author': {'nickname': 'Susan'},
				'body' : 'The Matrix movies were cool'
			}
	]
	return render_template("index.html",
		title = 'Home',
		user = user,
		posts = posts)
	
	
@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler									#Tells Flask-OpenID that this is the login view function
def login():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
		#flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
		#return redirect('/index')
	return render_template('login.html',
		title = 'Sign In',
		form = form,
		providers = app.config['OPENID_PROVIDERS'])
		
@lm.user_loader
def load_user(id):
	return User.query.get(int(id))


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))
	
	
@app.before_request
def before_request():
	g.user = current_user