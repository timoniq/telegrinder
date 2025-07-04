"""Webhook Bot example. This example uses fastapi + uvicorn."""

import asyncio
import os
import secrets
from contextlib import asynccontextmanager

import uvicorn  # type: ignore
from bot import dp  # type: ignore
from fastapi import FastAPI, Request, Response  # type: ignore

from telegrinder import API, Token
from telegrinder.modules import logger
from telegrinder.tools.loop_wrapper import LoopWrapper
from telegrinder.types.objects import Update
from telegrinder.verification_utils import verify_webapp_request

token = Token.from_env()
api = API(token=token)
loop_wrapper = LoopWrapper().bind_loop(loop_factory=asyncio.new_event_loop)

HOST = os.environ["HOST"]  # > host, for example: https://domain.com
PORT = int(os.environ["PORT"])  # > port, can be either 443, 80, 88, or 8443.
WEBHOOK_PATH = os.environ["WEBHOOK_PATH"] + token  # > webhook path, for example: /bot/ + token
WEBHOOK_URL = HOST + WEBHOOK_PATH  # > host + webhook path
SECRET_TOKEN = secrets.token_urlsafe(64)  # > random secret token


@asynccontextmanager
async def lifespan(_):
    await api.set_webhook(url=WEBHOOK_URL, secret_token=SECRET_TOKEN, drop_pending_updates=True)
    yield
    await api.delete_webhook(drop_pending_updates=True)


app = FastAPI(lifespan=lifespan)  # type: ignore


@app.post(WEBHOOK_PATH, response_class=Response)  # type: ignore
async def webhook_bot(request: Request) -> Response:  # type: ignore
    if not verify_webapp_request(SECRET_TOKEN, request.headers):  # type: ignore
        return Response(status_code=403)  # type: ignore

    update = Update.from_raw(await request.body())  # type: ignore
    logger.debug(
        "Webhook received update (update_id={}, update_type={!r})",
        update.update_id,
        update.update_type,
    )
    await loop_wrapper.create_task(dp.feed(update, api))
    return Response(status_code=200)  # type: ignore


async def run_application(server: uvicorn.Server, /) -> None:  # type: ignore
    await server.serve()  # type: ignore


if __name__ == "__main__":
    config = uvicorn.Config(app, host="0.0.0.0", port=PORT, loop="none")  # type: ignore
    loop_wrapper.add_task(run_application(uvicorn.Server(config)))  # type: ignore
    loop_wrapper.run()
