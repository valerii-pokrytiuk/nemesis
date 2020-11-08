import inspect
import random
from time import sleep

import tasks

from redis import Redis

from serializers import EnemySchema


ZERG_BREEDS = [
   'Zergling',
   # 'Baneling',
   'Roach',
   'Ravager',
   'Hydralisk',
   # 'Ultralisk',
   'Queen',
]

COMPLEXITY_TO_BREED = {
    0: ['Zergling'],
    1: ['Roach'],
    2: ['Hydralisk'],
    3: ['Ravager']
}

TASKS_LIST = []
for name, obj in inspect.getmembers(tasks):
    if inspect.isclass(obj) and issubclass(obj, tasks.Task) and name != 'Task':
        TASKS_LIST.append(obj)


redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)
redis_listener = redis.pubsub(ignore_subscribe_messages=True)
redis_listener.subscribe('game-commands')


class ID:
    id = 0

    @classmethod
    def next(cls):
        cls.id += 1
        return cls.id


def spawn_wave(complexity, enemies):
    def _spawn_enemy():
        allowed_tasks = [task for task in TASKS_LIST if task.complexity <= complexity]
        task = random.choice(allowed_tasks)()
        enemy = {
            'id': ID.next(),
            'breed': random.choice(COMPLEXITY_TO_BREED[task.complexity]),
            'type': type(task).__name__,
            'to_kill': task.task,
            'data': task.data,
            'nemesis': task.solution,
        }
        enemy_encoded = EnemySchema().dumps(enemy)
        redis.set(f'enemy:{enemy["id"]}', enemy_encoded)
        redis.publish('game-commands', f'create {enemy["breed"]} 1')

    # spawn
    for _ in range(enemies):
        _spawn_enemy()

    # sustain
    while True:
        while message := redis_listener.get_message():
            if 'kill' in message['data']:
                _spawn_enemy()
        sleep(1)


def clear_enemies_db():
    for key in redis.scan_iter("enemy:*"):
        redis.delete(key)


if __name__ == "__main__":
    spawn_wave(0, 5)
