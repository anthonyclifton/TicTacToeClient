from flask import Flask
import argparse

from services.t3_api_service import T3ApiService

app = Flask(__name__)


def create(server_base_url, game_name, player_name):
    t3_api_service = T3ApiService(server_base_url)
    t3_api_service.create_game(game_name, player_name)
    pass


@app.route('/update', methods=['POST'])
def update():
    # data = json.loads(request.data)
    # print("Pong from server {}".format(data["pong"]))

    # 1. receive an update from the server, that means it's our move
    # 2. analyze our choices
    # 3. send our move
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='t3client', description='Tic Tac Toe Client')

    subparsers = parser.add_subparsers(help='sub-command help')

    create_parser = subparsers.add_parser('create', help='create game help')
    create_parser.set_defaults(func=create)

    args = parser.parse_args()
    args.func()

    app.run(host='0.0.0.0', port=3333)
