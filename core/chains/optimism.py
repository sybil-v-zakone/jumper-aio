from config import OPTIMISM_RPC_ENDPOINT
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
    contract_address="0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85",
    abi=ERC20_CONTRACT_ABI,
    round_to=3
)

OPTIMISM_CHAIN = Chain(
    name=ChainName.OPTIMISM.value,
    chain_id=10,
    coin_symbol=TokenName.ETH.value,
    explorer="https://optimistic.etherscan.io/",
    rpc=OPTIMISM_RPC_ENDPOINT,
    okx_chain_name="Optimism",
    okx_withdrawal_fee="0.00004",
    tokens={ETH_TOKEN.symbol: ETH_TOKEN, USDC_TOKEN.symbol: USDC_TOKEN}
)
