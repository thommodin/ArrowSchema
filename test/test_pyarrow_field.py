import arrowschema
import pyarrow
import pytest
import pydantic

name = "test"
type_ = "null"
nullable = True
metadata = {
    "standard_name": "air_density",
    "units": "kg m-3",
}


def test_native():
    assert arrowschema.PyarrowField(
        name=name,
        type=type_,
        nullable=nullable,
        metadata=metadata,
    ).native.equals(
        pyarrow.field(
            name,
            type=type_,
            nullable=nullable,
            metadata=metadata,
        ),
    )


def test_from_native():
    assert arrowschema.PyarrowField.from_native(
        native_pyarrow_field=pyarrow.field(
            name,
            type=type_,
            nullable=nullable,
            metadata=metadata,
        ),
    ) == arrowschema.PyarrowField(
        name=name,
        type=type_,
        nullable=nullable,
        metadata=metadata,
    )


def test_validate_null_type_is_nullable():
    with pytest.raises(pydantic.ValidationError):
        arrowschema.PyarrowField(
            name=name,
            type=arrowschema.PyarrowType.from_native(type_),
            nullable=False,
            metadata=metadata,
        )
