from flask import Flask, request
import argparse
import json

app = Flask(__name__)


def start():
    app.run()


@app.route('/', methods=['POST'])
def foo():
    data = json.loads(request.data)
    print "New commit by: {}".format(data['commits'][0]['author']['name'])
    return "OK"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='t3client', description='Tic Tac Toe Client')
    subparsers = parser.add_subparsers(help='sub-command help')

    start_parser = subparsers.add_parser('start', help='start help')
    start_parser.set_defaults(func=start)

    args = parser.parse_args()
    args.func()

