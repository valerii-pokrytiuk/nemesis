import json

import requests


class Nemesis:
    BASE_API_URL = 'http://localhost:8000'

    def __init__(self, color='red', api_url=None):
        self.color = color
        self.api_url = api_url or self.BASE_API_URL
        self.database = {}

    def enemies(self, only_my=True):
        url = f'{self.api_url}/enemies/'
        if only_my:
            url += f'?color={self.color}'
        return requests.get(url).json()

    def scan_enemy(self, enemy_id):
        return requests.get(self.api_url + f'/enemies/{enemy_id}/').json()

    def kill(self, enemy_id, answer):
        response = requests.post(
            self.api_url + f'/enemies/{enemy_id}/kill/',
            json={'nemesis': json.dumps(answer)},
        )
        print(response.json())
            
    def connect(self):
        print(requests.get(self.api_url + f'/connect/').text)
