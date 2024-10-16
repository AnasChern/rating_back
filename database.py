from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import attributes as atr

engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(atr.dbuser, atr.dbpass, atr.dbhost, atr.dbname))
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
Base.query = db_session.query_property()


def init_db():

    Base.metadata.create_all(bind=engine)

def drop_db():

    Base.metadata.drop_all(bind=engine)
