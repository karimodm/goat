from abc import ABC
from typing import TypeVar, Generic, Type
from zon import ZonRecord

T = TypeVar('T', bound=ZonRecord)

class ToolParameters(Generic[T]):
    schema: T

def create_tool_parameters(schema: T) -> ToolParameters[T]:
    # Check if schema is an instance of ZonRecord
    if not isinstance(schema, ZonRecord):
        raise ValueError(f"Schema must be an instance of ZonRecord, got {type(schema)}")

    return type(
        'SchemaHolder',
        (ToolParameters,),
        {
            'schema': schema,
            '__init__': lambda self: super(type(self), self).__init__()
        }
    )()