import copy
import logging

import aiohttp

from src.core.exceptions import APINotStartupError

logger = logging.getLogger(__name__)


class APIMeta(type):
    def __new__(cls, name: str, bases: tuple, attrs: dict):
        cls._decorate_all_methods(attrs=attrs)
        return type.__new__(cls, name, bases, attrs)

    @classmethod
    def _decorate_all_methods(cls, attrs: dict) -> None:
        exceptions = ("startup", "shutdown")
        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and not attr_name.startswith("__") and attr_name not in exceptions:
                attrs[attr_name] = cls._requires_connection(attr_value)

    @staticmethod
    def _requires_connection(method):
        async def wrapper(self, *args, **kwargs):
            if not hasattr(self, "_session") or not self._session:
                raise APINotStartupError(
                    f"{self.__class__.__name__} is not running. "
                    f"To manage the application lifecycle, use the startup and shutdown "
                    f"methods of the parent API class."
                )

            return await method(self, *args, **kwargs)

        return wrapper


class API(metaclass=APIMeta):
    def __init__(self, config):
        self._url = config.url
        self._session = None
        self._headers = self.default_headers

    async def startup(self) -> None:
        if self._session is not None:
            return
        self._session = aiohttp.ClientSession(base_url=str(self._url), headers=self._headers)

    async def shutdown(self):
        if self._session:
            await self._session.close()

    @property
    def default_headers(self) -> dict:
        headers = {
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": str(self._url),
        }
        return copy.deepcopy(headers)
