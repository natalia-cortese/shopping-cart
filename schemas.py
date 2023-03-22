from marshmallow import Schema, fields


class ProductSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    quantity = fields.Float(required=True)
    category = fields.Str(required=True)


class CartSchema(Schema):
    id = fields.Str(dump_only=True)
    user_id = fields.Str(require=False)
    total = fields.Float(required=False)


class OrderSchema(Schema):
    id = fields.Str(dump_only=True)
    cart_id = fields.Str(required=True)
    user_id = fields.Str(require=False)
    total = fields.Float(required=False)


class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
