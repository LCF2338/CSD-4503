from bson import ObjectId
from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from database import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

main_routes = Blueprint('main_routes', __name__)


# Simple login form using Flask-WTF
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


# Routes for the frontend templates

@main_routes.route('/')
def index():
    users = db.users.find()
    return render_template('index.html', users=users)


@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Handle login, e.g., verify user in MongoDB
        user = db.users.find_one({'username': form.username.data})
        if user and user['password'] == form.password.data:
            flash('Login successful!', 'success')
            return redirect(url_for('main_routes.index'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html', form=form)
