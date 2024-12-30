from core.types.chain import Chain, EvmChain
import pytest
from dataclasses import dataclass
from core.decorators.tool import Tool, ToolDecoratorParams
from core.classes.wallet_client_base import Signature, Balance, WalletClientBase
from zon import ZonRecord, ZonString
from core.utils.create_tool_parameters import create_tool_parameters, ToolParametersStatic
from typing import TypedDict, Any, Dict, Type, cast

# Create test schemas and classes
test_schema = ZonRecord({
    "value": ZonString()
})

TestParameters = create_tool_parameters(test_schema)

class TestWalletClient(WalletClientBase):
    def get_address(self) -> str:
        return "0x123"
    
    def get_chain(self) -> Chain:
        return EvmChain(type="evm", id=1)
    
    async def sign_message(self, message: str) -> Signature:
        return Signature(signature=f"signed_{message}")
    
    async def balance_of(self, address: str) -> Balance:
        return Balance(decimals=18, symbol="ETH", name="Ethereum", value="100", in_base_units="100")

# Separate service class from test class to avoid pytest collecting it
class ToolService:
    @Tool(ToolDecoratorParams(description="Test tool"))
    def test_method(self, params: Any) -> str:
        return cast(Dict[str, str], params)["value"]
    
    @Tool(ToolDecoratorParams(description="Test tool with wallet", name="custom_name"))
    def test_method_with_wallet(self, params: Any, wallet: TestWalletClient) -> str:
        return f"{cast(Dict[str, str], params)['value']} with wallet"

class TestToolDecorator:
    def test_tool_decorator_functionality(self):
        # Create instance of service
        service = ToolService()
        
        # Test actual method execution
        result = service.test_method({"value": "test"})
        assert result == "test"
        
        result = service.test_method_with_wallet({"value": "test"}, TestWalletClient())
        assert result == "test with wallet"

    def test_tool_decorator_validation(self):
        # Test invalid method signatures
        with pytest.raises(ValueError, match="Tool methods must have at least one parameter"):
            class InvalidService:
                @Tool(ToolDecoratorParams(description="Invalid tool"))
                def no_params(self):
                    pass

        with pytest.raises(ValueError, match="Tool methods must have at least one parameter"):
            class InvalidService2:
                @Tool(ToolDecoratorParams(description="Invalid tool"))
                def too_many_params(self, param1: Any, param2: TestWalletClient, param3: str):
                    pass 