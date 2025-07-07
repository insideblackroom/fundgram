import sys
import logging
import platform

import telethon

from collections import namedtuple

logger = logging.getLogger(__name__)
botcli_logger = logging.getLogger('botcli')
TelethonLogger = logging.getLogger("Telethon")
TelethonLogger.setLevel(logging.INFO)

LANGconfig = namedtuple('LANGconfig', ['lang', 'path'])

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

    from .configs import Var
    import os
    if Var.DATABASE_URL:
        try:
            import psycopg2
        except ImportError:
            logger.info("Install psycopg2 to enable PostgreSQL")
            os.system(f"{sys.executable} -m pip install psycopg2-binary")
            import psycopg2

    from .start._db import db
    _DB = db(Var.DATABASE_URL)
    logger.info(f"Database info: {_DB.name}")
    _DB.close()
    
    from .start.baseclient import BaseClient, BotBaseClient
    # from telethon.sessions import StringSession
    cli = BaseClient(session="cloner", proxy={'proxy_type': 'http', 'addr': '127.0.0.1', 'port': 10809})
    botcli = BotBaseClient(
        session='clonerbot',
        api_id=Var.BOT_API_ID, api_hash=Var.BOT_API_HASH,
        bot_token=True,
        proxy={'proxy_type': 'http', 'addr': '127.0.0.1', 'port': 10809},
        logger=botcli_logger
        )
    # cli.run_in_loop(make_ass())


