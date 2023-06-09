import requests
import json
from datetime import datetime
from unittest import TestCase

from sqlalchemy.exc import SQLAlchemyError

from models.carts import CartModel
from models.orders import OrderModel
from sqlite.db import db

ENDPOINT = "http://127.0.0.1:5000/orders/{cart_id}"
LOGIN_ENDPOINT = "http://127.0.0.1:5000/login"


class testOrder(TestCase):

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

    def delete_dummy_order(self, cart_id):
        try:
            OrderModel.query.filter_by(cart_id=cart_id).delete()
            db.session.commit()
            return "Cart and Items deleted.", 201
        except Exception:
            return 404, "Product doesn't exist in DB."

    def search_dummy_order(self, cart_id):
        try:
            order = OrderModel.query.filter_by(cart_id=cart_id).first()
            db.session.commit()
        except Exception:
            return 404, "Product doesn't exist in DB."
        return order

    def get_token(self):
        headers = {'Content-type': 'application/json'}
        login_data = {'username': 'Natalia', 'password': 'qwerty1234'}
        token = requests.post(LOGIN_ENDPOINT, data=json.dumps(login_data), headers=headers)
        return token

    def test_get_order(self):
        cart = self.create_dummy_cart()
        url = ENDPOINT.format(cart_id=cart.id)
        response = requests.get(url)

        response_data = response.json()

        assert response.status_code == 201
        assert response_data["status"] == "in_progress"
        assert response_data["cart_id"] == cart.id

        self.delete_dummy_order(response_data['id'])

    def test_create_order(self):
        cart = self.create_dummy_cart()
        url = ENDPOINT.format(cart_id=cart.id)
        token = self.get_token()

        headers = {
            'Content-type': 'application/json',
            'Accept': 'text/plain',
            'cart_id': str(cart.id),
            'token': 'Bearer {}'.format(token)
        }
        response = requests.post(url, headers=headers)

        response_data = response.json()
        order = self.search_dummy_order(cart.id)

        assert response_data["id"] == order.id
        assert response_data["created"] == order.created
        self.delete_dummy_order(order.id)
