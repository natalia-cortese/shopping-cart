import secrets  # noqa # pylint: disable=unused-import

from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from sqlite.db import db
import models  # noqa # pylint: disable=unused-import

from resources.cart_manager import blp as CartBlueprint
from resources.product_manager import blp as ProductBlueprint
from resources.order_manager import blp as OrderBlueprint
from resources.user_manager import blp as UserBlueprint


def create_app(db_url=None):
    app = Flask(__name__)

    app.config.update({
        "PROPAGATE_EXCEPTIONS": True,
        "API_TITLE": "Shopping Cart REST API",
        "API_VERSION": "v1",
        "OPENAPI_VERSION": "3.0.3",
        "OPENAPI_URL_VERSION": "/",
    })
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    db.init_app(app)

    api = Api(app)
    # secrets.SystemRandom().getrandbits(24)
    app.config["JWT_SECRET_KEY"] = "5247512123"
    jwt = JWTManager(app)

    @app.before_first_request
    def create_tables():
        print("create tables on db.")
        db.create_all()

    api.register_blueprint(CartBlueprint)
    api.register_blueprint(OrderBlueprint)
    api.register_blueprint(ProductBlueprint)
    api.register_blueprint(UserBlueprint)

    return app


app = create_app()
