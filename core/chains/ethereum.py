from config import ETHEREUM_RPC_ENDPOINT
from core.constants import NATIVE_TOKEN_CONTRACT_ADDRESS
from core.models.chain import Chain
from core.models.enums import TokenName, TokenPriceApiId, ChainName
from core.models.token import Token

ETH_TOKEN = Token(
    symbol=TokenName.ETH.value,
    decimals=18,
    api_id=TokenPriceApiId.ETH.value,
    is_native=True,
    round_to=6,
    contract_address=NATIVE_TOKEN_CONTRACT_ADDRESS,
)

ETHEREUM_CHAIN = Chain(
    name=ChainName.ETHEREUM.value,
    chain_id=1,
    coin_symbol=TokenName.ETH.value,
    explorer="https://etherscan.io/",
    rpc=ETHEREUM_RPC_ENDPOINT,
    tokens={ETH_TOKEN.symbol: ETH_TOKEN},
    okx_withdrawal_fee="0.0008",
    okx_chain_name="ERC20"
)
