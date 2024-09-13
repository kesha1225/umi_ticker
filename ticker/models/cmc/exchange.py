import datetime

from pydantic import BaseModel


class Status(BaseModel):
    timestamp: datetime.datetime
    error_code: int
    error_message: str | None
    elapsed: int
    credit_count: int
    notice: str | None


class Platform(BaseModel):
    id: int
    name: str
    symbol: str
    slug: str
    token_address: str


class Quote(BaseModel):
    price: float
    volume_24h: float
    volume_change_24h: float
    percent_change_1h: float
    percent_change_24h: float
    percent_change_7d: float
    percent_change_30d: float
    percent_change_60d: float
    percent_change_90d: float
    market_cap: float
    market_cap_dominance: float
    fully_diluted_market_cap: float
    tvl: float | None
    last_updated: datetime.datetime


class CryptocurrencyData(BaseModel):
    id: int
    name: str
    symbol: str
    slug: str
    num_market_pairs: int
    date_added: datetime.datetime
    tags: list[str]
    max_supply: float | None
    circulating_supply: float
    total_supply: float
    platform: Platform | None
    is_active: int
    infinite_supply: bool
    cmc_rank: int
    is_fiat: int
    self_reported_circulating_supply: float | None
    self_reported_market_cap: float | None
    tvl_ratio: float | None
    last_updated: datetime.datetime
    quote: dict[str, Quote]


class CoinMarketCapExchangeResponse(BaseModel):
    status: Status
    data: dict[str, CryptocurrencyData]
