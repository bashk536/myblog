from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Bash'}
    posts = [
        { 
            'author': {'username': 'Adam'},
            'body': 'Beautiful day in Portland'
        },
        
        {
            'author': {'username': 'David'},
            'body': "Yay, I'm married now!"
        }
    ]
    return render_template('index.html', user= user, posts = posts)
