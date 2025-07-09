from aiohttp import ClientSession
import aiofiles
import json
from typing import Tuple

async def get_city_code(city: str) -> Tuple[int, str]:
    async with aiofiles.open('./src/utils/city.json', 'r') as f:
        load = json.loads(await f.read())
    for item in load:
        if item['Name'] == city:
            return item['Code'], item['LName']
    return -1, ""

async def get_req(url: str, *args, **kwargs):
    async with ClientSession() as session:
        result = await session.get(url, *args, **kwargs)
        return await result.json()

async def get_weather(
        url: str,
        header=None,
        resp_json: bool = False,
        resp_content: bool = False,
        head=None,
        post=None,
        *args, **kwargs
):
    async with ClientSession(headers=header) as session:
        session_method = session.head if head else (session.post if post else session.get)
        data = await  session_method(url, *args, **kwargs)
        if resp_json:
            return await data.json()
        if resp_content:
            return await data.read()
        if head:
            return data
        return await data.text()
