# CLIENT CONFIGURATION
VERIFY_TX_TIMEOUT = 300

GAS_LIMIT_MULTIPLIER = 1.2
GAS_PRICE_MULTIPLIER = 1.1

RETRIES = 3
RETRY_DELAY_RANGE = [5, 10]

NATIVE_TOKEN_CONTRACT_ADDRESS = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
MAX_SLIPPAGE = 5

"""
DEXES CONTRACT ADDRESSES / ABIS
"""

# JUMPER
JUMPER_ROUTE_URL = "https://li.quest/v1/advanced/routes"
JUMPER_BUILD_TX_URL = "https://li.quest/v1/advanced/stepTransaction"

JUMPER_TX_SIMULATION_VALUE = 100000000000000
JUMPER_FULL_BRIDGE_GAS_MULTIPLIER = 1.3

# regex for matching the valid proxy format
PROXY_PATTERN = r"^([^:@\s]+):([^:@\s]+)@([a-zA-Z0-9.-]+|\d+\.\d+\.\d+\.\d+):(\d+)$"

# api endpoint for fetching current token USD price
TOKEN_PRICE_FETCH_URL = "https://api.coinlore.net/api/ticker/?id={}"

# database/pks/proxies files paths
PRIVATE_KEYS_FILE_PATH = "data/private_keys.txt"
PROXIES_FILE_PATH = "data/proxies.txt"
DEPOSIT_ADDRESSES_PATH = "data/deposit_addresses.txt"
DATABASE_FILE_PATH = "data/database.json"

"""
CEX
"""
CEX_WITHDRAW_TRIES = 5
CEX_WITHDRAW_DELAY_RANGE = [60, 60]
CEX_WAIT_FOR_WITHDRAWAL_FINAL_STATUS_DELAY_RANGE = [10, 10]
CEX_WAIT_FOR_WITHDRAWAL_FINAL_STATUS_ATTEMPTS = 100
