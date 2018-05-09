import unittest

from mock import patch

from tictactoeclient.t3client import create


class TestApp(unittest.TestCase):

    @patch('tictactoeclient.t3client.T3ApiService')
    def test__create__calls_server_url_with_game_and_player_name(self, mock_t3_api):
        server_base_url = 'http://127.0.0.1'
        game_name = 'Test Game'
        player_name = 'Test Player'
        update_url = "http://something/update"

        create(game_name, player_name, server_base_url)

        mock_t3_api.return_value.create_game.assert_called_with(game_name,
                                                                player_name,
                                                                "http://127.0.0.1:3333/update")
