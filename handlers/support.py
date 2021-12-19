from database import database
import logging
from constants import CHOOSE_SUPPORT, SUPPORT_US, SUPPORT_BY_FINANCE, SUPPORT_BY_KINDS
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, Update

from telegram.ext import CallbackContext, ConversationHandler
from telegram.constants import PARSEMODE_HTML
from locales import get_string
from utils.helpers import format_number

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    """Starts the conversation and asks the user their name ."""
    user_data = context.user_data
    if "lang" not in user_data:
        user_data["lang"] = database.get_user_language(
            update.effective_user.id)
    lang = context.user_data["lang"]
    user = update.callback_query.from_user
    logger.info("User %s started  the conversation.", user.first_name)
    query = update.callback_query
    btn = get_string(user_data["lang"], 'btn')
    keyboard = [
        [InlineKeyboardButton(
         btn['support_financially'], callback_data='support_' + str(SUPPORT_BY_FINANCE))],
        [InlineKeyboardButton(
            btn['support_kind'], callback_data='support_' + str(SUPPORT_BY_KINDS))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send message with text and appended InlineKeyboard
    query.answer()

    # Edit message with text and appended InlineKeyboard
    query.edit_message_text(
        get_string(lang, 'which_support'), reply_markup=reply_markup)


def support_us(update: Update, context: CallbackContext) -> int:
    """Accept Phone numbers"""

    user_data = context.user_data
    if "lang" not in user_data:
        user_data["lang"] = database.get_user_language(
            update.effective_user.id)
    lang = context.user_data["lang"]

    query = update.callback_query
    support_type = query.data.replace("support_", "")
    print("support type is ", support_type)
    if support_type == str(SUPPORT_BY_FINANCE):
        query.edit_message_text(get_string(
            lang, 'financial_support'), parse_mode=PARSEMODE_HTML)
    elif support_type == str(SUPPORT_BY_KINDS):
        query.edit_message_text(get_string(
            lang, 'support_by_kind'))


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""

    user_data = context.user_data
    if "lang" not in user_data:
        user_data["lang"] = database.get_user_language(
            update.effective_user.id)
    lang = context.user_data["lang"]

    if(update.message):
        user = update.message.from_user
        logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(get_string(lang, 'cancel'), reply_markup=ReplyKeyboardRemove()
                              )
    return ConversationHandler.END


def fallback_phone(update: Update, context: CallbackContext) -> int:

    user_data = context.user_data
    if "lang" not in user_data:
        user_data["lang"] = database.get_user_language(
            update.effective_user.id)
    lang = context.user_data["lang"]

    update.message.reply_text(get_string(lang, 'fallback')['phone'])


def fallback_name(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    if "lang" not in user_data:
        user_data["lang"] = database.get_user_language(
            update.effective_user.id)
    lang = context.user_data["lang"]

    update.message.reply_text(get_string(lang, 'fallback')['name'])
