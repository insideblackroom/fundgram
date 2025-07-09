from decouple import config

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class Var:
    API_ID = config('API_ID', cast=int)
    API_HASH = config('API_HASH')
    PHONE = config('PHONE', default=None)

    BOT_API_ID = config('BOT_API_ID', cast=int)
    BOT_API_HASH = config('BOT_API_HASH')
    BOT_TOKEN = config('BOT_TOKEN', default=None)

    DATABASE_URL = config('DATABASE_URL')
    
    SESSION = config('SESSION', default=None)

    LANGUAGE = config('LANGUAGE', default='en')

    OPENWEATHER_API_KEY = config('OPENWEATHER_API_KEY', default=None)