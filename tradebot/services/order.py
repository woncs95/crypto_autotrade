import time
from hmac_sha256 import hmac_sha256
import requests
import json
from telegram_alert import send_telegram_message
from datetime import datetime, timezone


async def buy_order(coin, target_price, amount, key):
    url, api_key, secret_key = key
    req = {
        "id": 0,
        "method": "private/create-order",
        "api_key": api_key,
        "params": {"instrument_name": coin,
                   "side": "BUY",
                   "type": "LIMIT",
                   "price": target_price,
                   "quantity": amount,
                   "time_in_force": "GOOD_TILL_CANCEL",
                   },
        "nonce": int(time.time() * 1000)
    }
    await hmac_sha256(secret_key, req)
    while True:
        try:
            order = requests.post(url + "private/create-order", json=req,
                                  headers={'Content-Type': 'application/json'})
            info = json.loads(order.text)
            if info['code'] == 0:
                send_telegram_message("buy order successful")
            else:
                send_telegram_message("buy order not successful")
                raise ConnectionError
        except (ConnectionError, ValueError, KeyError, IOError, EOFError, KeyboardInterrupt, TypeError):
            continue
        break


async def sell_order(coin, amount, price, key):
    url, api_key, secret_key = key
    req = {
        "id": 0,
        "method": "private/create-order",
        "api_key": api_key,
        "params": {"instrument_name": coin,
                   "side": "SELL",
                   "type": "LIMIT",
                   "price": price,
                   "quantity": amount},
        "nonce": int(time.time() * 1000)
    }
    await hmac_sha256(secret_key, req)
    while True:
        try:
            order = requests.post(url + "private/create-order", json=req,
                                  headers={'Content-Type': 'application/json'})
            info = json.loads(order.text)
            if info['code'] == 0:
                send_telegram_message("sell order successful")
                break
            else:
                send_telegram_message("sell order not successful")
                raise ConnectionError
        except (ConnectionError, ValueError, KeyError, IOError, EOFError, KeyboardInterrupt, TypeError):
            continue


async def sell_order_instant(coin, amount, key):
    url, api_key, secret_key = key
    req = {
        "id": 0,
        "method": "private/create-order",
        "api_key": api_key,
        "params": {"instrument_name": coin,
                   "side": "SELL",
                   "type": "MARKET",
                   "quantity": amount},
        "nonce": int(time.time() * 1000)
    }
    await hmac_sha256(secret_key, req)
    while True:
        try:
            order = requests.post(url + "private/create-order", json=req,
                                  headers={'Content-Type': 'application/json'})
            info = json.loads(order.text)
            if info['code'] == 0:
                send_telegram_message("sell order successful")
                break
            else:
                send_telegram_message("sell order not successful")
                raise ConnectionError
        except (ConnectionError, ValueError, KeyError, IOError, EOFError, KeyboardInterrupt, TypeError):
            continue


async def cancel_all_order(instrument, key):
    url, api_key, secret_key = key
    req = {
        "id": 0,
        "method": "private/cancel-all-orders",
        "api_key": api_key,
        "params": {
            "instrument_name": instrument,
        },
        "nonce": int(time.time() * 1000)
    }
    await hmac_sha256(secret_key, req)
    while True:
        try:
            cancel_order = requests.post(url + "private/cancel-all-orders", json=req,
                                         headers={'Content-Type': 'application/json'})
            info = json.loads(cancel_order.text)
            cancel_order = info['code']
            if cancel_order == 0:
                send_telegram_message("all orders cancel succesfull")
                break
            else:
                send_telegram_message("error in canceling order")
                raise ConnectionError
        except (ConnectionError, ValueError, KeyError, IOError, EOFError, KeyboardInterrupt, TypeError):
            continue


async def get_order_history(instrument, key):
    url, api_key, secret_key = key
    now = datetime.now(timezone.utc)
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    midnight = midnight.timestamp()
    req = {
        "id": 0,
        "method": "private/get-order-history",
        "api_key": api_key,
        "params": {
            "instrument_name": instrument,
        },
        "start_ts": midnight
    }
    await hmac_sha256(secret_key, req)
    while True:
        try:
            order_history = requests.post(url + "private/get-order-history", json=req,
                                          headers={'Content-Type': 'application/json'})
            response = json.loads(order_history.text)
            order_list = response['order_list']
            return order_list
        except (ConnectionError, ValueError, KeyError, IOError, EOFError, KeyboardInterrupt, TypeError):
            continue


async def check_filled_order(instrument, key, position):
    order_list = await get_order_history(instrument, key)

    # order_list ={"side":"BUY", "status": "FILLED"}
    for order in order_list:
        order_type = order["side"]
        order_status = order["status"]

        # position shows if buy- & sell orders are complete
        if order_type is "BUY" and order_status is "FILLED":
            position["buy_order"] = True
        if order_type is "SELL" and order_status is "FILLED":
            position["sell_order"] = True

    return position


async def get_open_orders(instrument, key):
    url, api_key, secret_key = key
    req = {
        "id": 2,
        "method": "private/get-open-orders",
        "api_key": api_key,
        "params": {
            "instrument_name": instrument,
            "page_size": 20,
            "page": 0
        },
        "nonce": int(time.time() * 1000)
    }
    await hmac_sha256(secret_key, req)
    order_history = requests.post(url + "private/get-open-orders", json=req,
                                  headers={'Content-Type': 'application/json'})
    info = json.loads(order_history.text)
    order_history = info
    return order_history
