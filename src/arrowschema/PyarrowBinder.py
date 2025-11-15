import abc
import pydantic
import typing


class PyarrowBinder(abc.ABC, pydantic.BaseModel):
    """
    Abstract class for the pyarrow binding elements

    Enforces the contract:
        from_native -> pyarrow to binder
        native -> binder to pyarrow
    """

    @classmethod
    @abc.abstractmethod
    def from_native(cls, native_pyarrow_schema_element) -> typing.Self:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def native(self) -> typing.Any:
        raise NotImplementedError()
