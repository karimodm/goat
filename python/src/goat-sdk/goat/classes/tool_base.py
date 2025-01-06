from abc import ABC, abstractmethod
from typing import (
    Any,
    Callable,
    Generic,
    TypeVar,
    TypedDict,
    Optional,
    List,
    Dict,
    Type,
)
from pydantic import BaseModel, create_model
from zon import (
    Zon,
    ZonList,
    ZonRecord,
    ZonString,
    ZonNumber,
    ZonBoolean,
    ZonOptional,
    ZonRecord,
)

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
    config: ToolConfig[TParameters], execute_fn: Callable[[dict[str, Any]], TResult]
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
            validated_params = self.parameters.strict().validate(parameters)
            return execute_fn(validated_params)

    return Tool(config)


def zon_to_pydantic(
    zon_schema: ZonRecord, model_name: str = "DynamicModel"
) -> Type[BaseModel]:
    """
    Convert a Zon Record schema into a Pydantic BaseModel class.

    Args:
        zon_schema: A Zon Record schema
        model_name: Name for the generated Pydantic model class

    Returns:
        A Pydantic BaseModel class
    """

    def _convert_field(field: Zon) -> tuple[Type, Any]:
        if isinstance(field, ZonString):
            return (str, ...)
        elif isinstance(field, ZonNumber):
            return (float, ...)
        elif isinstance(field, ZonBoolean):
            return (bool, ...)
        elif isinstance(field, ZonList):
            item_type, _ = _convert_field(field.element)
            return (List[item_type], ...)
        elif isinstance(field, ZonOptional):
            inner_type, _ = _convert_field(field.unwrap())
            return (Optional[inner_type], None)  # type: ignore
        elif isinstance(field, ZonRecord):
            # Recursively create nested models
            nested_model = zon_to_pydantic(field, f"{model_name}Nested")
            return (nested_model, ...)
        else:
            raise ValueError(f"Unsupported Zon type: {type(field)}")

    # Convert Zon schema fields to Pydantic field definitions
    field_definitions: Dict[str, tuple[Type, Any]] = {}

    for field_name, field_schema in zon_schema.shape.items():
        field_type, field_default = _convert_field(field_schema)
        field_definitions[field_name] = (field_type, field_default)

    # Create and return the Pydantic model
    return create_model(model_name, **field_definitions)
