import logging
from src.core.bot_handler import BotHandler
from telegram.ext import Application
from telegram import Update

logger = logging.getLogger(__name__)


class TelegramBasicHandler(BotHandler):

    def __init__(self, bot_token):
        self._bot_token = bot_token
        self._application = None

    def build(self):
        logger.info("Start building bot")
        self._application = Application.builder().token(self._bot_token).build()

    def run(self):
        logger.info("Start running bot")
        self._application.run_polling(allowed_updates=Update.ALL_TYPES)
