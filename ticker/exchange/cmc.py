import aiohttp
from aiocache import cached

from ticker.constants import CMC_PRICE_CACHE_TIME
from ticker.enum import Currency
from ticker.exchange.base import BaseExchange
from ticker.models.cmc.exchange import CoinMarketCapExchangeResponse
from ticker_config import CMC_API_KEY


class CoinMarketCupExchange(BaseExchange):
    def __init__(self, session: aiohttp.ClientSession):
        super().__init__(session=session, base_path="https://pro-api.coinmarketcap.com")
        self.session.headers.update(
            {
                "X-CMC_PRO_API_KEY": CMC_API_KEY,
            }
        )

    async def get_currency_from_to_data(
        self, currency_from: Currency, currency_to: Currency
    ) -> CoinMarketCapExchangeResponse:
        return CoinMarketCapExchangeResponse(
            **await self.request(
                method="GET",
                path="/v1/cryptocurrency/quotes/latest",
                params={"symbol": currency_from, "convert": currency_to},
            )
        )

    async def get_price(self, currency_from: Currency, currency_to: Currency) -> float:
        return (
            (
                await self.get_currency_from_to_data(
                    currency_from=currency_from, currency_to=currency_to
                )
            )
            .data[currency_from]
            .quote[currency_to]
            .price
        )

    @cached(ttl=CMC_PRICE_CACHE_TIME)
    async def get_cached_price(
        self, currency_from: Currency, currency_to: Currency
    ) -> float:
        return await self.get_price(
            currency_from=currency_from, currency_to=currency_to
        )
