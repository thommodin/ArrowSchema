# ArrowSchema
Ever needed to 

It can be a bit of a chore having to deal with arrow schema's programatically... wouldn't it be nice to define the schema in some json instead?

ArrowSchema attempts to solve this issue by binding the `pyarrow.schema` interface to a primitive pydantic classes, allowing full json serialisation of an arrow schema.

## Caveats
Only a subset of types is allowed, and none of the more extended features eg list types.
