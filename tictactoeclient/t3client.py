import json
import os

from flask import Flask, request
import argparse

from services.t3_api_service import T3ApiService
from schemas.game_schema import GameSchema
from services.game_service import GameService

app = Flask(__name__)
t3_api_service = T3ApiService('http://localhost:3334')
game_service = GameService(t3_api_service)

start_host = os.environ.get("T3_CLIENT_START_HOST", "0.0.0.0")
update_host = os.environ.get("T3_CLIENT_UPDATE_HOST", "127.0.0.1")
port = os.environ.get("T3_CLIENT_PORT", "3333")


def create(game_name, player_name, server_base_url):
    update_url = "http://{}:{}/update".format(update_host, port)
    # t3_api_service = T3ApiService(server_base_url)
    t3_api_service.create_game(game_name, player_name, update_url)


def join(game_key, player_name, server_base_url):
    update_url = "http://{}:{}/update".format(update_host, port)
    # t3_api_service = T3ApiService(server_base_url)
    t3_api_service.join_game(game_key, player_name, update_url)


@app.route('/update', methods=['POST'])
def update():
    print "Received Update"
    updated_game, errors = GameSchema().loads(request.data)
    # game_service.game_loop(updated_game)
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='t3client', description='Tic Tac Toe Client')
    subparsers = parser.add_subparsers(help='sub-command help')

    create_parser = subparsers.add_parser('create', help='create game help')
    create_parser.add_argument("game_name", help="game name")
    create_parser.add_argument("player_name", help="player name")
    create_parser.add_argument("base_url", help="server base url")
    create_parser.set_defaults(func=create)

    join_parser = subparsers.add_parser('join', help='join game help')
    join_parser.add_argument("game_key", help="game key")
    join_parser.add_argument("player_name", help="player name")
    join_parser.add_argument("base_url", help="server base url")
    join_parser.set_defaults(func=join)

    args = parser.parse_args()

    if args.func is create:
        args.func(args.game_name,
                  args.player_name,
                  args.base_url)
    elif args.func is join:
        args.func(args.game_key,
                  args.player_name,
                  args.base_url)

    app.run(host=start_host, port=int(port))
