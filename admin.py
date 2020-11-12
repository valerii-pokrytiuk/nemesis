import inspect
import json
import random
from time import sleep

import tasks

from redis import Redis

from serializers import EnemySchema


ZERG_BREEDS = [
    'Drone',
    'Zergling',
    # 'Baneling',
    'Roach',
    'Ravager',
    'Hydralisk',
    'Queen',
    'Ultralisk',
]

COMPLEXITY_TO_BREED = {
    0: ['Drone'],
    1: ['Zergling'],
    2: ['Roach'],
    3: ['Hydralisk'],
    4: ['Ravager']
}


class ID:
    id = 0

    @classmethod
    def next(cls):
        cls.id += 1
        return cls.id


def spawn_wave(complexity, players_number, enemies):
    # Spawn starting enemies
    for _ in range(enemies):
        spawn_enemy(complexity)

    # Sustain wave
    while True:
        enemies_keys = [key for key in redis.scan_iter("enemy:*")]
        if len(enemies_keys) < players_number:
            spawn_enemy(complexity)
        sleep(2)


def spawn_enemy(complexity):
    allowed_tasks = [task for task in tasks_list if task.complexity <= complexity]
    task = random.choice(allowed_tasks)()
    enemy = {
        'id': ID.next(),
        'breed': random.choice(COMPLEXITY_TO_BREED[task.complexity]),
        'type': type(task).__name__,
        'task': task.task,
        'data': task.data,
        'nemesis': json.dumps(task.solution),
    }
    enemy_encoded = EnemySchema().dumps(enemy)
    redis.set(f'enemy:{enemy["id"]}', enemy_encoded)
    redis.publish('game-commands', f'create {enemy["breed"]} {enemy["id"]}')


def clear():
    for key in redis.scan_iter("enemy:*"):
        enemy = EnemySchema().loads(redis.get(key))
        redis.publish('game-commands', f'kill {enemy["id"]}')
        redis.delete(key)


redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)

tasks_list = []
for name, obj in inspect.getmembers(tasks):
    if inspect.isclass(obj) and issubclass(obj, tasks.Task) and name != 'Task':
        tasks_list.append(obj)

if __name__ == '__main__':
    spawn_wave(0, 1, 5)