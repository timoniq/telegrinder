"""Webhook Bot example. This example uses fastapi + uvicorn with uvloop."""

import asyncio
import secrets
import typing
from contextlib import asynccontextmanager, suppress

import uvicorn  # type: ignore
from bot import dp  # type: ignore
from envparse import env
from fastapi import FastAPI, Request, Response  # type: ignore

from telegrinder import API, Token
from telegrinder.modules import logger
from telegrinder.types.objects import Update

token = Token.from_env()
api = API(token=token)

HOST = typing.cast(str, env.str("HOST"))  # > host, for example: https://site.com
PORT = typing.cast(int, env.int("PORT"))  # > port, can be either 443, 80, 88, or 8443.
WEBHOOK_PATH = typing.cast(
    str, env.str("WEBHOOK_PATH") + token
)  # > webhook path, for example: /bot/ + bot token: 123:ABC...
WEBHOOK_URL = HOST + WEBHOOK_PATH  # > host + webhook path
SECRET_TOKEN = secrets.token_urlsafe(64)  # > random secret token


@asynccontextmanager
async def lifespan(_):
    await api.set_webhook(url=WEBHOOK_URL, secret_token=SECRET_TOKEN)
    yield
    await api.delete_webhook(drop_pending_updates=True)


app = FastAPI(lifespan=lifespan)  # type: ignore


@app.post(WEBHOOK_PATH, response_class=Response)  # type: ignore
async def webhook_bot(request: Request) -> Response:  # type: ignore
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != SECRET_TOKEN:  # type: ignore
        return Response(status_code=404)  # type: ignore
    update = Update.from_raw(await request.body())  # type: ignore
    logger.debug("Webhook received update (update_id={})", update.update_id)
    asyncio.get_running_loop().create_task(dp.feed(update, api))
    return Response(status_code=200)  # type: ignore


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        uvicorn.run(app, host="0.0.0.0", port=PORT, loop="uvloop")  # type: ignore
