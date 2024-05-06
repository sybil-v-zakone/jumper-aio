from config import BSC_RPC_ENDPOINT
from core.constants import ERC20_CONTRACT_ABI, ZERO_ADDRESS
from core.models.chain import Chain
from core.models.enums import ChainName, TokenName, TokenPriceApiId
from core.models.token import Token

BNB_TOKEN = Token(
    symbol=TokenName.BNB.value,
    decimals=18,
    api_id=TokenPriceApiId.BNB.value,
    is_native=True,
    contract_address=ZERO_ADDRESS,
    round_to=6
)

USDC_TOKEN = Token(
    symbol=TokenName.USDC.value,
    decimals=18,
    api_id=TokenPriceApiId.USDC.value,
    is_native=False,
    contract_address="0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",
    abi=ERC20_CONTRACT_ABI,
    round_to=3
)

BSC_CHAIN = Chain(
    name=ChainName.BSC.value,
    chain_id=56,
    coin_symbol=TokenName.BNB.value,
    explorer="https://bscscan.com/",
    rpc=BSC_RPC_ENDPOINT,
    okx_chain_name="BSC",
    okx_withdrawal_fee="0.002",
    tokens={BNB_TOKEN.symbol: BNB_TOKEN, USDC_TOKEN.symbol: USDC_TOKEN}
)
