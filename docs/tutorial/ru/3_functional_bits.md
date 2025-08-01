# Функциональные штучки

Как ты, вероятно, уже заметил, в telegrinder используются довольно странные конструкции вроде `.unwrap()`, `.map()` и других. Если у тебя уже был опыт работы с функциональными языками, такие концепции покажутся знакомыми. Но даже если нет — эта статья объяснит, почему это полезно.

В большинстве Python-библиотек, если что-то идёт не так, выбрасывается исключение. Мы считаем, что такой подход неудачен. Почему? Потому что трудно предсказать, какие исключения может вызвать тот или иной вызов функции. Исключение может возникнуть глубоко в зависимостях, и ты получишь что-то неожиданное. А мы, как программисты, стараемся избегать неожиданного поведения. Именно поэтому в telegrinder уделяется внимание качественной аннотации типов. С исключениями это делать крайне сложно.

Решение — не выбрасывать исключения, а возвращать результат в одном из двух возможных состояний: ошибка, если что-то пошло не так, или значение, если всё хорошо.

Мы используем библиотеку `fntypes`, чтобы реализовать функциональную основу в telegrinder. Давай рассмотрим простые примеры, чтобы глубже понять концепцию.

Напишем функцию с использованием `fntypes`, чтобы продемонстрировать подход:

```python
from fntypes import Result, Ok, Error

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Error("Cannot divide by zero")
    return Ok(a / b)
```

Это функция, которая позволяет безопасно делить `a` на `b`. Если делитель равен нулю, возвращаем `Error`. Если всё в порядке — `Ok` с результатом деления.

fntypes предоставляет множество утилит для работы со своими объектами.

Одна из них — `.unwrap()`, ты, вероятно, уже её встречал.

Это способ получить значение или выбросить исключение, если результат — ошибка. Если внутри ошибка — будет выброшено исключение, если значение — вернётся само значение.

```python
divide(6, 3).unwrap() == 2
divide(3, 0).unwrap()  # Исключение UnwrapError("Cannot divide by zero")
```

[Продвинутая документация со всеми методами](https://github.com/timoniq/fntypes/blob/main/docs/result.md#application)

---

Теперь можно строить цепочки вызовов и точно контролировать, что делать в случае ошибки:

```python
result = (
    divide(6, 2)  # Делим и получаем результат
    .map(int)     # Если результат успешен — преобразуем в int. int(3.0) == 3
    .then(lambda x: divide(x, 3))  # Если результат успешен — выполняем ещё одно деление
    .map_or(0)    # В случае ошибки заменяем результат на значение по умолчанию (0)
)
```

Таким образом, мы чётко контролируем результат выполнения и не теряем управление из-за исключений. Результатом будет `Result[float, str]`.

Обработать результат можно так:

```python
match result:
    case Ok(value):
        print("Value is", value)
    case Err(err):
        print("Something is wrong:", err)
```

Или можно преобразовать ошибку в собственное исключение с помощью `expect`:

```python
result.expect(ZeroDivisionError())  # 1
```

Пока что это может выглядеть немного абстрактно, но немного попрактиковавшись с этими типами, ты сможешь удобно и безопасно строить логику в telegrinder. Первая практическая польза появится уже в следующей статье, где мы начнём работать с методами API — и именно они возвращают два возможных состояния: ошибку или значение.

[>> Next: Telegram API](4_api.md)
