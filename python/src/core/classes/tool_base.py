from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, TypeVar, TypedDict
from zon import ZonRecord

TParameters = TypeVar("TParameters", bound=ZonRecord)
TResult = TypeVar("TResult")

class ToolConfig(Generic[TParameters], TypedDict):
    """
    Configuration interface for creating a Tool
    
    Generic Parameters:
        TParameters: The Zon schema type for the tool's parameters
    
    Attributes:
        name: The name of the tool
        description: A description of what the tool does
        parameters: The Zon schema defining the tool's parameters
    """
    name: str
    description: str
    parameters: TParameters
    
class ToolBase(Generic[TParameters, TResult], ABC):
    """Abstract base class for creating tools with typed parameters and results"""
    
    name: str
    description: str
    parameters: TParameters
    
    def __init__(self, config: ToolConfig[TParameters]):
        """
        Creates a new Tool instance
        
        Args:
            config: The configuration object for the tool
        """
        super().__init__()
        self.name = config["name"]
        self.description = config["description"]
        self.parameters = config["parameters"]

    @abstractmethod
    def execute(self, parameters: dict[str, Any]) -> TResult:
        """
        Executes the tool with the provided parameters
        
        Args:
            parameters: The parameters for the tool execution, validated against the tool's schema
            
        Returns:
            The result of the tool execution
        """
        pass


def create_tool(
    config: ToolConfig[TParameters],
    execute_fn: Callable[[dict[str, Any]], TResult]
) -> ToolBase[TParameters, TResult]:
    """
    Creates a new Tool instance with the provided configuration and execution function

    Args:
        config: The configuration object for the tool
        execute_fn: The function to be called when the tool is executed

    Returns:
        A new Tool instance
    """
    
    class Tool(ToolBase):
        def execute(self, parameters: dict[str, Any]) -> TResult:
            # Validate parameters using the tool's schema before executing
            validated_params = self.parameters.validate(parameters)
            return execute_fn(validated_params)
    
    return Tool(config) 