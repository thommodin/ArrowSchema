import arrowschema.model
import arrowschema.literal
import pyarrow
import re
import typing


def _test_simple_type(
    literal: typing.Type,
    pyarrow_types: list,
):
    # Hydrate and test all type to native calls for pyarrow integers
    pyarrow_literals = list(typing.get_args(literal))

    for pyarrow_literal in pyarrow_literals:
        pyarrow_type = arrowschema.model.PyarrowType(
            type=pyarrow_literal,
        )
        pyarrow_type.native

        # Check the native hydrated correctly
        assert pyarrow.type_for_alias(pyarrow_literal).equals(pyarrow_type.native)

    # Hydrate and test all native pyarrow types to type
    for pyarrow_type_ in pyarrow_types:
        pyarrow_type = arrowschema.model.PyarrowType.from_pyarrow(pyarrow_type_)
        assert pyarrow_type_.equals(pyarrow_type.native)


def _test_unit_type(
    literal: typing.Type,
    pyarrow_types: list,
):
    # Hydrate and test all type to native calls for pyarrow integers
    pyarrow_literals = list(typing.get_args(literal))

    # Filter to literals with units
    for pyarrow_literal in [
        pyarrow_literal
        for pyarrow_literal in pyarrow_literals
        if re.match(
            pattern=r"(\w+)\[.*\]",
            string=pyarrow_literal,
        )
        is not None
    ]:
        # Extract type and unit
        match = re.match(
            # Extract datatype elements
            pattern=(
                # Type
                r"^(\w+)"
                # Unit
                r"(?:\[(day|s|ms|ns|us)\])"
                # TZ
                # r"(?:,\s*tz=([\+\-]\d{1,2}:\d{2}|[Zz]))?\])?"
            ),
            string=pyarrow_literal,
        )
        type_ = match.group(1)
        unit = match.group(2)
        tz = "z" if type_ == "timestamp" else None

        pyarrow_type = arrowschema.model.PyarrowType(
            type=type_,
            unit=unit,
            tz=tz,
        )

        match type_:
            # Date 32 has units but only one for 32 and 64, so does not take them
            case "date32" | "date64":
                assert pyarrow.type_for_alias(type_).equals(pyarrow_type.native)

            # Time related with units
            case "time32" | "time64" | "duration" | "month_day_nano_interval":
                assert getattr(pyarrow, type_)(unit).equals(pyarrow_type.native)

    # Hydrate and test all native pyarrow types to type
    for pyarrow_type_ in pyarrow_types:
        pyarrow_type = arrowschema.model.PyarrowType.from_pyarrow(pyarrow_type_)
        assert pyarrow_type_.equals(pyarrow_type.native)


def test_null_type():
    _test_simple_type(
        literal=arrowschema.literal.pyarrow_null,
        pyarrow_types=[
            pyarrow.null(),
        ],
    )


def test_bool_type():
    _test_simple_type(
        literal=arrowschema.literal.pyarrow_boolean,
        pyarrow_types=[
            pyarrow.bool_(),
        ],
    )


def test_integer_types():
    _test_simple_type(
        literal=arrowschema.literal.pyarrow_integer,
        pyarrow_types=[
            pyarrow.int8(),
            pyarrow.int16(),
            pyarrow.int32(),
            pyarrow.int64(),
            pyarrow.uint8(),
            pyarrow.uint16(),
            pyarrow.uint32(),
            pyarrow.uint64(),
        ],
    )


def test_float_types():
    _test_simple_type(
        literal=arrowschema.literal.pyarrow_integer,
        pyarrow_types=[
            pyarrow.float16(),
            pyarrow.float32(),
            pyarrow.float64(),
        ],
    )


def test_string_types():
    _test_simple_type(
        literal=arrowschema.literal.pyarrow_string,
        pyarrow_types=[
            pyarrow.string(),
            pyarrow.utf8(),
            pyarrow.large_string(),
            pyarrow.large_utf8(),
            pyarrow.string_view(),
        ],
    )


def test_binary_types():
    _test_simple_type(
        literal=arrowschema.literal.pyarrow_binary,
        pyarrow_types=[
            pyarrow.binary(),
            pyarrow.large_binary(),
            pyarrow.binary_view(),
        ],
    )


def test_date_types():
    _test_unit_type(
        literal=arrowschema.literal.pyarrow_date,
        pyarrow_types=[
            pyarrow.date32(),
            pyarrow.date64(),
        ],
    )


def test_time_types():
    _test_unit_type(
        literal=arrowschema.literal.pyarrow_time,
        pyarrow_types=[
            pyarrow.time32("s"),
            pyarrow.time32("ms"),
            pyarrow.time64("us"),
            pyarrow.time64("ns"),
        ],
    )


def test_duration_types():
    _test_unit_type(
        literal=arrowschema.literal.pyarrow_duration,
        pyarrow_types=[
            pyarrow.duration("s"),
            pyarrow.duration("ms"),
            pyarrow.duration("us"),
            pyarrow.duration("ns"),
        ],
    )


def test_month_day_nano_interval_type():
    _test_unit_type(
        literal=arrowschema.literal.pyarrow_month_day_nano_interval,
        pyarrow_types=[
            pyarrow.month_day_nano_interval(),
        ],
    )


def test_timestamp_type():
    _test_unit_type(
        literal=arrowschema.literal.pyarrow_timestamp,
        pyarrow_types=[
            pyarrow.timestamp("s", tz="z"),
            pyarrow.timestamp("ms", tz="z"),
            pyarrow.timestamp("ns", tz="z"),
            pyarrow.timestamp("us", tz="z"),
        ],
    )
