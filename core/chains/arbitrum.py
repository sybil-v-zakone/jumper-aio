from config import ARBITRUM_RPC_ENDPOINT
from core.constants import ERC20_CONTRACT_ABI, ZERO_ADDRESS
from core.models.chain import Chain
from core.models.enums import ChainName, TokenName, TokenPriceApiId
from core.models.token import Token

ETH_TOKEN = Token(
    symbol=TokenName.ETH.value,
    decimals=18,
    api_id=TokenPriceApiId.ETH.value,
    is_native=True,
    contract_address=ZERO_ADDRESS,
    round_to=6
)

USDC_TOKEN = Token(
    symbol=TokenName.USDC.value,
    decimals=6,
    api_id=TokenPriceApiId.USDC.value,
    is_native=False,
    contract_address="0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
    abi=ERC20_CONTRACT_ABI,
    round_to=3
)


ARBITRUM_CHAIN = Chain(
    name=ChainName.ARBITRUM.value,
    chain_id=42161,
    coin_symbol=TokenName.ETH.value,
    explorer="https://arbiscan.io/",
    rpc=ARBITRUM_RPC_ENDPOINT,
    okx_chain_name="Arbitrum One",
    okx_withdrawal_fee="0.0001",
    tokens={ETH_TOKEN.symbol: ETH_TOKEN, USDC_TOKEN.symbol: USDC_TOKEN}
)
