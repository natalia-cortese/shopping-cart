import requests
import json
from datetime import datetime
from unittest import TestCase

from sqlalchemy.exc import SQLAlchemyError

from models.carts import CartModel
from models.items import ItemsModel
from sqlite.db import db

ENDPOINT = "http://127.0.0.1:5000/carts/{cart_id}"
LOGIN_ENDPOINT = "http://127.0.0.1:5000/login"


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

    def get_token(self):
        headers = {'Content-type': 'application/json'}
        login_data = {'username': 'Natalia', 'password': 'qwerty1234'}
        token = requests.post(LOGIN_ENDPOINT, data=json.dumps(login_data), headers=headers)
        return token

    def test_get_cart(self):
        cart = self.create_dummy_cart()
        url = ENDPOINT.format(cart_id=cart.id)
        response = requests.get(url)

        response_data = response.json()

        assert response.status_code == 201
        assert response_data["status"] == "in_progress"
        assert response_data["id"] == cart.id

        self.delete_dummy_cart(cart.id)

    def test_create_cart(self):
        cart_id = 11
        url = ENDPOINT.format(cart_id=cart_id)
        token = self.get_token()

        headers = {
            'Content-type': 'application/json',
            'Accept': 'text/plain',
            'cart_id': str(cart_id),
            'token': 'Bearer {}'.format(token)
        }

        data = {'product_name': 'martillo', 'quantity': 5}
        response = requests.post(url, data=json.dumps(data), headers=headers)

        response_data = response.json()
        cart_found, item_found = self.search_dummy_cart(cart_id)

        assert response_data["id"] == cart_found.id
        assert response_data["created"] == cart_found.created
        self.delete_dummy_cart(cart_id)

    def test_update_cart(self):
        cart_id = 11
        url = ENDPOINT.format(cart_id=cart_id)
        requests.post(url)
        token = self.get_token()

        headers = {
            'Content-type': 'application/json',
            'Accept': 'text/plain',
            'cart_id': str(cart_id),
            'token': 'Bearer {}'.format(token)
        }

        data = {
            "product_name": "martillo",
            "quantity": 2
        }

        response = requests.put(url, data=json.dumps(data), headers=headers)
        response_data = response.json()

        cart_found, item_found = self.search_dummy_cart(cart_id)
        assert response_data["id"] == cart_found.id
        assert response_data["created"] == cart_found.created
        assert response_data["quantity"] == item_found.quantity

        self.delete_dummy_cart(cart_id)
