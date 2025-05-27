# API

The essential part to build something for telegram is of course running telegram API methods.

We might not realise that but we have already made a lot of these API requests later but that was wrapped around with telegrinder interfaces. For instance, as we were sending a message reply, we were running `send_message` API method.

```python
async def message_handler(message: Message):
    await message.answer("Hi!")
```

Lets write an alternative for that using the low-level interface to interact with telegram API.

It can be found either inside `bot` or inside our event, since event is always bound to some API which it was received from.

```python
bot.api
message.api
```

Great! Now as we have our API instance it will be very easy to call `send_message`

```python
async def message_handler(message: Message):
    await message.api.send_message(
        chat_id=message.chat_id,
        text="Hi!",
    )
```

Thats it. We have the same behaviour. As you can guess, `answer` is just a shortcut which helps us to avoid specifying the id of the chat to send the message into, we already know it from the message.

Ok, but what if we want to get the result of our call. According to telegram bot API, `send_message` call returns the object of the message sent. From the previous article [Functional Bits](3_functional_bits.md) we know that telegrinder uses functional backend to separate successful and failed calls. Therefore we will need to be responsible and handle both possible cases: the one we get an error, or we get an actual value. Telegrinder provides us with an unbroken control flow, if we want to preserve it, we will handle the error state, but in case we don't really care we can just run `.unwrap()`.

Lets review both cases the one we care and one we don't

```python
# from fntypes import Ok, Err

match await message.api.send_message(
    chat_id=message.chat_id,
    text="Hi!",
):
    case Err(err):
        print("Failed to send a message:", err)
        return
    case Ok(message):
        message_id = message.message_id
```

```python
message_id = (
    await message.api.send_message(
        chat_id=message.chat_id,
        text="Hi!",
    )
).unwrap().message_id

# Even if we want to break the control flow, it might be much better to directly specify why the error happened (either with custom exception class or just a simple detail information). To transform the raising exception into something more detailed, we use expect

message_id = (
    await message.api.send_message(...)
).expect("Could not send a message").message_id
```

---

If we are playing around default views and built-in events we are likely to encounter looots of shortcuts that are provided out-of-box. We already have seen `answer` that is a shortcut of `send_message`. But we can for sure extend our knowledge with `reply`, `edit`, `delete` and others. Just install a good IDE and you will be more than pleased but what you get out of box.

```python
m = (await message.answer("Happy birthday")).unwrap()
await asyncio.sleep(1)
await m.edit("Oops wrong chat")
await asyncio.sleep(1)
await m.delete()
```
