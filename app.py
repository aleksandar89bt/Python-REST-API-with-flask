from datetime import timedelta

from flask import Flask, jsonify
from flask_jwt import JWT
from flask_restful import Api

from resources.item import Item, Items
from resources.store import Store, StoreList
from resources.user import UserRegister
from security import authenticate, identity as identity_function

app = Flask(__name__)
app.secret_key = "AleksandarSecret"
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


# change token endpoint to be /login, default is /auth
app.config['JWT_AUTH_URL_RULE'] = '/login'
# change expiration time of token to half an hour, default is 5 minutes
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
jwt = JWT(app, authenticate, identity_function)


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({"access_token": access_token.decode('utf-8'),
                    "user_id": identity.id})


api.add_resource(Item, "/item/<string:name>")
api.add_resource(Items, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

# This is to disable running the app if some other file runs and inside it is import app.py file
# Only runs app if file app.py is run
if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
