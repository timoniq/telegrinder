import pathlib
import typing

import jinja2

from .abc import ABCTemplating


def template_processing(template_source: str) -> str:
    return "\n".join(map(str.strip, template_source.splitlines()))


class JinjaFilter(typing.Protocol):
    __name__: str

    def __call__(
        self,
        env: jinja2.Environment,
        value: typing.Any,
        attribute: typing.Any | None = None,
    ) -> typing.Any:
        ...


class JinjaTemplating(ABCTemplating):
    def __init__(
        self,
        templates_dir_path: str | pathlib.Path | None = None,
        jinja_env: jinja2.Environment | None = None,
    ):
        self.env = jinja_env or jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                searchpath=templates_dir_path or "templates",
                encoding="UTF-8",
            ),
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=True,
            enable_async=True,
        )

    def add_filter(self, key: str | None = None):
        def wrapper(func: JinjaFilter) -> JinjaFilter:
            func = jinja2.filters.environmentfilter(func)
            self.env.filters[key or func.__name__] = func
            return func

        return wrapper

    async def render(self, template_name: str, **data: typing.Any) -> str:
        return template_processing(
            await self.env.get_template(template_name).render_async(**data)
        )

    async def render_from_string(self, template_source: str, **data: typing.Any) -> str:
        return template_processing(
            await self.env.from_string(template_source).render_async(**data)
        )
