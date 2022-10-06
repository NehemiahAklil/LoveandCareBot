import os
import sys
import logging
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(),override=True)



logger = logging.getLogger(__name__)


# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6 or sys.version_info[1] < 8:
    logger.error(
        "You must have a python version of at least 3.6.8! Multiple features depend on this. Bot quitting."
    )
    quit(1)

ENV = bool(os.environ.get("ENV", False))


if ENV:
    TOKEN = os.environ.get(
        "TOKEN", None)
    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", 528744128))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")
    CONNECTION_STRING = os.environ.get("CONNECTION_STRING", None)
    PORT = int(os.environ.get('PORT', '8443'))
    DOMAIN = os.environ.get('DOMAIN', None)
else:
    TOKEN = os.environ.get(
        "TOKEN", '5610492726:AAGHD5XO4klY37p_s9hf3NNUwOvL9Y-VJFk')
    CONNECTION_STRING = os.environ.get("CONNECTION_STRING", 'localhost')
    OWNER_ID = 528744128
    DOMAIN = None
    PORT = None
