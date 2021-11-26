from dataclasses import dataclass
from typing import Optional
from Bitcoin_Tradebot.common.constants import CURRENCIES

@dataclass
class Currency:
    short    : str
    longName : str
    symbol   : Optional[str] = ""

@dataclass
class CryptoWallet:
    """Represents a wallet
    """
    amount   : float
    currency : Currency = CURRENCIES["BTC"]
    