from flask import Flask
from .ext import mysql
from .routes import routes
from .auth import auth
import os
from dotenv import load_dotenv


def create_app():
    app = Flask(__name__)
    load_dotenv()  

    
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
    app.secret_key = os.getenv('SECRET_KEY')

    mysql.init_app(app)

    
    app.register_blueprint(routes)
    app.register_blueprint(auth)

    return app
