# Rules

Wow so in this part now we will learn how to filter the incoming events. That's pretty easy!

What we need to know is that in telegrinder event processing is parted into two stages. That is useful to firstly filter events broadly by types. For example, messages go into this `view` and callback queries (events when you press a callback button) go into another `view`.

Therefore, `view` is the first place the event is routed into.

Lets recall our example from the first part of the tutorial. There we declared a decorator:

```python
@bot.on.message()
```

Basically it says:

```
We accept all events that are of view 'message'
```

Inside the view, we can have multiple handlers.

In order to filter events inside our view we use **rules**.

Rule - is an instance that tells whether an event follows it.

---

Lets import one of a very simple prebuilt rules.

```python
from telegrinder.rules import Text
```

Rule may accept some arguments to specify how exactly it should work. Text accepts a `string` or a `list of strings`. If you use a proper IDE it will be easy for you to tell what exactly you should pass into a rule.

Lets write a simple handler using our rule.

```python
@bot.on.message(Text("ping"))
async def ping_handler(message: Message):
    await message.answer("Pong")
```

Cool! Now if you write "ping" to your bot, you will receive "Pong" reply!

There are tons of other prebuilt rules in telegrinder, you may easily find something what you need.

However, it is important not to be limited by what is available out-of-box in the framework. Lets dive into writing your own rules.

---

Rule is a class that must implement `check` method. Rule must be derived from `ABCRule`. Lets write one!

```python
from telegrinder import ABCRule

class IsMessageFromUserId(ABCRule):
    def __init__(self, user_id: int):
        self.user_id = user_id

    def check(self, message: Message) -> bool:
        return message.from_user.id == self.user_id
```

Done. This rule will check if the sender of the message. As you can see, there is an `__init__` method to later specify which `user_id` is going to pass the check.

```python
MY_ID = 123

@bot.on.message(IsMessageFromUserId(MY_ID), Text("/hey"))
async def hey_handler():
    return "Hey hey!"
```

Done! Here we just made a simple handler to catch "hey" message from user with user id = `MY_ID`.

I was also quite lazy and decided to use the telegrinder' syntaxic sugar which is that you can simply return a string from the handler function and it will used as an answer.

Here when we passed multiple rules into the decorator they are BOTH required to hold in order for the handler to run.

However, rules can be easily combined into complex constructs with logical operators. For example:

```python
from telegrinder.rules import Markup, FuzzyText, IsUserId

@bot.on.message(
    (
        Markup("<a:int> + <b:int>") | FuzzyText("example")
    ) & IsUserId(MY_ID)
)
async def sum_handler(message: Message, a: int, b: int):
    await message.answer(str(a + b))
```

In the example above you can also notice that `Markup` rule added 2 new arguments to our handler. Yes, that is actually possible - rules can add names to our context.

```python
from telegrinder import Context

class IsIntegerText(ABCRule):
    async def check(self, message: Message, ctx: Context):
        if not message.text.unwrap_or("").is_digit():
            return False
        ctx["integer"] = int(message.text.unwrap())
        return True

@bot.on.message(IsIntegerText())
async def integer_handler(message: Message, integer: int):
    await message.reply(f"{integer} / 3 = {integer / 3}")
```

This is not a recommended way to work with context. That is considered kinda dirty and implicit to change context in this way, but we are going to get to the best way soon when we will be discussing nodes. Force-changing context is not recommended but definitely possible!

[>> Next: Functional bits](3_functional_bits.md)
