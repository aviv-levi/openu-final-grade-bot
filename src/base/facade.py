from src.core.bot_handler import BotHandler


class Facade:
    def __init__(self, bot_handler: BotHandler):
        self._bot_handler = bot_handler

    def start(self):
        self._bot_handler.build()
        self._bot_handler.run()
