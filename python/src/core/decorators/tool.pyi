from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Type, TypedDict
from zon import ZonRecord

@dataclass
class ToolDecoratorParams:
    description: str
    name: Optional[str] = None

class ParameterMetadata(TypedDict):
    index: int
    schema: ZonRecord

class WalletClientMetadata(TypedDict):
    index: int

@dataclass 
class StoredToolMetadata:
    name: str
    description: str
    parameters: ParameterMetadata
    target: Callable
    wallet_client: Optional[WalletClientMetadata] = None

def Tool(params: ToolDecoratorParams) -> Callable: ...
def validate_method_parameters(target: Any, method_name: str) -> dict: ...
def get_tool_metadata(cls: Type) -> Dict[str, StoredToolMetadata]: ... 