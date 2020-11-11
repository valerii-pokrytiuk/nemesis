import json
from time import sleep

import requests


class Nemesis:
    BASE_API_URL = 'http://localhost:8000'

    def __init__(self, color='red', url=None):
        self.color = color
        self.api_url = url or self.BASE_API_URL

    def connect(self):
        print(requests.get(self.api_url + f'/connect/').text)

    def get_enemies_list(self, only_my=True):
        url = f'{self.api_url}/enemies/'
        if only_my:
            url += f'?color={self.color}'
        return requests.get(url).json()

    def get_enemy(self):
        return requests.get(self.api_url + f'/enemies/get/').json()

    def kill(self, enemy_id, answer, silent=False):
        response = requests.post(
            self.api_url + f'/enemies/{enemy_id}/kill/',
            json={'nemesis': json.dumps(answer)},
        )
        if not silent:
            print(response.json())
        return response

    def run_auto_fire(self, type_to_def_map: dict):
        run = True
        while run:
            enemy = self.get_enemy()
            if not enemy:
                print("No enemies, Zzz...")
                sleep(1)
            if enemy['type'] in type_to_def_map:
                self.kill(enemy['id'], type_to_def_map[enemy['type']](enemy))
            else:
                print(f"Unknown enemy type: {enemy['type']}; to kill -- {enemy['to_kill']}")
                run = False
