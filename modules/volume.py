import random

from config import (
    USE_MOBILE_PROXY,
    WALLET_DELAY_RANGE,
    TX_DELAY_RANGE,
    OKX_WITHDRAW_AMOUNT_RANGE,
    MANUAL_TRANSFERS_MODE,
    VOLUME_BRIDGE_PERCENTAGE_RANGE,
    AMOUNT_TO_LEAVE_RANGE,
    CHAINS_TO_VOLUME,
    BRIDGE_FULL_BALANCE,
    NATIVE_BRIDGE_MODE,
    USE_OKX_WITHDRAW,
)
from core import Client
from core.cex.okx import Okx
from core.dapps import JumperBridge
from core.models.chain import Chain
from core.models.enums import TokenName
from core.models.token import Token
from core.models.wallet import Wallet
from logger import logger
from modules.database import Database
from utils import change_ip, sleep, get_chain_by_name, find_token


async def volume():
    database = Database.read_from_json()

    if not database.ensure_ready_for_volume_mode():
        logger.error(f"Deposit addresses must be provided for each wallet")
        return

    while database.has_volume_actions_available():
        try:
            if USE_MOBILE_PROXY:
                await change_ip()

            wallet_data = database.get_first_volume_wallet()

            if wallet_data is None:
                break

            wallet, wallet_index = wallet_data

            logger.info(f"Working with wallet {wallet}")

            await perform_volume_mode_cycle(
                database=database,
                wallet=wallet,
                wallet_index=wallet_index
            )
            await sleep(delay_range=WALLET_DELAY_RANGE, send_message=False)
        except Exception as e:
            logger.exception(f"Error occurred: {e}")
    logger.success("No more wallets left")


async def perform_volume_mode_cycle(database: Database, wallet: Wallet, wallet_index: int) -> bool:
    while wallet.volume_mode_state['volume_reached'] < wallet.volume_mode_state['volume_goal']:
        if USE_MOBILE_PROXY:
            await change_ip()

        src_chain = get_chain_by_name(wallet.volume_mode_state['current_chain'])

        if src_chain is None:
            logger.warning(f"Cannot find source chain for chain {wallet.volume_mode_state['current_chain']}")
            return False

        src_client = wallet.to_client(chain=src_chain)
        dest_client = wallet.to_client(chain=get_random_volume_chain(excluded_chain=src_chain))

        if NATIVE_BRIDGE_MODE:
            src_token = find_token(tokens=src_client.chain.tokens, symbol=src_client.chain.coin_symbol)
            dest_token = find_token(tokens=dest_client.chain.tokens, symbol=dest_client.chain.coin_symbol)
        else:
            src_token = find_token(tokens=src_client.chain.tokens, symbol=TokenName.USDC.value)
            dest_token = find_token(tokens=dest_client.chain.tokens, symbol=TokenName.USDC.value)

        if wallet.volume_mode_state['okx_withdrawn'] is None and USE_OKX_WITHDRAW:
            if not await okx_withdraw_action(
                    wallet=wallet,
                    wallet_index=wallet_index,
                    database=database,
                    client=src_client
            ):
                return False

            if not NATIVE_BRIDGE_MODE:
                src_token = find_token(tokens=src_client.chain.tokens, symbol=src_client.chain.coin_symbol)
                dest_token = find_token(tokens=dest_client.chain.tokens, symbol=TokenName.USDC.value)

        if wallet.volume_mode_state["initial_balance"] is not None:
            if await check_if_bridge_finished(wallet=wallet, client=src_client, token=src_token):
                logger.success(f"Bridged token has successfully reached {src_client.chain.name.upper()}")
                database.update_item(item_index=wallet_index, volume_mode_state=wallet.volume_mode_state)
            else:
                logger.warning(f"Bridged token is still inflight")
                await sleep(delay_range=TX_DELAY_RANGE, send_message=False)
                continue

        src_balance = await src_client.get_token_balance(src_token, wei=False)

        if BRIDGE_FULL_BALANCE:
            amount = None
        else:
            amount = round(src_balance * random.randint(*VOLUME_BRIDGE_PERCENTAGE_RANGE) / 100, src_token.round_to)

        if amount is None or round(amount, src_token.round_to - 2) > 0:
            tx_status, bridged_amount = await JumperBridge(client=src_client).bridge(
                amount=amount, token_in=src_token, token_out=dest_token, dest_chain=dest_client.chain
            )
        else:
            logger.error(f"Amount of {src_token.symbol.upper()} in chain {src_client.chain.name.upper()} very low")
            break

        wallet.volume_mode_state['initial_balance'] = round(
            await dest_client.get_token_balance(dest_token, wei=False), dest_token.round_to
        )
        wallet.volume_mode_state['current_chain'] = dest_client.chain.name
        wallet.volume_mode_state['volume_reached'] += bridged_amount * (await src_client.fetch_token_price([src_token]))[0]
        database.update_item(item_index=wallet_index, volume_mode_state=wallet.volume_mode_state)

        await sleep(delay_range=TX_DELAY_RANGE, send_message=False)

    if not NATIVE_BRIDGE_MODE:
        if not await bridge_to_native(database=database, wallet=wallet, wallet_index=wallet_index):
            return False

    if not wallet.volume_mode_state['deposited_to_cex']:
        if not await transfer_to_cex_action(database=database, wallet=wallet, wallet_index=wallet_index):
            return False
    return True


async def bridge_to_native(wallet: Wallet, database: Database, wallet_index: int):
    while True:
        src_client = wallet.to_client(chain=get_chain_by_name(wallet.volume_mode_state['current_chain']))
        src_token = find_token(tokens=src_client.chain.tokens, symbol=TokenName.USDC.value)
        src_balance = await src_client.get_token_balance(src_token, wei=False)

        dest_client = wallet.to_client(get_random_volume_chain(excluded_chain=src_client.chain))
        dest_token = find_token(tokens=dest_client.chain.tokens, symbol=dest_client.chain.coin_symbol)

        if await check_if_bridge_finished(wallet=wallet, client=src_client, token=src_token):
            logger.success(f"Bridged token has successfully reached {src_client.chain.name.upper()}")
        else:
            logger.warning(f"Bridged token is still inflight")
            await sleep(delay_range=TX_DELAY_RANGE, send_message=False)
            continue

        if BRIDGE_FULL_BALANCE:
            amount = None
        else:
            amount = round(src_balance * random.randint(*VOLUME_BRIDGE_PERCENTAGE_RANGE) / 100, src_token.round_to)

        if amount is None or round(amount, src_token.round_to - 2) > 0:
            tx_status, _ = await JumperBridge(client=src_client).bridge(
                amount=amount, token_in=src_token, token_out=dest_token, dest_chain=dest_client.chain
            )
        else:
            return True

        if tx_status:
            wallet.volume_mode_state['initial_balance'] = round(
                await dest_client.get_token_balance(dest_token, wei=False), dest_token.round_to
            )
            wallet.volume_mode_state['current_chain'] = dest_client.chain.name
            database.update_item(item_index=wallet_index, volume_mode_state=wallet.volume_mode_state)
            await sleep(delay_range=TX_DELAY_RANGE, send_message=False)
        return True


async def okx_withdraw_action(wallet: Wallet, wallet_index: int, database: Database, client: Client) -> bool:
    okx = Okx(client=client)

    if not await okx.transfer_from_sub_accounts(symbol=client.chain.coin_symbol.upper()):
        return False

    if MANUAL_TRANSFERS_MODE:
        amount = float(input(f"Enter amount of {client.chain.coin_symbol} to withdraw from okx: "))
    else:
        amount = round(random.uniform(*OKX_WITHDRAW_AMOUNT_RANGE), 6)

    if amount > 0:
        if not await okx.withdraw(amount=amount):
            return False

    wallet.volume_mode_state['okx_withdrawn'] = amount
    database.update_item(item_index=wallet_index, volume_mode_state=wallet.volume_mode_state)
    return True


async def transfer_to_cex_action(database: Database, wallet: Wallet, wallet_index: int) -> bool:
    while True:
        src_client = wallet.to_client(chain=get_chain_by_name(wallet.volume_mode_state['current_chain']))
        src_token = find_token(tokens=src_client.chain.tokens, symbol=src_client.chain.coin_symbol)
        if await check_if_bridge_finished(wallet=wallet, client=src_client, token=src_token):
            logger.success(f"Bridged token has successfully reached {src_client.chain.name.upper()}")
        else:
            logger.warning(f"Bridged token is still inflight")
            await sleep(delay_range=TX_DELAY_RANGE, send_message=False)
            continue

        balance = await src_client.get_token_balance(src_token, wei=False)

        amount_to_leave = random.uniform(*AMOUNT_TO_LEAVE_RANGE)

        if balance < amount_to_leave:
            logger.error(f"AMOUNT_TO_LEAVE in {src_client.chain.name} is more than actual account balance")
            return False

        if MANUAL_TRANSFERS_MODE:
            amount_to_transfer = src_token.to_wei(float(input(f"Enter amount of {src_token.symbol} to send to CEX: ")))
        else:
            amount_to_transfer = src_token.to_wei(balance - amount_to_leave)

        if amount_to_transfer > 0:
            if not await src_client.transfer(to_address=wallet.deposit_address, amount=amount_to_transfer):
                return False

        wallet.volume_mode_state['deposited_to_cex'] = True
        database.update_item(item_index=wallet_index, volume_mode_state=wallet.volume_mode_state)
        return True


def get_random_volume_chain(excluded_chain: Chain):
    chains = []
    for chain in CHAINS_TO_VOLUME:
        chains.append(chain)
    if excluded_chain.name in chains:
        chains.remove(excluded_chain.name)
    return get_chain_by_name(random.choice(chains))


async def check_if_bridge_finished(wallet: Wallet, client: Client, token: Token) -> bool:
    current_balance = await client.get_token_balance(token, wei=False)
    return current_balance > wallet.volume_mode_state["initial_balance"]
