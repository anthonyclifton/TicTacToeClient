class GameService(object):
    def __init__(self, t3_api_service):
        self.t3_api_service = t3_api_service

    def game_loop(self, updated_game):
        self.render(updated_game)
        move_x, move_y = self.analyze(updated_game)
        self.move(move_x, move_y)

    @staticmethod
    def analyze(updated_game):
        # generate random cell
        # if not filled, use it
        # else repeat
        return 0, 0

    @staticmethod
    def move(self, x, y):
        del x, y
        pass

    @staticmethod
    def render(self, updated_game):
        del updated_game
        pass
