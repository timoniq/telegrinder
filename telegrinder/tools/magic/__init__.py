from telegrinder.tools.magic.annotations import AnnotationsEvaluator
from telegrinder.tools.magic.dictionary import join_dicts
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
    "AnnotationsEvaluator",
    "Bundle",
    "Shortcut",
    "bundle",
    "get_default_args",
    "get_func_annotations",
    "get_func_parameters",
    "join_dicts",
    "resolve_arg_names",
    "resolve_kwonly_arg_names",
    "resolve_posonly_arg_names",
    "shortcut",
)
