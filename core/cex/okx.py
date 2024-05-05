from typing import Dict, Any, Union, Optional

from ccxt import AuthenticationError
from ccxt.async_support import okx

from config import WAIT_FOR_DEPOSIT_DELAY_RANGE, OKX_API_KEY, OKX_API_SECRET, OKX_API_PASSWORD
from core.constants import (
    CEX_WITHDRAW_TRIES,
    CEX_WITHDRAW_DELAY_RANGE,
    CEX_WAIT_FOR_WITHDRAWAL_FINAL_STATUS_ATTEMPTS,
    CEX_WAIT_FOR_WITHDRAWAL_FINAL_STATUS_DELAY_RANGE
)
from core.exceptions import WithdrawalCancelledError
from logger import logger
from core import Client
from utils import sleep, find_token


class Okx:
    def __init__(self, client: Client) -> None:
        self.client = client
        self.exchange = okx(config=self._get_config())

    def _get_config(self) -> Dict[str, Any]:
        return {
            "apiKey": OKX_API_KEY,
            "secret": OKX_API_SECRET,
            "password": OKX_API_PASSWORD,
            "enableRateLimit": True,
        }

    async def withdraw(
        self,
        amount: Union[int, float],
        retry_count: Optional[int] = 0,
        wait_for_funds: Optional[bool] = True,
    ) -> bool:
        token = find_token(tokens=self.client.chain.tokens, symbol=self.client.chain.coin_symbol)
        logger.info(f"[OKX] Trying to withdraw {amount} {token.symbol.upper()} to {self.client.chain.name.upper()}")
        async with self.exchange as exchange:
            try:
                initial_balance = await self.client.get_token_balance(token)

                withdrawal_data = await exchange.withdraw(
                    code=token.symbol.upper(),
                    amount=amount,
                    address=self.client.address,
                    params={
                        "toAddress": self.client.address,
                        "chainName": f"{token.symbol.upper()}-{self.client.chain.okx_chain_name}",
                        "dest": 4,
                        "fee": self.client.chain.okx_withdrawal_fee,
                        "pwd": "-",
                        "amt": amount,
                        "network": self.client.chain.okx_chain_name,
                    },
                )

                withdrawal_id = withdrawal_data["info"]["wdId"]
            except Exception as e:
                error_message = str(e)
                if (
                    "Withdrawal address is not allowlisted for verification exemption"
                    in error_message
                ):
                    logger.error(f"[OKX] Address {self.client} is not allowlisted")
                elif "Insufficient balance" in error_message:
                    logger.error(f"[OKX] Insufficient funds for withdrawal")
                else:
                    logger.error(
                        f"[OKX] Error while withdrawing {amount} {token.symbol} to {self.client}: {error_message}"
                    )

                if retry_count < CEX_WITHDRAW_TRIES:
                    logger.info(
                        f"[OKX] Withdrawal unsuccessful, waiting for the next try"
                    )
                    await sleep(
                        delay_range=CEX_WITHDRAW_DELAY_RANGE, send_message=False
                    )
                    return await self.withdraw(
                        retry_count=retry_count + 1, amount=amount
                    )
                else:
                    logger.error(
                        f"[OKX] Withdrawal failed, attempt limit exceeded: {e}"
                    )
                    return False
            if wait_for_funds:
                tokens_delivered = await self._watch_for_delivery(
                    withdrawal_id=withdrawal_id, initial_balance=initial_balance
                )
                if tokens_delivered:
                    logger.success(
                        f"[OKX] Successfully withdrew {amount} {token.symbol}"
                    )
                    return True
                return False
            return True

    async def _watch_for_delivery(
        self, withdrawal_id: str, initial_balance: Union[int, float]
    ) -> bool:
        withdrawal_finalized = await self._wait_for_withdrawal_final_status(
            withdrawal_id=withdrawal_id
        )
        withdrawal_received = await self.client.wait_for_deposit(
            initial_balance=initial_balance,
            checkup_sleep_time_range=WAIT_FOR_DEPOSIT_DELAY_RANGE
        )
        return withdrawal_finalized and withdrawal_received

    async def _wait_for_withdrawal_final_status(self, withdrawal_id: str) -> bool:
        attempt_count = 1
        logger.info(f"[OKX] Waiting for withdrawal final status")
        while attempt_count < CEX_WAIT_FOR_WITHDRAWAL_FINAL_STATUS_ATTEMPTS:
            async with self.exchange as exchange:
                try:
                    status = await exchange.private_get_asset_deposit_withdraw_status(
                        params={"wdId": withdrawal_id}
                    )

                    if "Cancelation complete" in status["data"][0]["state"]:
                        raise WithdrawalCancelledError
                    if "Withdrawal complete" not in status["data"][0]["state"]:
                        attempt_count += 1
                        await sleep(
                            delay_range=CEX_WAIT_FOR_WITHDRAWAL_FINAL_STATUS_DELAY_RANGE,
                            send_message=False,
                            pr_bar=False,
                        )
                    else:
                        logger.info("[OKX] Withdrawal sent from OKX")
                        return True
                except Exception as e:
                    logger.error(f"[OKX] {e}")
                    return False
        logger.error(f"[OKX] Max attempts reached. Withdrawal status not finalized")
        return False

    async def _transfer_from_sub_account(self, name, symbol: str) -> bool:
        async with self.exchange as exchange:
            try:
                data = await exchange.private_get_asset_subaccount_balances(
                    params={"subAcct": name, "ccy": symbol}
                )
                amount = data["data"][0]["availBal"]
            except Exception as e:
                logger.error(f"[OKX] Failed to fetch sub-account's balances: {e}")
                return False

            if amount != "0":
                await exchange.load_markets()
                currency = exchange.currency(symbol)

                data = {
                    "ccy": currency["id"],
                    "amt": exchange.currency_to_precision(symbol, amount),
                    "from": "6",
                    "to": "6",
                    "type": "2",
                    "subAcct": name,
                }
                try:
                    await exchange.private_post_asset_transfer(data)
                    logger.info(
                        f"[OKX] Withdrew {amount} {symbol} from sub-account with name {name} to main account successfully"
                    )
                    return True
                except Exception as e:
                    error_message = str(e)
                    if "Parameter amt  error" in error_message:
                        logger.debug(
                            f"[OKX] Balance of sub-account {name} is too small"
                        )
                        return True
                    else:
                        logger.error(
                            f"Couldn't withdraw {symbol} from sub-account with name {name} to main account: {e}"
                        )
                        return False

    async def transfer_from_sub_accounts(self, symbol: str = "ETH") -> bool:
        async with self.exchange as exchange:
            try:
                response = await exchange.private_get_users_subaccount_list()
                sub_accounts = response["data"]

                for sub_acc in sub_accounts:
                    await self._transfer_from_sub_account(sub_acc["subAcct"], symbol)
                return True
            except AuthenticationError:
                logger.error(f"[OKX] Invalid OK-ACCESS-KEY")
                return False
            except Exception as e:
                logger.error(f"[OKX] Couldn't withdraw from from sub-accounts: {e}")
                return False
