import json
from time import sleep

import requests


class Nemesis:
    BASE_API_URL = 'http://localhost:8000'

    def __init__(self, username='red', url=None):
        self.player = username
        self.api_url = url or self.BASE_API_URL

    def connect(self):
        print(requests.get(self.api_url + f'/connect/{self.player}/').json()['message'])

    def select_enemy(self):
        try:
            return requests.post(self.api_url + f'/enemies/select/{self.player}/').json()
        except json.JSONDecodeError:
            print("No available enemies")
            return

    def kill(self, enemy_id, answer):
        response = requests.post(
            self.api_url + f'/enemies/{enemy_id}/kill/',
            json={'nemesis': json.dumps(answer)},
        )
        print(response.json()['message'])
        return response

    def run_autofire(self, type_to_handler_map: dict):
        run = True
        while run:
            enemy = self.select_enemy()
            if not enemy:
                print("Zzz...")
            elif enemy['type'] in type_to_handler_map:
                response = self.kill(
                    enemy['id'],
                    type_to_handler_map[enemy['type']](enemy)
                )
                if 'Failed' in response.json()['message']:
                    run = False
            else:
                print(f"Unknown enemy type: \"{enemy['type']}\"; to kill -- {enemy['task']}")
                run = False
