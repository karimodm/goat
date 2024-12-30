from abc import ABC
from typing import TypeVar, Generic
from zon import ZonRecord

T = TypeVar('T', bound=ZonRecord)

class ToolParametersStatic(Generic[T], ABC):
    schema: T

def create_tool_parameters(schema: T) -> ToolParametersStatic[T]:
    """
    Create a tool parameters class from a Zon schema.
    This mirrors the TypeScript version which uses Zod schemas.
    
    Args:
        schema: A Zon schema that defines the parameter structure
        
    Returns:
        A class type with the schema attached as a static property
    """
    class SchemaHolder(ToolParametersStatic):
        schema: T
        def __init__(self, schema: T):
            super().__init__()
            self.schema = schema
            
    return SchemaHolder(schema)