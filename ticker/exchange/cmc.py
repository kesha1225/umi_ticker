import aiohttp
from aiocache import cached

from ticker.constants import CMC_PRICE_CACHE_TIME
from ticker.enum import Currency
from ticker.exchange.abc import AbstractExchange
from ticker.models.cmc.exchange import CoinMarketCapExchangeResponse
from ticker_config import CMC_API_KEY


class CoinMarketCupExchange(AbstractExchange):
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        self.base_path = "https://pro-api.coinmarketcap.com"
        self.session.headers.update(
            {
                "X-CMC_PRO_API_KEY": CMC_API_KEY,
            }
        )

    async def request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        data: dict | str | None = None,
    ) -> dict:
        response = await self.session.request(
            method=method, url=f"{self.base_path}{path}", params=params, json=data
        )
        json_response = await response.json()
        return json_response

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

    async def close(self) -> None:
        await self.session.close()
