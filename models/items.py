from sqlite.db import db


class ItemsModel(db.Model):
    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), unique=False, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), unique=False, nullable=False)
    product = db.Column(db.String(80), unique=True, nullable=False)
    quantity = db.Column(db.Integer)
    sub_total = db.Column(db.Float)
    created = db.Column(db.Date, nullable=False)
    modified = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(25), nullable=False)
    carts = db.relationship("CartModel", back_populates="items")
    products = db.relationship("ProductModel", back_populates="items")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
