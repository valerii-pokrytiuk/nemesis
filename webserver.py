import json
from time import sleep

from bottle import request, response, run
from bottle import post, get, put, delete
from redis import Redis

from serializers import EnemySchema

redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)


@get('/connect/')
def connection_handler():
    return "Connection successful"


@get('/enemies/')
def enemies_list_handler():
    color = request.query.get('color')
    enemies = []
    for key in redis.scan_iter("enemy:*"):
        enemy = json.loads(redis.get(key))
        if not color or color == enemy['color']:
            enemies.append(enemy)
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


@post('/enemies/<pk>/kill/')
def kill_handler(pk):
    data = request.json
    enemy = redis.get(f'enemy:{pk}')

    if not enemy:
        response.headers['Content-Type'] = 'application/json'
        return json.dumps({"message": "Not Found"})

    enemy = EnemySchema().loads(enemy)
    nemesis = data.get('nemesis')
    if nemesis == enemy['nemesis']:
        redis.publish('game-commands', f'kill {enemy["breed"]} {enemy["color"]}')
        redis.delete(f'enemy:{pk}')
        ret = json.dumps({"message": "Success!"})
    else:
        ret = json.dumps({"message": "Failed!"})
    response.headers['Content-Type'] = 'application/json'
    return ret


@post('/send-command/')
def send_command():
    command = request.json.get('command')
    redis.publish('game-commands', command)
    return


if __name__ == "__main__":
    run(host='0.0.0.0', port=8000)
