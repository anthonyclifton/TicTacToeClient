from random import randint

from tictactoeclient.configuration import CLIENT_UPDATE_HOST, CREATE_GAME_NAME, CREATE_PLAYER_NAME, JOIN_PLAYER_NAME, \
    CREATE_PORT, JOIN_PORT

GAME_COMPLETED = 4
LOBBY_PORT = randint(44100, 44199)

CORNER_MARKER = '+'
HORIZONTAL_BORDER = '-'
VERTICAL_BORDER = '|'
X_MARKER = 'X'
O_MARKER = 'O'
EMPTY_MARKER = ' '

VALUE_TO_MARKER = {
    1: O_MARKER,
    2: X_MARKER
}


class GameService(object):
    def __init__(self, t3_api_service):
        self.t3_api_service = t3_api_service
        self.game_creator = False
        self.lobby = False
        self.player_key = None

    def process_update(self, updated_game):
        self.render(updated_game)
        if updated_game['state'] == GAME_COMPLETED:
            move = {'x': -1, 'y': -1}

            print ""
            if self.game_creator:
                if updated_game['player_x']['winner']:
                    print("I won!")
                else:
                    print("I lost!")
            elif self.lobby:
                if self._is_player_x(updated_game):
                    if updated_game['player_x']['winner']:
                        print("I won!")
                    else:
                        print("I lost!")
                else:
                    if updated_game['player_o']['winner']:
                        print("I won!")
                    else:
                        print("I lost!")
            else:
                if updated_game['player_o']['winner']:
                    print("I won!")
                else:
                    print("I lost!")
        else:
            move = self.game_loop(updated_game)

        return move

    def game_loop(self, updated_game):
        move_x, move_y = self.analyze(updated_game)
        return {'x': move_x, 'y': move_y}

    @staticmethod
    def analyze(updated_game):
        unmarked_cells = []
        for y in range(0, updated_game['size_y']):
            for x in range(0, updated_game['size_x']):
                if not next((cell for cell in updated_game['cells'] if
                             cell['x'] == x and cell['y'] == y), None):
                    unmarked_cells.append((x, y))

        next_move = unmarked_cells[randint(0, len(unmarked_cells) - 1)]

        return next_move[0], next_move[1]

    def render(self, updated_game):
        size_x = updated_game['size_x']
        size_y = updated_game['size_y']
        grid = [[EMPTY_MARKER for x in range(size_x)] for y in range(size_y)]

        for cell in updated_game['cells']:
            row = cell['y']
            column = cell['x']
            cell_marker = VALUE_TO_MARKER[cell['value']]
            grid[row][column] = cell_marker

        print ""
        print "Game: {}".format(updated_game['name'])
        print "Player X: {}".format(updated_game['player_x']['name'])
        print "Player O: {}".format(updated_game['player_o']['name'])
        self._draw_horizontal_border(size_x)

        for row in grid:
            line = VERTICAL_BORDER
            for column in row:
                line = line + column
            line = line + VERTICAL_BORDER
            print line

        self._draw_horizontal_border(size_x)

    @staticmethod
    def _draw_horizontal_border(size_x):
        print "{}{}{}".format(CORNER_MARKER,
                              (HORIZONTAL_BORDER * size_x),
                              CORNER_MARKER)

    def create(self):
        update_url = "http://{}:{}".format(CLIENT_UPDATE_HOST, self.get_port())
        game = self.t3_api_service.create_game(CREATE_GAME_NAME, CREATE_PLAYER_NAME, update_url)
        print ""
        print("To join this game, run:")
        print("./join {}".format(game['key']))

    def join_async(self, game_key):
        update_url = "http://{}:{}".format(CLIENT_UPDATE_HOST, self.get_port())
        self.t3_api_service.join_game(game_key, JOIN_PLAYER_NAME, update_url)

    def enter_lobby(self):
        update_url = "http://{}:{}".format(CLIENT_UPDATE_HOST, self.get_port())
        player = self.t3_api_service.enter_lobby(JOIN_PLAYER_NAME, update_url)
        self.player_key = player['key']
        print ""
        print("Entered lobby as: {}, using key: {}".format(player['name'], player['key']))

    def get_port(self):
        if self.game_creator:
            return CREATE_PORT
        elif self.lobby:
            return LOBBY_PORT
        else:
            return JOIN_PORT

    def _is_player_x(self, updated_game):
        return updated_game['player_x']['key'] == self.player_key
