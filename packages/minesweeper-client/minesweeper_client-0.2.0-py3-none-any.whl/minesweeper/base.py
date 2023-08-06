import os

import requests
from retry import retry

from .constants import RETRY_DELAY, RETRY_TRIES


class HttpClient:
    _api_base = os.getenv("MINES_API", "https://minesweeper.makecodes.dev")
    _headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
    }

    @retry(tries=RETRY_TRIES, delay=RETRY_DELAY)
    def post(self, resource, **kwargs):
        return requests.post(
            f"{self._api_base}/{resource}", headers=self.headers(**kwargs), **kwargs
        )

    @retry(tries=RETRY_TRIES, delay=RETRY_DELAY)
    def get(self, resource, **kwargs):
        return requests.get(
            f"{self._api_base}/{resource}", headers=self.headers(**kwargs), **kwargs
        )

    def headers(self, **kwargs):
        headers = {}
        headers.update(kwargs.get("headers", {}))
        return headers
