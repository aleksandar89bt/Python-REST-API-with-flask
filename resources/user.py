import sqlite3

from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username')
    parser.add_argument('password')

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User with this username already exists"}, 409

        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User was created"}, 201
