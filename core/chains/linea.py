from config import LINEA_RPC_ENDPOINT
from core.constants import NATIVE_TOKEN_CONTRACT_ADDRESS
from core.models.chain import Chain
from core.models.enums import TokenName, TokenPriceApiId, ChainName
from core.models.token import Token

ETH_TOKEN = Token(
    symbol=TokenName.ETH.value,
    decimals=18,
    api_id=TokenPriceApiId.ETH.value,
    is_native=True,
    contract_address=NATIVE_TOKEN_CONTRACT_ADDRESS,
    round_to=6
)

LINEA_CHAIN = Chain(
    name=ChainName.LINEA.value,
    chain_id=59144,
    coin_symbol=TokenName.ETH.value,
    explorer="https://lineascan.build/",
    rpc=LINEA_RPC_ENDPOINT,
    tokens={ETH_TOKEN.symbol: ETH_TOKEN},
    okx_withdrawal_fee="0.0002",
    okx_chain_name="Linea"
)
