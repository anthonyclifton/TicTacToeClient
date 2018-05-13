from random import randint


class GameService(object):
    def __init__(self, t3_api_service):
        self.t3_api_service = t3_api_service

    def game_loop(self, updated_game):
        self.render(updated_game)
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

        next_move = unmarked_cells[randint(0, len(unmarked_cells)-1)]

        return next_move[0], next_move[1]

    @staticmethod
    def render(updated_game):
        del updated_game
        pass
