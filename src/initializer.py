import os
from src.base.bot_handlers.openu_final_bot_handler import OpenUFinalBotHandler
from src.base.facade import Facade
import logging


class Initializer:
    def initialize_logger(self):
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        logging.basicConfig(format=log_format, level=logging.INFO)
        # set higher logging level for httpx to avoid all GET and POST requests being logged
        logging.getLogger("httpx").setLevel(logging.WARNING)

    def initialize_bot_token(self):
        empty_default_token = "empty"
        bot_token = os.getenv('BOT_TOKEN', empty_default_token)
        if bot_token == empty_default_token:
            raise Exception("Bot token not provided! please make sure you got BOT_TOKEN env variable.")
        return bot_token

    def initialize(self) -> Facade:
        self.initialize_logger()
        bot_token = self.initialize_bot_token()
        openu_bot = OpenUFinalBotHandler(bot_token)
        return Facade(bot_handler=openu_bot)
