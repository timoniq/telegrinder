import msgspec

from .objects import ObjectsFieldsLiteralTypesField


class MethodsParamsLiteralTypesParam(ObjectsFieldsLiteralTypesField):
    pass


class MethodsParamsLiteralTypes(msgspec.Struct):
    method_name: str
    params: list[MethodsParamsLiteralTypesParam]


class MethodsParamsAnnotationsAnnotationsParam(msgspec.Struct):
    name: str
    annotation: str


class MethodsParamsAnnotationsAnnotations(msgspec.Struct):
    method_name: str
    params: list[MethodsParamsAnnotationsAnnotationsParam]


class MethodsParamsAnnotations(msgspec.Struct):
    annotations: list[MethodsParamsAnnotationsAnnotations] = msgspec.field(default_factory=list)
    literals: list[MethodsParamsLiteralTypes] = msgspec.field(default_factory=list)


class MethodsParams(msgspec.Struct):
    annotations: MethodsParamsAnnotations = msgspec.field(default_factory=lambda: MethodsParamsAnnotations())


class GeneratorMethods(msgspec.Struct):
    params: MethodsParams = msgspec.field(default_factory=lambda: MethodsParams())


__all__ = (
    "GeneratorMethods",
    "MethodsParams",
    "MethodsParamsAnnotations",
    "MethodsParamsAnnotationsAnnotations",
    "MethodsParamsAnnotationsAnnotationsParam",
    "MethodsParamsLiteralTypes",
    "MethodsParamsLiteralTypesParam",
)
