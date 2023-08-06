from http import HTTPStatus

from .base import HttpClient
from . import exceptions


class Game(HttpClient):
    _game_instance = None

    def create(self, **kwargs):
        resp = self.post("games", json=kwargs)
        self._game_instance = resp.json()

    def get_one(self, game_id):
        resp = self.get(f"games/{game_id}")
        if resp.status_code == HTTPStatus.NOT_FOUND:
            raise exceptions.GameNotfound(f"Game {game_id} does not exist")
        self._game_instance = resp.json()

    def events(self, game_id):
        resp = self.get(f"games/{game_id}/events")
        if resp.status_code == HTTPStatus.NOT_FOUND:
            raise exceptions.GameNotfound(f"Game {game_id} does not exist")
        return resp.json()

    def click(self, row, col):
        game_id = self._game_instance["id"]
        data = {
            "row": row,
            "col": col,
        }

        resp = self.post(f"games/{game_id}/events", json=data)
        return resp.json()
