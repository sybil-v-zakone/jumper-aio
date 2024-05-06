from config import ETHEREUM_RPC_ENDPOINT
from core.constants import ERC20_CONTRACT_ABI, ZERO_ADDRESS
from core.models.chain import Chain
from core.models.enums import TokenName, TokenPriceApiId, ChainName
from core.models.token import Token

ETH_TOKEN = Token(
    symbol=TokenName.ETH.value,
    decimals=18,
    api_id=TokenPriceApiId.ETH.value,
    is_native=True,
    round_to=6,
    contract_address=ZERO_ADDRESS,
)

USDC_TOKEN = Token(
    symbol=TokenName.USDC.value,
    decimals=6,
    api_id=TokenPriceApiId.USDC.value,
    is_native=False,
    contract_address="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    abi=ERC20_CONTRACT_ABI,
    round_to=3
)

ETHEREUM_CHAIN = Chain(
    name=ChainName.ETHEREUM.value,
    chain_id=1,
    coin_symbol=TokenName.ETH.value,
    explorer="https://etherscan.io/",
    rpc=ETHEREUM_RPC_ENDPOINT,
    tokens={ETH_TOKEN.symbol: ETH_TOKEN, USDC_TOKEN.symbol: USDC_TOKEN},
    okx_withdrawal_fee="0.0008",
    okx_chain_name="ERC20"
)

