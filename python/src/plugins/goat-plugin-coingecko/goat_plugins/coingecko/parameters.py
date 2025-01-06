from zon import ZonRecord, ZonString, ZonNumber, ZonBoolean, ZonOptional
from goat.utils.create_tool_parameters import create_tool_parameters

# Create fields for GetTrendingCoinsParameters
limit_param = ZonOptional(ZonNumber())
limit_param.description = "The number of trending coins to return. Defaults to all coins." # type: ignore

include_platform_param = ZonOptional(ZonBoolean())
include_platform_param.description = "Include platform contract addresses (e.g., ETH, BSC) in response" # type: ignore

trending_coins_schema = ZonRecord({
    "limit": limit_param,
    "include_platform": include_platform_param
})

GetTrendingCoinsParameters = create_tool_parameters(trending_coins_schema)

# Create fields for GetCoinPriceParameters
coin_id_param = ZonString()
coin_id_param.description = "The ID of the coin on CoinGecko (e.g., 'bitcoin', 'ethereum')" # type: ignore

vs_currency_param = ZonString()
vs_currency_param.description = "The target currency to get price in (e.g., 'usd', 'eur', 'jpy')" # type: ignore

include_market_cap_param = ZonBoolean()
include_market_cap_param.description = "Include market cap data in the response" # type: ignore

include_24hr_vol_param = ZonBoolean()
include_24hr_vol_param.description = "Include 24 hour volume data in the response" # type: ignore

include_24hr_change_param = ZonBoolean()
include_24hr_change_param.description = "Include 24 hour price change data in the response" # type: ignore

include_last_updated_at_param = ZonBoolean()
include_last_updated_at_param.description = "Include last updated timestamp in the response" # type: ignore

coin_price_schema = ZonRecord({
    "coin_id": coin_id_param,
    "vs_currency": vs_currency_param,
    "include_market_cap": include_market_cap_param,
    "include_24hr_vol": include_24hr_vol_param,
    "include_24hr_change": include_24hr_change_param,
    "include_last_updated_at": include_last_updated_at_param
})

GetCoinPriceParameters = create_tool_parameters(coin_price_schema)

# Create fields for SearchCoinsParameters
query_param = ZonString()
query_param.description = "The search query to find coins (e.g., 'bitcoin' or 'btc')" # type: ignore

exact_match_param = ZonBoolean()
exact_match_param.description = "Only return exact matches for the search query" # type: ignore

search_coins_schema = ZonRecord({
    "query": query_param,
    "exact_match": exact_match_param
})

SearchCoinsParameters = create_tool_parameters(search_coins_schema)
