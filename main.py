import atexit
import json

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, Response
import argparse

from tictactoeclient.configuration import SERVER_BASE_URL, CREATE_PORT, JOIN_PORT, CREATE_PLAYER_NAME, \
    JOIN_PLAYER_NAME, CREATE_GAME_NAME, CLIENT_BIND_ADDRESS, CLIENT_UPDATE_HOST
from tictactoeclient.schemas.game_schema import GameSchema
from tictactoeclient.services.game_service import GameService
from tictactoeclient.services.t3_api_service import T3ApiService

GAME_COMPLETED = 4

app = Flask(__name__)
t3_api_service = T3ApiService(SERVER_BASE_URL)
game_service = GameService(t3_api_service)

scheduler = BackgroundScheduler()
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

game_creator = False


def create():
    update_url = "http://{}:{}/update".format(CLIENT_UPDATE_HOST, CREATE_PORT)
    game = t3_api_service.create_game(CREATE_GAME_NAME, CREATE_PLAYER_NAME, update_url)
    print("To join this game, run:")
    print("./join {}".format(game['key']))


def join_async(game_key):
    update_url = "http://{}:{}/update".format(CLIENT_UPDATE_HOST, JOIN_PORT)
    t3_api_service.join_game(game_key, JOIN_PLAYER_NAME, update_url)


@app.route('/update', methods=['POST'])
def update():
    print "Received Update: {}".format(request.data)
    updated_game, errors = GameSchema().loads(request.data)

    if errors:
        print("Errors: {}".format(errors))

    if updated_game['state'] == GAME_COMPLETED:
        move = {'x': -1, 'y': -1}

        if game_creator:
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
        move = game_service.game_loop(updated_game)

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
    create_parser.set_defaults(func=create)

    join_parser = subparsers.add_parser('join', help='join game help')
    join_parser.add_argument("game_key", help="game key")
    join_parser.set_defaults(func=join_async)

    args = parser.parse_args()

    if args.func is create:
        game_creator = True
        create()
    elif args.func is join_async:
        scheduler.add_job(
            func=join_async,
            args=[args.game_key],
            id='join',
            name='Join a game that is started',
            replace_existing=True)

    app.run(host=CLIENT_BIND_ADDRESS, port=(CREATE_PORT if game_creator else JOIN_PORT))
