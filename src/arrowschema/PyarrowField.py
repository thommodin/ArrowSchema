import arrowschema
import arrowschema.PyarrowBinder
import pyarrow
import pydantic
import typing


class PyarrowField(arrowschema.PyarrowType, arrowschema.PyarrowBinder.PyarrowBinder):
    """
    Validate and hydrate pyarrow fields
    """

    name: str
    # type: arrowschema.PyarrowType
    metadata: dict | None = pydantic.Field(default=None)
    nullable: bool = pydantic.Field(default=False)

    @classmethod
    def from_native(cls, native_pyarrow_field) -> typing.Self:
        # Extract type
        pyarrow_type = arrowschema.PyarrowType.from_native(
            native_pyarrow_field.type,
        )

        # Decode metadata if exists
        metadata = (
            {
                key.decode(): value.decode()
                for key, value in native_pyarrow_field.metadata.items()
            }
            if isinstance(native_pyarrow_field.metadata, dict)
            else None
        )

        return cls(
            name=native_pyarrow_field.name,
            metadata=metadata,
            nullable=native_pyarrow_field.nullable,
            type=pyarrow_type.type,
            unit=pyarrow_type.unit,
            tz=pyarrow_type.tz,
        )

    @property
    def native(self) -> pyarrow.Field:
        pyarrow_type = arrowschema.PyarrowType(
            type=self.type,
            unit=self.unit,
            tz=self.tz,
        )

        return pyarrow.field(
            self.name,
            type=pyarrow_type.native,
            metadata=self.metadata,
            nullable=self.nullable,
        )

    @pydantic.model_validator(mode="after")
    def validate_null_type_is_nullable(self) -> typing.Self:
        """
        Pyarrow does not allow null type fields to not be nullable
        """
        if self.type == "null" and not self.nullable:
            raise ValueError("null type fields must have nullable set to true")

        return self
