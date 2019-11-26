from flask_wtf import FlaskForm #FlaskForm is a base form class
from wtforms import StringField, PasswordField, BooleanField, SubmitField
# For each field, an object is created as a class variable in the LoginForm(forms.py) class,
# First argument is a label/description
# Second argument is validators(make sure textfield is not empty, etc)
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("User Name", validators=[DataRequired()])
    password = PasswordField("Password", validators= [DataRequired()])
    rememberMe = BooleanField("Remember Me?")
    submit = SubmitField("Sign In")
