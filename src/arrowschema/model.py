import arrowschema.literals
import pyarrow
import pydantic
import re
import typing


class PyarrowType(pydantic.BaseModel):
    """
    Validate and hydrate pyarrow types

    Will probably be limited a to a subset to avoid extra complex types
    """

    type: arrowschema.literals.pyarrow_integer
    unit: arrowschema.literals.pyarrow_time_units | None = pydantic.Field(
        default=None,
        description="The units. Applies to time related types",
    )
    tz: str | None = pydantic.Field(
        default=None,
        pattern=r"^([\+\-]\d{1,2}:\d{2}|[Zz])",
        description="The timezone. Applies to some time related types",
    )

    @property
    def native(self):
        """
        Convert to a native pyarrow type
        """

        # Extract the type function
        pyarrow_type = getattr(pyarrow, self.type)

        # Return the type with unit and timezone
        if self.tz is not None:
            return pyarrow_type(unit=self.unit, tz=self.timezone)

        # Return the type with unit
        elif self.unit is not None:
            return pyarrow_type(
                unit=self.unit,
            )

        # Return just the type
        else:
            return pyarrow_type()

    @classmethod
    def from_pyarrow(cls, native_pyarrow_type) -> typing.Self:
        """
        Convert from a native pyarrow type instantiation to a PyarrowType
        """

        # Extract datatype elements
        pattern = (
            # The type
            r"^(\w+)"
            # The units (if exists)
            r"|(?:\[(day|s|ms|us|ns)"
            # The timezone (if exists)
            r"|(?:,\s*tz=)?(([\+\-]\d{1,2}:\d{2}|[Zz]))?\])?$"
        )
        match = re.match(pattern, str(native_pyarrow_type))
        if isinstance(match, re.Match):
            pyarrow_datatype = match.group(1)
            pyarrow_unit = match.group(2)
            pyarrow_timezone = match.group(3)
        else:
            raise ValueError(f"incompatible field type: {native_pyarrow_type}")

        return cls(
            type=pyarrow_datatype,
            unit=pyarrow_unit,
            timezone=pyarrow_timezone,
        )


class PyarrowField(pydantic.BaseModel):
    """
    Validate and hydrate pyarrow fields
    """

    name: str
    metadata: dict
    pass


class PyarrowSchema(pydantic.BaseModel):
    """
    Validate and hydrate pyarrow schemas
    """

    fields: list[PyarrowField]
    metadata: dict
    pass
