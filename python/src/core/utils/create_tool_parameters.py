from abc import ABC
from typing import TypeVar, Generic, Type
from zon import ZonRecord

T = TypeVar('T', bound=ZonRecord)

class ToolParameters(Generic[T]):
    schema: T

def create_tool_parameters(schema: T) -> ToolParameters[T]:
    return type(
        'SchemaHolder',
        (ToolParameters,),
        {
            'schema': schema,
            '__init__': lambda self: super(type(self), self).__init__()
        }
    )()