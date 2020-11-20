import json
from time import sleep

from bottle import request, response, run, hook
from bottle import post, get, put, delete
from redis import Redis

import constants
from serializers import EnemySchema


redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)


@hook('after_request')
def set_headers():
    response.headers['Content-Type'] = 'application/json'


@get('/connect/<player>/')
def connection_handler(player):
    if player in constants.PLAYERS:
        message = f"Welcome to Nemesis, {player}!"
    else:
        message = "Invalid username!"
    return {"message": message}


@post('/enemies/select/<player>/')
def select_enemy_handler(player):
    enemies = []
    for key in redis.scan_iter("enemy:*"):
        enemy = json.loads(redis.get(key))
        enemies.append(enemy)

    selected_by_player = list(filter(lambda x: x['selected_by'] == player, enemies))
    if selected_by_player:
        return EnemySchema(exclude=['nemesis', 'selected_by']).dumps(selected_by_player[0])
    else:
        not_selected = list(filter(lambda x: x['selected_by'] == "", enemies))
        if not_selected:
            enemy = not_selected[-1]
            enemy['selected_by'] = player
            redis.set(f'enemy:{enemy["id"]}', json.dumps(enemy))
            redis.publish('game-commands', f'select {enemy["id"]} {player}')
            sleep(1)
            return EnemySchema(exclude=['nemesis']).dumps(enemy)

        sleep(1)
        return None


@post('/enemies/<pk>/kill/')
def kill_handler(pk):
    data = request.json
    enemy = redis.get(f'enemy:{pk}')

    if not enemy:
        return {"message": "Not Found"}

    enemy = EnemySchema().loads(enemy)
    nemesis = data.get('nemesis')
    if nemesis == enemy['nemesis']:
        redis.publish('game-commands', f'kill {enemy["id"]}')
        redis.delete(f'enemy:{pk}')
        message = f"Killed {enemy['type']}!"
    else:
        message = f"Failed to kill {enemy['type']}!"

    sleep(1)
    return {"message": message}


@post('/send-command/')
def send_command():
    command = request.json.get('command')
    redis.publish('game-commands', command)
    return


if __name__ == "__main__":
    run(host='0.0.0.0', port=8000)
