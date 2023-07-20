import os

from slack_sdk.rtm_v2 import RTMClient
from weather_info_parser import WeatherInfoParser

bot_token = os.getenv("BOT_TOKEN")
rtm = RTMClient(token=bot_token)


@rtm.on("message")
def handle(client: RTMClient, event: dict):
    keyword: str = event["text"]
    if keyword.endswith("날씨"):
        wip = WeatherInfoParser
        html = wip.get_weather(keyword=keyword)
        weather = wip.get_today_weather(html)
        channel_id: str = event["channel"]

        client.web_client.chat_postMessage(
            channel=channel_id,
            text=f""" 
    지역 {weather.area} 
    현재 온도 {weather.now_temperature}
    최저 온도 {weather.lowest_temperature}
    최고 온도 {weather.highest_temperature}
    날씨 상태 {weather.status}
""",
        )


# rtm.connect()
rtm.start()
