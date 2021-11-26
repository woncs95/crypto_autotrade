from Bitcoin_Tradebot.datamodels.wallet import Currency

# A List of Predefined Currencies
CURRENCIES = {
    "BTC"  : Currency("BTC", "BITCOIN", "₿"),
    "USDT" : Currency("USDT", "USD_TETHER", "₿<>$"),
    "USD"  : Currency("USD", "US DOLLER", "$"),
    "ETH"  : Currency("ETH", "ETHERIUM"),
}