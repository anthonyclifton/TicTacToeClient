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

    def test__process_update__generates_move_on_random_unmarked_cell(self, mock_stdout):
        game = {
            'size_x': 2,
            'size_y': 2,
            'cells': [
                {'x': 0, 'y': 0, 'value': 2},
                {'x': 1, 'y': 1, 'value': 2}
            ],
            'name': 'anything',
            'player_x': {
                'name': 'player x',
                'winner': False
            },
            'player_o': {
                'name': 'player o',
                'winner': False
            },
            'state': GAME_INPROGRESS
        }

        move = self.game_service.process_updated_game_from_server(game)

        assert move['x'] == 1 and move['y'] == 0 or \
               move['x'] == 0 and move['y'] == 1

    def test__process_update__displays_populated_square_on_stdout(self,
                                                                  mock_stdout):
        game = {
            'name': 'something',
            'player_x': {
                'name': 'player 1',
                'winner': False
            },
            'player_o': {
                'name': 'player 2',
                'winner': True
            },
            'size_x': 3,
            'size_y': 3,
            'cells': [
                {'x': 0, 'y': 0, 'value': 2},
                {'x': 2, 'y': 2, 'value': 1}
            ],
            'state': GAME_COMPLETED
        }

        self.game_service.process_updated_game_from_server(game)

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

    def test__render__displays_populated_rectangle_on_stdout(self,
                                                             mock_stdout):
        game = {
            'name': 'something',
            'player_x': {
                'name': 'player 1',
                'winner': False
            },
            'player_o': {
                'name': 'player 2',
                'winner': True
            },
            'size_x': 2,
            'size_y': 3,
            'cells': [
                {'x': 0, 'y': 0, 'value': 2},
                {'x': 1, 'y': 2, 'value': 1}
            ],
            'state': GAME_COMPLETED
        }

        self.game_service.process_updated_game_from_server(game)

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
