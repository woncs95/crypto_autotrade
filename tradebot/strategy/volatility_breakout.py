from candlestick import get_candlestick
from scipy.interpolate import *
import pandas as pd
import numpy as np


# 변동성돌파전략 - 구매가, 판매가 정하기
async def get_target_price(instrument, k):
    candle = await get_candlestick(instrument, "1D")
    # today open price + (yesterday highest + yesterday lowest)*0.5
    yesterday = candle.iloc[-2]
    today = candle.iloc[-1]
    yesterday_prce_difference = yesterday["h"] - yesterday["l"]
    buy_target = today["o"] + (yesterday_prce_difference * k)
    sell_target1 = buy_target + yesterday_prce_difference * 0.5
    sell_target1 = np.floor(sell_target1 * 100) / 100
    sell_target2 = buy_target * 1.015
    sell_target2 = np.floor(sell_target2 * 100) / 100
    buy_target_price = np.floor(buy_target * 100) / 100
    sell_target_price = max(sell_target1, sell_target2)
    return buy_target_price, sell_target_price
