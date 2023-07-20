import os

from dotenv import load_dotenv
from slack_sdk.rtm_v2 import RTMClient
from weather_info_parser import WeatherInfoParser

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
channel_id = os.getenv("CHANNEL_ID")
rtm = RTMClient(token=bot_token)


def send_slack_message():
    wip = WeatherInfoParser
    html = wip.get_weather(keyword="여의도 날씨")
    weather = wip.get_today_weather(html)

    rtm.web_client.chat_postMessage(
        channel=channel_id,
        blocks=[
            {"type": "divider"},
            {
                "type": "section",
                "text": {"type": "plain_text", "text": f"{weather.area}"},
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": f"""{weather.now_temperature}
{weather.lowest_temperature}
{weather.highest_temperature}
{weather.status}""",
                },
            },
        ],
    )


# rtm.connect()

if __name__ == "__main__":
    send_slack_message()
