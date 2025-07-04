# Setting up

Okay, so you decided to switch to telegrinder. Probably because you want something fresh and cool. Or probably its your first time with bots. This tutorial is ok for both occasions. Let's start with initializing the core instance of our bot.

For now you need to create your token from BotFather and import some classes from the module:

```python
from telegrinder import Telegrinder, API, Token

api = API(Token("your-token-here"))
bot = Telegrinder(api)
```

Here we have created three instances:

Your token, which in telegrinder is not just a string, its an instance of Token, this is needed for strong typing and security reasons. Also `Token` has some methods which we might need later.

Then `API`, is basically the instance we are accessing Telegram API with, we will later cover the interaction with it in this tutorial.

Then, finally, our core instance is `Telegrinder` that basically just collects a lot of components in it so we can run the whole bot easily.

---

Now, as we have created the core instance we want to declare some logic into it. Writing bots is event-based. We get an event from telegram, like 'Georgy sent you a message which says "Apple"' or 'Arseny sent a sticker'. Therefore in telegrinder we declare handlers for each kind of event we want to process. The preference of declaration syntax is the reason why we use python decorators. With decorators we can easily link a function to be a _handler_ of a specific event.

Lets imagine we want to handle any message that comes to our bot and send it back. Create something that's called an echo bot. Lets extend our code with a new handler:

```python
# Add one more import
from telegrinder import Message

@bot.on.message()
async def message_handler(message: Message):
    if message.text:
        await message.answer(message.text.unwrap())
```

At the end of the file you need to have this line:
```python
bot.run_forever()
```

This is going to run your bot asynchronously to receive updates in a loop.

Let's break down this code. We've just created a new handler which implements some logic. The line `@bot.on.message()` is very streightforward. We say that we are going to declare a handler which is going to be ran every time a message is received.

As we receive the message the function receives it as a featurized event (so-called CuteType in telegrinder).

If you have a proper IDE like VS Code with pylance you will get the hints to the contents of any data type as telegrinder is a fully typed framework.

As you can see, we used the `answer` method which is prebuilt in Message CuteType. It basically invokes telegram' `send_message` with already specified `chat_id`.

Before sending a message we also checked that message has some text as we can receive a message that is for example just a photo, or a sticker. Telegrinder uses functional types, so we never lose control over what we have in our variables, that's why we invoke `.unwrap()` on text. But don't worry, we will cover this topic later.

As a quick example, let's revise our code a bit, so when we receive no text we send "No text" instead of not replying anything.

```python
@bot.on.message()
async def message_handler(message: Message):
    await message.answer(message.text.unwrap_or("No text"))
```

Yup, that's how it works.

Okay, at this point, if you didn't forget to add the `bot.run_forever()` at the end you should be able to run your bot and receive a echoing reply to your message.

In the next part of the tutorial we will cover `rules`, an essential thing to add some diversity to your handler, so every handler does its own thing. To do that, we will need to add some filtering.

[>> Next: Rules](2_rules.md)
