import json

import requests


class Nemesis:
    BASE_API_URL = 'http://localhost:8000'

    def __init__(self, color='red', api_url=None):
        self.color = color
        self.api_url = api_url or self.BASE_API_URL
        self.database = {}

    def get_enemies_list(self, only_my=True):
        url = f'{self.api_url}/enemies/'
        if only_my:
            url += f'?color={self.color}'
        return requests.get(url).json()

    def get_enemy(self, enemy_id):
        return requests.get(self.api_url + f'/enemies/{enemy_id}/').json()

    def kill(self, enemy_id, answer, silent=False):
        response = requests.post(
            self.api_url + f'/enemies/{enemy_id}/kill/',
            json={'nemesis': json.dumps(answer)},
        )
        if not silent:
            print(response.json())
        return response

    def connect(self):
        print(requests.get(self.api_url + f'/connect/').text)

    def cycle(self):
        run = True
        while run:
            for enemy in self.enemies():
                if enemy['type'] in self.database:
                    self.kill(enemy['id'], self.database[enemy['type']](enemy), silent=True)
                else:
                    print(f"Unknown enemy type: {enemy['type']}; to kill -- {enemy['to_kill']}")
                    run = False
                    break
