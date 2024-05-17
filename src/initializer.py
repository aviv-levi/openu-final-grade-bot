import os
from src.base.bot_handlers.openu_final_bot_handler import OpenUFinalBotHandler
from src.base.facade import Facade


class Initializer:
    def initialize_bot_token(self):
        empty_default_token = "empty"
        bot_token = os.getenv('BOT_TOKEN', empty_default_token)
        if bot_token == empty_default_token:
            raise Exception("Bot token not provided! please make sure you got BOT_TOKEN env variable.")
        return bot_token

    def initialize(self) -> Facade:
        bot_token = self.initialize_bot_token()
        openu_bot = OpenUFinalBotHandler(bot_token)
        return Facade(bot_handler=openu_bot)
