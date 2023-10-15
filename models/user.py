from sqlalchemy import *
from extentions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False, index=True)
    lastName = Column(String, nullable=False, index=True)
    phone = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    address = Column(String, nullable=True, index=True)

    # carts = db.relationship('Cart', back_populates='user')
