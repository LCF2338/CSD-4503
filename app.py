from flask import Flask, render_template, redirect, url_for, request, flash

from flask_bootstrap import Bootstrap
from routes.users import users_bp
from routes.decks import decks_bp
from routes.questions import questions_bp
from routes.main import main_routes
# from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'


Bootstrap(app)


# Register blueprints
app.register_blueprint(main_routes)
app.register_blueprint(users_bp, url_prefix='/api')
app.register_blueprint(decks_bp, url_prefix='/api')
app.register_blueprint(questions_bp, url_prefix='/api')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)