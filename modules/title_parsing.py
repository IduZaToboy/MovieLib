from typing import List
import aiohttp
import asyncio


from modules.my_classes import Titles
from fake_useragent import UserAgent

ua = UserAgent()


class Client(object):
    """
    Класс для парсинга киношек с кинопоиска
    """

    def __init__(self) -> None:
        self.session = aiohttp.ClientSession()

    async def get_title_by_name(self, name: str) -> List[Titles]:
        response = await self.session.get(
            f"https://www.kinopoisk.ru/api/suggest/v2/?query={name}",
            headers={"User-Agent": ua.random, "X-Requested-With": "XMLHttpRequest"},
        )
        data = await response.json()
        top_title_data = data["suggest"]["top"]["topResult"]["global"]
        other_titles_data = data["suggest"]["top"]["movies"]
        titles_response = []
        top_film = Titles(top_title_data["title"]["russian"], top_title_data["id"])
        titles_response.append(top_film)
        for title in other_titles_data:
            other_title = Titles(title["movie"]["title"]["russian"], title["movie"]["id"])
            titles_response.append(other_title)
        return titles_response
