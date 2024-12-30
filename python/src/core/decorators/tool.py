from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Dict, Optional, Type, Union, TypedDict
import inspect
from core.decorators.tool import StoredToolMetadata
from zon import ZonRecord

from core.classes import WalletClientBase
from core.utils.snake_case import snake_case

# Store tool metadata at module level
_tool_metadata: Dict[Type, Dict[str, StoredToolMetadata]] = {}

def validate_method_parameters(target: Any, method_name: str) -> dict:
    """
    Validates the parameters of a tool method to ensure it has the correct signature.
    
    Args:
        target: The class instance or class containing the method
        method_name: Name of the method being decorated
    
    Returns:
        Dict containing validated parameter information
    """
    class_name = target.__class__.__name__ if hasattr(target, '__class__') else None
    log_prefix = f"Method '{method_name}'" + (f" on class '{class_name}'" if class_name else "")
    explainer = ("Tool methods must have at least one parameter that is a Zon schema class "
                "created with the create_tool_parameters function.")

    # Get method signature
    method = getattr(target, method_name)
    sig = inspect.signature(method)
    params = list(sig.parameters.values())

    if len(params) == 0:
        raise ValueError(f"{log_prefix} has no parameters. {explainer}")
    if len(params) > 2:
        raise ValueError(f"{log_prefix} has {len(params)} parameters. {explainer}")

    # Find parameters that match our requirements
    parameters_param = None
    wallet_client_param = None
    
    for idx, param in enumerate(params):
        if hasattr(param.annotation, 'schema') and isinstance(param.annotation.schema, ZonSchema):
            parameters_param = {'index': idx, 'schema': param.annotation.schema}
        elif (isinstance(param.annotation, type) and 
              issubclass(param.annotation, WalletClientBase)):
            wallet_client_param = {'index': idx}

    if not parameters_param:
        raise ValueError(
            f"{log_prefix} has no parameters parameter.\n\n"
            f"1.) {explainer}\n\n"
            "2.) Ensure that you are using proper Zon schema annotations."
        )

    result = {'parameters': parameters_param}
    if wallet_client_param:
        result['wallet_client'] = wallet_client_param

    return result

def Tool(params: ToolDecoratorParams):
    """
    Decorator that marks a class method as a tool accessible to the LLM.
    
    Args:
        params: Configuration parameters for the tool
        
    Returns:
        Decorated method
        
    Example:
        class MyToolService:
            @Tool(description="Adds two numbers")
            def add(self, params: AddParameters):
                return params.a + params.b
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Get the class from the first argument (self)
        if not args:
            raise ValueError("Tool decorator can only be used on class methods")
        
        target_class = args[0].__class__
        
        # Validate parameters and get metadata
        validated = validate_method_parameters(target_class, func.__name__)
        
        # Create tool metadata
        metadata = StoredToolMetadata(
            name=params.name or snake_case(func.__name__),
            description=params.description,
            parameters=validated['parameters'],
            wallet_client=validated.get('wallet_client'),
            target=func
        )

        # Store metadata
        if target_class not in _tool_metadata:
            _tool_metadata[target_class] = {}
        _tool_metadata[target_class][func.__name__] = metadata

        return wrapper
    return decorator

def get_tool_metadata(cls: Type) -> Dict[str, StoredToolMetadata]:
    """Get all tool metadata for a class"""
    return _tool_metadata.get(cls, {})