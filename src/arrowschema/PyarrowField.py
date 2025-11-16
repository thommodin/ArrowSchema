import arrowschema
import arrowschema.PyarrowBinder
import pyarrow
import pydantic
import typing


class PyarrowField(arrowschema.PyarrowBinder.PyarrowBinder):
    """
    Validate and hydrate pyarrow fields
    """

    name: str
    type: arrowschema.PyarrowType
    metadata: dict | None = pydantic.Field(default=None)
    nullable: bool = pydantic.Field(default=False)

    @classmethod
    def from_native(cls, native_pyarrow_field) -> typing.Self:
        return cls(
            name=native_pyarrow_field.name,
            metadata=native_pyarrow_field.metadata,
            nullable=native_pyarrow_field.nullable,
            type=arrowschema.PyarrowType.from_native(native_pyarrow_field.type),
        )

    @property
    def native(self) -> pyarrow.Field:
        return pyarrow.field(
            self.name,
            type=self.type.native,
            metadata=self.metadata,
            nullable=self.nullable,
        )

    @pydantic.model_validator(mode="after")
    def validate_null_type_is_nullable(self) -> typing.Self:
        """
        Pyarrow does not allow null type fields to not be nullable
        """
        if self.type.type == "null" and not self.nullable:
            raise ValueError("null type fields must have nullable set to true")

        return self
