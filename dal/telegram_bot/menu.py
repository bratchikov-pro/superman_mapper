from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, Application, CallbackQueryHandler, CommandHandler, ContextTypes
import logging

logger = logging.getLogger(__name__)

LOCATION, DISTANCE, CATEGORY = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Boy", "Girl", "Other"]]

    await update.message.reply_text(
        "Hi! My name is Professor Bot. I will hold a conversation with you. "
        "Send /cancel to stop talking to me.\n\n"
        "Are you a boy or a girl?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Boy or Girl?"
        ),
    )

    return LOCATION

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Привет! Я бот по поиску ближайших мест."
        "Прежде чем начать поиск, поделись своей live-геолокацией."
    ),
    user_location = update.message.location
    logger.info(
        "Ваша локация: %f / %f", user_location.latitude, user_location.longitude
    )
    return LOCATION

# async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     reply_keyboard_place = ["Найти ближайшее...", "Как далеко до...?"]
#     await update.message.reply_text(
#         reply_markup=ReplyKeyboardMarkup(
#             reply_keyboard_place, one_time_keyboard=True, input_field_placeholder="Куда нужно добраться?"
#         ),
#     )
#     return SEARCH

async def category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Питание", callback_data="catering"),
            InlineKeyboardButton("Образование", callback_data="education"),
            InlineKeyboardButton("Транспорт", callback_data="transport"),
            InlineKeyboardButton("Финансы", callback_data="finance"),
            InlineKeyboardButton("Здоровье", callback_data="health"),
            InlineKeyboardButton("Развлечение", callback_data="entertainment"),
            InlineKeyboardButton("Другое", callback_data="other"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Пожалуйста выбирите категорию:", reply_markup=reply_markup)
    return CATEGORY

async def distance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard_distance = ["100 метров", "300 метров", "500 метров", "1000 метров"]
    await update.message.reply_text(
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard_distance, one_time_keyboard=True, input_field_placeholder="В близи..."
        ),
    )
    return DISTANCE

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END