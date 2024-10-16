from database import db_session
from flask import Flask, request, redirect, abort, jsonify
from flask_bcrypt import Bcrypt
from flask_expects_json import expects_json
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Users, UsersSchema


def check_existing(username):
    existing_username = db_session.query(Users) \
        .filter(Users.username == username) \
        .first()
    if existing_username:
        return True
    else:
        return False


def load_user_crud(application, db_session):
    app = application
    db_session = db_session

    bcryptor = Bcrypt(app)




    @app.route('/user', methods=['POST'])  # add admin
    def add_user():
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            json_data = request.get_json()
            errors = UsersSchema().validate(json_data, session=db_session)
            if errors:
                print(errors)
                return {"Response": "Missing or incorrect information"}, 400
            elif check_existing(json_data["username"]):
                return {"Response": "Username already exists"}, 400
            else:
                hashed_password = bcryptor.generate_password_hash(json_data['password'])
                json_data["password"] = hashed_password
                new_admin = UsersSchema().load(json_data, session=db_session)
                db_session.add(new_admin)
                db_session.commit()
                return {"Response": "Created successful"}, 200
        else:
            return {"Response": 'Content-Type not supported!'}, 400

    @app.route('/user/<int:request_id>', methods=['GET', 'PUT', 'DELETE'])  # RUD admin for testing
    @jwt_required()
    def rud_admin(request_id):
        if (request_id) != get_jwt_identity():
            return {"Response": "You don't have permission to change this user info"}, 401

        content_type = request.headers.get('Content-Type')
        user = db_session.query(Users).filter(Users.id == request_id).first()
        if user:
            if request.method == 'GET':
                return jsonify(user.info()), 200
            elif request.method == 'DELETE':
                db_session.delete(user)
                db_session.commit()
                return {"Response": "Delete successful"}, 200
            else:
                if content_type == 'application/json':
                    json_data = request.get_json()
                    errors = UsersSchema().validate(json_data, session=db_session)
                    if errors:
                        print(errors)
                        return {
                                   "Response": "Missing or incorrect information"
                               }, 400
                    else:
                        new_password = bcryptor.generate_password_hash(json_data['password'])
                        # new_password = (json_data['password'])
                        json_data["password"] = new_password

                        db_session.query(Users). \
                            filter(Users.id == user.id). \
                            update(json_data)

                        db_session.commit()
                        return {"Response": "Updated successful"}, 200
                else:
                    return {"Response": "Wrong content type supplied, JSON expected"}, 400
        else:
            return {"Response": "User not found"}, 400


    @app.route('/users', methods=['GET'])
    def get_users():
        content_type = request.headers.get('Content-Type')
        # Витягуємо всіх користувачів
        users = db_session.query(Users).all()
        if users:
            if request.method == 'GET':
                # Ручне перетворення кожного користувача на словник
                users_list = []
                for user in users:
                    user_dict = {column.name: getattr(user, column.name) for column in user.__table__.columns}
                    users_list.append(user_dict)
                return jsonify(users_list), 200
        else:
            return {"Response": "User not found"}, 400
