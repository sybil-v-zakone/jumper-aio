from dataclasses import dataclass
from typing import Optional


@dataclass
class Chain:
    name: str
    chain_id: int
    coin_symbol: str
    explorer: str
    rpc: str
    tokens: dict
    okx_chain_name: Optional[str] = None
    okx_withdrawal_fee: Optional[str] = None
