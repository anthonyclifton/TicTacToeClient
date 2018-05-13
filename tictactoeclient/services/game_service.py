from random import randint


class GameService(object):
    def __init__(self, t3_api_service):
        self.t3_api_service = t3_api_service

    def game_loop(self, updated_game):
        # game_key = updated_game['key']
        # player_x = updated_game.get('player_x')
        # player_key = updated_game['player_x']['key'] if player_x else updated_game['player_o']['key']
        self.render(updated_game)
        move_x, move_y = self.analyze(updated_game)
        # self.move(game_key, player_key, move_x, move_y)
        return {'x': move_x, 'y': move_y}

    @staticmethod
    def analyze(updated_game):
        unmarked_cells = []
        for y in range(0, updated_game['size_y']):
            for x in range(0, updated_game['size_x']):
                if not next((cell for cell in updated_game['cells'] if
                             cell['x'] == x and cell['y'] == y), None):
                    unmarked_cells.append((x, y))

        next_move = unmarked_cells[randint(0, len(unmarked_cells)-1)]

        return next_move[0], next_move[1]

        # for attempt in range(0, 10):
        #     rand_x = randint(0, updated_game['size_x'] - 1)
        #     rand_y = randint(0, updated_game['size_y'] - 1)
        #
        #     cell = next((cell for cell in updated_game['cells'] if
        #                  cell['x'] == rand_x and cell['y'] == rand_y), None)
        #
        #     if not cell:
        #         return rand_x, rand_y

    def move(self, game_key, player_key, x, y):
        self.t3_api_service.mark_cell(game_key, player_key, x, y)

    @staticmethod
    def render(updated_game):
        del updated_game
        pass
