from telegrinder.tools.magic.annotations import Annotations, get_generic_parameters
from telegrinder.tools.magic.descriptors import (
    additional_property,
    class_cached_property,
    class_property,
    magic_cached_property,
    magic_property,
)
from telegrinder.tools.magic.function import (
    Bundle,
    bundle,
    get_default_args,
    get_func_annotations,
    get_func_parameters,
    resolve_arg_names,
    resolve_kwonly_arg_names,
    resolve_posonly_arg_names,
)
from telegrinder.tools.magic.shortcut import Shortcut, shortcut

__all__ = (
    "Annotations",
    "Bundle",
    "Shortcut",
    "additional_property",
    "bundle",
    "class_cached_property",
    "class_property",
    "get_default_args",
    "get_func_annotations",
    "get_func_parameters",
    "get_generic_parameters",
    "magic_cached_property",
    "magic_property",
    "resolve_arg_names",
    "resolve_kwonly_arg_names",
    "resolve_posonly_arg_names",
    "shortcut",
)
