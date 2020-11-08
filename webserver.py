import json
from time import sleep

from bottle import request, response, run
from bottle import post, get, put, delete
from redis import Redis

from serializers import EnemySchema

redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)


@get('/connect/')
def connection_handler():
    return "Успішно з'єднано з сервером"


@get('/enemies/')
def enemies_list_handler():
    enemies = []
    for key in redis.scan_iter("enemy:*"):
        enemies.append(json.loads(redis.get(key)))
    response.headers['Content-Type'] = 'application/json'
    return EnemySchema(exclude=['nemesis'], many=True).dumps(enemies)


@get('/enemies/<pk>/')
def enemies_detail_handler(pk):
    enemy = redis.get(f'enemy:{pk}')
    if enemy:
        response.headers['Content-Type'] = 'application/json'
        return EnemySchema(exclude=['nemesis']).dump(EnemySchema().loads(enemy))
    # response.status_code = 404
    return json.dumps({"message": "Not Found"})


LOCKED_ENEMIES = []


@post('/enemies/<pk>/transmit/')
def transmission_handler(pk):
    data = request.json
    enemy = redis.get(f'enemy:{pk}')

    if not enemy:
        response.headers['Content-Type'] = 'application/json'
        return json.dumps({"message": "Not Found"})

    enemy = json.loads(enemy)
    if enemy['id'] in LOCKED_ENEMIES:
        ret = json.dumps({"message": "Locked!"})

    else:
        LOCKED_ENEMIES.append(enemy['id'])
        transmission = data.get('transmission')
        if transmission == enemy['nemesis']:
            redis.publish('game-commands', f'kill {enemy["breed"]}')
            redis.delete(f'enemy:{pk}')
            ret = json.dumps({"message": "Success!"})
            sleep(3)
        else:
            ret = json.dumps({"message": "Failed!"})
            sleep(5)
        LOCKED_ENEMIES.pop(LOCKED_ENEMIES.index(enemy['id']))

    response.headers['Content-Type'] = 'application/json'
    return ret


@post('/send-command/')
def send_command():
    command = request.json.get('command')
    redis.publish('game-commands', command)
    return


if __name__ == "__main__":
    run(host='0.0.0.0', port=8000)
