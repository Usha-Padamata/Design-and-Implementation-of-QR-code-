from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_mail import Mail,Message

db =SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)#initializing the flask
    app.config['SECRET_KEY'] = "asdfgasdfj ghjkjhgfdfghj"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)
    app.config['MAIL_SERVER'] ='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = "maddi.kundana3@gmail.com"
    app.config['MAIL_PASSWORD'] = "bsii mhgh uohq ijgw"
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True


    mail=Mail(app)


    from .views import views # here '.views' means views.py file and 'views' means name of the blueprint in views.py
    from .auth import auth  

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth,url_prefix = '/')

    from .models import User,Note

    #create_database(app)

    return app

'''def create_database(app):
    if not path.exists('website/'+ DB_NAME):
        db.create_all(app=app)
        print("Created Database")'''
