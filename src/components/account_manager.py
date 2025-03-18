from src.utils.logger import logger

class AccountManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logger.info("Creating new AccountManager instance")
            cls._instance = super().__new__(cls)
            cls._instance._account_id = None
        return cls._instance

    def __init__(self):
        pass

    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        logger.info(f"Setting account_id to: {value}")
        self._account_id = value

    def clear(self):
        self._account_id = None
        logger.info("Account ID has been cleared")
