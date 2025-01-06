from zon import ZonRecord, ZonString, ZonNumber
from goat.utils.create_tool_parameters import create_tool_parameters

# GetTokenInfoBySymbol parameters
symbol_param = ZonString()
symbol_param.description = "The symbol of the token to get the info of"  # type: ignore

token_info_schema = ZonRecord({"symbol": symbol_param})

GetTokenInfoBySymbolParameters = create_tool_parameters(token_info_schema)

# GetTokenBalance parameters
wallet_param = ZonString()
wallet_param.description = "The address to get the balance of"  # type: ignore

token_address_param = ZonString()
token_address_param.description = "The address of the token to get the balance of"  # type: ignore

balance_schema = ZonRecord(
    {"wallet": wallet_param, "tokenAddress": token_address_param}
)

GetTokenBalanceParameters = create_tool_parameters(balance_schema)

# Transfer parameters
to_param = ZonString()
to_param.description = "The address to transfer the token to"  # type: ignore

amount_param = ZonString()
amount_param.description = "The amount of tokens to transfer in base units"  # type: ignore

transfer_schema = ZonRecord(
    {"tokenAddress": token_address_param, "to": to_param, "amount": amount_param}
)

TransferParameters = create_tool_parameters(transfer_schema)

# GetTokenTotalSupply parameters
total_supply_schema = ZonRecord({"tokenAddress": token_address_param})

GetTokenTotalSupplyParameters = create_tool_parameters(total_supply_schema)

# GetTokenAllowance parameters
owner_param = ZonString()
owner_param.description = "The address to check the allowance of"  # type: ignore

spender_param = ZonString()
spender_param.description = "The address to check the allowance for"  # type: ignore

allowance_schema = ZonRecord(
    {
        "tokenAddress": token_address_param,
        "owner": owner_param,
        "spender": spender_param,
    }
)

GetTokenAllowanceParameters = create_tool_parameters(allowance_schema)

# Approve parameters
approve_spender_param = ZonString()
approve_spender_param.description = "The address to approve the allowance to"  # type: ignore

approve_amount_param = ZonString()
approve_amount_param.description = "The amount of tokens to approve in base units"  # type: ignore

approve_schema = ZonRecord(
    {
        "tokenAddress": token_address_param,
        "spender": approve_spender_param,
        "amount": approve_amount_param,
    }
)

ApproveParameters = create_tool_parameters(approve_schema)

# TransferFrom parameters
from_param = ZonString()
from_param.description = "The address to transfer the token from"  # type: ignore

transfer_from_schema = ZonRecord(
    {
        "tokenAddress": token_address_param,
        "from": from_param,
        "to": to_param,
        "amount": amount_param,
    }
)

TransferFromParameters = create_tool_parameters(transfer_from_schema)

# ConvertToBaseUnit parameters
amount_number_param = ZonNumber()
amount_number_param.description = "The amount of tokens to convert from decimal units to base units"  # type: ignore

decimals_param = ZonNumber()
decimals_param.description = "The number of decimals of the token"  # type: ignore

convert_to_base_schema = ZonRecord(
    {"amount": amount_number_param, "decimals": decimals_param}
)

ConvertToBaseUnitParameters = create_tool_parameters(convert_to_base_schema)

# ConvertFromBaseUnit parameters
from_base_amount_param = ZonNumber()
from_base_amount_param.description = "The amount of tokens to convert from base units to decimal units"  # type: ignore

convert_from_base_schema = ZonRecord(
    {"amount": from_base_amount_param, "decimals": decimals_param}
)

ConvertFromBaseUnitParameters = create_tool_parameters(convert_from_base_schema)
