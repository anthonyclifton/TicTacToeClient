import unittest

from main import _get_port, _get_update_url
from tictactoeclient.configuration import CREATE_PORT, JOIN_PORT, CLIENT_UPDATE_HOST
from tictactoeclient.constants import LOBBY_PORT, CREATE_GAME_MODE, LOBBY_MODE, JOIN_GAME_MODE


class TestMain(unittest.TestCase):
    def test__get_port__returns_create_port_when_in_create_game_mode(self):
        port = _get_port(CREATE_GAME_MODE)
        self.assertEqual(CREATE_PORT, port)

    def test__get_port__returns_lobby_port_when_in_lobby_mode(self):
        port = _get_port(LOBBY_MODE)
        self.assertEqual(LOBBY_PORT, port)

    def test__get_port__returns_join_port_when_in_join_game_mode(self):
        port = _get_port(JOIN_GAME_MODE)
        self.assertEqual(JOIN_PORT, port)

    def test__get_update_url__returns_legitimate_url_from_our_host_and_port(self):
        port = 1234
        url = _get_update_url(port)
        self.assertEqual("http://{}:{}".format(CLIENT_UPDATE_HOST, port), url)
