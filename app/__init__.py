#!/usr/bin/env python
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir
from app import views, models




app = Flask(__name__)
app.config.from_object('config')		#Needed when there is a config.py file in root, that is used for CSRF_ENABLED
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

oid = OpenID(app,os.path.join(basedir, 'tmp'))


