import asyncio
import random
from typing import List, Optional, Dict

import aiohttp
from tqdm import tqdm
from web3 import AsyncWeb3
from web3.types import Wei

from config import PROXY_CHANGE_IP_URL, ETHEREUM_RPC_ENDPOINT
from core.chains import *
from core.models.token import Token
from logger import logger


async def change_ip() -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=PROXY_CHANGE_IP_URL) as response:
            if response.status == 200:
                logger.debug(f"Successfully changed ip address")
            else:
                logger.warning(f"Couldn't change ip address")


def read_from_txt(file_path: str):
    try:
        with open(file=file_path, mode="r") as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        logger.error(f"File `{file_path}` not found")
    except Exception as e:
        logger.error(f"Error while reading `{file_path}`: {e}")


def custom_round(number: float, decimals: int) -> float:
    return int(number * 10 ** decimals) / 10 ** decimals


async def sleep(delay_range: List[int], send_message: bool = True, pr_bar: bool = True) -> None:
    delay = random.randint(*delay_range)

    if send_message:
        logger.info(f"Sleeping for {delay} seconds...")

    if pr_bar:
        with tqdm(total=delay, desc="Waiting", unit="s", dynamic_ncols=True, colour="blue") as pbar:
            for _ in range(delay):
                await asyncio.sleep(delay=1)
                pbar.update(1)
    else:
        await asyncio.sleep(delay=delay)


def find_token(tokens: Dict[str, Token], symbol: str) -> Optional[Token]:
    return tokens.get(symbol)


def get_chain_by_name(name: str):
    chains = [
        ARBITRUM_CHAIN, BASE_CHAIN, BSC_CHAIN, OPTIMISM_CHAIN, POLYGON_CHAIN, LINEA_CHAIN, ZKERA_CHAIN, ETHEREUM_CHAIN
    ]
    for chain in chains:
        if chain.name == name:
            return chain


def get_chains():
    return [
        ARBITRUM_CHAIN, BASE_CHAIN, BSC_CHAIN, OPTIMISM_CHAIN, POLYGON_CHAIN, LINEA_CHAIN, ZKERA_CHAIN, ETHEREUM_CHAIN
    ]


async def get_chain_gas_fee() -> Wei:
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(ETHEREUM_RPC_ENDPOINT))
    return await w3.eth.gas_price
