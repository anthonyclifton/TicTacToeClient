
import requests


class T3ApiService(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def create_game(self, game_name, player_name, update_url):
        payload = {
            'game_name': game_name,
            'player_name': player_name,
            'update_url': update_url
        }
        self.generic_post("{}/create".format(self.base_url), payload)

    def join_game(self, game_key, player_name, update_url):
        payload = {
            'game_key': game_key,
            'player_name': player_name,
            'update_url': update_url
        }
        url = "{}/join".format(self.base_url)
        self.generic_post(url, payload)

    def mark_cell(self):
        payload = {
            'game_key': 'something',
            'player_key': 'something',
            'x': 1,
            'y': 2
        }

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
