import arrowschema
import arrowschema.PyarrowBinder


class PyarrowField(arrowschema.PyarrowBinder.PyarrowBinder):
    """
    Validate and hydrate pyarrow fields
    """

    name: str
    metadata: dict
    type: arrowschema.PyarrowType
