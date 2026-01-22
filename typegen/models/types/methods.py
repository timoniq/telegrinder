import msgspec

from .objects import ObjectsFieldsLiteralTypesField


class MethodsAnnotationsReturnType(msgspec.Struct):
    name: str
    return_type: str


class MethodsAnnotationsParametersParam(msgspec.Struct):
    name: str
    type: str


class MethodsAnnotationsParameters(msgspec.Struct):
    name: str
    params: list[MethodsAnnotationsParametersParam] = msgspec.field(default_factory=list)


class MethodsAnnotationsLiteralsParam(ObjectsFieldsLiteralTypesField):
    pass


class MethodsAnnotationsLiterals(msgspec.Struct):
    name: str
    params: list[MethodsAnnotationsLiteralsParam] = msgspec.field(default_factory=list)


class MethodsAnnotations(msgspec.Struct):
    return_type: list[MethodsAnnotationsReturnType] = msgspec.field(default_factory=list)
    parameters: list[MethodsAnnotationsParameters] = msgspec.field(default_factory=list)
    literals: list[MethodsAnnotationsLiterals] = msgspec.field(default_factory=list)


class GeneratorMethods(msgspec.Struct):
    annotations: MethodsAnnotations = msgspec.field(default_factory=lambda: MethodsAnnotations())


__all__ = (
    "GeneratorMethods",
    "MethodsAnnotations",
    "MethodsAnnotationsLiterals",
    "MethodsAnnotationsLiteralsParam",
    "MethodsAnnotationsParameters",
    "MethodsAnnotationsParametersParam",
    "MethodsAnnotationsReturnType",
)
