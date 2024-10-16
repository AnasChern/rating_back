import models
from CRUDs.user_crud import check_existing
from database import db_session
from flask_jwt_extended import create_access_token


def test_user_get(client):
    with client:
        response = client.get("/")
        lst_row = (
            (db_session.query(models.Users).order_by(models.Users.id.desc()).first()).id)
        access_token = create_access_token(identity=lst_row)
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = client.get(f"/user/{lst_row}", headers=headers)
        assert response.status_code == 200


def test_user_post(client):
    with client:
        response = client.get("/")
        access_token = create_access_token('testuser')

        response = client.post("/user", json={"username": "rtyujjjd",
                                              "firstname": "Anastasiia",
                                              "lastName": "Cher",
                                              "email": "ana@gmail.com",
                                              "password": "pass1234",
                                              "phone": "0987576722",
                                              "role":"student"
                                               })
        assert response.status_code == 200



def test_user_post_errors(client):
    with client:
        response = client.get("/")
        access_token = create_access_token('testuser')

        response = client.post("/user", json={"firstasdasdname": "Anastasiia"})
        
        assert response.status_code == 400


def test_user_post_username_exists(client):
    with client:
        response = client.get("/")
        access_token = create_access_token('testuser')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = client.post("/user", headers=headers, json={"usersname": "TheStudentfg",
                                                               "firstname": "Anastasiia",
                                                               "lastName": "Cher",
                                                               "email": "ana@gmail.com",
                                                               "password": "pass1234",
                                                               "phone": "0987576722",
                                                               "role": "student"
                                                               })
        assert response.status_code == 400


def test_user_post_wrong_format(client):

    with client:
        response = client.get("/")
        access_token = create_access_token('testuser')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = client.post("/user", headers=headers)
        assert response.status_code == 400


def test_existing_username(client):
    with client:
        response = client.get("/")
        res = check_existing("hsdguh408340+++/*/-/*-/-*/-*/asdadasd")
        assert res == False
        res = check_existing("rtyujjjd")
        assert res == True



def test_user_get_wrong_id(client):

    with client:
        response = client.get("/")
        lst_row = (
            (db_session.query(models.Users).order_by(models.Users.id.desc()).first()).id)  # get last inserted row
        access_token = create_access_token(identity=lst_row)
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = client.get(f"/user/{lst_row + 1}", headers=headers)
        assert response.status_code == 401


def test_user_put(client):

    with client:
        response = client.get("/")
        lst_row = (
            (db_session.query(models.Users).order_by(models.Users.id.desc()).first()).id)  # get last inserted row
        access_token = create_access_token(identity=lst_row)
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = client.put(f"/user/{lst_row}", headers=headers, json={"username": "TheStudentfg",
                                                                         "firstname": "Anastasiia",
                                                                         "lastName": "Cher",
                                                                         "email": "ana@gmail.com",
                                                                         "password": "pass1234",
                                                                         "phone": "0987576722",
                                                                         "role": "student"
                                                                         })
        assert response.status_code == 200


def test_user_put_wrong_fields(client):
    with client:
        response = client.get("/")
        lst_row = (
            (db_session.query(models.Users).order_by(models.Users.id.desc()).first()).id)  # get last inserted row
        access_token = create_access_token(identity=lst_row)
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = client.put(f"/user/{lst_row}", headers=headers, json={
            "firstname": "Anastasiia"})
        assert response.status_code == 400


def test_user_put_not_json(client):
    with client:
        response = client.get("/")
        lst_row = (
            (db_session.query(models.Users).order_by(models.Users.id.desc()).first()).id)  # get last inserted row
        access_token = create_access_token(identity=lst_row)
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = client.put(f"/user/{lst_row}", headers=headers)
        assert response.status_code == 400


def test_user_del(client):
    with client:
        response = client.get("/")
        lst_row = (
            (db_session.query(models.Users).order_by(models.Users.id.desc()).first()).id)  # get last inserted row
        access_token = create_access_token(identity=lst_row)
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }

        response = client.delete(f"/user/{lst_row}", headers=headers)
        assert response.status_code == 200


def test_user_put_after_deletion_of_user(client):
    with client:
        response = client.get("/")
        access_token = create_access_token('testuser')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = client.post("/user", headers=headers, json={"username": "TheStudent2",
                                                               "firstname": "Mary",
                                                               "lastName": "Rock",
                                                               "email": "mary@gmail.com",
                                                               "password": "pass1234",
                                                               "phone": "0987576722",
                                                               "role": "student"
                                                               })
        assert response.status_code == 200

        lst_row = (
            (db_session.query(models.Users).order_by(models.Users.id.desc()).first()).id)  # get last inserted row
        access_token = create_access_token(identity=lst_row)
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = client.delete(f"/user/{lst_row}", headers=headers)
        assert response.status_code == 200

        response = client.put(f"/user/{lst_row}", headers=headers, json={"username": "TheStu2",
                                                                         "firstname": "Mary",
                                                                         "lastName": "Rock",
                                                                         "email": "mary@gmail.com",
                                                                         "password": "pass1234",
                                                                         "phone": "0987576722",
                                                                         "role": "student"
                                                                         })
        assert response.status_code == 400
