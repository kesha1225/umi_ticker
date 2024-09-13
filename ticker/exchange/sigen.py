import aiohttp

from ticker.exchange.abc import AbstractExchange
from ticker.models.sigen.exchange import ExchangeResponse
from ticker.models.sigen.p2p import P2POffers


class SigenExchange(AbstractExchange):
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        self.base_path = "https://sigen.pro/v1"

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

    async def close(self):
        await self.session.close()

    async def get_p2p_offers_public_list(self) -> P2POffers:
        return P2POffers(
            **await self.request(
                method="GET",
                path="/server-public/p2p/offer/public-list",
            )
        )

    async def get_all_exchange(self) -> ExchangeResponse:
        return ExchangeResponse(
            **await self.request(
                method="GET",
                path="/web-public/exchange/summary",
            )
        )
