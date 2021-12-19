# from re import LOCALE
# import traceback
# import html
# import json
from logging import exception
# from bson.objectid import ObjectId
# from pymongo.collection import ReturnDocument
from constants import VOLUNTEER, ADOPT, SUPPORT, EN, AMH
import logging
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, Update
from telegram.error import BadRequest, ChatMigrated, NetworkError, TelegramError, TimedOut, Unauthorized
from telegram.ext import ConversationHandler, CallbackContext
from telegram.constants import PARSEMODE_HTML, PARSEMODE_MARKDOWN
from locales import get_string, new_strings
from database import database

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    user_data = context.user_data
    if "lang" not in user_data:
        user_data["lang"] = database.get_user_language(
            update.effective_user.id)

    lang = user_data["lang"]
    # Get user that sent /start and
    name = update.message.from_user.first_name
    logger.info('User %s started a converstion with me.', name)

    keyboard = [
        [InlineKeyboardButton(get_string(lang, 'btn')[
                              'pick_en'], callback_data='choose_' + str(EN)), ],
        [InlineKeyboardButton(get_string(lang, 'btn')['pick_amh'], callback_data='choose_' + str(AMH))]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    print("hdd")
    # Send message with text and appended InlineKeyboard
    update.message.reply_text(get_string(
        lang, "greeting"), reply_markup=reply_markup)


def change_lang(update: Update, context: CallbackContext) -> int:
    """Change Language of Bot."""
    user_data = context.user_data
    user_id = update.effective_user.id
    if "lang" not in user_data:
        user_data["lang"] = database.get_user_language(
            user_id)

    print(context.user_data)
    query = update.callback_query
    splitter = query.data.replace("choose_", "")
    if splitter.strip() == str(EN):
        context.user_data['lang'] = 'en'
        database.set_user_language(user_id, 'en')
    elif splitter.strip() == str(AMH):
        context.user_data['lang'] = 'amh'
        database.set_user_language(user_id, 'amh')

    # Send message with text and appended InlineKeyboard
    query.answer()

    print(get_string(
        user_data["lang"], 'btn'))

    # logger.info('User %s started a converstion with me.', name)
    keyboard = [
        [InlineKeyboardButton(
            get_string(
                user_data["lang"], 'btn')['pick_volunteer'], callback_data='pick_' + str(VOLUNTEER))],
        [InlineKeyboardButton(
            get_string(user_data["lang"], 'btn')['pick_support'], callback_data='pick_' + str(SUPPORT))],
        [InlineKeyboardButton(get_string(
            user_data["lang"], 'btn')['pick_adopt'], callback_data='pick_' + str(ADOPT))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send message with text and appended InlineKeyboard
    query.edit_message_text(get_string(user_data["lang"], "start"), reply_markup=reply_markup
                            )
