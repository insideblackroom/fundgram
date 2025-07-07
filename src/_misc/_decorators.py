from .. import botcli
from telethon.events import NewMessage

def cli_decorate(
    pattern=None, cli_bot=botcli
):
    def wrapper(func):
        async def inner(event):
            await func(event)
        cli_bot.add_event_handler(
            inner,
            NewMessage(pattern=pattern)
        )
        return inner
    return wrapper
