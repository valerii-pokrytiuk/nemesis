import json

import requests


class Nemesis:
    BASE_API_URL = 'http://localhost:8000'

    def __init__(self, color='red', base_url=None):
        self.color = color
        self.base_url = base_url or self.BASE_API_URL

    def enemies(self, only_my=True):
        url = f'{self.base_url}/enemies/'
        if only_my:
            url += f'?color={self.color}'
        return json.loads(requests.get(url).text)

    def scan_enemy(self, enemy_id):
        return json.loads(
            requests.get(
                self.base_url + f'/enemies/{enemy_id}/',
            ).text
        )

    def kill(self, enemy_id, answer):
        ret = requests.post(
            self.base_url + f'/enemies/{enemy_id}/kill/',
            json={'nemesis': json.dumps(answer)},
        )
        try:
            print(json.loads(ret.text))
        except Exception:
            print(ret)
            
    def connect(self):
        print(requests.get(self.base_url + f'/connect/').text)
