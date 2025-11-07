import pydantic


class PyarrowType(pydantic.BaseModel):
    """
    Validate and hydrate pyarrow types

    Will probably be limited a to a subset to avoid extra complex types
    """
    pass


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