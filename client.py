import json

import requests


class Nemesis:
    BASE_API_URL = 'https://d28128fd7359.ngrok.io'

    def __init__(self, base_url=None):
        self.base_url = base_url or self.BASE_API_URL

    def enemies(self):
        return json.loads(
            requests.get(
                self.base_url + '/enemies/',
            ).text
        )

    def scan_enemy(self, enemy_id):
        return json.loads(
            requests.get(
                self.base_url + f'/enemies/{enemy_id}/',
            ).text
        )

    def transmit(self, enemy_id, answer):
        ret = requests.post(
            self.base_url + f'/enemies/{enemy_id}/transmit/',
            json={'transmission': answer},
        )
        try:
            print(json.loads(ret.text))
        except Exception:
            print(ret)
            
    def connect(self):
        print(requests.get(
            self.base_url + f'/connect/',
        ).text)