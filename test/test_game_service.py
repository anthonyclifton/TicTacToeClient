from StringIO import StringIO
import unittest

from mock import MagicMock, patch

from test.game_data import GAME_COMPLETED_PLAYER_O_WINS, GAME_INPROGRESS_NO_MOVES_YET, GAME_INPROGRESS_2X2, \
    GAME_COMPLETED_3X3_PLAYER_O_WINS, GAME_COMPLETED_2X3_PLAYER_O_WINS, PLAYER_KEY_1, PLAYER_WINNER, PLAYER_LOSER
from tictactoeclient.constants import LOBBY_MODE, CREATE_GAME_MODE, JOIN_GAME_MODE
from tictactoeclient.services.game_service import GameService


@patch('sys.stdout', new_callable=StringIO)
class TestGameService(unittest.TestCase):
    def setUp(self):
        self.game_service = GameService(MagicMock(autospec=True))

    def test__process_update__returns_end_game_move_when_game_complete(self,
                                                                       mock_stdout):
        game = GAME_COMPLETED_PLAYER_O_WINS

        move = self.game_service.process_updated_game_from_server(game)

        self.assertEqual({'x': -1, 'y': -1}, move)

    def test__process_update__returns_legitimate_move_when_game_inprogress(self,
                                                                           mock_stdout):
        game = GAME_INPROGRESS_NO_MOVES_YET

        move = self.game_service.process_updated_game_from_server(game)

        self.assertEqual({'x': 0, 'y': 0}, move)

    def test__process_update__generates_move_on_random_unmarked_cell(self,
                                                                     mock_stdout):
        game = GAME_INPROGRESS_2X2

        move = self.game_service.process_updated_game_from_server(game)

        assert move['x'] == 1 and move['y'] == 0 or \
               move['x'] == 0 and move['y'] == 1

    def test__process_update__displays_populated_square_on_stdout(self,
                                                                  mock_stdout):
        game = GAME_COMPLETED_3X3_PLAYER_O_WINS

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
        game = GAME_COMPLETED_2X3_PLAYER_O_WINS

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

    def test__set_game_mode__sets_the_game_mode(self,
                                                mock_stdout):
        self.game_service.set_game_mode(LOBBY_MODE)
        self.assertEqual(LOBBY_MODE, self.game_service.game_mode)

    def test__set_player_key__sets_the_player_key(self,
                                                  mock_stdout):
        self.game_service.set_player_key(str(PLAYER_KEY_1))
        self.assertEqual(str(PLAYER_KEY_1), self.game_service.player_key)

    def test__display_game_result__winner_if_create_game_mode_and_player_x_winner(self,
                                                                                  mock_stdout):
        self.game_service.set_game_mode(CREATE_GAME_MODE)
        self.game_service._display_game_result(PLAYER_WINNER, PLAYER_LOSER)
        output_lines = mock_stdout.getvalue().split('\n')

        assert 'I won!' in output_lines

    def test__display_game_result__loser_if_create_game_mode_and_player_x_loser(self,
                                                                                  mock_stdout):
        self.game_service.set_game_mode(CREATE_GAME_MODE)
        self.game_service._display_game_result(PLAYER_LOSER, PLAYER_WINNER)
        output_lines = mock_stdout.getvalue().split('\n')
        assert 'I lost!' in output_lines

    def test__display_game_result__winner_if_join_game_mode_and_player_o_winner(self,
                                                                                  mock_stdout):
        self.game_service.set_game_mode(JOIN_GAME_MODE)
        self.game_service._display_game_result(PLAYER_LOSER, PLAYER_WINNER)
        output_lines = mock_stdout.getvalue().split('\n')

        assert 'I won!' in output_lines

    def test__display_game_result__loser_if_join_game_mode_and_player_o_loser(self,
                                                                                  mock_stdout):
        self.game_service.set_game_mode(JOIN_GAME_MODE)
        self.game_service._display_game_result(PLAYER_WINNER, PLAYER_LOSER)
        output_lines = mock_stdout.getvalue().split('\n')
        assert 'I lost!' in output_lines

    def test__display_game_result__winner_if_lobby_mode_and_player_is_x_and_winner(self,
                                                                                  mock_stdout):
        self.game_service.set_game_mode(LOBBY_MODE)
        self.game_service.set_player_key(str(PLAYER_WINNER['key']))
        self.game_service._display_game_result(PLAYER_WINNER, PLAYER_LOSER)
        output_lines = mock_stdout.getvalue().split('\n')

        assert 'I won!' in output_lines

    def test__display_game_result__loser_if_lobby_mode_and_player_is_x_and_loser(self,
                                                                                  mock_stdout):
        self.game_service.set_game_mode(LOBBY_MODE)
        self.game_service.set_player_key(str(PLAYER_LOSER['key']))
        self.game_service._display_game_result(PLAYER_LOSER, PLAYER_WINNER)
        output_lines = mock_stdout.getvalue().split('\n')

        assert 'I lost!' in output_lines

    def test__display_game_result__winner_if_lobby_mode_and_player_is_o_and_winner(self,
                                                                                  mock_stdout):
        self.game_service.set_game_mode(LOBBY_MODE)
        self.game_service.set_player_key(str(PLAYER_WINNER['key']))
        self.game_service._display_game_result(PLAYER_LOSER, PLAYER_WINNER)
        output_lines = mock_stdout.getvalue().split('\n')

        assert 'I won!' in output_lines

    def test__display_game_result__loser_if_lobby_mode_and_player_is_o_and_loser(self,
                                                                                  mock_stdout):
        self.game_service.set_game_mode(LOBBY_MODE)
        self.game_service.set_player_key(str(PLAYER_LOSER['key']))
        self.game_service._display_game_result(PLAYER_WINNER, PLAYER_LOSER)
        output_lines = mock_stdout.getvalue().split('\n')

        assert 'I lost!' in output_lines
