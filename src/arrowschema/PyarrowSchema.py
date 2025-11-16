import arrowschema
import arrowschema.PyarrowBinder
import pyarrow
import pydantic
import typing


class PyarrowSchema(arrowschema.PyarrowBinder.PyarrowBinder):
    """
    Validate and hydrate pyarrow schemas
    """

    fields: list[arrowschema.PyarrowField]
    metadata: dict | None = pydantic.Field(default=None)

    @classmethod
    def from_native(
        cls,
        native_pyarrow_schema: pyarrow.Schema,
    ) -> typing.Self:
        # Decode metadata if exists
        metadata = (
            {
                key.decode(): value.decode()
                for key, value in native_pyarrow_schema.metadata.items()
            }
            if isinstance(native_pyarrow_schema.metadata, dict)
            else None
        )

        # Hydrate schema
        fields = [
            arrowschema.PyarrowField.from_native(field)
            for field in native_pyarrow_schema
        ]

        return cls(
            fields=fields,
            metadata=metadata,
        )

    @property
    def native(self) -> pyarrow.Schema:
        return pyarrow.schema(
            fields=[field.native for field in self.fields], metadata=self.metadata
        )
