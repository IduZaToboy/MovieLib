from typing import List
import aiohttp


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
        if top_title_data["__typename"] == "Film":
            top_film = Titles(
                top_title_data["title"]["russian"],
                top_title_data["id"],
                top_title_data["productionYear"],
                top_title_data["__typename"],
            )
            titles_response.append(top_film)
        else:
            top_film = Titles(
                top_title_data["title"]["russian"],
                top_title_data["id"],
                top_title_data["releaseYears"][0]["start"],
                top_title_data["__typename"],
            )
            titles_response.append(top_film)

        for title in other_titles_data:
            if title["movie"]["__typename"] == "Film":
                other_title = Titles(
                    title["movie"]["title"]["russian"],
                    title["movie"]["id"],
                    title["movie"]["productionYear"],
                    title["movie"]["__typename"],
                )
                titles_response.append(other_title)
            else:
                other_title = Titles(
                    title["movie"]["title"]["russian"],
                    title["movie"]["id"],
                    title["movie"]["releaseYears"][0]["start"],
                    title["movie"]["__typename"],
                )
                titles_response.append(other_title)

        return titles_response
