import json
import requests
import pandas as pd


async def get_candlestick(instrument_name, timeframe):
    url = "https://api.crypto.com/v2/"
    while True:
        try:
            infos = requests.get(url+"public/get-candlestick?instrument_name="
                                 + instrument_name+"&timeframe="+timeframe)
            info = json.loads(infos.text)
            result = info["result"]["data"]
            df = pd.DataFrame(result)
            return df
        except (ConnectionError, ValueError, KeyError, IOError, EOFError, KeyboardInterrupt, TypeError):
            continue


def get_candlestick_sync(instrument_name, timeframe):
    url = "https://api.crypto.com/v2/"
    while True:
        try:
            infos = requests.get(url+"public/get-candlestick?instrument_name="
                                 + instrument_name+"&timeframe="+timeframe)
            info = json.loads(infos.text)
            result = info["result"]["data"]
            df = pd.DataFrame(result)
            return df
        except (ConnectionError, ValueError, KeyError, IOError, EOFError, KeyboardInterrupt, TypeError):
            continue
