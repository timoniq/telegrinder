from msgspec import Struct, field


class Model(Struct, omit_defaults=True):
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

    returns: list[str] | None = None
    """Return type."""

    description: list[str] | None = None
    """Method description."""

    params: list["MethodParameter"] | None = None
    """Method parameters."""


class ObjectSchema(Model):
    name: str
    """Object name."""

    href: str
    """Url of the documentation about object."""

    description: list[str] | None = None
    """Object description."""

    fields: list["ObjectField"] | None = None
    """Object fields."""

    subtypes: list[str] | None = None
    """Object is inherited by other objects."""
    
    subtype_of: list[str] | None = None
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
    "Model",
    "ObjectField",
    "MethodParameter",
    "TelegramBotAPISchema",
    "MethodSchema",
    "ObjectSchema",
)
