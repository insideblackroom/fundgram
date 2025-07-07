import psycopg2
import logging
import sys

logger = logging.getLogger('startup')

class SqlDB:
    def __init__(self, db_url):
        self.__url = db_url
        self.__conn = None
        try:
            self.__conn = psycopg2.connect(dsn=self.__url)
            self.__conn.autocommit = True
            self.__cursor = self.__conn.cursor()
            self.__cursor.execute("CREATE TABLE IF NOT EXISTS pyproj (pyprojterm varchar(50));")
        except Exception as e:
            logger.error(f'Failed to connect to database: {e}')
            logger.info('Invalid Database')
            if self.__conn:
                self.__conn.close()
            sys.exit()

    @property
    def name(self):
        return f"db: {self.__conn.info.dbname}"

    @property
    def current_use_space(self):
        self.__cursor.execute("SELECT pg_size_pretty(pg_relation_size('pyproj')) AS size")
        data = self.__cursor.fetchall()
        return int(data[0][0].splite()[0])

    def close(self):
        if self.__conn:
            self.__conn.close()
            self.__conn = None
            return 1
        return 0

def db(database_url):
    return SqlDB(database_url)
