from flask import request, jsonify
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from passlib.hash import pbkdf2_sha1
from flask_jwt_extended import create_access_token


from models import UserModel
from schemas import UserSchema
from sqlite.db import db

blp = Blueprint("users", __name__, description="Operations on users")


@blp.route("/user/")
class User(MethodView):

    def post(self):
        request_data = request.get_json()
        username = request_data.get("username")
        password = request_data.get("password")

        user_existent = UserModel.query.filter_by(username=username).first()
        if user_existent:
            abort(404, "User already exists")

        user = UserModel(
            username=username,
            password=pbkdf2_sha1.hash(password)
        )
        db.session.add(user)
        db.session.commit()
        return "user created", 201


@blp.route("/user/<int:user_id>")
class UserList(MethodView):

    def get(self, user_id):
        try:
            user = UserModel.query.filter_by(id=user_id).first()
            return user.as_dict()
        except AttributeError:
            return abort(404, "Product doesn't exist in DB.")

    def delete(self, user_id):
        try:
            info = UserModel.query.filter_by(id=user_id).delete()
            db.session.commit()
        except Exception:
            return abort(404, "User doesn't exist in DB.")
        return jsonify(info)


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, request):
        username = request.get("username")
        password = request.get("password")

        user = UserModel.query.filter_by(username=username).first()
        if user and pbkdf2_sha1.verify(password, user.password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}
        abort(404, "Invalid Credetials")
