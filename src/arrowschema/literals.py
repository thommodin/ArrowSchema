import typing


pyarrow_integer = typing.Literal[
    "int8",
    "int16",
    "int32",
    "int64",
    "uint8",
    "uint16",
    "uint32",
    "uint64",
]

pyarrow_boolean = typing.Literal[
    "bool_",
    "bool8",
]

pyarrow_time_units = typing.Literal[
    "day",
    "s",
    "ms",
    "us",
    "ns",
]
