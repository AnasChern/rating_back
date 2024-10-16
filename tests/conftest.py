import pytest
from CRUDs.user_crud import load_user_crud
from CRUDs.rating_crud import load_rating_crud
from CRUDs.login_module import load_login_module_crud
from database import db_session, engine, init_db, drop_db
from models import Users, Rating, Base

from main import create_app

import attributes as atr


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    load_login_module_crud(app, db_session)
    load_user_crud(app, db_session)
    load_rating_crud(app, db_session)

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()