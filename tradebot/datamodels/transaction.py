from Bitcoin_Tradebot import datamodels
from typing import Optional
from Bitcoin_Tradebot.datamodels.wallet import Currency, CryptoWallet
from dataclasses import dataclass
from datetime import datetime

@dataclass
class CryptoTransaction:
    """Represent a Transaction
    """
    amount    : float
    currency  : Currency
    date      : datetime
    sender    : Optional[CryptoWallet] = None
    recipient : Optional[CryptoWallet] = None

# Actually a Sale is literally a Transaction
# TODO: To be clarified
#@dataclass    
#class CryptoSale:
#    """Represent a Transaction
#    """
#    amount    : float
#    currency  : CryptoCurrency
#    recipient : Optional[CryptoWallet] = None
#    sender    : Optional[CryptoWallet] = None
    