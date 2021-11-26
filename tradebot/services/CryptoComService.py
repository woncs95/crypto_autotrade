from typing import List
from Bitcoin_Tradebot.datamodels.cryptocom import CandleStickRow, Instrument, Period

from aiohttp import ClientSession
class CryptoComService:
    
    def __init__(self,
                 session: ClientSession,
                 baseUrl = "https://api.crypto.com/v2/"):
        self.baseurl = baseUrl
        self.session = session
        pass
    
    async def getInstruments(self) -> List[Instrument]:
        async with self.session.get(self.getInstrumentsUrl()) as resp:
            responses = await resp.json()
            instrumentsJSONList = responses["result"]["instruments"]
            instruments: List[Instrument] = [ Instrument.fromInstrumentsAPI(x) 
                                               for x in instrumentsJSONList ]
            return instruments
        
    
    async def getDataForInstrumentAndPeriod(self, instrument: Instrument, period: Period):
        async with self.session.get(self.getCandleStickForInstrumentInPeriod(instrument, period)) as resp:
            responses = await resp.json()
            candleSticksJSONList = responses["result"]["data"]
            candleSticks: List[CandleStickRow] = [ CandleStickRow.fromCandleStickAPI(x) 
                                               for x in candleSticksJSONList ]
            return candleSticks
    
    
    #
    # URL Wrapper
    #
    def getPublicAPIUrl(self):
        return "{}/public".format(self.baseurl)
    
    def getInstrumentUrl(self):
        return "{}/get-instruments".format(self.getPublicAPIUrl())
    
    def getCandleStickBaseUrl(self):
        return "{}/get-candlestick".format(self.getPublicAPIUrl())
    
    def getCandleStickForInstrumentInPeriod(self,
                                            instrument: Instrument,
                                            period: Period):
        return "{}?instrument_name={}&timeframe={}".format(
            self.getCandleStickBaseUrl(),
            instrument.instrument_name,
            period.timeframe
        )