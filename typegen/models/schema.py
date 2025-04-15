from msgspec import Struct, field


class Model(Struct):
    pass


class TelegramBotAPISchema(Model, rename={"objects": "types"}):
    version: str
    """API version."""

    release_date: str
    """Release date."""

    changelog: str
    """Changelog."""

    methods: list["MethodSchema"] = field(default_factory=lambda: [])
    """Schema of methods."""

    objects: list["ObjectSchema"] = field(default_factory=lambda: [])
    """Schema of objects."""


class MethodSchema(Model, rename={"params": "fields"}):
    name: str
    """Method name."""

    href: str
    """Url of the documentation about method."""

    returns: list[str] = field(default_factory=lambda: [])
    """Return type."""

    description: list[str] = field(default_factory=lambda: [])
    """Method description."""

    params: list["MethodParameter"] = field(default_factory=lambda: [])
    """Method parameters."""


class ObjectSchema(Model):
    name: str
    """Object name."""

    href: str
    """Url of the documentation about object."""

    description: list[str] = field(default_factory=lambda: [])
    """Object description."""

    fields: list["ObjectField"] = field(default_factory=lambda: [])
    """Object fields."""

    subtypes: list[str] = field(default_factory=lambda: [])
    """Object is inherited by other objects."""

    subtype_of: list[str] = field(default_factory=lambda: [])
    """List of objects that object inherits."""


class ObjectField(Model):
    name: str
    """Field name."""

    types: list[str]
    """Field types."""

    required: bool = False
    """True if field is required."""

    description: str | None = None
    """Field description."""

    default: str | None = None
    """Default value."""

    default_factory: str | None = None
    """Default factory for dataclass."""


class MethodParameter(Model):
    name: str
    """Parameter name."""

    types: list[str]
    """Parameter types."""

    required: bool = False
    """True if parameter is required."""

    description: str | None = None
    """Parameter description."""


__all__ = (
    "MethodParameter",
    "MethodSchema",
    "Model",
    "ObjectField",
    "ObjectSchema",
    "TelegramBotAPISchema",
)
