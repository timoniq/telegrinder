# Правила

Отлично, теперь мы узнаем, как фильтровать входящие события. Это довольно просто!

Важно понимать, что в telegrinder обработка событий делится на два этапа. Это полезно, чтобы сначала фильтровать события по типам. Например, сообщения попадают в одно `view`, а callback-запросы (события при нажатии кнопки) — в другое `view`.

Таким образом, `view` — это первое место, куда направляется событие.

Вспомним пример из первой части руководства. Там мы использовали декоратор:

```python
@bot.on.message()
```

По сути, это означает:

```
Мы принимаем все события типа 'message'
```

Внутри `view` можно иметь несколько обработчиков.

Чтобы фильтровать события внутри `view`, мы используем правила.

Правило — это объект, который определяет, соответствует ли событие заданным условиям.

---

Импортируем одно из простейших встроенных правил:

```python
from telegrinder.rules import Text
```

Правило может принимать аргументы, чтобы задать, как именно оно должно работать. Например, `Text` принимает строку или список строк. Если вы используете нормальный `IDE`, то легко заметите, какие аргументы нужно передавать.

Напишем простой обработчик с использованием нашего правила:


```python
@bot.on.message(Text("ping"))
async def ping_handler(message: Message):
    await message.answer("Pong")
```

Круто! Теперь, если вы напишете боту "ping", он ответит "Pong"!

В telegrinder есть множество других готовых правил, вы легко найдёте то, что нужно.

Но важно не ограничиваться только тем, что есть из коробки. Давайте научимся писать свои правила.

---

Правило — это класс, реализующий метод `check`. Оно должно быть унаследовано от `ABCRule`. Напишем одно:

```python
from telegrinder import ABCRule

class IsMessageFromUserId(ABCRule):
    def __init__(self, user_id: int):
        self.user_id = user_id

    def check(self, message: Message) -> bool:
        return message.from_user.id == self.user_id
```

Готово. Это правило проверяет, кто отправил сообщение. Как видно, в конструкторе `__init__` мы указываем `user_id`, который должен пройти проверку.

```python
MY_ID = 123

@bot.on.message(IsMessageFromUserId(MY_ID), Text("/hey"))
async def hey_handler():
    return "Hey hey!"
```

Готово! Здесь мы сделали простой обработчик, который срабатывает на сообщение "hey" от пользователя с ID = MY_ID.

Я также был немного ленив и использовал синтаксический сахар telegrinder — можно просто вернуть строку из функции-обработчика, и она автоматически отправится как ответ.

Когда мы передаём несколько правил в декоратор, они все должны выполниться, чтобы обработчик сработал.

Однако правила можно комбинировать в сложные конструкции с помощью логических операторов. Например:

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

В примере выше видно, что правило `Markup` добавило два новых аргумента в функцию-обработчик. Да, такое возможно — правила могут добавлять значения в контекст.

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

Такой способ работы с контекстом не считается хорошим. Это считается «грязным» и неявным подходом. Но скоро мы узнаем лучший способ при изучении нод. Прямое изменение контекста не рекомендуется, но возможно!

[>> Next: Немного функционального программирования](3_functional_bits.md)
