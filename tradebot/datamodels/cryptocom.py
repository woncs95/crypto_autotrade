from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Instrument:
    """An Instrument ("Exchange-Pair")
    E.g. Bitcoin <> US Dollar Tether
    or Bitcoin <> Etherium
    """
    instrument_name            : str
    quote_currency             : str
    base_currency              : str
    price_decimals             : int
    quantity_decimals          : int
    margin_trading_enabled     : bool
    margin_trading_enabled_5x  : bool
    margin_trading_enabled_10x : bool

    @classmethod
    def fromInstrumentsAPI(cls, objectDict: dict[str, any]) -> Instrument:
        return cls(
            instrument_name            = objectDict["instrument_name"],
            quote_currency             = objectDict["quote_currency"],
            base_currency              = objectDict["base_currency"],
            price_decimals             = objectDict["price_decimals"],
            quantity_decimals          = objectDict["quantity_decimals"],
            margin_trading_enabled     = objectDict["margin_trading_enabled"],
            margin_trading_enabled_5x  = objectDict["margin_trading_enabled_5x"],
            margin_trading_enabled_10x = objectDict["margin_trading_enabled_10x"]
        )


@dataclass
class Period():
    """A Period represents a timespan of data set
    """
    timeframe: str
    
    
@dataclass
class CandleStickRow:
    """A measurement of pricedata at a given point in time

    Returns:
        [type]: [description]
    """
    timestamp    : int 
    openPrice    : float
    highestPrice : float
    lowestPrice  : float
    closedPrice  : float
    volume       : float = 0
    
    @classmethod
    def fromCandleStickAPI(cls, objectDict: dict[str, any]) -> CandleStickRow:
        return cls(
            timestamp     = objectDict["t"],
            openPrice     = objectDict["o"],
            highestPrice  = objectDict["h"],
            lowestPrice   = objectDict["l"],
            closedPrice   = objectDict["c"],
            volume        = objectDict["v"]
        )