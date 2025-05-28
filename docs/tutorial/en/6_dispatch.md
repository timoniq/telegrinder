# Dispatch

In this article we will review one of other core instances of telegrinder. `Dispatch` serves as a container and a router for all our events.

As a user who is just learning the basics what we need to know about it is that we can find a lot of use of it for code separation and therefore building a neat bot architecture. That is because `Dispatch` implements merging logic - one dispatch can be easily loaded into another one.

We have already used the default one in the previous parts of the tutorial. The 'main' dispatch is hidden inside `bot.on` instance. `bot.on` - is basically the dispatch we will be loading all our other parts of the bot into.

Inside the dispatch we usually have:

* Views: `message`, `callback_query`, etc

* Load methods. With `dispatch.load(another_dispatch)` we can easily load everything we have in `another_dispatch` into `dispatch`.

* `feed` method. This one takes an event model and does all the work to 'feed' to the final handler

There are also `load_many` and `load_from_dir` methods for a quicker dispatch assembly.

---

As we know what dispatch is, lets write our own one!

```python
from telegrinder import Dispatch, Message
from telegrinder.rules import IsBot, Command, Argument

dp = Dispatch()

@dp.message(IsBot())
async def bot_message_handler(m: Message):
    await m.api.send_message(
        chat_id=m.chat_id,
        text="Hey bot!",
    )

@dp.message(
    Command(
        "repeat",
        Argument("string"),
        Argument("times", [lambda s: int(s) if s.isdigit() else None], optional=True),
    ),
)
async def command_handler(m: Message, string: str, times: int = 5):
    await m.answer(", ".join([string] * times))
```

Done! Thats just like ordinary bot but we already work with `bot.on`.

Let's say we have this piece of code `in handlers/chat_utilities.py`.

Now what we want to to is load this dispatcher into our bot's one like this:

```python
from handlers import chat_utilities

api = API(Token("your-token-here"))
bot = Bot(api)

bot.on.load(chat_utilities.dp)

bot.run_forever()
```

Here we go. The newly written dispatcher was loaded into our bot's core dispatcher. Do you already see the potential for code separation here?

What about creating some folders like `handlers` for dispatchers with handlers, adding folders `nodes` and `rules`. The bot can be assembled in `main.py` or `bot.py`. That's very easy! Just find the best pattern for you. That will very much help you to find the right instance at ease.

You might probably need to reserve space for `keyboards` and `messages` as well, we will dive into that really soon \`>_o

[>> Next: Keyboard, payload handling](7_keyboard.md)
