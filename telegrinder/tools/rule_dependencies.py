from .magic import get_default_args, resolve_arg_names
import inspect
import typing
import typing_extensions

T = typing.TypeVar("T")
P = typing_extensions.ParamSpec("P")
RuleCallableChecker = typing.Callable[
    typing_extensions.Concatenate[T, dict, P],
    typing.Coroutine[typing.Any, typing.Any, bool]
]


class DependenceUnset(BaseException):
    def __init__(self, rule_name: str, dependence_name: str):
        self.rule_name = rule_name
        self.dependence_name = dependence_name
    
    def __repr__(self) -> str:
        return (
            f"There is no {self.dependence_name!r} dependency for rule "
            f"{self.rule_name!r}. You must set it in your dispatcher."
        )
    
    def __str__(self) -> str:
        return self.__repr__()


def dependencies_bundle(
    rule_name: str, checker: RuleCallableChecker,
    rule_dependencies: typing.Dict[str, typing.Any], 
) -> typing.Dict[str, typing.Any]:
    arg_names = resolve_arg_names(checker, skip_params_num=3)
    kw = inspect.getfullargspec(checker).varkw
    if not arg_names and kw is not None and kw == "rule_dependencies":
        return rule_dependencies.copy()
    arg_names = resolve_arg_names(checker, skip_params_num=3)
    depends = get_default_args(checker)
    for name in arg_names:
        if name not in rule_dependencies:
            raise DependenceUnset(rule_name, name)
        depends[name] = rule_dependencies[name]
    return depends
