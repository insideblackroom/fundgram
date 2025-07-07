import sys
import logging
import platform

import telethon

logger = logging.getLogger(__name__)
botcli_logger = logging.getLogger('botcli')
TelethonLogger = logging.getLogger("Telethon")
TelethonLogger.setLevel(logging.INFO)

if sys.argv[0] == '-m':
    from .version import date_version, __version__ as __pypr__
    from telethon import __version__
    from telethon.tl.alltlobjects import LAYER
    print("==> module starting <==")
    from utilities import load_logging_config
    load_logging_config('logging.json')
    logger.info(
        """
                    -----------------------------------
                            Starting Bot
                    -----------------------------------
        """
    )
    logger.info(f"Python Version: {platform.python_version()}")
    logger.info(f"Project Time: {date_version}")
    logger.info(f"Telethon Version: {__version__}")
    logger.info(f"Telethon Layer: {LAYER}")
    logger.info(f"Project Version: {__pypr__}")
