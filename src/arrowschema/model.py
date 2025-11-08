import arrowschema.literal
import pyarrow
import pydantic
import re
import typing
import warnings


class PyarrowType(pydantic.BaseModel):
    """
    Validate and hydrate pyarrow types

    Will probably be limited a to a subset to avoid extra complex types
    """

    type: (
        arrowschema.literal.pyarrow_null
        | arrowschema.literal.pyarrow_boolean
        | arrowschema.literal.pyarrow_integer
        | arrowschema.literal.pyarrow_float
        | arrowschema.literal.pyarrow_string
        | arrowschema.literal.pyarrow_binary
        | arrowschema.literal.pyarrow_date
        | arrowschema.literal.pyarrow_time
        | arrowschema.literal.pyarrow_duration
        | arrowschema.literal.pyarrow_month_day_nano_interval
        | arrowschema.literal.pyarrow_timestamp
    )
    unit: arrowschema.literal.pyarrow_time_units | None = pydantic.Field(
        default=None,
        description="The units. Applies to time related types",
    )
    tz: str | None = pydantic.Field(
        default=None,
        pattern=r"^([\+\-]\d{1,2}:\d{2}|[Zz])",
        description="The timezone. Applies to some time related types",
    )

    @property
    def alias(self) -> str:
        """
        The alias is a combination of the type and unit, if the unit exists

        Returns: str
        """
        return f"{self.type}[{self.unit}]" if self.unit else self.type

    @property
    def native(self):
        """
        Convert to a native pyarrow type
        """

        # Timestamp special case
        if self.type.startswith("timestamp"):
            return pyarrow.timestamp(
                self.unit,
                tz=self.tz,
            )

        # Otherwise use the type alias
        else:
            return pyarrow.type_for_alias(self.alias)

    @classmethod
    def from_pyarrow(cls, native_pyarrow_type) -> typing.Self:
        """
        Convert from a native pyarrow type instantiation to a PyarrowType

        `https://github.com/apache/arrow/blob/cd23a765442bdbaaef43d0e4b239094fb01e37ae/python/pyarrow/types.pxi#L5761C11-L5761C24`
        """
        # Extract datatype elements
        pattern = (
            # Type
            r"^(\w+)"
            # Unit
            r"(?:\[(day|s|ms|ns|us)"
            # TZ
            r"(?:,\s*tz=([\+\-]\d{1,2}:\d{2}|[Zz]))?\])?"
        )
        match = re.match(pattern, str(native_pyarrow_type))
        type_ = match.group(1)
        unit = match.group(2)
        tz = match.group(3)

        match type_:
            # Null
            case "null":
                return cls(type=type_)

            # Boolean
            case "bool":
                return cls(type=type_)

            # Integer
            case (
                "int8"
                | "int16"
                | "int32"
                | "int64"
                | "uint8"
                | "uint16"
                | "uint32"
                | "uint64"
            ):
                return cls(type=type_)

            # Float
            case "float16" | "halffloat" | "float32" | "float" | "float64" | "double":
                return cls(type=type_)

            # String
            case "utf8" | "string" | "large_string" | "large_utf8" | "string_view":
                return cls(type=type_)

            # String
            case "binary" | "large_binary" | "binary_view":
                return cls(type=type_)

            # Date
            case "date32" | "date64":
                return cls(
                    type=type_,
                    unit=unit,
                )

            # Time
            case "time32" | "time64":
                return cls(
                    type=type_,
                    unit=unit,
                )

            # Duration
            case "duration":
                return cls(
                    type=type_,
                    unit=unit,
                )

            # Month Day Nano Interval
            case "month_day_nano_interval":
                return cls(type=type_)

            # Timestamp
            case "timestamp":
                return cls(
                    type=type_,
                    unit=unit,
                    tz=tz,
                )

            case _:
                raise NotImplementedError(f"`{native_pyarrow_type}` not implemented")

    @pydantic.model_validator(mode="after")
    def check_time_type_unit_and_timezone_dependencies(self) -> typing.Self:
        """
        Validate the required units for time types
        are in place
        """
        if self.type.startswith("time32"):
            if self.unit not in {"s", "ms"}:
                raise ValueError(
                    f"time32 requires units `s` or `ms`, found: `{self.unit}`"
                )

        elif self.type.startswith("time64"):
            if self.unit not in {"us", "ns"}:
                raise ValueError(
                    f"time64 requires units `us` or `ns`, found: `{self.unit}`"
                )

        elif self.type.startswith("date32"):
            if self.unit != "day":
                raise ValueError(f"date32 requires units `day`, found: `{self.unit}`")

        elif self.type.startswith("date64"):
            if self.unit != "ms":
                raise ValueError(f"date64 requires units `ms`, found: `{self.unit}`")

        elif self.type.startswith("timestamp"):
            if self.unit not in {"s", "ms", "us", "ns"}:
                raise ValueError(
                    f"timestamp requires units `s`, `ms`, `us` or `ns`, found: `{self.unit}`"
                )
            elif self.tz is None:
                raise ValueError("timestamp requires a tz")

        elif self.type.startswith("duration"):
            if self.unit not in {"s", "ms", "us", "ns"}:
                raise ValueError(
                    f"duration requires units `s`, `ms`, `us` or `ns`, found: `{self.unit}`"
                )
        else:
            if self.unit is not None or self.tz is not None:
                warnings.warn(
                    f"unit of type `{self.type}` should not have a unit or timezone specified (unit=`{self.unit}`, timezone=`{self.unit})"
                )

        return self


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
