from abc import ABC, abstractmethod
import aiohttp


class AbstractExchange(ABC):
    session: aiohttp.ClientSession
    base_path: str

    @abstractmethod
    async def request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        data: dict | str | None = None,
    ) -> dict:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass


class BaseExchange(AbstractExchange, ABC):
    base_path: str

    def __init__(self, session: aiohttp.ClientSession, base_path: str):
        self.session = session
        self.base_path = base_path

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

    async def close(self) -> None:
        await self.session.close()
