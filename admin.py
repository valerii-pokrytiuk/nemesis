import inspect
import random
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


class ID:
    id = 0

    @classmethod
    def next(cls):
        cls.id += 1
        return cls.id


def spawn_wave(complexity):
    for _ in range(5):
        allowed_tasks = [task for task in TASKS_LIST if task.complexity <= complexity]
        task = random.choice(allowed_tasks)()
        enemy = {
            'id': ID.next(),
            'breed': random.choice(COMPLEXITY_TO_BREED[task.complexity]),
            'type': type(task),
            'to_kill': task.task,
            'data': task.data,
            'nemesis': task.solution,
        }
        enemy_encoded = EnemySchema().dumps(enemy)
        redis.set(f'enemy:{enemy["id"]}', enemy_encoded)
        redis.publish('game-commands', f'create {enemy["breed"]} 1')


def clear_enemies_db():
    for key in redis.scan_iter("enemy:*"):
        redis.delete(key)
