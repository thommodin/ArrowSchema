import arrowschema.model
import arrowschema.literals
import pyarrow
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

        # Check the native hydrated correctly
        assert (
            getattr(
                pyarrow,
                pyarrow_literal,
            )()
            is pyarrow_type.native
        )

    # Hydrate and test all native pyarrow types to type
    for pyarrow_type_ in pyarrow_types:
        pyarrow_type = arrowschema.model.PyarrowType.from_pyarrow(pyarrow_type_)

        assert pyarrow_type_ is pyarrow_type.native


def test_simple_types():
    _test_simple_type(
        literal=arrowschema.literals.pyarrow_integer,
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
