"""Webhook Bot example. This example uses fastapi + uvicorn."""

# type: ignore
# pyright: reportMissingImports=false

import asyncio
import os
import secrets
import typing
from contextlib import asynccontextmanager

import uvicorn
from bot import dp
from fastapi import FastAPI, Request, Response

from telegrinder import API, Token
from telegrinder.modules import configure_dotenv, setup_logger
from telegrinder.tools import verify_secret_token

configure_dotenv()

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


app = FastAPI(lifespan=lifespan)


@app.post(WEBHOOK_PATH, response_class=Response)
async def webhook_bot(request: Request) -> Response:
    if not verify_secret_token(SECRET_TOKEN, request.headers):
        return Response(
            content="The secret token verification failed; the request was not processed.",
            status_code=200,
        )

    asyncio.create_task(dp.feed_raw(api, await request.body()))
    return Response(status_code=202)


if __name__ == "__main__":
    setup_logger(level="DEBUG")

    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="DEBUG")
