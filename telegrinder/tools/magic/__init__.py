from telegrinder.tools.magic.annotations import Annotations, get_generic_parameters
from telegrinder.tools.magic.dictionary import extract, join_dicts
from telegrinder.tools.magic.function import (
    Bundle,
    bundle,
    function_context,
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
    "bundle",
    "extract",
    "function_context",
    "get_default_args",
    "get_func_annotations",
    "get_func_parameters",
    "get_generic_parameters",
    "join_dicts",
    "resolve_arg_names",
    "resolve_kwonly_arg_names",
    "resolve_posonly_arg_names",
    "shortcut",
)
