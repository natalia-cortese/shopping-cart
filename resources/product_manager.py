from datetime import datetime
from flask import request, jsonify
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from sqlalchemy.exc import SQLAlchemyError

from models import ProductModel
from schemas import ProductSchema
from sqlite.db import db

blp = Blueprint("products", __name__, description="Operations on products")


@blp.route("/products/<string:product_name>")
class ProductManager(MethodView):

    @blp.response(201, ProductSchema)
    def post(self, product_name):
        request_data = request.get_json()
        price = request_data.get("price")
        quantity = request_data.get("quantity")
        category = request_data.get("category")
        data = {
            "name": product_name.upper(),
            "quantity": int(quantity),
            "price": float(price),
            "category": str(category),
            "created": datetime.now(),
            "status": "in_stock"
        }
        print("save product: {}".format(data))
        try:
            product_ = ProductModel(**data)
            db.session.add(product_)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, "error inserting product")

        return product_

    @blp.response(201, ProductSchema)
    def get(self, product_name):
        try:
            product = ProductModel.query.filter_by(name=product_name.upper()).first()
            return product.as_dict()
        except AttributeError:
            return abort(404, "Product doesn't exist in DB.")

    @jwt_required()
    @blp.response(201, ProductSchema)
    def put(self, product_name):
        request_data = request.get_json()
        field_name = request_data.get("field_name")
        new_value = request_data.get("new_value")

        try:
            product = ProductModel.query.filter_by(name=product_name.upper()).first()
            product_dict = product.as_dict()
            product_dict[str(field_name)] = new_value
            product_updated = ProductModel(**product_dict)
            ProductModel.query.filter_by(id=product.id).delete()
            db.session.add(product_updated)
            db.session.commit()
            return product_updated.as_dict()
        except AttributeError:
            return abort(404, "Product doesn't exist in DB.")

    @jwt_required()
    def delete(self, product_name):
        try:
            info = ProductModel.query.filter_by(name=product_name.upper()).delete()
            db.session.commit()
        except Exception:
            return abort(404, "Product doesn't exist in DB.")
        return jsonify(info)
