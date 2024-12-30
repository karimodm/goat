from core.utils.add_parameters_to_description import add_parameters_to_description
import pytest
from zon import ZonRecord, ZonString, ZonError
from core.utils.create_tool_parameters import create_tool_parameters

def test_create_token_parameters():
    # Test GetTokenInfoBySymbol
    symbol_param = ZonString()
    symbol_param.description = "The symbol of the token to get the info of"
    GetTokenInfoBySymbolParameters = create_tool_parameters(
        ZonRecord({
            "symbol": symbol_param
        })
    )
    
    # Test GetTokenBalance
    wallet_param = ZonString()
    wallet_param.description = "The wallet to get the balance of"
    token_address_param = ZonString()
    token_address_param.description = "The token address to get the balance of"
    
    GetTokenBalanceParameters = create_tool_parameters(
        ZonRecord({
            "wallet": wallet_param,
            "tokenAddress": token_address_param
        })
    )

    # Verify the schemas are accessible
    assert "symbol" in GetTokenInfoBySymbolParameters.schema.shape
    assert "wallet" in GetTokenBalanceParameters.schema.shape
    assert "tokenAddress" in GetTokenBalanceParameters.schema.shape

    # Test schema validation
    token_info_schema = GetTokenInfoBySymbolParameters.schema
    assert token_info_schema.validate({"symbol": "ETH"})

    # This should raise a validation error
    with pytest.raises(ZonError):
        token_info_schema.validate({"symbol": 123}) 