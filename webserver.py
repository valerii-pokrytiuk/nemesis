import json
from time import sleep

from bottle import request, response, run
from bottle import post, get, put, delete
from redis import Redis

redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)


@get('/enemies/')
def enemies_list_handler():
    enemies = []
    for key in redis.scan_iter("enemy:*"):
        enemies.append(json.loads(redis.get(key)))
    response.headers['Content-Type'] = 'application/json'
    return json.dumps(enemies)


@get('/enemies/<pk>/')
def enemies_detail_handler(pk):
    enemy = redis.get(f'enemy:{pk}')
    if enemy:
        response.headers['Content-Type'] = 'application/json'
        return json.dumps(enemy)
    response.status_code = 404
    return


@post('/enemies/<pk>/transmit/')
def transmission_handler(pk):
    data = request.json
    enemy = redis.get(f'enemy:{pk}')

    if not enemy:
        response.status_code = 404
        return

    transmission = data.get('transmission')
    enemy = json.loads(enemy)
    if transmission == enemy['nemesis']:
        redis.publish('game-commands', f'kill {enemy["breed"]}')
        redis.delete(f'enemy:{pk}')
        ret = json.dumps({"message": "Success!"})
    else:
        ret = json.dumps({"message": "Failed!"})

    response.headers['Content-Type'] = 'application/json'
    sleep(5)
    return ret


@post('/send-command/')
def send_command():
    command = request.json.get('command')
    redis.publish('game-commands', command)
    return


if __name__ == "__main__":
    run(host='0.0.0.0', port=8000)
