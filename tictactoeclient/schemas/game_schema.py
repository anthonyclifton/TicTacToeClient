from marshmallow import Schema, fields


class MarkSchema(Schema):
    x = fields.Number()
    y = fields.Number()
    value = fields.Number()


class PlayerSummarySchema(Schema):
    name = fields.String()


class GameSchema(Schema):
    name = fields.String()
    key = fields.UUID()
    size_x = fields.Number()
    size_y = fields.Number()
    player_x = fields.Nested(PlayerSummarySchema, required=False)
    player_o = fields.Nested(PlayerSummarySchema, required=False)
    cells = fields.Nested(MarkSchema, many=True)
    winning_length = fields.Number()
    state = fields.Integer()
