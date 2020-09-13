# 9/13/2020
# Test interface to initiate a game between local host and opponent

import requests

r = requests.get('https://lichess.org/api/account', auth=('user', 'pass'))
# I dont know how to add header with requests api (curl -H)
print(r.content)