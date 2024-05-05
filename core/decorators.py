import asyncio
import random
from functools import wraps
from typing import List

from tqdm import tqdm
from web3 import AsyncWeb3

from config import GAS_DELAY_RANGE, GAS_THRESHOLD
from core.constants import RETRIES, RETRY_DELAY_RANGE
from logger import logger
from utils import get_chain_gas_fee, sleep


def retry_on_fail(tries: int = RETRIES, retry_delay: List[int] = RETRY_DELAY_RANGE):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for _ in range(tries):
                result = await func(*args, **kwargs)
                if result is None or result is False:
                    await sleep(delay_range=retry_delay, send_message=False)
                else:
                    return result
            return False

        return wrapper

    return decorator


def gas_delay(gas_threshold: int = GAS_THRESHOLD, delay_range: List = GAS_DELAY_RANGE):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            while True:
                current_eth_gas_price = await get_chain_gas_fee()
                threshold = AsyncWeb3.to_wei(gas_threshold, "gwei")
                if current_eth_gas_price > threshold:
                    random_delay = random.randint(*delay_range)

                    logger.warning(
                        f"Current gas fee {round(AsyncWeb3.from_wei(current_eth_gas_price, 'gwei'), 2)} GWEI > "
                        f"Gas threshold {AsyncWeb3.from_wei(threshold, 'gwei')} GWEI. "
                        f"Waiting for {random_delay} seconds...",
                        send_to_tg=False,
                    )

                    with tqdm(total=random_delay, desc="Waiting", unit="s", dynamic_ncols=True, colour="blue") as pbar:
                        for _ in range(random_delay):
                            await asyncio.sleep(1)
                            pbar.update(1)
                else:
                    break

            return await func(*args, **kwargs)

        return wrapper

    return decorator
