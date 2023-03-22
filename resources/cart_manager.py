from datetime import datetime
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from sqlalchemy.exc import SQLAlchemyError

from models.carts import CartModel
from models.items import ItemsModel
from models.products import ProductModel
from sqlite.db import db

blp = Blueprint("carts", __name__, description="Operations on carts")


@blp.route("/carts/<string:cart_id>")
class CartManager(MethodView):

    def post(self, cart_id):
        # Select one Product by name only if is in_stock
        request_data = request.get_json()
        product_name = request_data.get("product_name")
        quantity = request_data.get("quantity")

        data = {
            "user_id": 1,
            "status": "in_progress",
            "created": datetime.now(),
            "total": 0.0
        }

        cart = CartModel.query.filter_by(id=cart_id).first()
        if not cart:
            try:
                cart = CartModel(**data)
                db.session.add(cart)
                db.session.commit()
            except SQLAlchemyError:
                abort(500, "error creating cart")
        print("Cart Find: {}".format(cart.as_dict()))

        product = ProductModel.query.filter_by(name=product_name.upper()).first()

        if product and product.quantity >= quantity:
            print("Product Find: {}".format(product.__dict__))

            try:
                item_data = {
                    "cart_id": cart_id,
                    "product_id": product.id,
                    "product": product.name,
                    "quantity": quantity,
                    "sub_total": product.price * quantity,
                    "created": datetime.now(),
                    "status": "in_process"
                }
                detail = ItemsModel(**item_data)

                db.session.add(detail)

                product.quantity = product.quantity - quantity
                if cart.total is None:
                    cart.total = 0.0
                cart.total = cart.total + (product.price * quantity)
                db.session.commit()
                return detail.as_dict(), 201
            except Exception as e:
                # If we can't create the cart we return the stock
                db.session.rollback()
                return abort(404, message="Error adding new product to cart: {}".format(e))
        else:
            return abort(404, message="Product cant be added to cart because it doesn't exist.")

    @jwt_required()
    def put(self, cart_id):
        data = request.get_json()
        product_name = data.get("product_name")
        quantity = data.get("quantity")
        cart = CartModel.query.filter_by(id=cart_id).first()
        if cart:
            # so we can update.
            detail = ItemsModel.query.filter_by(cart_id=cart_id).filter_by(
                product=product_name
            ).first()

            old_quantity = detail.quantity
            old_total = detail.sub_total
            price = old_total/old_quantity
            detail.quantity = quantity
            detail.sub_total = quantity * price

            cart.total = cart.total - old_total
            cart.total = cart.total + (quantity * price)
            db.session.commit()
            return detail.as_dict(), 200
        return {"message": "Can found that cart"}, 400

    def get(self, cart_id):
        try:
            cart = CartModel.query.filter_by(id=cart_id).first()
            items = ItemsModel.query.filter_by(cart_id=cart_id).all()

            items_data = []
            for item in items:
                items_data.append(item.as_dict())
            data = {
                "Cart": cart.as_dict(),
                "Items": items_data
            }
            return data, 201
        except AttributeError:
            return abort(404, "Product doesn't exist in DB.")

    @jwt_required()
    def delete(self, cart_id):
        try:
            ItemsModel.query.filter_by(cart_id=cart_id).delete()
            CartModel.query.filter_by(id=cart_id).delete()
            db.session.commit()
            return "Cart and Items deleted.", 201
        except Exception:
            return abort(404, "Product doesn't exist in DB.")
