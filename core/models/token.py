from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Token:
    symbol: str
    decimals: int
    is_native: bool
    round_to: int
    api_id: Optional[str] = None
    contract_address: Optional[str] = None
    abi: Optional[Dict] = None

    def to_wei(self, value: float) -> int:
        return int(value * pow(10, self.decimals))

    def from_wei(self, value: int) -> float:
        return value / pow(10, self.decimals)

    def __repr__(self) -> str:
        return self.symbol

    def __str__(self) -> str:
        return self.symbol

    def __hash__(self):
        return hash(self.symbol)

    def __eq__(self, other):
        return self.symbol == other.symbol if isinstance(other, Token) else False
