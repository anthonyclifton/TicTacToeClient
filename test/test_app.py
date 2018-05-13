import json
import unittest
from uuid import uuid4

from flask import Response
from mock import patch

from tictactoeclient.schemas.game_schema import GameSchema
from main import update


class TestApp(unittest.TestCase):

    @patch('tictactoeclient.t3client.request')
    @patch('tictactoeclient.t3client.game_service', autospec=True)
    def test__update__responses_with_player_move(self, mock_game_service, mock_request):
        request_data = GameSchema().dumps({
            'name': 'Test Game',
            'key': uuid4(),
            'size_x': 3,
            'size_y': 3,
            'player_x': {
                'key': uuid4(),
                'name': 'player 1'
            },
            'player_o': {
                'key': uuid4(),
                'name': 'player 2'
            },
            'cells': [],
            'winning_length': 3,
            'state': 2
        })
        mock_request.data = request_data.data

        new_move = {'x': 1, 'y': 2}
        mock_game_service.game_loop.return_value = new_move

        expected_response = Response(
            response=json.dumps(new_move),
            status=200,
            mimetype='application/json'
        )

        response = update()

        self.assertEqual(expected_response.json, response.json)
