from sqlalchemy import *
from sqlalchemy.orm import backref

from extentions import db


class Cart(db.Model):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True)
    status = Column(String, default="pending")
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", backref=backref('carts', lazy='dynamic'))

    def total_price(self):
        total = 0
        for item in self.cart_items:
            t = item.price * item.quantity
            total += t
        return total

    def get_status_english(self):
        if self.status == 'pending':
            return "waiting for purchase"

        if self.status == 'purchased':
            return "purchased"

        if self.status == 'sent':
            return "sent"

        if self.status == 'rejected':
            return "rejected"
