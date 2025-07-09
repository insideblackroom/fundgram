from src._misc._decorators import cli_decorate
from lang import get_text
from src.configs import Var
from src.utils.helper import get_weather, get_city_code, get_req
from datetime import timedelta
from datetime import datetime
import pytz
from src import logger

async def get_timezone(offset_s):
    offset = timedelta(seconds=offset_s)
    hours, _ = divmod(offset.seconds, 3600)
    s = "+" if offset.total_seconds() > 0 else "-"
    for tz_name in pytz.all_timezones:
        tz = pytz.timezone(tz_name)
        now = datetime.now(tz)
        if now.utcoffset() == offset:
            return f"{tz_name}/UTC{s}{hours}"

@cli_decorate(pattern='هوای ?(.*)')
async def weather(event):
    if event.fwd_from:
        return
    sent = await event.timing_send(get_text("gl_1"))
    key = Var.OPENWEATHER_API_KEY
    if not key:
        await event.timing_send(get_text('err_1'), time=6)
        return
    
    input_text = event.pattern_match.group(1)
    if not input_text:
        await event.timing_send(get_text("err_2"), time=7)
        return

    tz_resp = None
    city_code, input_text = await get_city_code(input_text)
    if city_code:
        tz_resp = await get_req(f"https://prayer.aviny.com/api/prayertimes/{city_code}")

    url = f"https://api.openweathermap.org/data/2.5/weather?q={input_text}&APPID={Var.OPENWEATHER_API_KEY}&units=metric"
    try:
        resp = await get_weather(url, resp_json=True)
        if resp['cod'] == 200:
            if not tz_resp:
                c_timezone = resp['timezone']
                tz = await get_timezone(c_timezone)
            else:
                timezone = tz_resp['TimeZone'].split(".")
                hour = int(timezone[0]) * 3600
                sec = 1800 if int(timezone[1]) else 0
                tz = await get_timezone(offset_s=hour + sec)
            await sent.edit(
                f">>{tz_resp['CountryName']} => {tz_resp['CityName']}\n"
                f">>تاریخ : {tz_resp['Today']}\n"
                f">>موقعیت زمانی : {tz}\n"
                f">>طلوع خورشید : {tz_resp['Sunrise']}\n"
                f">>غروب خورشید : {tz_resp['Sunset']}\n\n"
                f"------------------------\n"
                f"-> ++دمای هوا : {resp['main']['temp']}°C\n"
                f"-> کمترین دما:     {resp['main']['temp_min']}\n"
                f"-> بیشترین دما :     {resp['main']['temp_max']}\n"
                f"-> ++هوا : {resp['weather'][0]['description']}\n"
                f"-> ++فشار هوا : {resp['main']['pressure']}\n"
                f"-> ++رطوبت : {resp['main']['humidity']}%\n"
                f"-> ++ابری : {resp['clouds']['all']}%\n"
                f"-> ++سرعت باد : {resp['wind']['speed']}\n"
                f"------------------------\n"
                f"lat: {int(resp['coord']['lat']):02d}, lon: {int(resp['coord']['lon']):02d}"
            )
        else:
            logger.warning("There was an error getting weather data from OpenWeatherMap.")
            if tz_resp:
                timezone = tz_resp['TimeZone'].split(".")
                hour = int(timezone[0])*3600
                sec = 1800 if int(timezone[1]) else 0
                tz = await get_timezone(offset_s=hour+sec)
                await event.client.send_message(
                    event.chat_id,
                    message=
                    f">>{tz_resp['CountryName']} => {tz_resp['CityName']}\n"
                    f">>تاریخ : {tz_resp['Today']}\n"
                    f">>موقعیت زمانی : {tz}\n"
                    f">>طلوع خورشید : {tz_resp['Sunrise']}\n"
                    f">>غروب خورشید : {tz_resp['Sunset']}\n\n"
                )
            await sent.edit(get_text("err_1"))

    except Exception as e:
        logger.error(f"Error in weather gathering: {e}")
        await event.timing_send(get_text("gl_1"))
