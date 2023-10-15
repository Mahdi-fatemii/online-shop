from sqlalchemy import *
from extentions import db


class Cart(db.Model):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True)
    status = Column(String, default="pending", nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='carts')
    # user = db.relationship('User', back_populates='carts')
