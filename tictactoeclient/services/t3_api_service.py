
from marshmallow import Schema, fields

from tictactoeclient.configuration import GAME_M, GAME_N, GAME_K


class T3ApiService(object):
    def __init__(self, base_url, requests):
        self.base_url = base_url
        self.requests = requests

    def create_game(self, game_name, player_name, update_url):
        size_x, size_y, winning_length = _get_board_size()
        payload = {
            'game_name': game_name,
            'player_name': player_name,
            'update_url': update_url,
            'size_x': size_x,
            'size_y': size_y,
            'winning_length': winning_length
        }
        response = self._generic_post("{}/create".format(self.base_url), payload)
        game, errors = GameSchema().loads(response.content)

        print ""
        print("To join this game, run:")
        print("./join {}".format(game['key']))

    def join_game(self, game_key, player_name, update_url):
        payload = {
            'game_key': game_key,
            'player_name': player_name,
            'update_url': update_url
        }
        url = "{}/join".format(self.base_url)
        self._generic_post(url, payload)

    def enter_lobby(self, player_name, update_url):
        payload = {
            'player_name': player_name,
            'update_url': update_url
        }
        url = "{}/lobby".format(self.base_url)
        response = self._generic_post(url, payload)
        player, errors = PlayerSchema().loads(response.content)

        print ""
        print("Entered lobby as: {}, using key: {}".format(player['name'], player['key']))

    def _generic_post(self, url, payload):
        return self.requests.post(url, json=payload)


def _get_board_size():
    return GAME_M, GAME_N, GAME_K


class MarkSchema(Schema):
    x = fields.Number()
    y = fields.Number()
    value = fields.Number()


class PlayerSchema(Schema):
    key = fields.UUID()
    name = fields.String()
    winner = fields.Boolean()


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
