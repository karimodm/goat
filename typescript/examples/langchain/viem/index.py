from javascript import require
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Node.js packages using require
viem = require('viem')
viem_accounts = require('viem/accounts')
viem_chains = require('viem/chains')
langchain_core_prompts = require('@langchain/core/prompts')
langchain_openai = require('@langchain/openai')
langchain_agents = require('langchain/agents')
langchain_hub = require('langchain/hub')
goat_sdk_adapter_langchain = require('@goat-sdk/adapter-langchain')
goat_sdk_plugin_erc20 = require('@goat-sdk/plugin-erc20')
goat_sdk_wallet_evm = require('@goat-sdk/wallet-evm')
goat_sdk_wallet_viem = require('@goat-sdk/wallet-viem')

# Create account and wallet client
account = viem_accounts.privateKeyToAccount(os.environ['WALLET_PRIVATE_KEY'])

wallet_client = viem.createWalletClient({
    'account': account,
    'transport': viem.http(os.environ['RPC_PROVIDER_URL']),
    'chain': viem_chains.sepolia
})

# Initialize LLM with tracing
llm = langchain_openai.ChatOpenAI({
    'model': 'gpt-4o-mini',
})

async def main():
    # Get prompt template
    prompt = langchain_hub.pull(
        'hwchase17/structured-chat-agent'
    )

    # Get tools
    tools = goat_sdk_adapter_langchain.getOnChainTools({
        'wallet': goat_sdk_wallet_viem.viem(wallet_client),
        'plugins': [
            goat_sdk_wallet_evm.sendETH(),
            goat_sdk_plugin_erc20.erc20({
                'tokens': [
                    goat_sdk_plugin_erc20.USDC,
                    goat_sdk_plugin_erc20.PEPE
                ]
            })
        ]
    })

    # Create agent with tracing
    agent = langchain_agents.createStructuredChatAgent({
        'llm': llm,
        'tools': tools,
        'prompt': prompt,
    })

    # Create agent executor with tracing
    agent_executor = langchain_agents.AgentExecutor({
        'agent': agent,
        'tools': tools,
    })

    # Execute agent
    response = agent_executor.invoke({
        'input': 'Get my balance in USDC',
        'timeout': 100000,
    }, timeout=100000)

    print(response)

# Run the async main function
if __name__ == '__main__':
    import asyncio
    asyncio.run(main()) 