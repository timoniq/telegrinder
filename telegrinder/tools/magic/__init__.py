from telegrinder.tools.magic.annotations import Annotations, get_generic_parameters
from telegrinder.tools.magic.descriptors import additional_property
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
    "get_default_args",
    "get_func_annotations",
    "get_func_parameters",
    "get_generic_parameters",
    "resolve_arg_names",
    "resolve_kwonly_arg_names",
    "resolve_posonly_arg_names",
    "shortcut",
)
