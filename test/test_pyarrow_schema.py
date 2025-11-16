import arrowschema
import pyarrow

field = pyarrow.field(
    name="test",
    type=pyarrow.null(),
    nullable=True,
    metadata=None,
)

schema_metadata = {
    "This is a test schema metadat": "Ja, ja.",
}


def test_native():
    assert arrowschema.PyarrowSchema(
        fields=[
            arrowschema.PyarrowField.from_native(field),
        ],
        metadata=schema_metadata,
    ).native == pyarrow.schema(
        fields=[
            field,
        ],
        metadata=schema_metadata,
    )


def test_from_native():
    assert arrowschema.PyarrowSchema.from_native(
        pyarrow.schema(
            fields=[
                field,
            ],
            metadata=schema_metadata,
        )
    ).native == pyarrow.schema(
        fields=[
            field,
        ],
        metadata=schema_metadata,
    )
