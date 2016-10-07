import requests
import threading
import hashlib

credentials = ('learning','learning')

api_base = 'https://msesandbox.cisco.com:8081/api'

list_clients = '/location/v1/clients'

floor_id = '723413320329068590'

def get_all_clients():
    data = {
        "floorRefId": floor_id
    }

    clients = requests.get(api_base + list_clients, data, auth=credentials)

    return clients.json()


def freeze(d):
    if isinstance(d, dict):
        return frozenset((key, freeze(value)) for key, value in d.items())
    elif isinstance(d, list):
        return tuple(freeze(value) for value in d)
    return d

def tick():
    threading.Timer(0.1, tick).start()
    clients = get_all_clients()

    print(hash(freeze(clients)))

    #print(len(clients))
