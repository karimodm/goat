from abc import abstractmethod
from typing import Dict

from core.types.chain import EvmChain

from core.classes.wallet_client_base import WalletClientBase
from .types import EVMTransaction, EVMReadRequest, EVMReadResult, EVMTypedData


class EVMWalletClient(WalletClientBase):
    @abstractmethod
    def get_chain(self) -> EvmChain:
        """Get the EVM chain this wallet is connected to."""
        pass

    @abstractmethod
    async def send_transaction(self, transaction: EVMTransaction) -> Dict[str, str]:
        """Send a transaction on the EVM chain."""
        pass

    @abstractmethod
    async def read(self, request: EVMReadRequest) -> EVMReadResult:
        """Read data from a smart contract."""
        pass

    @abstractmethod
    async def resolve_address(self, address: str) -> str:
        """Resolve an address to its canonical form."""
        pass

    @abstractmethod
    async def sign_typed_data(self, data: EVMTypedData) -> str:
        """Sign typed data according to EIP-712."""
        pass
