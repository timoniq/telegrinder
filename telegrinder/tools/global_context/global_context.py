import collections
import dataclasses
import types
import typing
from functools import wraps

from telegrinder.modules import logger
from telegrinder.option import Nothing, Option, Some
from telegrinder.result import Error, Ok, Result

from .abc import ABCGlobalContext, CtxValue, CtxVar, GlobalCtxVar

T = typing.TypeVar("T")
F = typing.TypeVar("F", bound=typing.Callable)
_: typing.TypeAlias = None


def type_check(value: object, value_type: type[T]) -> typing.TypeGuard[T]:
    if value_type is typing.Any:
        return True
    origin_type = typing.get_origin(value_type) or value_type
    if origin_type is collections.abc.Callable:  # type: ignore
        return callable(value)
    if origin_type in (typing.Union, types.UnionType):
        origin_type = typing.get_args(value_type)
    return isinstance(value, origin_type)


def root_protection(func: F) -> F:
    if func.__name__ not in ("__setattr__", "__getattr__", "__delattr__"):
        raise RuntimeError(
            "You cannot decorate a {!r} function with this decorator, only "
            "'__setattr__', __getattr__', '__delattr__' methods.".format(
                func.__name__,
            )
        )

    @wraps(func)
    def wrapper(self: "GlobalContext", __name: str, *args) -> typing.Any:
        if self.is_root_context_variable(__name):
            raise AttributeError(
                f"Unable to set, get, delete root context variable {__name!r}."
            )

        if self.is_root_attribute(__name) and __name in (
            self.__dict__ | self.__class__.__dict__
        ):
            root_attr = self.get_root_attribute(__name).unwrap()
            if all((not root_attr.can_be_rewritten, not root_attr.can_be_read)):
                raise AttributeError(
                    f"Unable to set, get, delete root attribute {__name!r}."
                )
            if func.__name__ == "__setattr__" and not root_attr.can_be_rewritten:
                raise AttributeError(f"Unable to set root attribute {__name!r}.")
            if func.__name__ == "__getattr__" and not root_attr.can_be_read:
                raise AttributeError(f"Unable to get root attribute {__name!r}.")
            if func.__name__ == "__delattr__":
                raise AttributeError(f"Unable to delete root attribute {__name!r}.")

        return func(self, __name, *args)  # type: ignore

    return wrapper  # type: ignore


def ctx_var(value: T, *, const: bool = False) -> T:
    """Example:
    ```
    class MyCtx(GlobalContext):
        name: typing.Final[str]
        URL: typing.Final = ctx_var("https://google.com", const=True)

    ctx = MyCtx(name=ctx_var("Alex", const=True))
    ctx.URL  #: 'https://google.com'
    ctx.URL = '...'  #: type checking fail and raise exception 'TypeError'
    ```
    """
    return typing.cast(T, CtxVar(value, const=const))


@dataclasses.dataclass(frozen=True, eq=False)
class RootAttr:
    name: str
    can_be_read: bool = dataclasses.field(default=True, kw_only=True)
    can_be_rewritten: bool = dataclasses.field(default=True, kw_only=True)

    def __eq__(self, __value: str) -> bool:
        return self.name == __value


@typing.dataclass_transform(
    kw_only_default=True,
    order_default=True,
    field_specifiers=(ctx_var,),
)
class GlobalContext(ABCGlobalContext):
    __ctx_name__: str | None
    __root_attributes__: typing.ClassVar = (
        RootAttr("__ctx_name__", can_be_rewritten=False),
        RootAttr("__root_attributes__", can_be_rewritten=False),
        RootAttr("__root_context_variables__", can_be_rewritten=False),
    )
    __root_context_variables__: typing.ClassVar = ("__other_ctxs__",)

    __context_storage: typing.ClassVar[dict[str, GlobalCtxVar[typing.Any]]] = {
        "__other_ctxs__": GlobalCtxVar("__other_ctxs__", dict()),
    }

    def __init__(
        self,
        __ctx_name: str | None = None,
        **variables: typing.Any | CtxVar[typing.Any],
    ):
        if not hasattr(self.__class__, "__ctx_name__"):
            self.__ctx_name__ = __ctx_name

        if not issubclass(GlobalContext, self.__class__):
            defaults = {}
            for name in self.__class__.__annotations__:
                if (
                    name in self.__class__.__dict__
                    and name not in self.__root_attributes__
                ):
                    defaults[name] = getattr(self.__class__, name)
                    delattr(self.__class__, name)
                    if isinstance(defaults[name], CtxVar) and defaults[name].const:
                        variables.pop(name, None)

            variables = defaults | variables

        for name, value in variables.items():
            self.__setattr__(name, value)

    def __repr__(self) -> str:
        return "<{!r} -> ({})>".format(
            f"{self.__class__.__name__}@" + (self.__ctx_name__ or "MainContext"),
            ", ".join(repr(var) for var in self),
        )

    def __iter__(self):
        return iter(
            self.__copy_context_storage(exclude_root_context_vars=True).values()
        )

    def __next__(self):
        return next(iter(self))

    def __contains__(self, __value: str) -> bool:
        """Returns True if the context variable name
        exists in a context."""
        return __value in self.__get_context_storage()

    def __eq__(self, __value: typing.Self) -> bool:
        """Returns True if the names of context stores
        that use self and __value instances are equivalent."""
        return self.__ctx_name__ == __value.__ctx_name__

    def __bool__(self):
        """Returns True if context is not empty otherwise False."""
        return bool(self.__copy_context_storage(exclude_root_context_vars=True))

    @root_protection
    def __setattr__(self, __name: str, __value: CtxValue):
        """Setting a root attribute or context variable."""
        if self.is_root_attribute(__name):
            return object.__setattr__(self, __name, __value)
        ctx_storage = self.__get_context_storage()
        var = ctx_storage.get(__name)
        if var is not None and var.const:
            raise TypeError(
                f"Unable to set variable {__name!r}, because it's a constant."
            )
        ctx_storage[__name] = GlobalCtxVar.collect(__name, __value)

    @root_protection
    def __getattr__(self, __name: str) -> typing.Any:
        """Getting a root attribute or context variable."""
        if self.is_root_attribute(__name):
            return object.__getattribute__(self, __name)
        return self.get(__name).unwrap().value

    @root_protection
    def __delattr__(self, __name: str):
        """Removing a context variable."""
        var = self.get(__name).unwrap()
        if var.const:
            raise TypeError(
                f"Unable to delete variable {__name!r}, because it's a constant."
            )
        del self.__get_context_storage()[__name]

    def __get_context_storage(self) -> dict[str, GlobalCtxVar[typing.Any]]:
        """Get context storage by `__ctx_name__`."""
        main_ctx_storage = self.__class__.__context_storage
        other_ctxs: dict = main_ctx_storage["__other_ctxs__"].value
        if self.__ctx_name__ is None:
            return main_ctx_storage
        return other_ctxs.setdefault(self.__ctx_name__, dict())

    def __copy_context_storage(
        self,
        *,
        exclude_root_context_vars: bool = False,
    ) -> dict[str, GlobalCtxVar[typing.Any]]:
        """Copy context storage."""
        ctx = self.__get_context_storage().copy()
        if exclude_root_context_vars:
            for root_ctx_var in self.__root_context_variables__:
                ctx.pop(root_ctx_var, None)
        return ctx

    def is_root_context_variable(self, name: str) -> bool:
        """Returns True if exists root context variable
        otherwise False."""
        return name in self.__root_context_variables__

    def is_root_attribute(self, name: str) -> bool:
        """Returns True if exists root attribute
        otherwise False."""
        return name in self.__root_attributes__

    def get_root_attribute(self, name: str) -> Option[RootAttr]:
        """Get root attribute by name."""
        if self.is_root_attribute(name):
            for rattr in self.__root_attributes__:
                if rattr.name == name:
                    return Some(rattr)
        return Nothing

    def get(
        self,
        var_name: str,
        var_value_type: type[T] = typing.Any,
    ) -> Result[GlobalCtxVar[T], str]:
        """Get context variable by name.
        Returns `GlobalCtxVar[value_type]` object."""
        var = self.__get_context_storage().get(var_name)
        if var is None:
            return Error(
                f"Variable {var_name!r} is not defined in global context {self.__ctx_name__!r}."
            )
        assert type_check(var.value, var_value_type), (
            "Context variable value type of {!r} does not correspond to the expected type {!r}.".format(
                type(var.value).__name__,
                getattr(var_value_type, "__name__", repr(var_value_type)),
            ),
        )
        return Ok(var)

    def get_value(
        self,
        var_name: str,
        value_type: type[T] = typing.Any,
    ) -> Result[T, str]:
        """Get context variable value by name."""
        return self.get(var_name, value_type).map(lambda var: var.value)

    def rename(self, old_var_name: str, new_var_name: str) -> Result[_, str]:
        """Rename context variable."""
        if self.is_root_context_variable(new_var_name):
            return Error(
                f"Cannot rename {old_var_name!r} to {new_var_name!r}, because "
                f"{new_var_name!r} is a root context variable."
            )
        var = self.get(old_var_name).unwrap()
        if var.const:
            return Error(
                f"Unable to rename variable {old_var_name!r}, because it's a constant."
            )
        ctx_storage = self.__get_context_storage()
        del ctx_storage[old_var_name]
        ctx_storage[new_var_name] = GlobalCtxVar(
            new_var_name, var.value, const=var.const
        )
        return Ok(_)  # type: ignore

    def clear(self, *, include_consts: bool = False) -> None:
        """Clear context. If `include_consts = True`,
        then the context is completely cleared."""
        ctx_storage = self.__get_context_storage()
        if not ctx_storage:
            return
        if include_consts:
            logger.warning(
                "Constants from the global context {!r} have been cleaned up!",
                self.__ctx_name__ or "MainContext at %#x" % id(self),
            )

        for name, var in ctx_storage.copy().items():
            if self.is_root_context_variable(name) or (
                var.const and not include_consts
            ):
                continue
            ctx_storage.pop(name)

    def delete_ctx(self) -> Result[_, str]:
        """Delete context by `self.__ctx_name__`."""
        if self.__ctx_name__ is None:
            return Error(
                "You are trying to delete the main context, but this is "
                "not possible. If you want to clear it, use method '.clear'"
            )
        ctxs = self.__class__.__context_storage["__other_ctxs__"].value
        ctxs.pop(self.__ctx_name__, None)
        logger.warning(
            f"Global context {self.__ctx_name__!r} has been deleted. "
            f"If you still have instances of the {self.__class__.__name__!r} "
            "class with the name of the deleted context, it is recommended "
            "to delete them, for they will refer to the new empty context."
        )
        return Ok(_)  # type: ignore
