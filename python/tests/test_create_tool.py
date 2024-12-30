import pytest
from zon import ZonRecord, ZonString, ZonNumber, ZonError
from core.classes.tool_base import create_tool, ToolConfig

def test_create_tool():
    # Create a simple parameter schema
    parameters = ZonRecord({
        "message": ZonString(),
        "count": ZonNumber()
    })

    parameters.shape["message"].description = "A test message" # type: ignore
    parameters.shape["count"].description = "Number of times to repeat" # type: ignore
    
    # Create tool configuration
    config = ToolConfig(
        name="test_tool",
        description="A test tool that repeats a message",
        parameters=parameters
    )
    
    # Define the execution function
    def execute_fn(params):
        return params["message"] * params["count"]
    
    # Create the tool
    tool = create_tool(config, execute_fn)
    
    # Test tool attributes
    assert tool.name == "test_tool"
    assert tool.description == "A test tool that repeats a message"
    assert tool.parameters == parameters
    
    # Test tool execution with valid parameters
    result = tool.execute({
        "message": "hello ",
        "count": 3
    })
    assert result == "hello hello hello "
    
    # Test parameter validation
    with pytest.raises(ZonError):
        tool.execute({
            "message": "hello",
            "count": "not a number"  # This should fail validation
        })
    
    with pytest.raises(ZonError):
        tool.execute({
            "message": 123,  # This should fail validation
            "count": 3
        })
    
    # Test missing parameters
    with pytest.raises(ZonError):
        tool.execute({
            "message": "hello"
            # missing count parameter
        })

def test_create_tool_async():
    # Create a simple parameter schema
    parameters = ZonRecord({
        "delay": ZonNumber()
    })

    parameters.shape["delay"].description = "Delay in seconds" # type: ignore
    
    # Create tool configuration
    config = ToolConfig(
        name="async_test_tool",
        description="A test tool that returns after a delay",
        parameters=parameters
    )
    
    # Define an async execution function
    async def execute_fn(params):
        import asyncio
        await asyncio.sleep(params["delay"])
        return f"Completed after {params['delay']} seconds"
    
    # Create the tool
    tool = create_tool(config, execute_fn)
    
    # Test tool attributes
    assert tool.name == "async_test_tool"
    assert tool.description == "A test tool that returns after a delay"
    assert tool.parameters == parameters
    
    # Note: Testing async execution would require running in an async context
    # This is just testing the tool creation for async functions 