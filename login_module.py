from database import db_session
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_json import FlaskJSON
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, current_user, get_jwt_identity

from models import Users


def load_login_module_crud(application, database):
    app = application
    db = database

    FlaskJSON(app)
    bcryptor = Bcrypt(app)

    jwt = JWTManager(app)

    @app.route('/login', methods=['POST'])
    def login():
        if request.is_json:
            username = request.json['username']
            password = request.json['password']
        else:
            return {"Response": "Not JSON data"}, 400

        test = db_session.query(Users).filter_by(username=username).first()
        if test and bcryptor.check_password_hash(test.password, password):
            access_token = create_access_token(identity=test.id)
            return jsonify(message='Login Success', access_token=access_token, userid=test.id)
        else:
            return jsonify('Bad username or Password'), 401

    @app.route('/protected')
    @jwt_required()
    def protected():
        return {"Response": "You got access to protected address " + str(get_jwt_identity())}, 200

    @app.route('/', methods=['GET'])
    def home():
        return {"Title": "Home page"}, 200
