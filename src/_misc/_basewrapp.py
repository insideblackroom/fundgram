from asyncio import sleep
from telethon.tl.custom import Message

async def timing_send(event, text=None, link_preview=None, time: int = None, **args):
    reply_to = event.reply_to_msg_id or event
    sent = await event.client.send_message(
        event.chat_id, text, link_preview=link_preview, reply_to=reply_to, **args
    )
    if time:
        await sleep(time)
        return await sent.delete()
        
    return sent

setattr(Message, 'timing_send', timing_send)