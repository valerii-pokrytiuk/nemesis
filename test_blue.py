import client

nemesis = client.Nemesis(username='blue')
nemesis.connect()

database = {
    'Echo': lambda x: x['data'],
}
nemesis.autofire(database)
