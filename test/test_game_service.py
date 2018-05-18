from StringIO import StringIO
import unittest

from mock import MagicMock, patch

from tictactoeclient.services.game_service import GameService, GAME_COMPLETED, GAME_INPROGRESS


@patch('sys.stdout', new_callable=StringIO)
class TestGameService(unittest.TestCase):
    def setUp(self):
        self.game_service = GameService(MagicMock(autospec=True))

    def test__process_update__returns_phoney_move_when_game_complete(self, mock_stdout):
        game = {
            'size_x': 3,
            'size_y': 3,
            'cells': [],
            'name': 'anything',
            'player_x': {
                'name': 'player x',
                'winner': False
            },
            'player_o': {
                'name': 'player o',
                'winner': True
            },
            'state': GAME_COMPLETED
        }

        move = self.game_service.process_updated_game_from_server(game)

        self.assertEqual({'x': -1, 'y': -1}, move)

    def test__process_update__returns_legitimate_move_when_game_inprogress(self, mock_stdout):
        game = {
            'size_x': 1,
            'size_y': 1,
            'cells': [],
            'name': 'anything',
            'player_x': {
                'name': 'player x',
                'winner': False
            },
            'player_o': {
                'name': 'player o',
                'winner': True
            },
            'state': GAME_INPROGRESS
        }

        move = self.game_service.process_updated_game_from_server(game)

        self.assertEqual({'x': 0, 'y': 0}, move)

    def test__render__produces_populated_square_from_game_object(self,
                                                                 mock_stdout):
        game_service = GameService(MagicMock(autospec=True))
        game = {
            'name': 'something',
            'player_x': {
                'name': 'player 1'
            },
            'player_o': {
                'name': 'player 2'
            },
            'size_x': 3,
            'size_y': 3,
            'cells': [
                {'x': 0, 'y': 0, 'value': 2},
                {'x': 2, 'y': 2, 'value': 1}
            ]
        }

        game_service.render(game)

        expected_output_lines = [
            '',
            'Game: something',
            'Player X: player 1',
            'Player O: player 2',
            '+---+',
            '|X  |',
            '|   |',
            '|  O|',
            '+---+'
        ]
        output_lines = mock_stdout.getvalue().split('\n')

        for line_number in range(0, len(expected_output_lines)):
            self.assertEqual(expected_output_lines[line_number],
                             output_lines[line_number])

    def test__render__produces_populated_rectangle_from_game_object(self,
                                                                    mock_stdout):
        game_service = GameService(MagicMock(autospec=True))
        game = {
            'name': 'something',
            'player_x': {
                'name': 'player 1'
            },
            'player_o': {
                'name': 'player 2'
            },
            'size_x': 2,
            'size_y': 3,
            'cells': [
                {'x': 0, 'y': 0, 'value': 2},
                {'x': 1, 'y': 2, 'value': 1}
            ]
        }

        game_service.render(game)

        expected_output_lines = [
            '',
            'Game: something',
            'Player X: player 1',
            'Player O: player 2',
            '+--+',
            '|X |',
            '|  |',
            '| O|',
            '+--+'
        ]
        output_lines = mock_stdout.getvalue().split('\n')

        for line_number in range(0, len(expected_output_lines)):
            self.assertEqual(expected_output_lines[line_number],
                             output_lines[line_number])
