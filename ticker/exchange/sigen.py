import aiohttp

from ticker.exchange.base import BaseExchange
from ticker.models.sigen.exchange import ExchangeResponse
from ticker.models.sigen.p2p import P2POffers


class SigenExchange(BaseExchange):
    def __init__(self, session: aiohttp.ClientSession):
        super().__init__(session=session, base_path="https://sigen.pro/v1")

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
