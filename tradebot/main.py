from services.investbtc import invest_btc
import asyncio

from dotenv import load_dotenv

load_dotenv(".env")

op_mode = False
position = {
    "type": None,
    "amount": 0,
    "buy_order": False,
    "sell_order": False
}
surplus = {
    "begin": 0,
    "before": 0,
    "after": 0
}

asyncio.run(invest_btc(op_mode, position, surplus))