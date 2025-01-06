from typing import Any
import pytest
from core.core.decorators.tool import Tool
from core.core.classes.wallet_client_base import Signature, Balance, WalletClientBase
from core.core.types.chain import Chain, EvmChain
from zon import ZonRecord, ZonString
from core.core.utils.create_tool_parameters import create_tool_parameters

# Create test schemas and classes
test_schema = ZonRecord({
    "value": ZonString()
})

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
    @Tool({
        "description": "Test tool",
        "parameters": create_tool_parameters(test_schema)
    })
    def test_method(self, params: dict) -> str:
        return params["value"]
    
    @Tool({
        "description": "Test tool with wallet",
        "name": "custom_name",
        "parameters": create_tool_parameters(test_schema)
    })
    def test_method_with_wallet(self, params: dict, wallet: TestWalletClient) -> str:
        return f"{params['value']} with wallet"

class TestToolDecorator:
    def test_tool_decorator_functionality(self):
        service = ToolService()
        
        # Test with valid parameters
        result = service.test_method({"value": "test"})
        assert result == "test"
        
        result = service.test_method_with_wallet({"value": "test"}, TestWalletClient())
        assert result == "test with wallet"

    def test_tool_decorator_validation(self):
        # Test invalid method signatures
        with pytest.raises(ValueError):
            class InvalidService:
                @Tool({ # type: ignore
                    "description": "Invalid tool",
                })
                def no_params(self):
                    pass

        with pytest.raises(ValueError):
            class InvalidService2:
                @Tool({
                    "description": "Invalid tool",
                    "parameters": test_schema # type: ignore
                })
                def too_many_params(self, param1: Any, param2: TestWalletClient, param3: str):
                    pass 