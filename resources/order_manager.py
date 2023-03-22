from datetime import datetime

from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from sqlalchemy.exc import SQLAlchemyError

from models.carts import CartModel
from models.items import ItemsModel
from models.orders import OrderModel
from models.products import ProductModel

from schemas import OrderSchema
from sqlite.db import db

blp = Blueprint("orders", __name__, description="Operations on orders")


@blp.route("/orders/<string:cart_id>")
class OrderManager(MethodView):
    """
    ● If you buy two or more products with category Coffee, then you receive one extra for free
    ● If you buy more than 3 products from the Equipment category, then you get free shipping
    ● If you spend more than 70 dollars on category Accessories then you receive 10%
discounts
    """

    @jwt_required()
    @blp.response(201, OrderSchema)
    def post(self, cart_id):

        cart = CartModel.query.filter_by(id=cart_id).first()
        items = ItemsModel.query.filter_by(cart_id=cart_id).all()

        if not cart:
            abort(500, "error cart not found")
        if not items:
            abort(500, "error cart does not have items added.")

        shipping = self.calculateShipping(items)
        discount = self.calculateDiscount(cart.total, items)

        data_order = {
            "cart_id": cart.id,
            "user_id": cart.user_id,
            "shipping": shipping,
            "discount": discount,
            "total": (cart.total + shipping - discount),
            "created": datetime.now(),
            "status": "created"
        }

        try:
            new_order = OrderModel(**data_order)
            cart.status = "finished"
            db.session.add(new_order)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, "error order can be created.")

        return new_order.as_dict()

    @jwt_required()
    def put(self, cart_id):
        try:
            order = OrderModel.query.filter_by(cart_id=cart_id).first()
            order.status = "finished"
            db.session.commit()
        except AttributeError:
            return abort(404, "Product doesn't exist in DB.")

        return order.as_dict(), 201

    def calculateShipping(self, items):
        shipping = 15
        limit_products_free = 3
        products = []
        for item in items:
            products.append(item.product_id)

        Equipment_products = ProductModel.query.filter_by(id.in_(products)).filter_by(
            category="Equipment"
        ).count()

        if Equipment_products >= limit_products_free:
            shipping = 0
        return shipping

    def calculateDiscount(self, cart_total, items):
        discount = 0
        accesory_limit = 70
        accesory_discount = 0.10

        products = []
        for item in items:
            products.append(item.product_id)

        accesory_products = ProductModel.query.filter_by(id.in_(products)).filter_by(
            category="Accessories"
        ).all()
        accesories_products = [product.id for product in accesory_products]

        accesory_cost = 0
        for item in items:
            if item.product_id in accesories_products:
                accesory_cost =+ item.sub_total

        if accesory_cost > accesory_limit:
            discount = cart_total * accesory_discount
        return cart_total - discount

    def get(self, cart_id):
        try:
            order_ = OrderModel.query.filter_by(cart_id=cart_id).first()
            return order_.as_dict()
        except AttributeError:
            return abort(404, "Product doesn't exist in DB.")
