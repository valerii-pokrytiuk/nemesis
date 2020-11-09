import client

nemesis = client.Nemesis(base_url='http://d28128fd7359.ngrok.io')

for n in nemesis.enemies():
    print(n)

