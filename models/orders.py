from sqlite.db import db


class OrderModel(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), unique=False, nullable=False)
    user_id = db.Column(db.Integer)
    shipping = db.Column(db.Float, nullable=True)
    discount = db.Column(db.Float, nullable=True)
    total = db.Column(db.Float, nullable=True)
    created = db.Column(db.Date, nullable=False)
    modified = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(25), nullable=False)
    cart = db.relationship("CartModel", back_populates="order")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
