import sys
from telethon import TelegramClient
from telethon import utils
from telethon.errors import (
    ApiIdInvalidError,
    AccessTokenExpiredError,
    AccessTokenInvalidError
)
from ..configs import Var
from .. import TelethonLogger
from logging import Logger
from .. import  logger

class BaseClient(TelegramClient):
    def __init__(
            self,
            session,
            api_id=None,
            api_hash=None,
            bot_token: bool=False,
            phone: bool = False,
            logger: Logger = logger,
            *args,
            **kwargs
    ):
        self.__logger = logger
        kwargs['api_id'] = api_id or Var.API_ID
        kwargs['api_hash'] = api_hash or Var.API_HASH
        kwargs['base_logger'] = TelethonLogger
        super().__init__(session, *args, **kwargs)
        if bot_token:
            self.run_in_loop(self.start_client(bot_token=Var.BOT_TOKEN))
        elif phone:
            self.run_in_loop(self.start_client(phone=Var.PHONE))
        else:
            self.run_in_loop(self.start_client())
            
    async def start_client(self, **kwargs):
        try:
            await self.start(**kwargs)
        except ApiIdInvalidError:
            self.__logger.critical("API ID and API HASH are invalid")
            sys.exit()
        except (AccessTokenExpiredError, AccessTokenInvalidError):
            self.__logger.critical(
                "Bot Token is expired or invalid."
            )
            sys.exit()
        self.me = await self.get_me()
        self._bot = self.is_bot()
        if self.me.bot:
            me = f"@{self.me.username}"
        else:
            me = self.full_name
        self.__logger.info(f"logged in as {me}")

    def run_in_loop(self, func):
        self.loop.run_until_complete(func)

    def run(self):
        self.run_until_disconnected()

    @property
    def full_name(self):
        return utils.get_display_name(self.me)


class BotBaseClient(BaseClient):
    ...

