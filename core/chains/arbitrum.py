from config import ARBITRUM_RPC_ENDPOINT
from core.constants import NATIVE_TOKEN_CONTRACT_ADDRESS
from core.models.chain import Chain
from core.models.enums import ChainName, TokenName, TokenPriceApiId
from core.models.token import Token

ETH_TOKEN = Token(
    symbol=TokenName.ETH.value,
    decimals=18,
    api_id=TokenPriceApiId.ETH.value,
    is_native=True,
    contract_address=NATIVE_TOKEN_CONTRACT_ADDRESS,
    round_to=6
)


ARBITRUM_CHAIN = Chain(
    name=ChainName.ARBITRUM.value,
    chain_id=42161,
    coin_symbol=TokenName.ETH.value,
    explorer="https://arbiscan.io/",
    rpc=ARBITRUM_RPC_ENDPOINT,
    okx_chain_name="Arbitrum One",
    okx_withdrawal_fee="0.0001",
    tokens={ETH_TOKEN.symbol: ETH_TOKEN}
)
