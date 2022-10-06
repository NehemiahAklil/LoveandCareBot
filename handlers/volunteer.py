from database import database
import logging
from constants import VOLUNTEER_EMAIL, VOLUNTEER_NAME, VOLUNTEER_PHONE, VOLUNTEER_REMARK
from objects.volunteer import Volunteer
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update

from telegram.ext import CallbackContext, ConversationHandler
from locales import get_string
from utils.helpers import format_number, mongo_export_to_file

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
    query.answer()
    query.edit_message_text(
        text=get_string(lang, 'send_name'),
    )
    return VOLUNTEER_NAME


def name(update: Update, context: CallbackContext) -> int:
    """Accept full name and ask for phone number"""
    user = update.message.from_user
    user_data = context.user_data
    if "lang" not in user_data:
        user_data["lang"] = database.get_user_language(
            update.effective_user.id)
    lang = context.user_data["lang"]

    context.user_data['name'] = update.message.text
    logger.info("User %s's name is %s.", user.first_name, update.message.text)
    keyboard = [[KeyboardButton(
        'Share contact', request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard)

    update.message.reply_text(
        get_string(lang, 'send_phone'),
        reply_markup=reply_markup)
    return VOLUNTEER_PHONE


def phone(update: Update, context: CallbackContext) -> int:
    """Accept Phone numbers"""
    user = update.message.from_user

    user_data = context.user_data
    if "lang" not in user_data:
        user_data["lang"] = database.get_user_language(
            update.effective_user.id)
    lang = context.user_data["lang"]

    if update.message.contact:
        user_phone = update.message.contact.phone_number
        logger.info("User %s's account phone nubmer is %s.",
                    user.first_name, user_phone)
    else:
        user_phone = format_number(update.message.text)
        logger.info("User %s's phone nubmer is %s.",
                    user.first_name, user_phone)
    user_data['phone'] = user_phone

    update.message.reply_text(get_string(
        lang, 'send_email'), reply_markup=ReplyKeyboardRemove())
    return VOLUNTEER_EMAIL


def email(update: Update, context: CallbackContext) -> int:
    """Accept email and ask for church membership"""
    user = update.message.from_user
    user_data = context.user_data
    if "lang" not in user_data:
        user_data["lang"] = database.get_user_language(
            update.effective_user.id)
    lang = context.user_data["lang"]

    context.user_data['email'] = update.message.text
    logger.info("User %s's email is %s.", user.first_name, update.message.text)

    update.message.reply_text(
        get_string(lang, 'send_remark'))
    return VOLUNTEER_REMARK


def ask_remark(update: Update, context: CallbackContext) -> int:
    """Accept full name and ask for phone number"""
    user = update.message.from_user
    user_data = context.user_data
    if "lang" not in user_data:
        user_data["lang"] = database.get_user_language(
            update.effective_user.id)
    lang = context.user_data["lang"]

    context.user_data['church'] = update.message.text

    logger.info("User %s's church is %s.",
                user.first_name, update.message.text)

    database.create_volunteer(
        Volunteer(user.id, user_data['name'], user_data['phone'], user_data['email'], user_data['church']))

    update.message.reply_text(get_string(
        lang, 'thank_volunteer'))
    return ConversationHandler.END


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


def fallback_email(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    if "lang" not in user_data:
        user_data["lang"] = database.get_user_language(
            update.effective_user.id)
    lang = context.user_data["lang"]

    update.message.reply_text(get_string(lang, 'fallback')['email'])


def fallback_church(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    if "lang" not in user_data:
        user_data["lang"] = database.get_user_language(
            update.effective_user.id)
    lang = context.user_data["lang"]

    update.message.reply_text(get_string(lang, 'fallback')['church'])


def report(update: Update, context: CallbackContext) -> int:
    filedir = mongo_export_to_file('volunteer')
    with open(filedir, "rb") as file:
        context.bot.send_document(
            chat_id=update.message.chat.id, document=file, filename='volunteer_reports.csv')
