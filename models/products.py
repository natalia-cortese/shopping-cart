from sqlite.db import db


class ProductModel(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    created = db.Column(db.Date, nullable=False)
    modified = db.Column(db.Date, nullable=True)
    category = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(25), nullable=False)
    items = db.relationship("ItemsModel", back_populates="products", lazy="dynamic")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
