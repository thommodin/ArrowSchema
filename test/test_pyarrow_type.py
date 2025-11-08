import arrowschema.model
import arrowschema.literals
import pyarrow
import typing


def test_int():
    # Hydrate and test all type to native calls for pyarrow integers
    pyarrow_integer_literals = list(
        typing.get_args(arrowschema.literals.pyarrow_integer)
    )

    for literpyarrow_integer_literal in pyarrow_integer_literals:
        pyarrow_type = arrowschema.model.PyarrowType(
            type=literpyarrow_integer_literal,
        )

        # Check the native hydrated correctly
        assert (
            getattr(
                pyarrow,
                literpyarrow_integer_literal,
            )()
            is pyarrow_type.native
        )

    # Hydrate and test all native to type calls for pyarrow integers
    pyarrow_integer_types = [
        pyarrow.int8(),
        pyarrow.int16(),
        pyarrow.int32(),
        pyarrow.int64(),
        pyarrow.uint8(),
        pyarrow.uint16(),
        pyarrow.uint32(),
        pyarrow.uint64(),
    ]
    for pyarrow_integer_type in pyarrow_integer_types:
        pyarrow_type = arrowschema.model.PyarrowType.from_pyarrow(pyarrow_integer_type)

        assert pyarrow_integer_type is pyarrow_type.native
