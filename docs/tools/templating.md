# Templating

To avoid using large lines of text there is templating for that. Telegrinder has an `ABCTemplating` interface for creating Templating classes.

```python
from telegrinder.tools.templating import ABCTemplating
```

Telegrinder has class `JinjaTemplating` to work with jinja templates.

```python
from telegrinder.tools.templating import JinjaTemplating
```

`JinjaTemplating` methods:
* `render(template_name: str, **data: Any) -> str`
* `render_from_string(template_source: str, **data: Any) -> str`
* `@add_filter(key: str | None) -> wrapper(func: JinjaFilter)`


Example:
```python
import asyncio
import pathlib

import jinja2

from telegrinder.tools.templating import JinjaTemplating

jt = JinjaTemplating(pathlib.Path(__file__).resolve().parent / "templates")


@jt.add_filter("title")
def title_string(env: jinja2.Environment, value: str, attribute=None) -> str:
    # attribute can be obtained if you pass it in the filter call
    # ... | title_string(1) -> attribute=1
    return value.strip().title()


async def main():
    await jt.render("template.j2", digits=[1, 2, 3])
    await jt.render_from_string("{{ name }} | title", name="alex")


asyncio.run(main())
```

Example with use Telegrinder [*CLICK*](https://github.com/timoniq/telegrinder/blob/dev/examples/templating.py)

More details about `Jinja` can be found [*HERE*](https://jinja.palletsprojects.com/en)