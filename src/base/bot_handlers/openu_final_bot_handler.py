from src.base.bot_handlers.telegram_basic_handler import TelegramBasicHandler
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters, CommandHandler,
)
from src.base.models.openu_task_details import OpenUTaskDetails
from src.base.calculators.openu_calculator import OpenUCalculator

CHOOSE_MENU, TASKS_COUNT, TASK_WEIGHT, TASK_GRADE, EXAM_GRADE, DESIRED_FINAL = range(6)
ONLY_TEXT_FILTER = filters.TEXT & ~filters.COMMAND
MENU = ["חישוב ציון סופי", "חישוב ציון בחינה מינימלי"]


class OpenUFinalBotHandler(TelegramBasicHandler):

    def __init__(self, bot_token):
        super().__init__(bot_token)

    async def _welcome_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
            Starts the conversation and show user the menu.
        """

        welcome_message = "ברוכים הבאים למחשבון ציון סופי בפתוחה!\n" \
                          "מה תרצו לעשות?"

        await update.message.reply_text(welcome_message,
                                        reply_markup=ReplyKeyboardMarkup([MENU],
                                                                         one_time_keyboard=True,
                                                                         input_field_placeholder="בחרו אופציה מהתפריט"))
        return CHOOSE_MENU

    async def _choose_menu_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
            Stores the selected option and asks for tasks count
        """
        context.user_data['selected_option'] = update.message.text
        message = "הכניסו בבקשה את כמות המטלות שיש בקורס שלכם"
        await update.message.reply_text(message)
        return TASKS_COUNT

    async def _tasks_count_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
            Stores the selected task count and asks foreach task details.
        """

        context.user_data['tasks_count'] = int(update.message.text)
        context.user_data['task_index'] = 1
        context.user_data['tasks_details'] = []

        if context.user_data['tasks_count'] > 0:
            await update.message.reply_text(f'הכניסו בבקשה את משקל מטלה מספר {context.user_data["task_index"]}')
            return TASK_GRADE
        else:
            await update.message.reply_text('נראה כי אין לך מטלות בקורס.')
            return ConversationHandler.END

    async def _task_grade_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
            Stores the task weight and ask for task grade
        """
        context.user_data['current_task_weight'] = int(update.message.text)
        await update.message.reply_text(f'הכניסו בבקשה את ציון מטלה מספר {context.user_data["task_index"]}')
        return TASK_WEIGHT

    async def _task_weight_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
            Stores the task grade and build OpenU task.
            When we finish storing all tasks, we ask the next thing depend by selected option:
            1. ask for exam grade
            2. ask for desire final grade
        """
        current_task_grade = int(update.message.text)
        current_task_weight = context.user_data['current_task_weight']
        openu_task = OpenUTaskDetails(current_task_weight, current_task_grade)
        context.user_data['tasks_details'].append(openu_task)
        context.user_data['task_index'] += 1

        if context.user_data['task_index'] <= context.user_data['tasks_count']:
            await update.message.reply_text(f'הכניסו בבקשה את משקל מטלה מספר {context.user_data["task_index"]}')
            return TASK_GRADE
        else:
            # navigate by selected option
            selected_option = context.user_data['selected_option']
            if selected_option == MENU[0]:
                await update.message.reply_text('הכניסו בבקשה את ציון הבחינה')
                return EXAM_GRADE
            if selected_option == MENU[1]:
                await update.message.reply_text('הכניסו בבקשה את ציון סופי הרצוי')
                return DESIRED_FINAL
            else:
                return ConversationHandler.END

    async def _exam_grade_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
            Stores the exam grade and show user the final course grade.
        """
        exam_grade = int(update.message.text)
        if exam_grade < 60:
            await update.message.reply_text(f'הציון הסופי שלך בקורס הוא: {exam_grade}')
            return ConversationHandler.END

        tasks_details = context.user_data['tasks_details']
        final_grade = OpenUCalculator.calculate_final_grade(tasks_details, exam_grade)

        await update.message.reply_text(f'הציון הסופי שלך בקורס הוא: {final_grade}')
        return ConversationHandler.END

    async def _desire_grade_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
            Stores the desire final grade and show user the minimum exam grade.
        """
        desire_grade = int(update.message.text)
        if desire_grade < 60:
            await update.message.reply_text(f'הציון המינימלי לבחינה הוא: {desire_grade}')
            return ConversationHandler.END
        tasks_details = context.user_data['tasks_details']
        min_exam_grade = OpenUCalculator.calculate_desired_exam_grade(tasks_details, desire_grade)

        await update.message.reply_text(f'הציון המינימלי לבחינה הוא: {min_exam_grade}')
        return ConversationHandler.END

    async def _cancel_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
            Cancels and ends the conversation.
        """
        await update.message.reply_text("המשך יום טוב (:", reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

    def _build_conversion(self):
        welcome_point = MessageHandler(ONLY_TEXT_FILTER, self._welcome_callback)
        choose_menu_point = MessageHandler(filters.Regex(f"^({'|'.join(MENU)})$"), self._choose_menu_callback)
        tasks_count_point = MessageHandler(ONLY_TEXT_FILTER, self._tasks_count_callback)
        tasks_weight_point = MessageHandler(ONLY_TEXT_FILTER, self._task_weight_callback)
        tasks_grade_point = MessageHandler(ONLY_TEXT_FILTER, self._task_grade_callback)
        exam_grade_point = MessageHandler(ONLY_TEXT_FILTER, self._exam_grade_callback)
        desire_grade_point = MessageHandler(ONLY_TEXT_FILTER, self._desire_grade_callback)
        cancel_fallback = CommandHandler("cancel", self._cancel_callback)

        conversion_handler = ConversationHandler(
            entry_points=[welcome_point],
            states={
                CHOOSE_MENU: [choose_menu_point],
                TASKS_COUNT: [tasks_count_point],
                TASK_WEIGHT: [tasks_weight_point],
                TASK_GRADE: [tasks_grade_point],
                EXAM_GRADE: [exam_grade_point],
                DESIRED_FINAL: [desire_grade_point],
            },
            fallbacks=[cancel_fallback],
        )

        self._application.add_handler(conversion_handler)

    def build(self):
        super().build()
        self._build_conversion()
