from src._misc._decorators import cli_decorate

@cli_decorate(pattern="^!ping")
async def handler(event):
    await event.eor(event, "This is a test ping message!, Delete after 5 seconds.", time=5)