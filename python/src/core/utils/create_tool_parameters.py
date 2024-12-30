from abc import ABC
from typing import TypeVar, Generic, Type
from zon import ZonRecord

T = TypeVar('T', bound=ZonRecord)

class ToolParametersStatic(Generic[T], ABC):
    schema: T

def create_tool_parameters(schema: T) -> ToolParametersStatic[T]:
    class SchemaHolder(ToolParametersStatic):
        schema: T
        def __init__(self, schema: T):
            super().__init__()
            self.schema = schema
            
    return SchemaHolder(schema)