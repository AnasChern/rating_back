import models
from database import db_session
from flask_jwt_extended import create_access_token



def test_rating_post(client):
    with client:
        response = client.get("/")
        access_token = create_access_token('testuser')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = client.post("/rating", headers=headers, json={"student_id": 2,
                                                                 "score": 4})
        assert response.status_code == 200
        
def test_rating_get(client):
    with client:
        response = client.get("/")
        lst_row = (
            (db_session.query(models.Rating).order_by(models.Rating.id.desc()).first()).id)
        access_token = create_access_token(identity= lst_row)
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = client.get(f"/rating/{lst_row}", headers=headers)
        assert response.status_code == 200



def test_rating_get_wrong_id_type(client):
    with client:
        response = client.get("/")
        access_token = create_access_token('testuser')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = client.get("/rating/-1", headers=headers)
        assert response.status_code == 404


def test_rating_get_wrong_id(client):
    with client:
        response = client.get("/")
        access_token = create_access_token('testuser')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = client.get("/rating/9999", headers=headers)
        assert response.status_code == 400

def test_rating_post_wrong_content_type(client):
    with client:
        response = client.get("/")
        access_token = create_access_token('testuser')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = client.post("/rating", headers=headers)
        assert response.status_code == 400


def test_rating_put(client):
    with client:
        response = client.get("/")
        access_token = create_access_token('testuser')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        lst_row = (
            db_session.query(models.Rating).order_by(models.Rating.id.desc()).first()).id
        response = client.put(f"/rating/{lst_row}", headers=headers, json={"student_id": 2,
                                                                           "score": 3})
        assert response.status_code == 200

def test_rating_put_wrong_type(client):
    with client:
        response = client.get("/")
        access_token = create_access_token('testuser')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        lst_row = (
            db_session.query(models.Rating).order_by(models.Rating.id.desc()).first()).id 
        response = client.put(f"/rating/{lst_row}", headers=headers)
        assert response.status_code == 400


def test_rating_put_wrong_id(client):
    with client:
        response = client.get("/")
        access_token = create_access_token('testuser')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = client.put("/rating/9999", headers=headers)
        assert response.status_code == 400


def test_rating_del(client):
    with client:
        response = client.get("/")
        lst_row = (
            db_session.query(models.Rating).order_by(models.Rating.id.desc()).first()).id
        access_token = create_access_token(identity=lst_row)
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = client.delete(f"/rating/{lst_row}", headers=headers)
        assert response.status_code == 200
