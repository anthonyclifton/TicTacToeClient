from marshmallow import Schema, fields


class MarkSchema(Schema):
    x = fields.Integer()
    y = fields.Integer()
    value = fields.Integer()


class PlayerSchema(Schema):
    key = fields.UUID()
    name = fields.String()


class GameSchema(Schema):
    name = fields.String()
    key = fields.UUID()
    size_x = fields.Integer()
    size_y = fields.Integer()
    player_x = fields.Nested(PlayerSchema, required=False)
    player_o = fields.Nested(PlayerSchema, required=False)
    cells = fields.Nested(MarkSchema, many=True)
    winning_length = fields.Integer()
    state = fields.Integer()
