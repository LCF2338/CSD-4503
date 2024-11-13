from flask import Flask, render_template, redirect, url_for, request, flash
from flask_pymongo import MongoClient
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from flask_bootstrap import Bootstrap
from routes import main_routes  # Import the Blueprint from routes.py
# from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'


Bootstrap(app)


# Simple login form using Flask-WTF
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


# Register the Blueprint
app.register_blueprint(main_routes, url_prefix='/api')


# @app.route('/')
# def index():
#     users = db.users.find()
#     return render_template('index.html', users=users)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         # Handle login, e.g., verify user in MongoDB
#         user = db.users.find_one({'username': form.username.data})
#         if user and user['password'] == form.password.data:
#             flash('Login successful!', 'success')
#             return redirect(url_for('index'))
#         flash('Invalid credentials.', 'danger')
#     return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
