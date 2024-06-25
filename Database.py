from typing import Any

import psycopg2

conn = psycopg2.connect(dbname="DiaryTelegramBot", host="localhost", user="postgres", password="root",
                        port="5432")

conn.autocommit = True


def GetUserByTelegramId(telegramId: int) -> list[tuple[Any, ...]]:
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM public."Users" WHERE "telegramId" = {telegramId};')
    result = cursor.fetchall()

    cursor.close()

    return result


def RegisterUser(userId: int, telegramId: int, accessTokrn: str, refreshToken: str) -> None:
    cursor = conn.cursor()

    cursor.execute(
        f'INSERT INTO public."Users"( "userId", "telegramId", "accessToken", "refreshToken") VALUES ( {userId}, {telegramId}, \'{accessTokrn}\', \'{refreshToken}\');')

    cursor.close()

def LoginUser(userId: int, access_token: str, refreshToken: str) -> None:
    cursor = conn.cursor()
    cursor.execute(
        f'UPDATE public."Users" SET   "accessToken"=\'{access_token}\', "refreshToken"=\'{refreshToken}\' WHERE "userId"={userId};'
    )
    cursor.close()
