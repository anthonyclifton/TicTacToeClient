import unittest

from mock import patch, Mock
from requests import Response

from tictactoeclient.services.t3_api_service import T3ApiService


class TestT3ApiService(unittest.TestCase):
    @patch('tictactoeclient.services.t3_api_service._get_board_size')
    @patch('tictactoeclient.services.t3_api_service.requests')
    def test__create_game__calls_post_with_game_size(self,
                                                     mock_requests,
                                                     mock_get_board_size):

        mock_get_board_size.side_effect = self._fake_get_board_size

        t3_api_service = T3ApiService('base')

        mock_response = Mock()
        mock_response.content = '{}'

        mock_requests.post.return_value = mock_response

        t3_api_service.create_game("Test Game", "Player Name", "Update URL")

        call_args = mock_requests.post.call_args

        expected_json = {
            'update_url': 'Update URL',
            'player_name': 'Player Name',
            'game_name': 'Test Game',
            'size_x': 3,
            'size_y': 3,
            'winning_length': 3
        }

        self.assertEqual(expected_json, call_args[1]['json'])

    @staticmethod
    def _fake_get_board_size():
        return 3, 3, 3
