import asyncio

import pytest

from telegrinder.bot.polling.polling import Polling


@pytest.mark.asyncio()
async def test_polling_stop_interrupts_listen(api_instance, monkeypatch):
    polling = Polling(api_instance, timeout=0.0)
    request_started = asyncio.Event()

    async def get_updates():
        request_started.set()
        await asyncio.Event().wait()

    monkeypatch.setattr(polling, "get_updates", get_updates)

    async def consume_polling():
        async for _updates in polling.listen():
            pass

    task = asyncio.create_task(consume_polling())
    await asyncio.wait_for(request_started.wait(), timeout=1.0)

    polling.stop()

    await asyncio.wait_for(task, timeout=1.0)
    assert not polling.running
