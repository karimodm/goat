from abc import ABC, abstractmethod
from typing import List, TypedDict
from zon import ZonRecord, ZonString

from core.classes.tool_base import ToolBase, create_tool
from core.types.chain import Chain
from core.utils.create_tool_parameters import create_tool_parameters

EmptyParams = create_tool_parameters(ZonRecord({}))
BalanceParams = create_tool_parameters(ZonRecord({
    "address": ZonString()
}))


class Signature(TypedDict):
    signature: str


class Balance(TypedDict):
    decimals: int
    symbol: str
    name: str
    value: str
    in_base_units: str


class WalletClientBase(ABC):
    @abstractmethod
    def get_address(self) -> str:
        pass

    @abstractmethod
    def get_chain(self) -> Chain:
        pass

    @abstractmethod
    async def sign_message(self, message: str) -> Signature:
        pass

    @abstractmethod
    async def balance_of(self, address: str) -> Balance:
        pass

    def get_core_tools(self) -> List[ToolBase]:
        return [
            create_tool(
                {
                    "name": "get_address",
                    "description": "Get the address of the wallet",
                    "parameters": EmptyParams.schema, # type: ignore
                },
                lambda _: self.get_address()
            ),
            create_tool(
                {
                    "name": "get_chain",
                    "description": "Get the chain of the wallet",
                    "parameters": EmptyParams.schema, # type: ignore
                },
                lambda _: self.get_chain()
            ),
            create_tool(
                {
                    "name": "get_balance",
                    "description": "Get the balance of the wallet",
                    "parameters": BalanceParams.schema, # type: ignore
                },
                lambda parameters: self.balance_of(parameters["address"])
            )
        ] 