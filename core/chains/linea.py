from config import LINEA_RPC_ENDPOINT
from core.constants import ERC20_CONTRACT_ABI, ZERO_ADDRESS
from core.models.chain import Chain
from core.models.enums import TokenName, TokenPriceApiId, ChainName
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
    contract_address="0x176211869cA2b568f2A7D4EE941E073a821EE1ff",
    abi=ERC20_CONTRACT_ABI,
    round_to=3
)

LINEA_CHAIN = Chain(
    name=ChainName.LINEA.value,
    chain_id=59144,
    coin_symbol=TokenName.ETH.value,
    explorer="https://lineascan.build/",
    rpc=LINEA_RPC_ENDPOINT,
    tokens={ETH_TOKEN.symbol: ETH_TOKEN, USDC_TOKEN.symbol: USDC_TOKEN},
    okx_withdrawal_fee="0.0002",
    okx_chain_name="Linea"
)
