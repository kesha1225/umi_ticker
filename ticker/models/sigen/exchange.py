import pydantic

from ticker.enum import SigenExchangePair, CryptoCurrency


class ExchangeOrder(pydantic.BaseModel):
    id: str
    last: float
    lowest_ask: str = pydantic.Field(alias="lowestAsk")
    highest_bid: str = pydantic.Field(alias="highestBid")
    percent_change: str = pydantic.Field(alias="percentChange")
    base_volume: str | int = pydantic.Field(alias="baseVolume")
    quote_volume: str | int = pydantic.Field(alias="quoteVolume")
    is_frozen: int = pydantic.Field(alias="isFrozen")
    high_24_hour: str | int = pydantic.Field(alias="high24hr")
    low_24_hour: str | int = pydantic.Field(alias="low24hr")


class CoinInfo(pydantic.BaseModel):
    name: str
    withdraw: str
    deposit: str


PAIRS = dict[SigenExchangePair, ExchangeOrder]
COINS = dict[CryptoCurrency, CoinInfo]


class PairsData(pydantic.BaseModel):
    pairs: PAIRS
    coins: COINS


class ExchangeResponse(pydantic.BaseModel):
    success: bool
    data: PairsData
    code: int | None
    run_time: float

    def get_pair_last_price(self, pair: SigenExchangePair) -> float:
        return self.data.pairs[pair].last
