# Telegram API

Самая важная часть при создании чего-либо для Telegram — это, конечно же, выполнение методов Telegram API.

Мы могли этого не заметить, но уже не раз отправляли такие запросы — просто они были обёрнуты в интерфейсы telegrinder. Например, когда мы отправляли ответ на сообщение, фактически вызывался API метод `send_message`.


```python
async def message_handler(message: Message):
    await message.answer("Hi!")
```

Давай напишем альтернативу этому с использованием низкоуровневого интерфейса для работы с telegram API.

API можно найти либо внутри объекта `bot`, либо внутри события (`message`), так как каждое событие связано с API, из которого оно пришло.

```python
bot.api
message.api
```

Отлично! Теперь, когда у нас есть доступ к API, можно легко вызвать `send_message`:

```python
async def message_handler(message: Message):
    await message.api.send_message(
        chat_id=message.chat_id,
        text="Hi!",
    )
```

Вот и всё — поведение такое же. Как ты, вероятно, уже понял, `answer` — это просто сокращение, которое избавляет от необходимости указывать `chat_id`, потому что он уже известен из сообщения.

Хорошо, но что если нам нужно получить результат вызова? Согласно TBA (Telegram Bot API), метод `send_message` возвращает объект отправленного сообщения. Из предыдущей статьи [Функциональные штучки](3_functional_bits.md) мы знаем, что telegrinder использует функциональную модель для разделения успешных и неуспешных вызовов. Поэтому мы должны ответственно обрабатывать оба варианта: либо получили ошибку, либо — значение. Telegrinder предоставляет непрерывный поток управления. Если хотим сохранить контроль, — обрабатываем состояние ошибки. Если же нам не важен результат — можно использовать `.unwrap()`.

Рассмотрим оба случая: когда нам важна ошибка и когда — нет.

```python
from fntypes import Error, Ok

match await message.api.send_message(
    chat_id=message.chat_id,
    text="Hi!",
):
    case Error(err):
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

# Даже если мы хотим прервать выполнение при ошибке, лучше указать причину этой ошибки —
# либо с помощью собственного класса исключения, либо хотя бы текстом.
# Для этого используем .expect()

message_id = (
    await message.api.send_message(...)
).expect("Could not send a message").message_id
```

---

Если мы используем стандартные представления (views) и встроенные события, то скорее всего часто будем сталкиваться с множеством удобных сокращений, которые доступны из коробки. Мы уже видели `answer`, которое является сокращением `send_message`. Но есть и другие: `reply`, `edit`, `delete` и т.д. Просто установи хороший `IDE`, и ты будешь приятно удивлён тем, сколько удобств доступно сразу.

```python
m = (await message.answer("Happy birthday")).unwrap()
await asyncio.sleep(1)
await m.edit("Oops wrong chat")
await asyncio.sleep(1)
await m.delete()
```

[>> Next: Ноды](5_nodes.md)
