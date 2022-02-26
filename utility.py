import os
import re
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate,identity
from resources.user import UserRegister
from resources.item import Item,itemlist
from resources.store import Store, Storelist

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] =os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL?sslmode=require').replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity) #/auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(itemlist, '/items')
api.add_resource(Storelist, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port = 5000, debug= True)

