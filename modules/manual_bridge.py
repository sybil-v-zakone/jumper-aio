import random

from config import (
    BRIDGE_PERCENTAGE_RANGE,
    TX_DELAY_RANGE,
    USE_MOBILE_PROXY,
    BRIDGE_FULL_BALANCE,
    FINISH_CHAIN,
    START_CHAIN,
)
from core.client import Client
from core.dapps import JumperBridge
from logger import logger
from modules.database import Database
from utils import sleep, change_ip, find_token, get_chain_by_name


async def manual_bridge():
    database = Database.read_from_json()

    while database.has_manual_bridge_available():
        if USE_MOBILE_PROXY:
            await change_ip()

        wallet_data = database.get_random_item_by_criteria(manual_bridge_finished=False)
        wallet, wallet_index = wallet_data

        logger.info(f"Working with wallet {wallet}")

        src_client = wallet.to_client(chain=get_chain_by_name(START_CHAIN))
        dest_client = wallet.to_client(chain=get_chain_by_name(FINISH_CHAIN))

        await bridge_action(
            src_client=src_client,
            dest_client=dest_client,
            wallet_index=wallet_index,
            database=database,
        )
        await sleep(delay_range=TX_DELAY_RANGE, send_message=False)
    logger.success("No more wallets left")


async def bridge_action(src_client: Client, dest_client: Client, wallet_index: int, database: Database) -> None:
    src_token = find_token(tokens=src_client.chain.tokens, symbol=src_client.chain.coin_symbol)

    if BRIDGE_FULL_BALANCE:
        amount = None
    else:
        balance = await src_client.get_token_balance(src_token, wei=False)
        amount = round(balance * random.randint(*BRIDGE_PERCENTAGE_RANGE) / 100, src_token.round_to)

    if amount is None or round(amount, 4) > 0:
        tx_status, _ = await JumperBridge(client=src_client).bridge(amount=amount, token=src_token, dest_chain=dest_client.chain)
    else:
        tx_status = False
        logger.error(f"Amount of {src_token.symbol.upper()} in chain {src_client.chain.name.upper()} very low")

    if tx_status:
        database.update_item(item_index=wallet_index, manual_bridge_finished=True)
