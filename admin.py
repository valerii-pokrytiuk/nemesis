import inspect
import json
import random
from time import sleep

import tasks

from redis import Redis

from serializers import EnemySchema


redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)


class ID:
    id = 0

    @classmethod
    def next(cls):
        cls.id += 1
        return cls.id


class AdminService:
    PLAYER_COLORS = [
        'red',
        'green',
        'blue',
    ]

    ZERG_BREEDS = [
       'Zergling',
       # 'Baneling',
       'Roach',
       'Ravager',
       'Hydralisk',
       'Queen',
        # 'Ultralisk',
    ]

    COMPLEXITY_TO_BREED = {
        0: ['Zergling'],
        1: ['Roach'],
        2: ['Hydralisk'],
        3: ['Ravager']
    }

    def __init__(self):
        self.tasks_list = []
        for name, obj in inspect.getmembers(tasks):
            if inspect.isclass(obj) and issubclass(obj, tasks.Task) and name != 'Task':
                self.tasks_list.append(obj)

    def spawn_wave(self, complexity, players_number, enemies):
        # Spawn starting enemies
        for color in self.PLAYER_COLORS[:players_number]:
            for _ in range(enemies):
                self.spawn_enemy(color, complexity)

        # Sustain wave
        while True:
            enemies = [EnemySchema().loads(redis.get(key)) for key in redis.scan_iter("enemy:*")]
            for color in self.PLAYER_COLORS[:players_number]:
                if not filter(lambda enemy: enemy['color'] == color, enemies):
                    self.spawn_enemy(color, complexity)
            sleep(1)

    def spawn_enemy(self, color, complexity):
        allowed_tasks = [task for task in self.tasks_list if task.complexity <= complexity]
        task = random.choice(allowed_tasks)()
        enemy = {
            'id': ID.next(),
            'breed': random.choice(self.COMPLEXITY_TO_BREED[task.complexity]),
            'type': type(task).__name__,
            'to_kill': task.task,
            'data': task.data,
            'nemesis': json.dumps(task.solution),
            'color': color,
        }
        enemy_encoded = EnemySchema().dumps(enemy)
        redis.set(f'enemy:{enemy["id"]}', enemy_encoded)
        redis.publish('game-commands', f'create {enemy["breed"]} {color}')

    def clear_enemies_db(self):
        for key in redis.scan_iter("enemy:*"):
            enemy = EnemySchema().loads(redis.get(key))
            redis.publish('game-commands', f'kill {enemy["breed"]} {enemy["color"]}')
            redis.delete(key)
