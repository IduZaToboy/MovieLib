from datetime import datetime, timezone
from mysql.connector.aio import connect
from modules.my_classes import Users, Titles, TitlesHistory
from modules.tables_text import create_tables_text


class Client(object):
    def __init__(self):
        pass

    async def init_async(self, host: str, user: str, password: str, database: str):
        self.connection = await connect(host=host, user=user, password=password, database=database)
        self.cursor = await self.connection.cursor()
        await self.create_table(create_tables_text)

    async def create_table(self, create_table_text: list[str]):
        for table_text in create_table_text:
            table_text_with_not_exists = table_text.replace(
                "CREATE TABLE", "CREATE TABLE IF NOT EXISTS"
            )
            await self.cursor.execute(table_text_with_not_exists)
        await self.connection.commit()

    async def user_create(self, user: Users) -> None:
        await self.cursor.execute(
            """
                INSERT INTO users
                    (telegram_id, datetime_create)
                    VALUES (%s, %s)
                            """,
            (user.telegram_id, user.datetime_create.isoformat()),
        )
        await self.connection.commit()

    async def user_get(self, telegram_id: int) -> Users:
        await self.cursor.execute(
            """
                SELECT *
                    FROM users
                    WHERE telegram_id = %s
                                  """,
            (telegram_id,),
        )
        user_data = await self.cursor.fetchone()
        user = Users(
            id=user_data[0],
            telegram_id=telegram_id,
            datetime_create=user_data[2],
        )
        return user

    async def title_create(self, title: Titles) -> None:
        await self.cursor.execute(
            """
                INSERT INTO titles
                    (`name`, id_kinopoisk)
                    VALUES (%s, %s)
                                  """,
            (title.name, title.id_kinopoisk),
        )
        await self.connection.commit()

    async def title_get(self, name: str) -> Titles:
        await self.cursor.execute(
            """
                SELECT *
                    FROM titles
                    WHERE `name` = %s
                                  """,
            (name,),
        )
        title_data = await self.cursor.fetchone()
        title = Titles(id=title_data[0], name=name, id_kinopoisk=title_data[2])
        return title

    async def title_history_create(self, title_history: TitlesHistory):
        await self.cursor.execute(
            """
                INSERT INTO titles_history
                    (user_id, title_id, `status`, status_change)
                    VALUES (%s, %s, %s, %s)
                                  """,
            (
                title_history.user_id,
                title_history.title_id,
                title_history.status,
                title_history.status,
            ),
        )
        await self.connection.connect()

    async def title_history_get(self, user_id: int, title_id: int):
        await self.cursor.execute(
            """
                SELECT *
                    FROM titles_history
                    WHERE user_id = %s AND title_id = %s
                                  """,
            (user_id, title_id),
        )
        title_history_data = await self.cursor.fetchone()
        title_history = TitlesHistory(
            id=title_history_data[0],
            user_id=title_history_data[1],
            title_id=title_history_data[2],
            status=title_history_data[3],
            status_change=title_history_data[4],
        )
        return title_history

    async def titles_history_get(self, user_id: int, limit: int = 10, offset: int = 0):
        await self.cursor.execute(
            """
                SELECT *
                    FROM titles_history
                    WHERE user_id = %s
                    ORDER BY id DESC
                    LIMIT %s OFFSET %s
                                  """,
            (user_id, limit, offset),
        )
        titles_history_data = await self.cursor.fetchall()
        titles_history = [
            TitlesHistory(title_history[1], title_history[2], title_history[3], title_history[4])
            for title_history in titles_history_data
        ]
        return titles_history

    async def title_history_change_status(self, title_history: TitlesHistory, new_status: str):
        await self.cursor.execute(
            """
                UPDATE titles_history
                    SET
                        `status`=%s,
                        status_change=%s
                    WHERE id = %s
                                   """,
            (new_status, datetime.now(timezone.utc), title_history.id),
        )
        await self.connection.commit()

    async def title_history_delete(self, title_history: TitlesHistory):
        await self.cursor.execute(
            """
                DELETE FROM titles_history WHERE id=%s
                                  """,
            (title_history.id,),
        )
        await self.connection.commit()
