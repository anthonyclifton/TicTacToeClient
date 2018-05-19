import unittest

from mock import Mock

from test.game_data import GAME_KEY, CREATE_RESPONSE, LOBBY_RESPONSE
from tictactoeclient.services.t3_api_service import T3ApiService


class TestT3ApiService(unittest.TestCase):

    def test__create_game__calls_post_with_correct_keys(self):
        base_url = 'http://base_url'
        expected_url = "{}/create".format(base_url)

        expected_json = {
            'update_url': 'Update URL',
            'player_name': 'Player Name',
            'game_name': 'Test Game',
            'size_x': 3,
            'size_y': 3,
            'winning_length': 3
        }

        fake_requests = FakeRequests(expected_url, expected_json)
        t3_api_service = T3ApiService(base_url, fake_requests)

        t3_api_service.create_game("Test Game", "Player Name", "Update URL")

    def test__join_game__calls_post_with_correct_keys(self):
        base_url = 'http://base_url'
        expected_url = "{}/join".format(base_url)

        expected_json = {
            'game_key': GAME_KEY,
            'player_name': "Player Name",
            'update_url': "Update URL"
        }

        fake_requests = FakeRequests(expected_url, expected_json)
        t3_api_service = T3ApiService(base_url, fake_requests)

        t3_api_service.join_game(GAME_KEY, "Player Name", "Update URL")

    def test__enter_lobby__calls_post_with_correct_keys(self):
        base_url = 'http://base_url'
        expected_url = "{}/lobby".format(base_url)

        expected_json = {
            'player_name': "Player Name",
            'update_url': "Update URL"
        }

        fake_requests = FakeRequests(expected_url, expected_json)
        t3_api_service = T3ApiService(base_url, fake_requests)

        t3_api_service.enter_lobby("Player Name", "Update URL")

    @staticmethod
    def _fake_get_board_size():
        return 3, 3, 3


class FakeRequests(object):
    def __init__(self, expected_url, expected_payload):
        self.expected_url = expected_url
        self.expected_payload = expected_payload

    def post(self, url, json):
        assert url == self.expected_url
        assert json == self.expected_payload

        response = Mock()
        response.content = LOBBY_RESPONSE if 'lobby' in url else CREATE_RESPONSE

        return response
