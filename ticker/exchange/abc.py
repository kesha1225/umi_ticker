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
