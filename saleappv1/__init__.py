from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
import cloudinary



app =  Flask(__name__)
app.secret_key = '@@@@@##$$EE@@@!122333444555EE$%^&&'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://root:%s@localhost/airdb?charset=utf8mb4' % quote('1954052097Thuy')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['CART_KEY'] = 'cart'

cloudinary.config(cloud_name='dzsri5fco',
           api_key='661911538457193',
           api_secret='3dPUatFpXOgQW-Jkmy6g3nXzUO8')

db = SQLAlchemy(app=app)

login = LoginManager(app=app)