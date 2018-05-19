import json
import logging

import requests
from flask import Flask, request, Response
import argparse

from tictactoeclient.configuration import SERVER_BASE_URL, CLIENT_BIND_ADDRESS, CREATE_PORT, JOIN_PORT, \
    CLIENT_UPDATE_HOST, CREATE_GAME_NAME, CREATE_PLAYER_NAME, JOIN_PLAYER_NAME
from tictactoeclient.schemas.game_schema import GameSchema
from tictactoeclient.services.game_service import GameService, LOBBY_PORT
from tictactoeclient.services.t3_api_service import T3ApiService


app = Flask(__name__)
logging.basicConfig()

tictactoe_api_service = T3ApiService(SERVER_BASE_URL, requests)
game_service = GameService(tictactoe_api_service)


@app.route('/update', methods=['POST'])
def update():
    updated_game, errors = GameSchema().loads(request.data)

    if errors:
        print("Errors: {}".format(errors))

    move = game_service.process_updated_game_from_server(updated_game)

    response = Response(
        response=json.dumps(move),
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def _setup_arg_parser():
    global args
    parser = argparse.ArgumentParser(prog='t3client', description='Tic Tac Toe Client')
    subparsers = parser.add_subparsers(help='sub-command help')
    create_parser = subparsers.add_parser('create', help='create game help')
    create_parser.set_defaults(mode='create')
    join_parser = subparsers.add_parser('join', help='join game help')
    join_parser.add_argument("game_key", help="game key")
    join_parser.set_defaults(mode='join')
    lobby_parser = subparsers.add_parser('lobby', help='enter lobby help')
    lobby_parser.set_defaults(mode='lobby')
    args = parser.parse_args()


def _parse_command_line_arguments(client_mode):
    if client_mode is 'create':
        port = _get_port(create_game_mode=True)
        update_url = _get_update_url(port)
        tictactoe_api_service.create_game(CREATE_GAME_NAME, CREATE_PLAYER_NAME, update_url)
        _run_game_update_listener(port)
    elif client_mode is 'join':
        port = _get_port()
        update_url = _get_update_url(port)
        tictactoe_api_service.join_game(args.game_key, JOIN_PLAYER_NAME, update_url)
        _run_game_update_listener(port)
    elif client_mode is 'lobby':
        port = _get_port(lobby_mode=True)
        update_url = _get_update_url(port)
        tictactoe_api_service.enter_lobby(JOIN_PLAYER_NAME, update_url)
        _run_game_update_listener(port)


def _display_ready_message():
    print "\nGREETINGS PROFESSOR FALKEN."
    print "SHALL WE PLAY A GAME?\n"


def _get_port(create_game_mode=False, lobby_mode=False):
    if create_game_mode:
        return CREATE_PORT
    elif lobby_mode:
        return LOBBY_PORT
    else:
        return JOIN_PORT


def _get_update_url(port):
    return "http://{}:{}".format(CLIENT_UPDATE_HOST, port)


def _run_game_update_listener(port):
    app.run(host=CLIENT_BIND_ADDRESS, port=port)


if __name__ == '__main__':
    _setup_arg_parser()
    _display_ready_message()
    _parse_command_line_arguments(args.mode)
