from arrowschema.PyarrowField import PyarrowField


import pydantic


class PyarrowSchema(pydantic.BaseModel):
    """
    Validate and hydrate pyarrow schemas
    """

    fields: list[PyarrowField]
    metadata: dict
    pass
