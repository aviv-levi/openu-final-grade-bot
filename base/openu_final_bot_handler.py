from base.telegram_basic_handler import TelegramBasicHandler


class OpenUFinalBotHandler(TelegramBasicHandler):

    def __init__(self, bot_token):
        super().__init__(bot_token)

    def build(self):
        super().build()

        # TODO: build conversion handler
