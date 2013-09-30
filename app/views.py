from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
	user = { 'nickname': 'GuitarNinja' }
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
	