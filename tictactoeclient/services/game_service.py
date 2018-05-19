from random import randint

from tictactoeclient.constants import GAME_COMPLETED, END_GAME_NULL_MOVE, \
    EMPTY_MARKER, VALUE_TO_MARKER, \
    VERTICAL_BORDER, CORNER_MARKER, HORIZONTAL_BORDER, CREATE_GAME_MODE, LOBBY_MODE


class GameService(object):
    def __init__(self):
        self.game_mode = None
        self.player_key = None

    def set_game_mode(self, game_mode):
        self.game_mode = game_mode

    def set_player_key(self, player_key):
        self.player_key = player_key

    def process_updated_game_from_server(self, updated_game):
        self._display_game_board(updated_game)
        if updated_game['state'] == GAME_COMPLETED:
            return self._display_game_result(updated_game['player_x'],
                                             updated_game['player_o'])
        else:
            return self._choose_next_move(updated_game)

    @staticmethod
    def _choose_next_move(updated_game):
        unmarked_cells = []
        for y in range(0, updated_game['size_y']):
            for x in range(0, updated_game['size_x']):
                if not next((cell for cell in updated_game['cells'] if
                             cell['x'] == x and cell['y'] == y), None):
                    unmarked_cells.append((x, y))

        next_move = unmarked_cells[randint(0, len(unmarked_cells) - 1)]

        move_x = next_move[0]
        move_y = next_move[1]
        return {'x': move_x, 'y': move_y}

    def _display_game_result(self, player_x, player_o):
        print ""
        if self.game_mode == CREATE_GAME_MODE:
            self._display_win_loss_message(self._is_player_winner(player_x))
        elif self.game_mode == LOBBY_MODE:
            if not self._is_player_winner(player_x) and \
                    not self._is_player_winner(player_o):
                print "A draw!"
            else:
                if self._is_player_x(player_x):
                    self._display_win_loss_message(self._is_player_winner(player_x))
                else:
                    self._display_win_loss_message(self._is_player_winner(player_o))
        else:
            self._display_win_loss_message(self._is_player_winner(player_o))
        return END_GAME_NULL_MOVE

    @staticmethod
    def _display_win_loss_message(is_winner):
        print "I won!" if is_winner else "I lost!"

    def _display_game_board(self, updated_game):
        size_x = updated_game['size_x']
        size_y = updated_game['size_y']

        grid = self._create_empty_grid(size_x, size_y)
        self._populate_grid_from_updated_game(grid, updated_game)

        print "\nGame: {}".format(updated_game['name'])
        print "Player X: {}".format(updated_game['player_x']['name'])
        print "Player O: {}".format(updated_game['player_o']['name'])

        self._draw_horizontal_border(size_x)
        self._draw_marks_on_board(grid)
        self._draw_horizontal_border(size_x)

    @staticmethod
    def _draw_marks_on_board(grid):
        for row in grid:
            line = VERTICAL_BORDER
            for column in row:
                line = line + column
            line = line + VERTICAL_BORDER
            print line

    @staticmethod
    def _create_empty_grid(size_x, size_y):
        grid = [[EMPTY_MARKER for x in range(size_x)] for y in range(size_y)]
        return grid

    @staticmethod
    def _populate_grid_from_updated_game(grid, updated_game):
        for cell in updated_game['cells']:
            row = cell['y']
            column = cell['x']
            cell_marker = VALUE_TO_MARKER[cell['value']]
            grid[row][column] = cell_marker

    @staticmethod
    def _draw_horizontal_border(size_x):
        print "{}{}{}".format(CORNER_MARKER,
                              (HORIZONTAL_BORDER * size_x),
                              CORNER_MARKER)

    def _is_player_x(self, player_x):
        return player_x['key'] == self.player_key

    @staticmethod
    def _is_player_winner(player):
        return player['winner'] is True
