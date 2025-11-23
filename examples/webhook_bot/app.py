"""Webhook Bot example. This example uses fastapi + uvicorn."""

import asyncio
import os
import secrets
import typing
from contextlib import asynccontextmanager

import uvicorn  # type: ignore
from bot import dp
from fastapi import FastAPI, Request, Response  # type: ignore

from telegrinder import API, Token
from telegrinder.modules import logger, setup_logger
from telegrinder.tools.loop_wrapper import LoopWrapper
from telegrinder.types.objects import Update
from telegrinder.verification_utils import verify_secret_token

TOKEN = Token.from_env()
HOST = os.environ["HOST"]  # > host, for example: https://domain.com
PORT = int(os.environ["PORT"])  # > port, can be either 443, 80, 88, or 8443.
WEBHOOK_PATH = os.environ["WEBHOOK_PATH"] + TOKEN  # > webhook path, for example: /bot/ + token
WEBHOOK_URL = HOST + WEBHOOK_PATH  # > host + webhook path
SECRET_TOKEN = secrets.token_urlsafe(64)  # > random secret token

api = API(token=TOKEN)


@asynccontextmanager
async def lifespan(_) -> typing.AsyncGenerator[None, None]:
    await api.set_webhook(url=WEBHOOK_URL, secret_token=SECRET_TOKEN, drop_pending_updates=True)
    yield
    await api.delete_webhook(drop_pending_updates=True)


app = FastAPI(lifespan=lifespan)  # type: ignore


@app.post(WEBHOOK_PATH, response_class=Response)  # type: ignore
async def webhook_bot(request: Request) -> Response:  # type: ignore
    if not verify_secret_token(SECRET_TOKEN, request.headers):  # type: ignore
        return Response(status_code=404)  # type: ignore

    update = Update.from_raw(await request.body())  # type: ignore
    logger.debug(
        "Webhook received update (update_id={}, update_type={!r})",
        update.update_id,
        update.update_type,
    )
    await loop_wrapper.create_task(dp.feed(api, update))
    return Response(status_code=200)  # type: ignore


async def run_application(server_config: uvicorn.Config, /) -> None:  # type: ignore
    server = uvicorn.Server(server_config)  # type: ignore
    await server.serve()  # type: ignore


if __name__ == "__main__":
    setup_logger(level="DEBUG")

    loop_wrapper = LoopWrapper().bind_loop(loop_factory=asyncio.new_event_loop)
    config = uvicorn.Config(app, host="0.0.0.0", port=PORT, loop="none")  # type: ignore
    loop_wrapper.add_task(run_application(config))  # type: ignore
    loop_wrapper.run()
