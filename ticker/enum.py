import enum


class OrderType(enum.StrEnum):
    buy = "buy"  # цена по которой продают
    sale = "sale"  # цена по которой покупают


class Currency(enum.StrEnum): ...


class CryptoCurrency(Currency):
    rod = "ROD"
    umi = "UMI"
    btc = "BTC"
    usdt = "USDT"
    ton = "TON"
    not_coin = "NOT"
    ton_usdt = "USDTON"


class FiatCurrency(Currency):
    rub = "RUB"


class SigenExchangePair(enum.StrEnum):
    BTC_USDT = "BTC_USDT"
    NOT_TON = "NOT_TON"
    NOT_USDTON = "NOT_USDTON"
    ROD_BTC = "ROD_BTC"
    ROD_USDT = "ROD_USDT"
    TON_USDTON = "TON_USDTON"
    UMI_BTC = "UMI_BTC"
    UMI_TON = "UMI_TON"
    UMI_USDT = "UMI_USDT"
    UMI_USDTON = "UMI_USDTON"
    USDT_USDTON = "USDT_USDTON"
