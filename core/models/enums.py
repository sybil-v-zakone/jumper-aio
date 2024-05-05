from enum import Enum


class ChainName(Enum):
    BSC = "bsc"
    ARBITRUM = "arbitrum"
    OPTIMISM = "optimism"
    BASE = "base"
    POLYGON = "polygon"
    ETHEREUM = "ethereum"
    LINEA = "linea"
    ZKERA = "zkera"


class TokenName(Enum):
    ETH = "eth"
    MATIC = "matic"
    BNB = "bnb"


class TokenPriceApiId(Enum):
    ETH = "80"
    MATIC = "33536"
    BNB = "2710"
