import os
import sys
# from pymongo.mongo_client import MongoClient
from bot import logger


# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6 or sys.version_info[1] < 8:
    logger.error(
        "You must have a python version of at least 3.6.8! Multiple features depend on this. Bot quitting."
    )
    quit(1)

ENV = bool(os.environ.get("ENV", False))


if ENV:
    TOKEN = os.environ.get("TOKEN", None)
    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", 528744128))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    ADMIN_CHAT = int(os.environ.get("ADMIN_CHAT", -723186175))
    ALBUM_CHANNEL = int(os.environ.get("ALBUM_CHANNEL", -1001749458906))
    CONNECTION_STRING = os.environ.get("CONNECTION_STRING", None)
    PORT = int(os.environ.get('PORT', '8443'))
    DOMAIN = os.environ.get('DOMAIN', None)
else:
    TOKEN = os.environ.get(
        "TOKEN", "5051746326:AAE-T9lc7TNEq9DDH8UpmpLOnyGZ8qBKuok")
    CONNECTION_STRING = os.environ.get("CONNECTION_STRING", 'localhost')
    ADMIN_CHAT = -1001437225779.
    ALBUM_CHANNEL = -1001505626599
    OWNER_ID = 528744128
    DOMAIN = None
    PORT = None
