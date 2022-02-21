from flask_restful import Resource, reqparse
import sqlite3
from models.user import Usermodel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required = True,
        help = "This feild cannot be blank "
    )
    parser.add_argument('password',
        type = str,
        required = True,
        help = "This feild cannot be blank"
    )
    def post(self):
        data = UserRegister.parser.parse_args()

        if Usermodel.find_by_username(data['username']):
            return {"message": "A user with that that username already exist"}, 400
         
        user = Usermodel(**data)
        user.save_to_db()

        return {"message": "user created successfully."}, 201

        