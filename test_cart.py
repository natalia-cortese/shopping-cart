import requests
from datetime import datetime
from unittest import TestCase

from sqlalchemy.exc import SQLAlchemyError

from models.carts import CartModel
from models.items import ItemsModel
from sqlite.db import db

ENDPOINT = "https://127.0.0.1:5000/carts/{cart_id}"


class testCart(TestCase):

    def create_dummy_cart(self):
        data = {
            "status": "in_progress",
            "created": datetime.now(),
            "total": 0.0
        }

        try:
            cart = CartModel(**data)
            db.session.add(cart)
            db.session.commit()
        except SQLAlchemyError:
            return 500, "error creating cart"
        return cart

    def delete_dummy_cart(self, cart_id):
        try:
            ItemsModel.query.filter_by(cart_id=cart_id).delete()
            CartModel.query.filter_by(id=cart_id).delete()
            db.session.commit()
            return "Cart and Items deleted.", 201
        except Exception:
            return 404, "Product doesn't exist in DB."

    def search_dummy_cart(self, cart_id):
        try:
            items = ItemsModel.query.filter_by(cart_id=cart_id).first()
            cart = CartModel.query.filter_by(id=cart_id).first()
            db.session.commit()
        except Exception:
            return 404, "Product doesn't exist in DB."
        return cart, items

    def test_get_cart(self):
        cart = self.create_dummy_cart()
        url = ENDPOINT.format(cart.id)
        response = requests.get(url)

        response_data = response.json()

        assert response.status_code == 201
        assert response_data["status"] == "in_progress"
        assert response_data["id"] == cart.id

        self.delete_dummy_cart(cart.id)

    def test_create_cart(self):
        cart_id = 11
        url = ENDPOINT.format(cart_id)
        response = requests.post(url)

        response_data = response.json()
        cart_found, item_found = self.search_dummy_cart(cart_id)

        assert response_data["id"] == cart_found.id
        assert response_data["created"] == cart_found.created
        self.delete_dummy_cart(cart_id)

    def test_update_cart(self):
        cart_id = 11
        url = ENDPOINT.format(cart_id)
        requests.post(url)

        data = {
            "product_name": "martillo",
            "quantity": 2
        }

        response = requests.put(url, request=data)
        response_data = response.json()

        cart_found, item_found = self.search_dummy_cart(cart_id)
        assert response_data["id"] == cart_found.id
        assert response_data["created"] == cart_found.created
        assert response_data["quantity"] == item_found.quantity

        self.delete_dummy_cart(cart_id)
