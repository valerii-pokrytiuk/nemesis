import json

import requests


class Nemesis:
    BASE_API_URL = 'http://localhost:8000/'

    def __init__(self, username, base_url=None):
        self.token = username
        self.base_url = base_url or self.BASE_API_URL

    def enemies(self):
        return json.loads(
            requests.get(
                self.BASE_API_URL + 'enemies/',
            ).text
        )

    def scan_enemy(self, enemy_id):
        return json.loads(
            requests.get(
                self.BASE_API_URL + f'enemies/{enemy_id}/',
            ).text
        )

    def transmit(self, enemy_id, answer):
        print(json.loads(
            requests.post(
                self.BASE_API_URL + f'enemies/{enemy_id}/transmit/',
                json={'transmission': answer},
            ).text
        ))
