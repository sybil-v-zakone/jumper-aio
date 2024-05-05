class NoRPCEndpointSpecifiedError(Exception):
    def __init__(
        self,
        chain,
        message: str = "No RPC endpoint specified for {}. Specify one in config.py file.",
        *args: object,
    ) -> None:
        self.message = message.format(chain.name)
        super().__init__(self.message, *args)


class WithdrawalCancelledError(Exception):
    def __init__(self, message: str = "Withdrawal cancelled", *args: object) -> None:
        self.message = message
        super().__init__(self.message, *args)
