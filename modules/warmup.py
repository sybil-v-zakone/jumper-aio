import random

from config import (
    BRIDGE_PERCENTAGE_RANGE,
    TX_DELAY_RANGE,
    USE_MOBILE_PROXY,
    USE_OKX_WITHDRAW,
    MANUAL_TRANSFERS_MODE,
    OKX_WITHDRAW_AMOUNT_RANGE,
    BRIDGE_FULL_BALANCE,
    FINISH_CHAIN,
)
from core.cex.okx import Okx
from core.client import Client
from core.dapps import JumperBridge
from logger import logger
from core.models.wallet import Wallet
from modules.database import Database
from utils import sleep, change_ip, find_token, get_chain_by_name


async def warmup():
    database = Database.read_from_json()

    while database.has_actions_available():
        if USE_MOBILE_PROXY:
            await change_ip()

        wallet_data = database.get_random_item_by_criteria(warmup_finished=False)
        wallet, wallet_index = wallet_data

        logger.info(f"Working with wallet {wallet}")

        if wallet.current_chain is None:
            src_chain = await wallet.get_random_chain()
        else:
            src_chain = get_chain_by_name(wallet.current_chain)

        if src_chain is None:
            logger.success(f"No more actions for this wallet")
            database.update_item(item_index=wallet_index, warmup_finished=True)
            continue

        dest_chain = await wallet.get_random_chain(excluded_chain=src_chain)

        if dest_chain is None:
            if FINISH_CHAIN != "":
                dest_chain = get_chain_by_name(FINISH_CHAIN)
                if src_chain == dest_chain or dest_chain is None:
                    logger.warning(f"Last chain for this wallet is {src_chain.name} and finish chain is {FINISH_CHAIN}")
                    database.update_item(item_index=wallet_index, warmup_finished=True)
                    continue
            else:
                logger.warning(f"Cannot find destination chain for chain {src_chain.name.upper()}")
                database.update_item(item_index=wallet_index, warmup_finished=True)
                continue

        src_client = wallet.to_client(chain=src_chain)
        dest_client = wallet.to_client(chain=dest_chain)

        if wallet.okx_withdrawn is None and USE_OKX_WITHDRAW:
            if not await okx_withdraw_action(
                wallet_index=wallet_index,
                database=database,
                client=src_client
            ):
                continue
            database.update_item(item_index=wallet_index, current_chain=src_chain.name)

        await perform_warmup_action(
            wallet=wallet,
            src_client=src_client,
            dest_client=dest_client,
            wallet_index=wallet_index,
            database=database,
        )
        await sleep(delay_range=TX_DELAY_RANGE, send_message=False)
    logger.success("No more wallets left")


async def perform_warmup_action(
        src_client: Client, dest_client: Client, wallet: Wallet, wallet_index: int, database: Database
) -> None:
    has_actions_left = await bridge_action(
        wallet=wallet,
        wallet_index=wallet_index,
        database=database,
        src_client=src_client,
        dest_client=dest_client,
    )

    if not has_actions_left:
        database.update_item(item_index=wallet_index, warmup_finished=True)


async def bridge_action(
        wallet: Wallet, wallet_index: int, database: Database, src_client: Client, dest_client: Client
) -> bool:
    if wallet.initial_balance is not None:
        if await check_if_bridge_finished(wallet=wallet, client=src_client):
            logger.success(f"Bridged token has successfully reached {src_client.chain.name.upper()}")
            database.update_item(item_index=wallet_index, initial_balance=None)
        else:
            logger.warning(f"Bridged token is still inflight")
            return True

    src_token = find_token(tokens=src_client.chain.tokens, symbol=src_client.chain.coin_symbol)
    dest_token = find_token(tokens=dest_client.chain.tokens, symbol=dest_client.chain.coin_symbol)

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
        database.update_item(
            item_index=wallet_index,
            current_chain=dest_client.chain.name,
            initial_balance=await dest_client.get_token_balance(dest_token, wei=False)
        )

        database.decrease_bridge_count(item_index=wallet_index, wallet=wallet, chain=src_client.chain)
    return wallet.has_actions_available()


async def okx_withdraw_action(wallet_index: int, database: Database, client: Client) -> bool:
    okx = Okx(client=client)

    if not await okx.transfer_from_sub_accounts(symbol=client.chain.coin_symbol.upper()):
        return False

    if MANUAL_TRANSFERS_MODE:
        amount = float(input("Enter amount to withdraw from okx: "))
    else:
        amount = round(random.uniform(*OKX_WITHDRAW_AMOUNT_RANGE), 6)

    if amount > 0:
        if not await okx.withdraw(amount=amount):
            return False

    database.update_item(item_index=wallet_index, okx_withdrawn=amount)
    return True


async def check_if_bridge_finished(wallet: Wallet, client: Client) -> bool:
    token = find_token(tokens=client.chain.tokens, symbol=client.chain.coin_symbol)
    current_balance = await client.get_token_balance(token, wei=False)
    return current_balance > wallet.initial_balance
