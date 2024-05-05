from config import ZKERA_RPC_ENDPOINT
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

ZKERA_CHAIN = Chain(
    name=ChainName.ZKERA.value,
    chain_id=324,
    coin_symbol=TokenName.ETH.value,
    explorer="https://explorer.zksync.io/",
    rpc=ZKERA_RPC_ENDPOINT,
    tokens={ETH_TOKEN.symbol: ETH_TOKEN},
    okx_withdrawal_fee="0.000041",
    okx_chain_name="zkSync Era"
)
