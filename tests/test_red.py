import client

nemesis = client.Nemesis(username='red')
nemesis.connect()

database = {
    'Echo': lambda x: x['data'],
}
nemesis.autofire(database)
