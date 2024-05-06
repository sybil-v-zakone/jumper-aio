from config import USE_MOBILE_PROXY, TX_DELAY_RANGE, FINISH_CHAIN, NATIVE_BRIDGE_MODE
from core.dapps import JumperBridge
from core.models.enums import TokenName
from logger import logger
from modules.database import Database
from utils import sleep, change_ip, get_chains, find_token, get_chain_by_name


async def collector_batch():
    database = Database.read_from_json()

    while True:
        if USE_MOBILE_PROXY:
            await change_ip()

        wallet_data = database.get_random_item_by_criteria(collector_finished=False)

        if wallet_data is None:
            break

        wallet, wallet_index = wallet_data
        logger.info(f"Working with wallet {wallet}")

        chains = get_chains()
        dest_chain = get_chain_by_name(FINISH_CHAIN)

        for src_chain in chains:
            if src_chain == dest_chain:
                continue
            logger.info(f"Collecting from chain {src_chain.name.upper()}")
            client = wallet.to_client(chain=src_chain)
            jumper = JumperBridge(client=client)

            if NATIVE_BRIDGE_MODE:
                src_token = find_token(src_chain.tokens, src_chain.coin_symbol)
            else:
                src_token = find_token(src_chain.tokens, TokenName.USDC.value)

            dest_token = find_token(dest_chain.tokens, dest_chain.coin_symbol)

            if round(await client.get_token_balance(src_token, wei=False), src_token.round_to - 2) > 0:
                tx_status, _ = await jumper.bridge(
                    token_in=src_token, token_out=dest_token, dest_chain=dest_chain, amount=None
                )
                if tx_status:
                    await sleep(delay_range=TX_DELAY_RANGE, send_message=False)

        logger.success(f"All tokens on this wallet collected successfully to chain {dest_chain.name.upper()}")
        database.update_item(item_index=wallet_index, collector_finished=True)
    logger.success("No more wallets left")
