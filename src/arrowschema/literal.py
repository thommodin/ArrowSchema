import typing

pyarrow_null = typing.Literal["null",]


pyarrow_boolean = typing.Literal["bool",]


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


pyarrow_float = typing.Literal[
    "float16",
    "halffloat",
    "float32",
    "float",
    "float64",
    "double",
]


pyarrow_string = typing.Literal[
    "string",
    "utf8",
    "large_string",
    "large_utf8",
    "string_view",
]


pyarrow_binary = typing.Literal[
    "binary",
    "large_binary",
    "binary_view",
]


pyarrow_date = typing.Literal[
    "date32",
    "date32[day]",
    "date64",
    "date64[ms]",
]


pyarrow_time = typing.Literal[
    "time32",
    "time32[s]",
    "time32[ms]",
    "time64",
    "time64[us]",
    "time64[ns]",
]


pyarrow_duration = typing.Literal[
    "duration",
    "duration[s]",
    "duration[ms]",
    "duration[us]",
    "duration[ns]",
]


pyarrow_month_day_nano_interval = typing.Literal["month_day_nano_interval",]


pyarrow_timestamp = typing.Literal[
    "timestamp",
    "timestamp[s]",
    "timestamp[ms]",
    "timestamp[us]",
    "timestamp[ns]",
]

pyarrow_time_units = typing.Literal[
    "day",
    "s",
    "ms",
    "us",
    "ns",
]
