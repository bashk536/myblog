from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm

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

@app.route('/login', methods = ['GET', 'POST']) #Default is GET
def login():
    form = LoginForm()
    if form.validate_on_submit():   #processes all form data, returns True upon succesful processing
        ####### Error messages stored in flash() gets wiped out after calling it once ########
        flash('Login requested for user {}, remember_me={}'.format (    #flash error message to user
            form.username.data, form.rememberMe.data ))
        return redirect( url_for('index') )
    return render_template('login.html', title = 'Login Page', form = form)

