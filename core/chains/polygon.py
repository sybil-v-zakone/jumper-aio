from config import POLYGON_RPC_ENDPOINT
from core.constants import ERC20_CONTRACT_ABI, ZERO_ADDRESS
from core.models.chain import Chain
from core.models.enums import ChainName, TokenName, TokenPriceApiId
from core.models.token import Token

MATIC_TOKEN = Token(
    symbol=TokenName.MATIC.value,
    decimals=18,
    api_id=TokenPriceApiId.MATIC.value,
    is_native=True,
    contract_address=ZERO_ADDRESS,
    round_to=4
)

USDC_TOKEN = Token(
    symbol=TokenName.USDC.value,
    decimals=6,
    api_id=TokenPriceApiId.USDC.value,
    is_native=False,
    contract_address="0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
    abi=ERC20_CONTRACT_ABI,
    round_to=3
)

POLYGON_CHAIN = Chain(
    name=ChainName.POLYGON.value,
    chain_id=137,
    coin_symbol=TokenName.MATIC.value,
    explorer="https://polygonscan.com/",
    rpc=POLYGON_RPC_ENDPOINT,
    okx_chain_name="Polygon",
    okx_withdrawal_fee="0.1",
    tokens={MATIC_TOKEN.symbol: MATIC_TOKEN, USDC_TOKEN.symbol: USDC_TOKEN}
)
