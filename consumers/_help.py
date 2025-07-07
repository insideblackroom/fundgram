from src._misc._decorators import cli_decorate

@cli_decorate(pattern="help( (.*)|$)")
async def _help(event):
    await event.client.send_message(event.chat_id, "hello")
