
import requests


class T3ApiService(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def create_game(self, game_name, player_name):
        payload = {
            'game_name': game_name,
            'player_name': player_name,
            'update_url': 'http://my-ipaddress/update'
        }
        self.generic_post("{}/create".format(self.base_url), payload)

    def join_game(self):
        pass

    def mark_cell(self):
        pass

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
        return requests.post(url, data=payload)
