from datetime import datetime, timedelta, timezone
from typing import Union


class Users:
    def __init__(
        self, telegram_id: int, datetime_create: Union[datetime, str], id: int = None
    ) -> None:
        self.id = id
        self.telegram_id = telegram_id
        if type(datetime_create) is str:
            self.datetime_create = datetime.fromisoformat(datetime_create).astimezone(
                timezone(timedelta(hours=7))
            )
        elif type(datetime_create) is datetime:
            self.datetime_create = datetime_create
        else:
            raise TypeError


class Titles:
    def __init__(self, name: str, id_kinopoisk: int, year: int, type: str, id: int = None) -> None:
        self.id = id
        self.name = name
        self.year = year
        self.type = type
        self.id_kinopoisk = id_kinopoisk


class TitlesHistory:
    def __init__(
        self,
        user_id: int,
        title_id: int,
        status: str,
        status_change: Union[datetime, str],
        id: int = None,
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.title_id = title_id
        self.status = status
        if type(status_change) is str:
            self.datetime_create = datetime.fromisoformat(status_change).astimezone(
                timezone(timedelta(hours=7))
            )
        elif type(status_change) is datetime:
            self.datetime_create = status_change
        else:
            raise TypeError
