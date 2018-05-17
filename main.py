import atexit
import json

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, Response
import argparse

from tictactoeclient.configuration import SERVER_BASE_URL, CLIENT_BIND_ADDRESS
from tictactoeclient.schemas.game_schema import GameSchema
from tictactoeclient.services.game_service import GameService
from tictactoeclient.services.t3_api_service import T3ApiService


app = Flask(__name__)
t3_api_service = T3ApiService(SERVER_BASE_URL)
game_service = GameService(t3_api_service)

scheduler = BackgroundScheduler()
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


@app.route('/update', methods=['POST'])
def update():
    print "Received Update: {}".format(request.data)
    updated_game, errors = GameSchema().loads(request.data)

    if errors:
        print("Errors: {}".format(errors))

    move = game_service.process_update(updated_game)

    response = Response(
        response=json.dumps(move),
        status=200,
        mimetype='application/json'
    )

    return response


if __name__ == '__main__':
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
    client_mode = args.mode

    if client_mode is 'create':
        game_service.game_creator = True
        game_service.create()
    elif client_mode is 'join':
        scheduler.add_job(
            func=game_service.join_async,
            args=[args.game_key],
            id='join',
            name='Join a game that is started',
            replace_existing=True)
    elif client_mode is 'lobby':
        game_service.lobby = True
        game_service.enter_lobby()

    app.run(host=CLIENT_BIND_ADDRESS, port=(game_service.get_port()))
