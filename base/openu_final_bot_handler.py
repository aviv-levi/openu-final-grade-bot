from base.telegram_basic_handler import TelegramBasicHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)


TASKS_COUNT, TASK_DETAILS, EXAM_GRADE, DESIRED_FINAL, FINAL_SCORE, MIN_EXAM = range(6)

ONLY_TEXT_FILTER = filters.TEXT & ~filters.COMMAND


class OpenUFinalBotHandler(TelegramBasicHandler):

    def __init__(self, bot_token):
        super().__init__(bot_token)

    async def _welcome_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Starts the conversation and show user the menu."""
        menu = ["חישוב ציון סופי", "חישוב ציון בחינה מינימלי"]
        welcome_message = """
            ברוכים הבאים למחשבון ציון סופי בפתוחה!
מה תרצו לעשות?
        """
        await update.message.reply_text(welcome_message,
                                        reply_markup=ReplyKeyboardMarkup([menu],
                                                                         one_time_keyboard=True,
                                                                         input_field_placeholder="בחרו אופציה מהתפריט"))
        return TASKS_COUNT

    def _build_conversion(self):
        entry_point = MessageHandler(ONLY_TEXT_FILTER, self._welcome_callback)

        conversion_handler = ConversationHandler(
            entry_points=[entry_point],
            states={
                TASKS_COUNT: [],
                TASK_DETAILS: [],
                EXAM_GRADE: [],
                DESIRED_FINAL: [],
                FINAL_SCORE: [],
                MIN_EXAM: []
            },
            fallbacks=[]
        )

        self._application.add_handler(conversion_handler)

    def build(self):
        super().build()
        self._build_conversion()
