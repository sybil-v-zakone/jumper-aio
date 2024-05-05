from config import BSC_RPC_ENDPOINT
from core.constants import NATIVE_TOKEN_CONTRACT_ADDRESS
from core.models.chain import Chain
from core.models.enums import ChainName, TokenName, TokenPriceApiId
from core.models.token import Token

BNB_TOKEN = Token(
    symbol=TokenName.BNB.value,
    decimals=18,
    api_id=TokenPriceApiId.BNB.value,
    is_native=True,
    contract_address=NATIVE_TOKEN_CONTRACT_ADDRESS,
    round_to=6
)

BSC_CHAIN = Chain(
    name=ChainName.BSC.value,
    chain_id=56,
    coin_symbol=TokenName.BNB.value,
    explorer="https://bscscan.com/",
    rpc=BSC_RPC_ENDPOINT,
    okx_chain_name="BSC",
    okx_withdrawal_fee="0.002",
    tokens={BNB_TOKEN.symbol: BNB_TOKEN}
)
