from src import LANGconfig, logger
from src.configs import Var
import os
from yaml import safe_load

LANGconfig.lang = Var.LANGUAGE
lang_path = "lang/langs/{}.yml"

def read_lang(file_path):
    if not file_path.endswith(".yml"):
        return
    elif not os.path.exists(file_path):
        file_path = lang_path.format('en')

    try:
        data = safe_load(open(file_path, encoding='UTF-8'))
    except Exception as e:
        logger.error(f"Error in language file --> {file_path[:-4]}")
        logger.exception(e)
        
    return {file_path.split('/')[-1][:-4]: data}

language = read_lang(lang_path.format(LANGconfig.lang))

def get_text(key: str):
    l = LANGconfig.lang or 'en'
    try:
        return language[l][key]
    except Exception as err:
        logger.error(f"Error in get Language text: {err}")
        return "Something went wrong"
    