import msgspec


class ObjectsFieldsIdByDefaultField(msgspec.Struct):
    name: str
    nbytes: int


class ObjectsFieldsIdByDefault(msgspec.Struct):
    object_name: str
    fields: list[ObjectsFieldsIdByDefaultField]


class ObjectsFieldsDefaults(msgspec.Struct):
    random_id: list[ObjectsFieldsIdByDefault] = msgspec.field(default_factory=list)


class ObjectsFieldsLiteralTypesEnumLiterals(msgspec.Struct):
    name: str
    enumerations: list[str] = msgspec.field(default_factory=list)


class ObjectsFieldsLiteralTypesField(msgspec.Struct):
    name: str
    literals: list[str | int] = msgspec.field(default_factory=list)
    enum: str | None = None
    enum_literals: ObjectsFieldsLiteralTypesEnumLiterals | None = None
    default: str | None = None

    @property
    def enum_default(self) -> str | None:
        if self.enum is not None and self.default is not None:
            return f"{self.enum}.{self.default}"
        return None

    @property
    def enum_literals_default(self) -> str | None:
        if self.enum_literals is not None and self.default is not None:
            return f"{self.enum_literals.name}.{self.default}"
        return None

    @property
    def literals_default(self) -> str | None:
        if self.enum is None and self.default is not None:
            return self.default
        return None


class ObjectsFieldsLiteralTypes(msgspec.Struct):
    object_name: str
    fields: list[ObjectsFieldsLiteralTypesField]


class ObjectsFieldsAnnotationsAnnotationsField(msgspec.Struct):
    name: str
    annotation: str
    convert_from: str | None = None


class ObjectsFieldsAnnotationsAnnotations(msgspec.Struct):
    object_name: str
    fields: list[ObjectsFieldsAnnotationsAnnotationsField]


class ObjectsFieldsAnnotations(msgspec.Struct):
    annotations: list[ObjectsFieldsAnnotationsAnnotations] = msgspec.field(default_factory=list)
    literals: list[ObjectsFieldsLiteralTypes] = msgspec.field(default_factory=list)


class ObjectsFields(msgspec.Struct):
    defaults: ObjectsFieldsDefaults = msgspec.field(default_factory=lambda: ObjectsFieldsDefaults())
    annotations: ObjectsFieldsAnnotations = msgspec.field(default_factory=lambda: ObjectsFieldsAnnotations())


class GeneratorObjects(msgspec.Struct):
    fields: ObjectsFields = msgspec.field(default_factory=lambda: ObjectsFields())


__all__ = (
    "GeneratorObjects",
    "ObjectsFields",
    "ObjectsFieldsAnnotations",
    "ObjectsFieldsAnnotationsAnnotations",
    "ObjectsFieldsAnnotationsAnnotationsField",
    "ObjectsFieldsDefaults",
    "ObjectsFieldsIdByDefault",
    "ObjectsFieldsIdByDefaultField",
    "ObjectsFieldsLiteralTypes",
    "ObjectsFieldsLiteralTypesField",
)
