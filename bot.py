import logging
from telegram.ext import CommandHandler, CallbackQueryHandler, Filters, MessageHandler, ConversationHandler, Updater

from constants import VOLUNTEER, ADOPT, SUPPORT, VOLUNTEER_NAME, VOLUNTEER_PHONE, ADOPTER_PHONE, ADOPTER_NAME
from config import TOKEN, DOMAIN, PORT, ENV
from handlers import dev, private, volunteer, adopt, support

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO, filename="log.log")

logger = logging.getLogger(__name__)


def main():
    updater = Updater(token=TOKEN, use_context=True,
                      request_kwargs={'read_timeout': 10, 'connect_timeout': 10})
    dp = updater.dispatcher
    # export_handler = CommandHandler('')

    dp.add_handler(CommandHandler(
        'start', private.start, filters=Filters.chat_type.private))
    dp.add_handler(CommandHandler('help', help))

    volunteer_reg_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(volunteer.start, pattern="pick_" + str(VOLUNTEER))],
        states={
            VOLUNTEER_NAME: [MessageHandler(Filters.text & (~Filters.command), volunteer.name), MessageHandler((~Filters.command) & Filters.all, volunteer.fallback_name)],
            VOLUNTEER_PHONE: [MessageHandler(Filters.regex('^(?:\+2519|09)+\d{8}$'), volunteer.phone),
                              MessageHandler(Filters.contact, volunteer.phone),
                              MessageHandler((~Filters.command) & Filters.all, volunteer.fallback_phone)], },
        fallbacks=[CommandHandler('cancel', volunteer.cancel)]
    )

    adoption_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(adopt.start, pattern="pick_" + str(ADOPT))],
        states={
            ADOPTER_NAME: [MessageHandler(Filters.text & (~Filters.command), adopt.name), MessageHandler((~Filters.command) & Filters.all, adopt.fallback_name)],
            ADOPTER_PHONE: [MessageHandler(Filters.regex('^(?:\+2519|09)+\d{8}$'), adopt.phone),
                            MessageHandler(Filters.contact, adopt.phone),
                            MessageHandler((~Filters.command) & Filters.all, adopt.fallback_phone)], },
        fallbacks=[CommandHandler('cancel', adopt.cancel)]
    )

    support_handler = CallbackQueryHandler(
        support.start, pattern="pick_" + str(SUPPORT))

    pick_support_handler = CallbackQueryHandler(
        support.support_us, pattern=r"support_")

    dp.add_handler(CommandHandler(
        'rp_volunteer', volunteer.report, filters=Filters.chat_type.groups))
    dp.add_handler(CommandHandler('rp_adopt', adopt.report,
                   filters=Filters.chat_type.groups))

    dp.add_handler(support_handler)
    dp.add_handler(pick_support_handler)

    dp.add_handler(volunteer_reg_handler)
    dp.add_handler(adoption_handler)
    dp.add_error_handler(dev.error_handler)

    # Start bot
    if ENV:
        logger.info(f"Using webhook with {DOMAIN + TOKEN}.")
        # add handlers
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN,
                              webhook_url=DOMAIN + TOKEN)
    else:
        logger.info("Using long polling.")
        updater.start_polling(timeout=15, read_latency=4,
                              drop_pending_updates=True)

    updater.idle()


if __name__ == '__main__':
    main()
