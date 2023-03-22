from sqlite.db import db


class CartModel(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False)
    total = db.Column(db.Float)
    created = db.Column(db.Date, nullable=False)
    modified = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(25), nullable=False)
    items = db.relationship("ItemsModel", back_populates="carts", lazy="dynamic")
    order = db.relationship("OrderModel", back_populates="cart", lazy="dynamic")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
