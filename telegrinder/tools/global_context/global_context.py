import collections
import dataclasses
import types
from copy import deepcopy
from functools import wraps

import typing_extensions as typing

from telegrinder.modules import logger
from telegrinder.option import Nothing, Option, Some
from telegrinder.result import Error, Ok, Result

from .abc import ABCGlobalContext, CtxVar, CtxVariable, GlobalCtxVar

T = typing.TypeVar("T")
F = typing.TypeVar("F", bound=typing.Callable)
CtxValueT = typing.TypeVar("CtxValueT", default=typing.Any)

if typing.TYPE_CHECKING:

    _: typing.TypeAlias = None
else:

    _ = lambda: None


def type_check(value: object, value_type: type[T]) -> typing.TypeGuard[T]:
    if value_type is typing.Any:
        return True
    origin_type = typing.get_origin(value_type) or value_type
    if origin_type is collections.abc.Callable:  # type: ignore
        return callable(value)
    if origin_type in (typing.Union, types.UnionType):
        origin_type = typing.get_args(value_type)
    return isinstance(value, origin_type)


def is_dunder(name: str) -> bool:
    return name.startswith("__") and name.endswith("__")


def get_orig_class(obj: T) -> type[T]:
    return getattr(obj, "__orig_class__", obj.__class__)


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
    ctx.URL = '...'  #: type checking error & exception 'TypeError'
    ```
    """
    
    return typing.cast(T, CtxVar(value, const=const))


@dataclasses.dataclass(frozen=True, eq=False)
class RootAttr:
    name: str
    _: dataclasses.KW_ONLY
    can_be_read: bool = dataclasses.field(default=True, kw_only=True)
    can_be_rewritten: bool = dataclasses.field(default=False, kw_only=True)

    def __eq__(self, __value: str) -> bool:
        return self.name == __value


@dataclasses.dataclass(repr=False, frozen=True)
class Storage:
    _storage: dict[str, "GlobalContext"] = dataclasses.field(
        default_factory=lambda: {},
        init=False,
    )

    def __repr__(self) -> str:
        return "<ContextStorage: %s>" % ", ".join(
            "ctx @" + repr(x) for x in self._storage
        )

    @property
    def storage(self) -> dict[str, "GlobalContext"]:
        return self._storage.copy()

    def set(self, name: str, ctx: "GlobalContext") -> None:
        self._storage.setdefault(name, ctx)

    def get(self, ctx_name: str) -> Option["GlobalContext"]:
        ctx = self._storage.get(ctx_name)
        return Some(ctx) if ctx is not None else Nothing

    def delete(self, ctx_name: str) -> None:
        assert self._storage.pop(ctx_name, None) is not None, f"Context {ctx_name!r} is not defined in storage."


@typing.dataclass_transform(
    kw_only_default=True,
    order_default=True,
    field_specifiers=(ctx_var,),
)
class GlobalContext(ABCGlobalContext, typing.Generic[CtxValueT], dict[str, GlobalCtxVar[CtxValueT]]):
    """GlobalContext.
    
    ```
    ctx = GlobalContext()
    ctx["client"] = Client()
    ctx.address = CtxVar("128.0.0.7:8888", const=True)

    def request():
        data = {"user": "root_user", "password": "secret_password"}
        ctx.client.request(ctx.address + "/login", data)
    """
    
    __ctx_name__: str | None
    __storage__: typing.ClassVar[Storage] = Storage()
    __root_attributes__: typing.ClassVar[tuple[RootAttr, ...]] = (
        RootAttr("__ctx_name__"),
        RootAttr("__root_attributes__"),
        RootAttr("__storage__"),
    )

    def __new__(
        cls,
        ctx_name: str | None = None,
        /,
        **variables: typing.Any | CtxVar[CtxValueT],
    ) -> typing.Self:
        """Create or get from storage a new `GlobalContext` object."""

        if not issubclass(GlobalContext, cls):
            defaults = {}
            for name in cls.__annotations__:
                if (
                    name in cls.__dict__
                    and name not in cls.__root_attributes__
                ):
                    defaults[name] = getattr(cls, name)
                    delattr(cls, name)
                    if isinstance(defaults[name], CtxVar) and defaults[name].const:
                        variables.pop(name, None)
    
            variables = defaults | variables 

        ctx_name = getattr(cls, "__ctx_name__", ctx_name)
        if ctx_name is None:
            ctx = dict.__new__(cls)
        elif ctx_name in cls.__storage__.storage:
            ctx = cls.__storage__.get(ctx_name).unwrap()
        else:
            ctx = dict.__new__(cls, ctx_name)
            cls.__storage__.set(ctx_name, ctx)
        
        ctx.set_context_variables(variables)
        return ctx  # type: ignore

    def __init__(
        self,
        ctx_name: str | None = None,
        /,
        **variables: CtxValueT | CtxVariable[CtxValueT],
    ):
        """Initialization of `GlobalContext` with passed variables."""

        if not hasattr(self, "__ctx_name__"):
            self.__ctx_name__ = ctx_name
        
        if variables and not self:
            self.set_context_variables(variables)
                
    def __repr__(self) -> str:
        return "<{!r} -> ({})>".format(
            f"{self.__class__.__name__}@{self.ctx_name}",
            ", ".join(repr(var) for var in self),
        )
    
    def __eq__(self, __value: "GlobalContext") -> bool:
        """Returns True if the names of context stores
        that use self and __value instances are equivalent."""

        return self.ctx_name == __value.ctx_name
    
    def __setitem__(self, __name: str, __value: CtxValueT | CtxVariable[CtxValueT]):
        if is_dunder(__name):
            raise NameError("Cannot set a context variable with dunder name.")
        var = self.get(__name)
        if var and var.unwrap().const:
            raise TypeError(
                f"Unable to set variable {__name!r}, because it's a constant."
            )
        dict.__setitem__(self, __name, GlobalCtxVar.collect(__name, __value))

    def __getitem__(self, __name: str) -> CtxValueT:
        return self.get(__name).unwrap().value
    
    def __delitem__(self, __name: str):
        var = self.get(__name).unwrap()
        if var.const:
            raise TypeError(
                f"Unable to delete variable {__name!r}, because it's a constant."
            )
        dict.__delitem__(self, __name)

    @root_protection
    def __setattr__(self, __name: str, __value: CtxValueT | CtxVariable[CtxValueT]):
        """Setting a context variable."""

        if is_dunder(__name):
            return object.__setattr__(self, __name, __value)
        self.__setitem__(__name, __value)

    @root_protection
    def __getattr__(self, __name: str) -> CtxValueT:
        """Getting a context variable."""

        if is_dunder(__name):
            return object.__getattribute__(self, __name)
        return self.__getitem__(__name)

    @root_protection
    def __delattr__(self, __name: str) -> None:
        """Removing a context variable."""

        if is_dunder(__name):
            return object.__delattr__(self, __name)
        self.__delitem__(__name)

    @property
    def ctx_name(self) -> str:
        """Context name."""

        return self.__ctx_name__ or "<Unnamed ctx at %#x>" % id(self)

    @classmethod
    def is_root_attribute(cls, name: str) -> bool:
        """Returns True if exists root attribute
        otherwise False."""

        return name in cls.__root_attributes__

    def set_context_variables(self, variables: typing.Mapping[str, CtxValueT | CtxVariable[CtxValueT]]) -> None:    
        """Set context variables from mapping."""
        
        for name, var in variables.items():
            self[name] = var

    def get_root_attribute(self, name: str) -> Option[RootAttr]:
        """Get root attribute by name."""

        if self.is_root_attribute(name):
            for rattr in self.__root_attributes__:
                if rattr.name == name:
                    return Some(rattr)
        return Nothing
        
    def items(self) -> list[tuple[str, GlobalCtxVar[CtxValueT]]]:
        """Return context variables as set-like items."""

        return list(dict.items(self))
    
    def keys(self) -> list[str]:
        """Returns context variable names as keys."""

        return list(dict.keys(self))
    
    def values(self) -> list[GlobalCtxVar[CtxValueT]]:
        """Returns context variables as values."""

        return list(dict.values(self))
    
    def update(self, other: typing.Self) -> None:
        """Update context."""

        dict.update(dict(other.items()))
    
    def copy(self) -> typing.Self:
        """Copy context. Returns copied context without ctx_name."""

        return self.__class__(**deepcopy(self.dict()))
    
    def dict(self) -> dict[str, GlobalCtxVar[CtxValueT]]:
        """Returns context as dict."""

        return {name: var for name, var in self.items()}
    
    @typing.overload
    def pop(self, var_name: str) -> Option[GlobalCtxVar[CtxValueT]]:
        ...
    
    @typing.overload
    def pop(
        self,
        var_name: str,
        var_value_type: type[T],
    ) -> Option[GlobalCtxVar[T]]:
        ...
    
    def pop(
        self,
        var_name: str,
        var_value_type: type[T] = typing.Any
    ) -> Option[GlobalCtxVar[T]]:
        """Pop context variable by name.
        Returns Option[GlobalCtxVar[T]] object.
        """

        val = self.get(var_name, var_value_type)
        if val:
            del self[var_name]
            return val
        return Nothing
    
    @typing.overload
    def get(self, var_name: str) -> Option[GlobalCtxVar[CtxValueT]]:
        ...
    
    @typing.overload
    def get(
        self,
        var_name: str,
        var_value_type: type[T],
    ) -> Option[GlobalCtxVar[T]]:
        ...
    
    def get(
        self,
        var_name: str,
        var_value_type: type[T] = typing.Any,
    ) -> Option[GlobalCtxVar[T]]:
        """Get context variable by name.
        Returns `GlobalCtxVar[value_type]` object."""

        generic_types = typing.get_args(get_orig_class(self))
        if generic_types and var_value_type is typing.Any:
            var_value_type = generic_types[0]
        var = dict.get(self, var_name)
        if var is None:
            return Nothing
        assert type_check(var.value, var_value_type), (
            "Context variable value type of {!r} does not correspond to the expected type {!r}.".format(
                type(var.value).__name__,
                getattr(var_value_type, "__name__", repr(var_value_type)),
            )
        )
        return Some(var)

    @typing.overload
    def get_value(self, var_name: str) -> Option[CtxValueT]:
        ...
    
    @typing.overload
    def get_value(
        self,
        var_name: str,
        var_value_type: type[T],
    ) -> Option[T]:
        ...

    def get_value(
        self,
        var_name: str,
        var_value_type: type[T] = typing.Any,
    ) -> Option[T]:
        """Get context variable value by name."""

        return self.get(var_name, var_value_type).map(lambda var: var.value)

    def rename(self, old_var_name: str, new_var_name: str) -> Result[_, str]:
        """Rename context variable."""

        var = self.get(old_var_name).unwrap()
        if var.const:
            return Error(
                f"Unable to rename variable {old_var_name!r}, "
                "because it's a constant."
            )
        del self[old_var_name]
        self[new_var_name] = var.value
        return Ok(_())

    def clear(self, *, include_consts: bool = False) -> None:
        """Clear context. If `include_consts = True`,
        then the context is completely cleared."""

        if not self:
            return
        if include_consts:
            logger.warning(
                "Constants from the global context {!r} have been cleaned up!",
                self.ctx_name + " at %#x" % id(self),
            )
            return dict.clear(self)

        for name, var in self.dict().items():
            if var.const:
                continue
            del self[name]

    def delete_ctx(self) -> Result[_, str]:
        """Delete context by `self.__ctx_name__`."""

        if not self.__ctx_name__:
            return Error("Cannot delete unnamed context.")
        ctx = self.__storage__.get(self.ctx_name).unwrap()
        dict.clear(ctx)
        self.__storage__.delete(self.ctx_name)
        logger.warning(f"Global context {self.ctx_name!r} has been deleted!")
        return Ok(_())


__all__ = (
    "ABCGlobalContext",
    "CtxVar",
    "CtxVariable",
    "GlobalCtxVar",
    "GlobalContext",
    "Storage",
    "RootAttr",
    "type_check",
    "root_protection",
    "is_dunder",
    "ctx_var",
    "get_orig_class",
)
