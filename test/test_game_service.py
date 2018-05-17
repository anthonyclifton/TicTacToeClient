from StringIO import StringIO
import unittest

from mock import MagicMock, patch

from tictactoeclient.services.game_service import GameService


@patch('sys.stdout', new_callable=StringIO)
class TestGameService(unittest.TestCase):
    def test__render__produces_populated_array_from_game_object(self,
                                                                mock_stdout):
        game_service = GameService(MagicMock(autospec=True))
        game = {
            'size_x': 3,
            'size_y': 3,
            'cells': [
                {'x': 0, 'y': 0, 'value': 2},
                {'x': 2, 'y': 2, 'value': 1}
            ]
        }

        game_service.render(game)

        expected_output_lines = [
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


