from typing import Any

from src.core import redis_db


class _Cache:
    def __init__(self):
        self.__cache: dict = dict()

    def set_primary_cache(self, _cache: dict):
        self.__cache = _cache

    async def set_term(self, user_id: int, term: str) -> None:
        await self.__update_cache(user_id, "term", term)

    def get_term(self, user_id: int) -> str:
        return self.__get_from_cache(user_id, "term")

    async def set_subject(self, user_id: int, subject: str) -> None:
        await self.__update_cache(user_id, "subject", subject)

    def get_subject(self, user_id: int) -> str:
        return self.__get_from_cache(user_id, "subject")

    def __init_user_in_cache(self, user_id: int) -> None:
        if not self.__cache.get(user_id):
            self.__cache[user_id] = {
                "term": "",
                "subject": "",
            }

    async def __update_cache(self, user_id: int, key: Any, value: Any) -> None:
        self.__init_user_in_cache(user_id)
        self.__cache[user_id][key] = value

        await redis_db.hmset(user_id, self.__cache[user_id])

    def __get_from_cache(self, user_id: int, key: Any) -> Any:
        self.__init_user_in_cache(user_id)
        return self.__cache[user_id][key]


cache: _Cache = _Cache()
