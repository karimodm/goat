from abc import ABC, abstractmethod
from typing import List, Any, Union, Awaitable, TypeVar, Generic
from typing_extensions import TypeVar

from core.classes.tool_base import ToolBase, create_tool
from core.classes.wallet_client_base import WalletClientBase
from core.types.chain import Chain
from core.decorators.tool import StoredToolMetadata

TWalletClient = TypeVar("TWalletClient", bound=WalletClientBase)

class PluginBase(Generic[TWalletClient], ABC):
    """
    Abstract base class for plugins that provide tools for wallet interactions.
    """
    
    def __init__(self, name: str, tool_providers: List[Any]):
        """
        Creates a new Plugin instance.
        
        Args:
            name: The name of the plugin
            tool_providers: Array of class instances that provide tools
        """
        self.name = name
        self.tool_providers = tool_providers

    @abstractmethod
    def supports_chain(self, chain: Chain) -> bool:
        """
        Checks if the plugin supports a specific blockchain.
        
        Args:
            chain: The blockchain to check support for
            
        Returns:
            True if the chain is supported, false otherwise
        """
        pass

    def get_tools(self, wallet_client: WalletClientBase) -> Union[List[ToolBase], Awaitable[List[ToolBase]]]:
        """
        Retrieves the tools provided by the plugin.
        
        Args:
            wallet_client: The wallet client to use for tool execution
            
        Returns:
            An array of tools
        """
        tools: List[ToolBase] = []

        for tool_provider in self.tool_providers:
            # Get all class attributes including the metadata
            tool_map = getattr(tool_provider.__class__, TOOL_METADATA_KEY, None)

            if not tool_map:
                constructor_name = tool_provider.__class__.__name__
                if constructor_name == "function":
                    print("Detected a non-instance tool provider. Please ensure you're passing instances of your tool providers, by using `MyToolProvider(..)`")
                else:
                    print(f"No tools found for {constructor_name}. Please ensure you're using the '@tool' decorator to expose your tools.")
                continue

            for tool in tool_map.values():
                tools.append(
                    create_tool(
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": tool.parameters.schema
                        },
                        lambda params, tool=tool: self._execute_tool(tool, tool_provider, wallet_client, params)
                    )
                )

        return tools

    def _execute_tool(
        self,
        tool: StoredToolMetadata,
        tool_provider: Any,
        wallet_client: WalletClientBase,
        params: Any
    ) -> Any:
        """
        Helper method to execute a tool with the correct arguments.
        
        Args:
            tool: The tool metadata
            tool_provider: The instance providing the tool
            wallet_client: The wallet client to use
            params: The parameters for the tool
            
        Returns:
            The result of the tool execution
        """
        args = []
        if tool.wallet_client is not None:
            args.insert(tool.wallet_client.index, wallet_client)
        
        if tool.parameters is not None:
            args.insert(tool.parameters.index, params)

        method = getattr(tool_provider, tool.target.__name__)
        return method(*args) 