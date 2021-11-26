import json
import os


def key_connect():
    url = "https://api.crypto.com/v2/"
    fileDir = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(fileDir, 'keys.json')
    with open(filename) as keys:
        information = json.load(keys)
        api_key = information['api_key']
        secret_key = information['secret_key']
    key = (url, api_key, secret_key)
    return key
