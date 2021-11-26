import requests
import json
import time
from pymongo import MongoClient


'''username = "chang"
password = "!Lassmichinruhe69"
client = MongoClient('mongodb://%s:%s@csdb.manapot.de' % (username, password))
db = client.crypto
'''


# TODO: Stream
def get_ticker(instrument_name):  # a:price of latest trade
    url = "https://api.crypto.com/v2/"
    for j in range(1, 100):
        try:
            infos = requests.get(url + "public/get-ticker?instrument_name=" + instrument_name)
            info = json.loads(infos.text)
            result = info["result"]["data"]
            price = result['b']
            return price
        except (ConnectionError, ValueError, KeyError, IOError, EOFError, KeyboardInterrupt, TypeError):
            time.sleep(0.1)


# TODO: Promise einbauen
def get_info(instrument_name):  # a:price of latest trade
    url = "https://api.crypto.com/v2/"
    for j in range(1, 100):
        try:
            infos = requests.get(url + "public/get-ticker?instrument_name=" + instrument_name)
            info = json.loads(infos.text)
            result = info["result"]["data"]
            new_result = {"Instrument_Name": result["i"], "current_best_bid": result["b"],
                          "current_best_ask": result["k"], "price_latest_trade": result["a"], "time": result["t"],
                          "24h_traded_volume": result["v"], "24h_lowest_price": result["l"],
                          "24h_price_change": result["c"]}
            return new_result
        except (ConnectionError, ValueError, KeyError, IOError, EOFError, KeyboardInterrupt, TypeError):
            time.sleep(0.1)


'''def save_data_to_db(instrument_name):
    while True:
        data = get_info(instrument_name)
        result = db.btc_usdt.insert_one(data)
        print(result.inserted_id)
        time.sleep(10)
'''

# for i in range(1, 10):
    # save_data_to_db("BTC_USDT")
