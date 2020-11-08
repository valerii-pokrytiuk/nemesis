import client

nemesis = client.Nemesis(base_url='http://d28128fd7359.ngrok.io')

for enemy in nemesis.enemies():
    print(enemy)

while True:
    for enemy in nemesis.enemies():
        nemesis.transmit(enemy['id'], enemy['data'])