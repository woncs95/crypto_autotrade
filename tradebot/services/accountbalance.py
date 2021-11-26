import pandas as pd
import requests
import json
import time
from hmac_sha256 import hmac_sha256
import numpy as np


async def account_balance(key):
    url, api_key, secret_key = key
    req = {
        "id": 0,
        "method": "private/get-account-summary",
        "api_key": api_key,
        "params": {},
        "nonce": int(time.time() * 1000)
    }
    await hmac_sha256(secret_key, req)
    while True:
        try:
            balance = requests.post(url + "private/get-account-summary",
                                    json=req, headers={'Content-Type': 'application/json'})
            info = json.loads(balance.text)
            balance = info['result']['accounts']
            return balance
        except (ConnectionError, ValueError, KeyError, IOError, EOFError, KeyboardInterrupt, TypeError):
            # send_warning("Error in Account Balance... Trying again")
            continue


async def balance_usdt(key):
    balance = await account_balance(key)
    df = pd.DataFrame(balance)
    row = df[df['currency'].str.match('USDT')]
    value = float(row['available'])
    return value


async def balance_btc(key):
    balance = await account_balance(key)
    df = pd.DataFrame(balance)
    row = df[df['currency'].str.match('BTC')]
    value = float(row['available'])
    value = np.floor(value * 1e6) / 1e6
    return value
