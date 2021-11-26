from candlestick import get_candlestick
import numpy as np


# 5일 이동평균 구하기
async def get_yesterday_ma5(instrument):
    candle = await get_candlestick(instrument, "1D")
    ma = candle["c"].rolling(5).mean()
    ma = np.floor(ma.iloc[-2]*1e6)/1e6
    return ma


# 상승장인가 하락장인가?
async def is_over_ma5(ma, cur_price):
    if cur_price - ma > 0:
        return True
    else:
        return False

