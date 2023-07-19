import os
import sys
import httpx

from dotenv import load_dotenv
from dataclasses import dataclass
from slack_sdk.rtm_v2 import RTMClient
from selectolax.parser import HTMLParser

bot_token = os.getenv("BOT_TOKEN")
wheather_url = os.getenv("WHEATHER_URL")

rtm = RTMClient(token=bot_token)


@dataclass
class WheatherMap:
    area: str
    now_temperature: float
    lowest_temperature: float
    highest_temperatrue: float
    status: str


def today_wheather(html) -> WheatherMap:
    wheather_map = WheatherMap
    wheather_map.area = html.css_first("h2.title").text()
    wheather_map.now_temperature = html.css_first(
        "div._today div.temperature_text strong"
    ).text(deep=False)
    wheather_map.lowest_temperature = (
        html.css("li.today span.lowest")[0].text(deep=False).replace("°", "")
    )
    wheather_map.highest_temperatrue = (
        html.css("li.today span.highest")[0].text(deep=False).replace("°", "")
    )
    wheather_map.status = html.css_first(
        "div._today div.weather_graphic div.weather_main span.blind"
    ).text()

    return wheather_map


def get_wheather() -> HTMLParser:
    try:
        resp = httpx.get(wheather_url)
        html = HTMLParser(resp.text)
    except Exception as e:
        print(e)
        rtm.disconnect()

    return html


@rtm.on("message")
def handle(client: RTMClient, event: dict):
    keyword: str = event["text"]
    if keyword.endswith("날씨"):
        html = get_wheather()
        wheather = today_wheather(html)

        channel_id = event["channel"]
        thread_ts = event["ts"]
        user = event[
            "user"
        ]  # This is not username but user ID (the format is either U*** or W***)

        client.web_client.chat_postMessage(
            channel=channel_id,
            text=f"Hi <@{user}>! i'm in {wheather.status} ",
            thread_ts=thread_ts,
        )


# rtm.connect()
rtm.start()
