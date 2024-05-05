import binascii
import itertools
import json
import random
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from config import (
    USE_MOBILE_PROXY,
    VOLUME_GOAL_RANGE,
    ARBITRUM_BRIDGE_COUNT,
    BASE_BRIDGE_COUNT,
    BSC_BRIDGE_COUNT,
    OPTIMISM_BRIDGE_COUNT,
    POLYGON_BRIDGE_COUNT,
    LINEA_BRIDGE_COUNT,
    ETHEREUM_BRIDGE_COUNT,
    ZKERA_BRIDGE_COUNT,
    START_CHAIN, CHAINS_TO_VOLUME,
)
from core import Client
from core.constants import DATABASE_FILE_PATH, PRIVATE_KEYS_FILE_PATH, PROXIES_FILE_PATH, DEPOSIT_ADDRESSES_PATH
from core.models.chain import Chain
from core.models.enums import ChainName
from core.models.wallet import Wallet
from logger import logger
from utils import read_from_txt


@dataclass
class Database:
    data: List[Wallet]

    def _to_dict(self) -> List[Dict[str, Any]]:
        return [vars(wallet) for wallet in self.data]

    @staticmethod
    def _create_database() -> "Database":
        try:
            data = []

            private_keys = read_from_txt(file_path=PRIVATE_KEYS_FILE_PATH)
            proxies = read_from_txt(file_path=PROXIES_FILE_PATH)
            deposit_addresses = read_from_txt(file_path=DEPOSIT_ADDRESSES_PATH)

            if USE_MOBILE_PROXY:
                proxies = proxies * len(private_keys)

            if len(private_keys) < len(proxies):
                raise DataAmountMismatchError

            for private_key, proxy, deposit_address in itertools.zip_longest(
                    private_keys, proxies, deposit_addresses, fillvalue=None
            ):
                try:
                    start_chain = random.choice(CHAINS_TO_VOLUME) if len(START_CHAIN) == 0 else START_CHAIN
                    wallet = Wallet(
                        client=Client(private_key=private_key, proxy=proxy),
                        deposit_address=deposit_address,
                        arbitrum_bridge_count=random.randint(*ARBITRUM_BRIDGE_COUNT),
                        base_bridge_count=random.randint(*BASE_BRIDGE_COUNT),
                        bsc_bridge_count=random.randint(*BSC_BRIDGE_COUNT),
                        optimism_bridge_count=random.randint(*OPTIMISM_BRIDGE_COUNT),
                        polygon_bridge_count=random.randint(*POLYGON_BRIDGE_COUNT),
                        linea_bridge_count=random.randint(*LINEA_BRIDGE_COUNT),
                        ethereum_bridge_count=random.randint(*ETHEREUM_BRIDGE_COUNT),
                        zkera_bridge_count=random.randint(*ZKERA_BRIDGE_COUNT),
                        volume_mode_state={
                            'volume_goal': round(random.uniform(*VOLUME_GOAL_RANGE), 5),
                            'volume_reached': 0.0,
                            'okx_withdrawn': None,
                            'current_chain': start_chain,
                            'initial_balance': None,
                            'deposited_to_cex': False
                        }
                    )
                except binascii.Error:
                    logger.error(f"Provided private key is not valid: {private_key}")
                    sys.exit(1)
                data.append(wallet)
            logger.success("Database created successfully")
            return Database(data=data)
        except Exception as e:
            logger.exception(f"Error while creating database: {e}")
            sys.exit(1)

    def save_database(self, file_path: str = DATABASE_FILE_PATH) -> None:
        data_dict = self._to_dict()
        with open(file=file_path, mode="w") as json_file:
            json.dump(data_dict, json_file, indent=4)

    @staticmethod
    def create_database():
        db = Database._create_database()
        db.save_database()

    @classmethod
    def read_from_json(cls, file_path: str = DATABASE_FILE_PATH) -> "Database":
        try:
            with open(file=file_path, mode="r") as json_file:
                data_dict = json.load(fp=json_file)
        except Exception as e:
            logger.error(f"Failed to read database: {e}")
            sys.exit(1)

        data = []
        for item in data_dict:
            wallet_data = {
                "private_key": item.pop("private_key"),
                "proxy": item.pop("proxy"),
            }
            item.pop("address")
            client = Client(**wallet_data)
            wallet = Wallet(client=client, **item)
            data.append(wallet)
        return cls(data=data)

    def update_item(self, item_index: int, **kwargs):
        if 0 <= item_index < len(self.data):
            item = self.data[item_index]

            for key, value in kwargs.items():
                setattr(item, key, value)

            self.save_database()
        else:
            logger.error(f"Invalid item index: {item_index}")

    def decrease_bridge_count(self, item_index: int, wallet: Wallet, chain: Chain):
        if chain.name == ChainName.ARBITRUM.value:
            self.update_item(item_index=item_index, arbitrum_bridge_count=wallet.arbitrum_bridge_count - 1)
        elif chain.name == ChainName.BASE.value:
            self.update_item(item_index=item_index, base_bridge_count=wallet.base_bridge_count - 1)
        elif chain.name == ChainName.BSC.value:
            self.update_item(item_index=item_index, bsc_bridge_count=wallet.bsc_bridge_count - 1)
        elif chain.name == ChainName.OPTIMISM.value:
            self.update_item(item_index=item_index, optimism_bridge_count=wallet.optimism_bridge_count - 1)
        elif chain.name == ChainName.POLYGON.value:
            self.update_item(item_index=item_index, polygon_bridge_count=wallet.polygon_bridge_count - 1)
        elif chain.name == ChainName.LINEA.value:
            self.update_item(item_index=item_index, linea_bridge_count=wallet.linea_bridge_count - 1)
        elif chain.name == ChainName.ETHEREUM.value:
            self.update_item(item_index=item_index, ethereum_bridge_count=wallet.ethereum_bridge_count - 1)
        elif chain.name == ChainName.ZKERA.value:
            self.update_item(item_index=item_index, zkera_bridge_count=wallet.zkera_bridge_count - 1)

    def get_random_item_by_criteria(self, **kwargs) -> Optional[Tuple[Wallet, int]]:
        """
        Returns a random wallet and its index that matches the given kwargs.
        If no wallet matches, returns None.
        """
        # Filter wallets based on kwargs
        filtered_wallets = [
            wallet
            for wallet in self.data
            if all(getattr(wallet, k, None) == v for k, v in kwargs.items())
        ]

        # Check if there are any wallets after filtering
        if not filtered_wallets:
            return None

        # Select a random wallet
        selected_wallet = random.choice(filtered_wallets)
        index = self.data.index(selected_wallet)

        return selected_wallet, index

    def get_first_volume_wallet(self) -> Optional[Tuple[Wallet, int]]:
        for item in self.data:
            if item.volume_mode_state['deposited_to_cex']:
                continue
            return item, self.data.index(item)
        return None

    def has_actions_available(self) -> bool:
        """
        Check if any item in the database has "warmup_finished" set to False.
        Return True if the first instance is found, else return False.
        """
        for wallet in self.data:
            if not getattr(wallet, "warmup_finished", True):
                return True
        return False

    def has_manual_bridge_available(self) -> bool:
        for wallet in self.data:
            if not getattr(wallet, "manual_bridge_finished", True):
                return True
        return False

    def has_volume_actions_available(self) -> bool:
        for wallet in self.data:
            if not wallet.volume_mode_state['deposited_to_cex']:
                return True
        return False

    def ensure_ready_for_volume_mode(self) -> bool:
        for wallet in self.data:
            if not wallet.deposit_address:
                return False
        return True


class DataAmountMismatchError(Exception):
    def __init__(self):
        super().__init__(f"Amount of private keys and proxies do not match")
