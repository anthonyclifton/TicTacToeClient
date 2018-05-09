
import requests
from marshmallow import Schema, fields


class T3ApiService(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def create_game(self, game_name, player_name, update_url):
        payload = {
            'game_name': game_name,
            'player_name': player_name,
            'update_url': update_url
        }
        response = self.generic_post("{}/create".format(self.base_url), payload)
        game, errors = GameSchema().loads(response.content)
        return game

    def join_game(self, game_key, player_name, update_url):
        payload = {
            'game_key': game_key,
            'player_name': player_name,
            'update_url': update_url
        }
        url = "{}/join".format(self.base_url)
        self.generic_post(url, payload)

    def mark_cell(self, game_key, player_key, x, y):
        payload = {
            'game_key': str(game_key),
            'player_key': str(player_key),
            'x': x,
            'y': y
        }
        url = "{}/markcell".format(self.base_url)
        self.generic_post(url, payload)

    def ping(self):
        url = 'http://localhost:3334/ping'
        payload = {
            'myurl': 'my own url'
        }
        self.generic_post(url, payload)

    def generic_get(self, url):
        pass

    @staticmethod
    def generic_post(url, payload):
        return requests.post(url, json=payload)


class MarkSchema(Schema):
    x = fields.Number()
    y = fields.Number()
    value = fields.Number()


class PlayerSchema(Schema):
    key = fields.UUID()
    name = fields.String()


class GameSchema(Schema):
    name = fields.String()
    key = fields.UUID()
    size_x = fields.Number()
    size_y = fields.Number()
    player_x = fields.Nested(PlayerSchema, required=False)
    player_o = fields.Nested(PlayerSchema, required=False)
    cells = fields.Nested(MarkSchema, many=True)
    winning_length = fields.Number()
    state = fields.Integer()
