from flask import Flask, request, redirect, jsonify
from flask_jwt_extended import jwt_required

from models import Rating, RatingSchema

from models import Users, UsersSchema


def load_rating_crud(application, db_session):
    app = application
    db_session = db_session

    @app.route('/rating', methods=['POST'])
    @jwt_required()
    def add_rating():
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            json_data = request.get_json()
            errors = RatingSchema().validate(json_data, session=db_session)
            print(errors)
            if errors:
                return {"Response": "Missing or incorrect information"}, 400
            else:
                new_rating = RatingSchema().load(json_data, session=db_session)
                db_session.add(new_rating)
                db_session.commit()
                return {"Response": "Created successful"}, 200

        else:
            return {"Response": "Content-Type not supported!"}, 400


    @app.route('/rating/<int:request_id>', methods=['GET'])
    def get_rating_by_id(request_id):
        rating = db_session.query(Rating).filter(Rating.id == request_id).first()
        if rating:
            info = rating.info()
            return jsonify(info), 200
        else:
            return {"Response": "Rating not found"}, 400


    @app.route('/rating/<int:request_id>', methods=['PUT', 'DELETE'])
    @jwt_required()
    def ud_rating(request_id):
        content_type = request.headers.get('Content-Type')
        rating = db_session.query(Rating).filter(Rating.id == request_id).first()
        if rating:
            if request.method == 'DELETE':
                db_session.delete(rating)
                db_session.commit()
                return {"Response": "Successfully deleted"}, 200
            else:
                if content_type == 'application/json':
                    json_data = request.get_json()
                    errors = RatingSchema().validate(json_data, session=db_session)
                    if errors:
                        return {
                                   "Response": "Missing or incorrect information"
                               }, 400
                    else:
                        db_session.query(Rating). \
                            filter(Rating.id == rating.id). \
                            update(json_data)
                        db_session.commit()
                        return {"Response": "Updated successful"}, 200
                else:
                    return {"Response": "Wrong content type supplied, JSON expected"}, 400
        else:
            return {"Response": "Rating not found"}, 400

    @app.route('/ratings', methods=['GET'])
    def get_ratings():
        content_type = request.headers.get('Content-Type')

        # Витягуємо всіх користувачів
        ratings = db_session.query(Rating).all()

        if ratings:
            if request.method == 'GET':
                # Ручне перетворення кожного користувача на словник
                ratings_list = []
                for rating in ratings:
                    rating_dict = {column.name: getattr(rating, column.name) for column in rating.__table__.columns}
                    ratings_list.append(rating_dict)
                return jsonify(ratings_list), 200
        else:
            return {"Response": "Rating not found"}, 400