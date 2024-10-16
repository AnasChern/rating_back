from flask import Flask
from flask_cors import CORS
import attributes as atr
from user_crud import load_user_crud
from rating_crud import load_rating_crud
from login_module import load_login_module_crud

from database import db_session, init_db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    CORS(app, resources={r"/*": {
        "origins": "*",
        "allow_headers": ["Content-Type", "Authorization"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    }})
    return app

app = create_app()

conn = 'mysql+pymysql://{}:{}@{}/{}'.format(atr.dbuser, atr.dbpass, atr.dbhost, atr.dbname)
app.config['SQLALCHEMY_DATABASE_URI'] = conn

if __name__ == "__main__":
    load_user_crud(app, db_session)
    load_rating_crud(app, db_session)
    load_login_module_crud(app, db_session)

    app.run()
