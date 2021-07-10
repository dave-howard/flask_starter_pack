import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from flask_login import UserMixin, AnonymousUserMixin

from flaskr import app
basedir = os.path.abspath(os.path.dirname(__file__))
db_file_name = "flask_database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, db_file_name)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


def session():
    return db.session


class User(db.Model, UserMixin):
    user_id = Column(Integer(), primary_key=True)
    user_name = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255))
    role = Column(String(255))
    status = Column(String(255))

    @property
    def id(self):
        return self.user_id

    @staticmethod
    def get_by_id(user_id: int):
        return session().query(User).filter_by(user_id=user_id).first()

    @staticmethod
    def get_by_user_name(user_name: str):
        return session().query(User).filter_by(user_name=user_name).first()

    @staticmethod
    def all():
        return session().query(User).all()
