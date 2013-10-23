#!/usr/bin/env python

from flask.ext.wtf import Form, TextField, BooleanField 
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class LoginForm(Form):
	openid = TextField('openid', validators = [Required()])
	remember_me = BooleanField('remember_me', default = False)