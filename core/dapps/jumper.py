from typing import Optional

from web3 import AsyncWeb3

from core.client import Client
from core.constants import (
    MAX_SLIPPAGE,
    JUMPER_TX_SIMULATION_VALUE,
    JUMPER_FULL_BRIDGE_GAS_MULTIPLIER,
    JUMPER_BUILD_TX_URL,
    JUMPER_ROUTE_URL
)
from core.decorators import gas_delay, retry_on_fail
from core.models.chain import Chain
from core.models.token import Token
from logger import logger


class JumperBridge:
    def __init__(self, client: Client):
        self.client = client

    async def _calculate_amount_for_full_bridge(self, dest_chain: Chain, token_in: Token, token_out: Token):
        try:
            data = (await self._build_tx(
                dest_chain=dest_chain, amount=JUMPER_TX_SIMULATION_VALUE, token_in=token_in, token_out=token_out
            ))["transactionRequest"]

            tx_params = await self.client.get_tx_params(
                to=AsyncWeb3.to_checksum_address(data["to"]), data=data["data"], value=int(data["value"], 16)
            )

            gas = await self.client.get_gas_estimate(tx_params=tx_params)
            gas_fee = int((gas * tx_params["gasPrice"] * JUMPER_FULL_BRIDGE_GAS_MULTIPLIER))
            fee = int(data["value"], 16) - JUMPER_TX_SIMULATION_VALUE
            balance = await self.client.get_token_balance(token_in)
            return balance - gas_fee - fee
        except Exception as e:
            raise Exception(f"Error while estimating full bridge amount: {e}")

    async def _build_tx(self, dest_chain: Chain, amount: int, token_in: Token, token_out: Token):
        try:
            route_data = await self._get_route(
                dest_chain=dest_chain, amount=amount, token_in=token_in, token_out=token_out
            )
            if not len(route_data["routes"]) > 0:
                raise Exception(f"Find zero routes")

            return await self.client.send_post_request(
                url=JUMPER_BUILD_TX_URL, data=route_data["routes"][0]["steps"][0], headers={
                    "X-Lifi-Sdk": "3.0.0-alpha.57",
                    "X-Lifi-Widget": "3.0.0-alpha.35"
                }
            )
        except Exception as e:
            raise Exception(f"Error while build tx: {e}")

    async def _get_route(self, dest_chain: Chain, amount: int, token_in: Token, token_out: Token):
        try:
            headers = {
                "X-Lifi-Sdk": "3.0.0-alpha.57",
                "X-Lifi-Widget": "3.0.0-alpha.35"
            }

            return await self.client.send_post_request(url=JUMPER_ROUTE_URL, headers=headers, data={
                "fromAddress": self.client.address,
                "fromAmount": str(amount),
                "fromChainId": self.client.chain.chain_id,
                "fromTokenAddress": token_in.contract_address,
                "toAddress": self.client.address,
                "toChainId": dest_chain.chain_id,
                "toTokenAddress": token_out.contract_address,
                "options": {
                    "integrator": "jumper.exchange",
                    "order": "CHEAPEST",
                    "slippage": MAX_SLIPPAGE / 100,
                    "maxPriceImpact": 1,
                    "allowSwitchChain": False,
                    "insurance": False
                }
            })
        except Exception as e:
            raise Exception(f"Error while getting route: {e}")

    @gas_delay()
    @retry_on_fail()
    async def bridge(self, dest_chain: Chain, token_in: Token, token_out: Token, amount: Optional[float]):
        try:
            if amount is None:
                if token_in.is_native:
                    amount = await self._calculate_amount_for_full_bridge(
                        dest_chain=dest_chain, token_in=token_in, token_out=token_out
                    )
                else:
                    amount = await self.client.get_token_balance(token_in)
            else:
                amount = token_in.to_wei(amount)

            if amount == 0:
                return False, 0

            logger.info(
                f"[JumperBridge] Bridging {round(token_in.from_wei(amount), token_in.round_to)} {token_in.symbol.upper()}"
                f" from {self.client.chain.name.upper()} to {token_out.symbol.upper()} on {dest_chain.name.upper()}"
            )

            data = (await self._build_tx(
                dest_chain=dest_chain, amount=amount, token_in=token_in, token_out=token_out
            ))["transactionRequest"]

            await self.client.approve(spender=AsyncWeb3.to_checksum_address(data["to"]), token=token_in, value=amount)

            tx_hash = await self.client.send_transaction(
                to=AsyncWeb3.to_checksum_address(data["to"]),
                data=data["data"],
                value=int(data["value"], 16)
            )
            return await self.client.verify_tx(tx_hash=tx_hash), token_in.from_wei(amount)
        except Exception as e:
            logger.error(f"[JumperBridge] Error: {e}")
            return False
