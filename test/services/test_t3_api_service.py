import unittest

from mock import patch

from tictactoeclient.services.t3_api_service import T3ApiService


class TestT3ApiService(unittest.TestCase):

    @patch('tictactoeclient.services.t3_api_service.requests', autospec=True)
    def test__create_game__makes_request(self, mock_requests):
        base_url = 'http://base-url'
        t3 = T3ApiService(base_url)

        game_name = 'Test Game'
        player_name = 'Test Player'
        update_url = 'http://my-ipaddress/update'

        expected_payload = {
            'game_name': game_name,
            'player_name': player_name,
            'update_url': update_url
        }

        t3.create_game(game_name, player_name, update_url)

        mock_request_args = mock_requests.post.call_args

        self.assertEqual(mock_request_args[0][0], "{}/create".format(base_url))
        self.assertEqual(mock_request_args[1]['json'], expected_payload)
