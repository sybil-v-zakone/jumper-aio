import random
from typing import Optional

from core import Client
from core.chains import *
from core.models.chain import Chain


class Wallet:
    def __init__(
        self,
        client: Client,
        deposit_address: str,
        arbitrum_bridge_count: int,
        base_bridge_count: int,
        bsc_bridge_count: int,
        optimism_bridge_count: int,
        polygon_bridge_count: int,
        ethereum_bridge_count: int,
        linea_bridge_count: int,
        zkera_bridge_count: int,
        volume_mode_state: dict,
        warmup_finished: bool = False,
        collector_finished: bool = False,
        manual_bridge_finished: bool = False,
        okx_withdrawn: Optional[float] = None,
        initial_balance: Optional[float] = None,
        current_chain: Optional[str] = None,
    ) -> None:
        self.private_key = client.private_key
        self.address = client.address
        self.proxy = client.proxy
        self.deposit_address = deposit_address
        self.current_chain = current_chain
        self.initial_balance = initial_balance
        self.arbitrum_bridge_count = arbitrum_bridge_count
        self.base_bridge_count = base_bridge_count
        self.bsc_bridge_count = bsc_bridge_count
        self.optimism_bridge_count = optimism_bridge_count
        self.polygon_bridge_count = polygon_bridge_count
        self.ethereum_bridge_count = ethereum_bridge_count
        self.linea_bridge_count = linea_bridge_count
        self.zkera_bridge_count = zkera_bridge_count
        self.warmup_finished = warmup_finished
        self.collector_finished = collector_finished
        self.manual_bridge_finished = manual_bridge_finished
        self.okx_withdrawn = okx_withdrawn
        self.volume_mode_state = volume_mode_state

    def __str__(self):
        return self.address

    def to_client(self, chain: Chain) -> Client:
        return Client(private_key=self.private_key, chain=chain, proxy=self.proxy)

    def has_actions_available(self) -> bool:
        if (
            self.arbitrum_bridge_count > 0
            or self.base_bridge_count > 0
            or self.bsc_bridge_count > 0
            or self.optimism_bridge_count > 0
            or self.polygon_bridge_count > 0
            or self.ethereum_bridge_count > 0
            or self.linea_bridge_count > 0
            or self.zkera_bridge_count > 0
        ):
            return True
        return False

    async def get_random_chain(self, excluded_chain: Chain = None) -> Optional[str]:
        available_chains = []
        if self.arbitrum_bridge_count > 0:
            available_chains.append(ARBITRUM_CHAIN)
        if self.base_bridge_count > 0:
            available_chains.append(BASE_CHAIN)
        if self.bsc_bridge_count > 0:
            available_chains.append(BSC_CHAIN)
        if self.optimism_bridge_count > 0:
            available_chains.append(OPTIMISM_CHAIN)
        if self.polygon_bridge_count > 0:
            available_chains.append(POLYGON_CHAIN)
        if self.ethereum_bridge_count > 0:
            available_chains.append(ETHEREUM_CHAIN)
        if self.linea_bridge_count > 0:
            available_chains.append(LINEA_CHAIN)
        if self.zkera_bridge_count > 0:
            available_chains.append(ZKERA_CHAIN)

        if excluded_chain is not None and excluded_chain in available_chains:
            available_chains.remove(excluded_chain)

        if available_chains:
            return random.choice(available_chains)
        return None
