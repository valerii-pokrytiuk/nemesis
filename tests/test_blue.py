import client

nemesis = client.Nemesis(username='blue')
nemesis.connect()

database = {
    'Echo': lambda x: x['data'],
    'Constant': lambda x: 'Goodbye world',
}
nemesis.autofire(database)
