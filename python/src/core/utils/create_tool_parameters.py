from abc import ABC
from typing import TypeVar, Generic, Type
from zon import ZonRecord

T = TypeVar('T', bound=ZonRecord)

class ToolParametersStatic(Generic[T], ABC):
    schema: T

def create_tool_parameters(schema: T) -> Type[ToolParametersStatic[T]]:
    return type(
        'SchemaHolder',
        (ToolParametersStatic,),
        {
            'schema': schema,
            '__init__': lambda self: super(type(self), self).__init__()
        }
    )