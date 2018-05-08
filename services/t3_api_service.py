
import requests


class T3ApiService(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def create_game(self):
        pass

    def join_game(self):
        pass

    def mark_cell(self):
        pass

    def ping(self):
        url = 'http://localhost:3334/ping'
        payload = {
            'myurl': 'my own url'
        }
        self.generic_post(url, payload)

    def generic_get(self, url):
        pass

    def generic_post(self, url, payload):
        # base_url = "www.server.com"
        # final_url = "/{0}/friendly/{1}/url".format(base_url, uuid4())
        #
        # payload = {'number': 2, 'value': 1}
        requests.post(url, data=payload)
