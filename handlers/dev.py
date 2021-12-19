import sys
import traceback
from datetime import datetime
from json import JSONDecodeError
import logging

from telegram import Update, ParseMode
from telegram.ext import CallbackContext, Updater, CommandHandler, Filters
from telegram.utils.helpers import mention_html
from threading import Timer

from database import database
from locales import get_string, new_strings


logger = logging.getLogger(__name__)


def error_handler(update: Update, context: CallbackContext):
    if not update:
        text = "Hey jo, error outside of update, The full traceback:\n\n < code > {trace} < / code > "
        context.bot.send_message(208589966, text, parse_mode=ParseMode.HTML)
        return
    chat = update.effective_chat
    if chat.type == "private":
        if "lang" not in context.user_data:
            context.user_data["lang"] = database.get_user_language(
                update.effective_user.id)
        lang = context.user_data["lang"]
    else:
        if "lang" not in context.chat_data:
            context.chat_data["lang"] = database.get_language_chat(
                update.effective_chat.id)
        lang = context.chat_data["lang"]
    if update.callback_query:
        update.callback_query.answer(
            get_string(lang, "error"), show_alert=True)
    else:
        update.effective_message.reply_text(get_string(lang, "error"))
    payload = ""
    # normally, we always have an user. If not, its either a channel or a poll update.
    if update.effective_user:
        payload += f' with the user {mention_html(update.effective_user.id, update.effective_user.first_name)}'
    # there are more situations when you don't get a chat
    if update.effective_chat:
        payload += f' within the chat <i>{update.effective_chat.title}</i>'
        if update.effective_chat.username:
            payload += f' (@{update.effective_chat.username})'
    # but only one where you have an empty payload by now: A poll (buuuh)
    if update.poll:
        payload += f' with the poll id {update.poll.id}.'
    trace = "".join(traceback.format_tb(sys.exc_info()[2]))
    text = f"Oh no. The error <code>{context.error}</code> happened{payload}. The type of the chat is " \
           f"<code>{chat.type}</code>. The current user data is <code>{context.user_data}</code>, the chat data " \
           f"<code>{context.chat_data}</code>.\nThe full traceback:\n\n<code>{trace}</code>"
    context.bot.send_message(208589966, text, parse_mode=ParseMode.HTML)
    raise


def reply_id(update, _):
    update.effective_message.reply_text(f"{update.effective_chat.id}")
