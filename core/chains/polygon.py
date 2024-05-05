from config import POLYGON_RPC_ENDPOINT
from core.constants import NATIVE_TOKEN_CONTRACT_ADDRESS
from core.models.chain import Chain
from core.models.enums import ChainName, TokenName, TokenPriceApiId
from core.models.token import Token

MATIC_TOKEN = Token(
    symbol=TokenName.MATIC.value,
    decimals=18,
    api_id=TokenPriceApiId.MATIC.value,
    is_native=True,
    contract_address=NATIVE_TOKEN_CONTRACT_ADDRESS,
    round_to=6
)


POLYGON_CHAIN = Chain(
    name=ChainName.POLYGON.value,
    chain_id=137,
    coin_symbol=TokenName.MATIC.value,
    explorer="https://polygonscan.com/",
    rpc=POLYGON_RPC_ENDPOINT,
    okx_chain_name="Polygon",
    okx_withdrawal_fee="0.1",
    tokens={MATIC_TOKEN.symbol: MATIC_TOKEN}
)
