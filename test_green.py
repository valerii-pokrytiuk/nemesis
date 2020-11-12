import client

nemesis = client.Nemesis(username='green')
nemesis.connect()

database = {
    'Echo': lambda x: x['data'],
}
nemesis.autofire(database)
