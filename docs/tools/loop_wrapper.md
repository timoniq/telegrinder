# Loop Wrapper

`LoopWrapper` is telegrinder's event-loop orchestration utility. It is responsible for:

- scheduling background tasks
- running startup and shutdown hooks
- handling delayed and periodic tasks
- shutting down tasks safely

`Telegrinder` already uses a `LoopWrapper` internally, so in most bots you interact with it through `bot.loop_wrapper`.

## Basic idea

```python
from telegrinder.tools import LoopWrapper

loop_wrapper = LoopWrapper()


async def main() -> None:
    await open_db_connection()
    await close_db_connection()


loop_wrapper.add_task(main())
loop_wrapper.run()
```

In actual bot code you usually do not create and run a separate wrapper manually. Instead:

```python
bot.loop_wrapper.add_task(...)
bot.loop_wrapper.lifespan.on_startup(...)
bot.loop_wrapper.timer(...)
```

## Singleton behavior

`LoopWrapper` is a singleton. The same shared wrapper is used across the application unless you explicitly rebind it to another event loop.

Useful properties:

- `lifespan` for startup and shutdown tasks
- `loop` for the underlying event loop
- `time` for loop time
- `running` to check whether the wrapper is active
- `shutting_down` to check whether shutdown has started

## Startup and shutdown hooks

The most common use is startup and shutdown registration:

```python
from telegrinder.tools import LoopWrapper

loop_wrapper = LoopWrapper()


@loop_wrapper.lifespan.on_startup
async def start() -> None:
    await open_db_connection()


@loop_wrapper.lifespan.on_shutdown
async def stop() -> None:
    await close_db_connection()
```

In a bot:

```python
@bot.loop_wrapper.lifespan.on_startup
async def hello() -> None:
    await bot.api.send_message(chat_id=SECRET_CHAT_ID, text="Hello!!!")


@bot.loop_wrapper.lifespan.on_shutdown
async def bye() -> None:
    print("Bye!!!")
```

Reference: [examples/loop_wrapper.py](https://github.com/timoniq/telegrinder/blob/dev/examples/loop_wrapper.py)

## Adding tasks

`add_task(...)` schedules a task for the wrapper.

If the wrapper is not running yet:

- the task is queued
- it will start when the wrapper starts

If the wrapper is already running:

- the task is created immediately in the current loop

That makes it safe to prepare background work before `bot.run_forever()` as well as while the wrapper is already active.

## Delayed and periodic tasks

`LoopWrapper` provides two decorators:

- `timer(...)` for one-shot delayed execution
- `interval(...)` for repeated execution

Example:

```python
@bot.loop_wrapper.timer(minutes=1)
async def once_yum() -> None:
    print("yum-yum!")


@bot.loop_wrapper.interval(seconds=10)
async def repeat_yum() -> None:
    print("repeat yum-yum!!!")
```

`timer` is executed once after the delay.
`interval` is re-scheduled after each run.

Delayed tasks expose `.cancel()` on the decorated function.

## Running the wrapper manually

If you use `LoopWrapper` outside `Telegrinder`, call:

```python
loop_wrapper.run()
```

By default it closes the loop after shutdown. If you need to keep the loop open:

```python
loop_wrapper.run(close_loop=False)
```

Usually you should not call `run()` yourself when the bot lifecycle is already managed by `Telegrinder`.

## Shutdown

To stop the wrapper programmatically:

```python
loop_wrapper.shutdown()
```

The wrapper also installs signal handlers where possible and performs safe cancellation of pending tasks during shutdown.

## Working with an already running loop

If some other framework owns the event loop, `LoopWrapper` can attach itself to that running loop.

Current relevant methods are:

- `attach_to_running_loop()`
- `bind_event_loop(loop)`
- `create_task_group()`

`create_task_group()` is especially useful when you want structured concurrent work integrated with the wrapper's loop handling.

## Event-loop binding

If you need to explicitly bind a loop:

```python
import asyncio

from telegrinder.tools import LoopWrapper

loop_wrapper = LoopWrapper()
loop_wrapper.bind_event_loop(asyncio.new_event_loop())
```

This replaces older documentation that referred to `bind_loop(...)` or `event_loop`; the current API uses `bind_event_loop(...)` and the `loop` property.

## Practical guidance

Use `LoopWrapper` for:

- startup initialization
- graceful shutdown cleanup
- repeating polling or maintenance jobs
- delayed follow-up actions
- background coroutines that should live with the bot lifecycle

Do not use it as a replacement for persistent job scheduling or long-term workflow state. For those cases you still need external storage or a dedicated scheduler.
