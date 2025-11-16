import arrowschema
import pathlib

# Load from json
pyarrow_schema = arrowschema.PyarrowSchema.model_validate_json(
    json_data=pathlib.Path("example/example.schema.json").read_text()
)

print(pyarrow_schema.model_dump(exclude_none=True))
print(pyarrow_schema.native)
