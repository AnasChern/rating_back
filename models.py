from sqlalchemy import Column, Integer, Float, String, BLOB, TEXT, Text,  Boolean, ForeignKey, DateTime, create_engine
from sqlalchemy import Column, Integer, String
from database import Base

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema




class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    username = Column(String(100), nullable=False)
    firstname = Column(String(100), nullable=False)
    lastName = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)

    def __repr__(self):
        return str(UsersSchema().dump(self))


    def info(self):
        return UsersSchema().dump(self)

class UsersSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True


class Rating(Base):
    __tablename__ = "rating"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    student_id = Column(Integer)
    score = Column(Float)


    def __repr__(self):
        return str(RatingSchema().dump(self))


    def info(self):
        return RatingSchema().dump(self)



class RatingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Rating
        load_instance = True


