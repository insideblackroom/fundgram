from src._misc._decorators import cli_decorate
from lang import get_text

@cli_decorate(pattern='weather ?(.*)')
async def weather(event):
    if event.fwd_from:
        return
    sent = await event.timing_send(get_text("gl_1"))