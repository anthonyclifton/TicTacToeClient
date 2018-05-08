import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, request
import argparse
import json

from services.t3_api_service import T3ApiService

t3_api_service = T3ApiService('some-base-url')

app = Flask(__name__)


def ping():
    print("Pinging server")
    t3_api_service.ping()


scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=ping,
    trigger=IntervalTrigger(seconds=5),
    id='ping_server',
    name='Ping server every five seconds',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


def start():
    pass


@app.route('/pong', methods=['POST'])
def update():
    data = json.loads(request.data)
    print("Pong from server {}".format(data["pong"]))
    return "OK"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='t3client', description='Tic Tac Toe Client')
    subparsers = parser.add_subparsers(help='sub-command help')

    start_parser = subparsers.add_parser('start', help='start help')
    start_parser.set_defaults(func=start)

    args = parser.parse_args()
    args.func()

    app.run(host='0.0.0.0', port=3333)
